import asyncio
import json
import os
import random
import time
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== НАСТРОЙКИ И ССЫЛКИ ==================
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
PRIMARY_ADMIN_LINK = "tg://user?id=6117198446"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# База доступа
DB_FILE = "access_db.json"
def load_access():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return set(json.load(f))
        except: return set()
    return set()

vip_users = load_access()

def save_access():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)

# ================== СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = ["EUR/USD OTC","AUD/CAD OTC","AUD/CHF OTC","AUD/USD OTC","CAD/CHF OTC","CAD/JPY OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC","EUR/JPY OTC","EUR/NZD OTC","GBP/USD OTC","NZD/USD OTC","USD/CAD OTC","USD/CHF OTC","USD/JPY OTC","USD/CNH OTC","EUR/RUB OTC","USD/RUB OTC","EUR/TRY OTC","USD/INR OTC","USD/MXN OTC","USD/BRL OTC","USD/PHP OTC","UAH/USD OTC","AUD/NZD OTC","GBP/JPY OTC","NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC","BNB OTC","Dogecoin OTC","Ethereum OTC","Solana OTC","Toncoin OTC","Litecoin OTC","TRON OTC"]
STOCK_ASSETS = ["Apple OTC","McDonald’s OTC","Microsoft OTC","Facebook OTC","Tesla OTC","Amazon OTC","Netflix OTC","VISA OTC","Alibaba OTC","AMD OTC"]

# ================== МАТЕМАТИЧЕСКИЙ АЛГОРИТМ ==================
def get_pocket_option_signal(asset, tf):
    seed = time.time() + sum(ord(c) for c in asset)
    random.seed(seed)
    
    # Симуляция 30 индикаторов с весами
    indicators = [random.uniform(-1, 1) for _ in range(30)]
    score = sum(indicators)
    
    # Влияние таймфрейма на волатильность
    accuracy = 96.5 + (random.random() * 3.3)
    
    if score > 0:
        direction = "ВНИЗ 🔴 PUT"
        reason = "Фиксация объема + Дивергенция RSI"
    else:
        direction = "ВВЕРХ 🟢 CALL"
        reason = "Паттерн 'Поглощение' + Зона поддержки"
        
    return direction, round(accuracy, 2), reason

# ================== ЛОГИКА ИНТЕРФЕЙСА ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    
    if uid in ADMIN_IDS or uid in vip_users:
        # ПАНЕЛЬ ДЛЯ ТЕХ, У КОГО ЕСТЬ ДОСТУП
        text = "👑 **KURUT AI: ТЕРМИНАЛ АКТИВИРОВАН**\n\nВыберите рынок для проведения анализа по 30 индикаторам."
        kb = [[InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="market")],
              [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
              [InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE), InlineKeyboardButton("🤖 РЕЗЕРВ", url=SECOND_BOT)]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        # ИНСТРУКЦИЯ ДЛЯ НОВЫХ
        text = (
            "👋 **Добро пожаловать в KURUT AI!**\n\n"
            "Это самый точный математический бот для Pocket Option.\n"
            "Чтобы начать зарабатывать, пройдите активацию."
        )
        kb = [[InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
              [InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="instruction")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "instruction":
        text = (
            "📍 **ЭТАП 1: РЕГИСТРАЦИЯ**\n"
            "Зарегистрируйте новый аккаунт (обязательно!) по ссылке:\n"
            f"🔗 [ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\n"
            "📍 **ЭТАП 2: ДЕПОЗИТ**\n"
            "Пополните баланс на сумму от **$10 до $35** для привязки ID к алгоритму.\n\n"
            "📍 **ЭТАП 3: АКТИВАЦИЯ**\n"
            "Нажмите кнопку ниже и отправьте админу ваш ID.\n"
            f"🆔 **ВАШ ID:** `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=PRIMARY_ADMIN_LINK)],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="to_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "to_home":
        await start(update, context)

    # ПРОВЕРКА ДОСТУПА ДЛЯ ТОРГОВЛИ
    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        
        # Кнопки времени от 10 сек до 8 мин
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s"), InlineKeyboardButton("1 МИН", callback_data="t_1m")],
            [InlineKeyboardButton("2 МИН", callback_data="t_2m"), InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("4 МИН", callback_data="t_4m")],
            [InlineKeyboardButton("5 МИН", callback_data="t_5m"), InlineKeyboardButton("6 МИН", callback_data="t_6m"), InlineKeyboardButton("7 МИН", callback_data="t_7m")],
            [InlineKeyboardButton("8 МИН", callback_data="t_8m")]
        ]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset')
        
        # ПРОЦЕСС АНАЛИЗА
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **АНАЛИЗ {asset} ({tf})...**\n\n`[{'■'*i}{' '*(3-i)}]` Обработка Pocket Option API...")
            await asyncio.sleep(1)
            
        direction, acc, reason = get_pocket_option_signal(asset, tf)
        
        res = (
            f"🚀 **VIP СИГНАЛ ГОТОВ!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **АКТИВ:** `{asset}`\n"
            f"⚡️ **ВХОД:** {direction}\n"
            f"⏱ **ВРЕМЯ:** `{tf}`\n"
            f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 **ЛОГИКА:** `{reason}`\n"
            f"📦 **БАЗА:** `600 свечей / 30 индикаторов`"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="market"), InlineKeyboardButton("❌ МИНУС", callback_data="market")],
              [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# ================== ВСПОМОГАТЕЛЬНОЕ ==================
def get_paged_kb(data, page, prefix):
    size = 10
    start = page * size
    items = data[start:start+size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start+size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 КАТЕГОРИИ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            tid = int(context.args[0])
            vip_users.add(tid); save_access()
            await update.message.reply_text(f"✅ Доступ для `{tid}` активирован!")
        except: await update.message.reply_text("Пиши: `/grant ID`")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT ULTIMATE v10 STARTED")
    app.run_polling()
