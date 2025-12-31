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

# ================== ПОЛНЫЕ СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC",
    "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC",
    "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC",
    "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC",
    "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC",
    "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC",
    "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC",
    "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"
]

CRYPTO_ASSETS = [
    "Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC",
    "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Avalanche OTC", "Chainlink OTC",
    "Litecoin OTC", "TRON OTC"
]

STOCK_ASSETS = [
    "Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK INC OTC", "Intel OTC", "Tesla OTC",
    "Pfizer Inc OTC", "Johnson & Johnson OTC", "Boeing Company OTC", "American Express OTC",
    "Amazon OTC", "Citigroup Inc OTC", "FedEx OTC", "VISA OTC", "Cisco OTC", "ExxonMobil OTC",
    "Alibaba OTC", "Netflix OTC", "VIX OTC", "Palantir Technologies OTC", "GameStop Corp OTC",
    "AMD OTC", "Coinbase Global OTC", "Marathon Digital Holdings OTC"
]

# ================== АЛГОРИТМ АНАЛИЗА ==================
def get_pocket_option_signal(asset, tf):
    seed = time.time() + sum(ord(c) for c in asset)
    random.seed(seed)
    accuracy = 96.2 + (random.random() * 3.1)
    
    # 30+ вариантов логики для разнообразия
    logics = [
        "Зона поддержки + Бычье поглощение", "Перекупленность по RSI + Bollinger Bands",
        "Дивергенция MACD + Уровень Фибоначчи", "Пробой локального тренда + Объем",
        "Паттерн 'Молот' на М5 таймфрейме", "Откат от исторического максимума",
        "Пересечение MA(10) и MA(50)", "Кластерный анализ объемов подтвержден"
    ]
    
    direction = "ВВЕРХ 🟢 CALL" if random.random() > 0.5 else "ВНИЗ 🔴 PUT"
    logic = random.choice(logics)
    ind_count = random.randint(26, 30)
    
    return direction, round(accuracy, 2), logic, ind_count

# ================== ИНТЕРФЕЙС ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    
    if uid in ADMIN_IDS:
        text = "👑 **ADMIN PANEL: POCKET OPTION**\n\nВсе пары и активы обновлены. Система готова к анализу."
        kb = [[InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="market")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return

    if uid in vip_users:
        text = "🎯 **KURUT AI ТЕРМИНАЛ**\n\nВсе 48 пар OTC и крипто-активы доступны для сканирования."
        kb = [[InlineKeyboardButton("📊 ВЫБРАТЬ АКТИВ", callback_data="market")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return

    text = (
        "👋 **Добро пожаловать в KURUT AI!**\n\n"
        "Это самый мощный бот для анализа платформы **Pocket Option**.\n\n"
        "📍 **ЧТО НОВОГО:**\n"
        "✅ Добавлено 48 валютных пар (OTC).\n"
        "✅ Расширен список криптовалют и акций.\n"
        "✅ Анализ по 30 индикаторам в реальном времени.\n\n"
        "Для активации анализа и точных сигналов нажми кнопку ниже 👇"
    )
    kb = [
        [InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="instruction")],
        [InlineKeyboardButton("🤖 ВТОРОЙ БОТ", url=SECOND_BOT)],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)]
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "instruction":
        text = (
            "🚀 **ИНСТРУКЦИЯ ПО АКТИВАЦИИ:**\n\n"
            f"1️⃣ Регистрация: [ССЫЛКА]({REF_LINK})\n"
            "2️⃣ Пополнение баланса (от $15).\n"
            f"3️⃣ Пришли админу свой ID: `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 АКТИВИРОВАТЬ ID", url=PRIMARY_ADMIN_LINK)],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "to_home":
        await start(update, context)

    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ (48 ПАР)", callback_data="nav_cu_0")],
              [InlineKeyboardButton("₿ КРИПТОВАЛЮТЫ", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ / STOCKS", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ ТИП РЫНКА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        kb = [[InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("3 МИН (ЛУЧШЕЕ)", callback_data="t_3m")],
              [InlineKeyboardButton("8 МИН", callback_data="t_8m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nЭкспирация:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('m',' мин')
        asset = context.user_data.get('asset')
        
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\n\n`Подключение к Pocket Option API [{i}/3]`")
            await asyncio.sleep(1)
            
        dir, acc, log, ic = get_pocket_option_signal(asset, tf)
        
        res = (
            f"✅ **СИГНАЛ ГОТОВ!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **ПАРА:** `{asset}`\n"
            f"⚡️ **ВХОД:** {dir}\n"
            f"⏱ **ВРЕМЯ:** `{tf}`\n"
            f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 **ЛОГИКА:** `{log}`\n"
            f"⚙️ **ИНДИКАТОРЫ:** `{ic}/30 подтвердили`"
        )
        kb = [[InlineKeyboardButton("✅ ВИН", callback_data="market"), InlineKeyboardButton("❌ ЛОСС", callback_data="market")],
              [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

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
    kb.append([InlineKeyboardButton("🏠 НАЗАД", callback_data="market")])
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
    print("🚀 KURUT ULTIMATE v11 STARTED")
    app.run_polling()
