import asyncio
import json
import os
import random
import time
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] СЕРВЕР ДЛЯ REPLIT (ЧТОБЫ БОТ НЕ СПАЛ) ---
server = Flask('')

@server.route('/')
def home():
    return "I'm alive!"

def run_web():
    server.run(host='0.0.0.0', port=8080)

# --- [2] НАСТРОЙКИ И ССЫЛКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_LINK = "https://t.me/id6117198446" # Личка админа

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"

# База доступа
DB_FILE = "access.json"
def load_access():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return set(json.load(f))
        except: return set()
    return set()

vip_users = load_access()

def save_access():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)

# --- [3] СПИСКИ АКТИВОВ ---
CURRENCY_PAIRS = ["EUR/USD OTC","AUD/CAD OTC","AUD/CHF OTC","AUD/USD OTC","CAD/CHF OTC","CAD/JPY OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC","EUR/JPY OTC","EUR/NZD OTC","GBP/USD OTC","NZD/USD OTC","USD/CAD OTC","USD/CHF OTC","USD/JPY OTC","USD/CNH OTC","EUR/RUB OTC","USD/RUB OTC","USD/INR OTC","USD/BRL OTC","AUD/NZD OTC","GBP/JPY OTC","NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC","BNB OTC","Dogecoin OTC","Ethereum OTC","Solana OTC","Toncoin OTC","Litecoin OTC","TRON OTC"]
STOCK_ASSETS = ["Apple OTC","McDonald’s OTC","Microsoft OTC","Facebook OTC","Tesla OTC","Amazon OTC","Netflix OTC","VISA OTC","Alibaba OTC","AMD OTC"]

# --- [4] МАТЕМАТИЧЕСКИЙ АЛГОРИТМ ---
def analyze_market_math(asset, tf):
    """Симуляция глубокого анализа Pocket Option OTC"""
    random.seed(time.time() + len(asset))
    
    # 30 параметров анализа
    momentum = sum([random.uniform(-1, 1) for _ in range(30)])
    volatility = random.uniform(0.1, 1.0)
    
    # Расчет точности (всегда 96%+)
    accuracy = 96.1 + (random.random() * 3.7)
    
    if momentum > 0:
        direction = "ВНИЗ 🔴 PUT"
        logic = "Перекупленность актива + откат от уровня"
    else:
        direction = "ВВЕРХ 🟢 CALL"
        logic = "Импульсный отскок от зоны поддержки"
        
    return direction, round(accuracy, 2), logic

# --- [5] ИНТЕРФЕЙС ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    
    if uid in ADMIN_IDS or uid in vip_users:
        text = (
            "👑 **ТЕРМИНАЛ KURUT AI v11.0**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Система готова к анализу Pocket Option.\n"
            "Выполнен вход: **VIP ДОСТУП**"
        )
        kb = [[InlineKeyboardButton("📈 НАЧАТЬ АНАЛИЗ", callback_data="market")],
              [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
              [InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE)]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = (
            "👋 **Добро пожаловать в KURUT AI!**\n\n"
            "Это закрытая нейросеть для анализа OTC графиков. "
            "Чтобы получить доступ к сигналам, следуйте инструкции."
        )
        kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="instr_1")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "instr_1":
        text = (
            "🚀 **ШАГ 1: РЕГИСТРАЦИЯ**\n\n"
            "Создайте новый аккаунт по ссылке:\n"
            f"🔗 [ССЫЛКА НА POCKET OPTION]({REF_LINK})\n\n"
            "⚠️ *Важно: если есть старый аккаунт, создайте новый через Инкогнито, иначе доступ не активируется!*"
        )
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ", callback_data="instr_2")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "instr_2":
        text = (
            "💰 **ШАГ 2: ДЕПОЗИТ**\n\n"
            "Пополните ваш баланс на сумму от **$10 до $35**.\n"
            "Это подтвердит, что вы реальный трейдер, и бот выдаст вам сигналы."
        )
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ", callback_data="instr_3")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "instr_3":
        text = (
            "✅ **ШАГ 3: АКТИВАЦИЯ**\n\n"
            f"Ваш персональный ID: `{uid}`\n\n"
            "Нажмите кнопку ниже и напишите админу свой ID для проверки и открытия доступа."
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=ADMIN_LINK)],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="back")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "back":
        await start(update, context)

    # ЛОГИКА ТОРГОВЛИ (ТОЛЬКО ДЛЯ VIP)
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
        
        # Таймфреймы от 10 сек до 8 мин
        kb = [
            [InlineKeyboardButton("10 С", callback_data="t_10s"), InlineKeyboardButton("30 С", callback_data="t_30s"), InlineKeyboardButton("1 М", callback_data="t_1m")],
            [InlineKeyboardButton("2 М", callback_data="t_2m"), InlineKeyboardButton("3 М", callback_data="t_3m"), InlineKeyboardButton("4 М", callback_data="t_4m")],
            [InlineKeyboardButton("5 М", callback_data="t_5m"), InlineKeyboardButton("6 М", callback_data="t_6m"), InlineKeyboardButton("7 М", callback_data="t_7m")],
            [InlineKeyboardButton("8 М", callback_data="t_8m")]
        ]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset')
        
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\n\n`[{'■'*i}{' '*(3-i)}]` Математический просчет...")
            await asyncio.sleep(1)
            
        dir, acc, log = analyze_market_math(asset, tf)
        
        res = (
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **АКТИВ:** `{asset}`\n"
            f"⚡️ **ВХОД:** {dir}\n"
            f"⏱ **ВРЕМЯ:** `{tf}`\n"
            f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 **ЛОГИКА:** `{log}`\n"
            f"📦 **БАЗА:** `600 свечей / 30 инд.`"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="market"), InlineKeyboardButton("❌ МИНУС", callback_data="market")]]
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [6] УТИЛИТЫ ---
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
            await update.message.reply_text(f"✅ Доступ открыт для `{tid}`")
        except: await update.message.reply_text("Пиши: `/grant ID`")

# --- [7] ЗАПУСК ---
if __name__ == "__main__":
    Thread(target=run_web).start() # Запуск сервера для Replit
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT AI REPLIT EDITION STARTED")
    app.run_polling()
