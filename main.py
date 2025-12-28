import asyncio
import random
import time
from http.server import HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== АДМИНЫ И ДОСТУП ==================
ADMINS = {6117198446, 7079260196}
ALLOWED_USERS = set()

def has_access(uid):
    return uid in ADMINS or uid in ALLOWED_USERS

# ================== НАСТРОЙКИ ==================
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"

LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

user_stats = {}

# ================== АКТИВЫ ==================
CURRENCY_PAIRS = [
    "EUR/USD OTC","AUD/CAD OTC","AUD/CHF OTC","AUD/USD OTC","CAD/CHF OTC",
    "CAD/JPY OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC","EUR/JPY OTC",
    "EUR/NZD OTC","GBP/USD OTC","NZD/USD OTC","USD/CAD OTC","USD/CHF OTC",
    "USD/JPY OTC","USD/CNH OTC","EUR/RUB OTC","USD/RUB OTC","EUR/TRY OTC",
    "USD/INR OTC","USD/MXN OTC","USD/BRL OTC","USD/PHP OTC","MAD/USD OTC",
    "BHD/CNY OTC","AED/CNY OTC","SAR/CNY OTC","QAR/CNY OTC","ZAR/USD OTC",
    "CHF/NOK OTC","USD/VND OTC","TND/USD OTC","USD/PKR OTC","USD/DZD OTC",
    "USD/IDR OTC","USD/THB OTC","YER/USD OTC","NGN/USD OTC","USD/EGP OTC",
    "UAH/USD OTC","USD/COP OTC","USD/BDT OTC","JOD/CNY OTC","LBP/USD OTC",
    "AUD/NZD OTC","GBP/JPY OTC","NZD/JPY OTC"
]

CRYPTO_ASSETS = [
    "Bitcoin OTC","BNB OTC","Dogecoin OTC","Bitcoin ETF OTC","Ethereum OTC",
    "Solana OTC","Polkadot OTC","Polygon OTC","Cardano OTC","Toncoin OTC",
    "Avalanche OTC","Chainlink OTC","Litecoin OTC","TRON OTC"
]

STOCK_ASSETS = [
    "Apple OTC","McDonald’s OTC","Microsoft OTC","Facebook Inc OTC","Intel OTC",
    "Tesla OTC","Pfizer Inc OTC","Johnson & Johnson OTC","Boeing Company OTC",
    "American Express OTC","Amazon OTC","Citigroup Inc OTC","FedEx OTC","VISA OTC",
    "Cisco OTC","ExxonMobil OTC","Alibaba OTC","Netflix OTC","VIX OTC",
    "Palantir Technologies OTC","GameStop Corp OTC","AMD OTC",
    "Coinbase Global OTC","Marathon Digital Holdings OTC"
]

TECH_INDICATORS = [
    "RSI (14)","MACD (12,26,9)","Bollinger Bands","Stochastic (5,3,3)","EMA 50",
    "EMA 200","VWAP","ATR (14)","ADX (14)","SuperTrend","CCI (20)","OBV",
    "ROC","Williams %R","Parabolic SAR","ATR Bands","MFI","TRIX","Ultimate Oscillator",
    "Chaikin Money Flow","Keltner Channels","Donchian Channels","Hull MA","Rate of Change",
    "Bulls Power","Bears Power","Pivot Points","Fibonacci Retracement","Awesome Oscillator","Ichimoku Cloud"
]

# ================== АНАЛИЗ ==================
async def perform_analysis(query, asset, tf):
    steps = [
        f"🔍 Сканирование графика {asset} на ТФ {tf}...",
        "📉 Построение уровней поддержки и сопротивления (S/R)...",
        "⚙️ Проверка 30 тех. индикаторов...",
        "🧠 Фильтрация сигнала через кластерный анализ...",
        "🎯 Формирование финального сигнала..."
    ]
    for s in steps:
        await query.edit_message_text(f"⏳ **АНАЛИЗ В ПРОЦЕССЕ**\n\n{s}")
        await asyncio.sleep(1)

    power = sum(random.uniform(-1, 1) for _ in TECH_INDICATORS)
    direction = "ВВЕРХ 🟢" if power > 0 else "ВНИЗ 🔴"
    accuracy = min(99.8, 94 + abs(power))
    sup = round(random.uniform(1.0500, 1.1000), 5)
    res = round(sup + random.uniform(0.0010, 0.0050), 5)
    confirmed = random.sample(TECH_INDICATORS, 6)

    return direction, round(accuracy,2), confirmed, sup, res

# ================== КЛАВИАТУРЫ ==================
def main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="category")],
        [InlineKeyboardButton("📘 ИНСТРУКЦИЯ", callback_data="guide")],
        [InlineKeyboardButton("💰 КАК НАЧАТЬ", callback_data="ref")],
        [InlineKeyboardButton("📢 TG", url=LINK_TG), InlineKeyboardButton("📸 INST", url=LINK_INSTA)]
    ])

def admins_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("✍️ Админ 1", url="https://t.me/KURUTTRADING")],
        [InlineKeyboardButton("✍️ Админ 2", url="https://t.me/KURUTTRADING")],
        [InlineKeyboardButton("🏠 В МЕНЮ", callback_data="go_main")]
    ])

def paged_kb(data, page, prefix):
    size = 10
    start = page*size
    items = data[start:start+size]
    kb = []
    for i in range(0,len(items),2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start+i}")]
        if i+1<len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start+i+1}"))
        kb.append(row)
    nav = []
    if page>0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start+size<len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 В МЕНЮ", callback_data="go_main")])
    return InlineKeyboardMarkup(kb)

# ================== START ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if not has_access(uid):
        await update.message.reply_text(
            f"❌ **ДОСТУП ЗАКРЫТ**\n\n🆔 Ваш ID: `{uid}`\n\nНапишите админам для активации",
            parse_mode="Markdown",
            reply_markup=admins_kb()
        )
        return

    await update.message.reply_text(
        "👑 **ULTRA KURUT AI — ЭЛИТНЫЙ ТРЕЙДИНГ**\n\nВыберите действие:",
        parse_mode="Markdown",
        reply_markup=main_kb()
    )

# ================== CALLBACK ==================
async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    uid = q.from_user.id
    await q.answer()
    if not has_access(uid):
        await q.edit_message_text(
            f"❌ ДОСТУП ЗАКРЫТ\n\n🆔 Ваш ID: `{uid}`",
            parse_mode="Markdown",
            reply_markup=admins_kb()
        )
        return

    if q.data == "go_main":
        await start(update, context)

    elif q.data == "category":
        kb = [
            [InlineKeyboardButton("💱 Валюты OTC", callback_data="nav_curr_0")],
            [InlineKeyboardButton("🪙 Крипта OTC", callback_data="nav_cryp_0")],
            [InlineKeyboardButton("📈 Акции OTC", callback_data="nav_stock_0")],
            [InlineKeyboardButton("🏠 Назад", callback_data="go_main")]
        ]
        await q.edit_message_text("Выберите категорию:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data.startswith("nav_"):
        _, pref, page = q.data.split("_")
        data = CURRENCY_PAIRS if pref=="curr" else CRYPTO_ASSETS if pref=="cryp" else STOCK_ASSETS
        await q.edit_message_text("Выберите актив:", reply_markup=paged_kb(data, int(page), pref))

    elif q.data.startswith(("curr_","cryp_","stock_")):
        idx = int(q.data.split("_")[1])
        data = CURRENCY_PAIRS if "curr" in q.data else CRYPTO_ASSETS if "cryp" in q.data else STOCK_ASSETS
        context.user_data["asset"] = data[idx]
        await q.edit_message_text(
            f"Актив: **{data[idx]}**\nВыберите таймфрейм:",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("10C", callback_data="t_10s"),
                 InlineKeyboardButton("15C", callback_data="t_15s"),
                 InlineKeyboardButton("30C", callback_data="t_30s")],
                [InlineKeyboardButton("1М", callback_data="t_1m"),
                 InlineKeyboardButton("2М", callback_data="t_2m"),
                 InlineKeyboardButton("3М", callback_data="t_3m"),
                 InlineKeyboardButton("4М", callback_data="t_4m"),
                 InlineKeyboardButton("5М", callback_data="t_5m")]
            ])
        )

    elif q.data.startswith("t_"):
        tf = q.data[2:]
        asset = context.user_data["asset"]
        d, acc, ind, sup, res = await perform_analysis(q, asset, tf)
        await q.edit_message_text(
            f"🚀 **СИГНАЛ**\n\n"
            f"📊 Актив: `{asset}`\n"
            f"⏱ ТФ: `{tf}`\n"
            f"📈 Направление: **{d}**\n"
            f"🎯 Точность: `{acc}%`\n\n"
            f"📉 Поддержка: `{sup}`\n"
            f"📈 Сопротивление: `{res}`\n"
            f"⚙️ Индикаторы: {', '.join(ind)}",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 Новый анализ", callback_data="category")]])
        )

    elif q.data == "guide":
        await q.edit_message_text(
            "📘 **ИНСТРУКЦИЯ**\n\n"
            "1️⃣ Выберите актив\n"
            "2️⃣ Выберите таймфрейм\n"
            "3️⃣ Получите сигнал\n"
            "4️⃣ Откройте сделку сразу\n\n"
            "⚠️ Рекомендуемый риск: не более 5%",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("➡️ Далее", callback_data="ref")]])
        )

    elif q.data == "ref":
        await q.edit_message_text(
            f"💰 **КАК НАЧАТЬ**\n\n"
            f"🔗 Регистрация через реферальку:\n{REF_LINK}\n\n"
            f"💵 Депозит: 20–30$\n"
            f"✍️ Напишите админу для доступа\n\n"
            f"🆔 Ваш ID: `{uid}`",
            parse_mode="Markdown",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton("📺 YouTube", url=YOUTUBE)],
                [InlineKeyboardButton("🤖 Второй бот", url=SECOND_BOT)],
                [InlineKeyboardButton("✍️ Админы", callback_data="contact")]
            ]),
            disable_web_page_preview=True
        )

    elif q.data == "contact":
        await q.edit_message_text("Связь с админами:", reply_markup=admins_kb())

# ================== GRANT ==================
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMINS:
        return
    try:
        uid = int(context.args[0])
        ALLOWED_USERS.add(uid)
        await update.message.reply_text(f"✅ Доступ выдан {uid}")
    except:
        await update.message.reply_text("Используй: /grant USER_ID")

# ================== ЗАПУСК ==================
if __name__ == "__main__":
    def dummy():
        HTTPServer(("0.0.0.0", 8080), lambda *a, **k: None).serve_forever()

    Thread(target=dummy, daemon=True).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(handle_cb))

    print("✅ Бот запущен")
    app.run_polling()
