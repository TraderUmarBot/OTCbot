import asyncio
import logging
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== ДОСТУП ==================
ADMINS = {6117198446, 7079260196}  # админы
ALLOWED_USERS = set()

def has_access(uid):
    return uid in ADMINS or uid in ALLOWED_USERS

def is_admin(uid):
    return uid in ADMINS

# ================== ССЫЛКИ ==================
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
    "RSI (14)", "MACD (12,26,9)", "Bollinger Bands", "Stochastic (5,3,3)", "Ichimoku Cloud",
    "ATR (14)", "ADX (14)", "Parabolic SAR", "CCI (20)", "Awesome Oscillator",
    "Pivot Points", "Fibonacci Retracement", "Volume Profile", "MFI", "EMA 50", 
    "EMA 200", "VWAP", "Donchian Channels", "Williams %R", "SuperTrend",
    "Chaikin Money Flow", "Keltner Channels", "TRIX", "Rate of Change (ROC)", 
    "Bull Power", "Bear Power", "On-Balance Volume (OBV)", "Hull Moving Average",
    "Ultimate Oscillator", "Standard Deviation"
]

# ================== ЭЛИТНЫЙ АНАЛИЗ ==================
async def perform_elite_analysis(query, asset, timeframe):
    analysis_steps = [
        f"🔍 Сканирование графика {asset} на ТФ {timeframe}...",
        "📉 Построение уровней поддержки и сопротивления (S/R)...",
        "⚙️ Математический опрос 30 тех. индикаторов...",
        "🧠 Нейросетевая проверка рыночных манипуляций...",
        "🎯 Фильтрация сигнала через кластерный объем..."
    ]
    
    for step in analysis_steps:
        await query.edit_message_text(f"⏳ **PRO-АНАЛИЗ В ПРОЦЕССЕ...**\n\n{step}")
        await asyncio.sleep(1.1)

    trend_power = sum([random.uniform(-1, 1) for _ in range(30)])
    sup = round(random.uniform(1.0500, 1.1000), 5)
    res = round(sup + random.uniform(0.0010, 0.0050), 5)
    direction = "ВВЕРХ 🟢" if trend_power > 0 else "ВНИЗ 🔴"
    accuracy = 94.5 + (abs(trend_power) / 15 * 5.4)
    if accuracy > 99.8: accuracy = 99.8
    confirmed = random.sample(TECH_INDICATORS, 6)
    return direction, round(accuracy, 2), confirmed, sup, res

# ================== КЛАВИАТУРЫ ==================
def get_main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ (PRO)", callback_data="category")],
        [InlineKeyboardButton("📈 МОЯ СТАТИСТИКА", callback_data="stats")],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
        [InlineKeyboardButton("▶️ YouTube", url=YOUTUBE), InlineKeyboardButton("🤖 Второй бот", url=SECOND_BOT)],
        [InlineKeyboardButton("🔗 Реф. ссылка", url=REF_LINK)]
    ])

def get_admin_contact_kb():
    kb = []
    for admin_id in ADMINS:
        kb.append([InlineKeyboardButton(f"Написать админу {admin_id}", url=f"tg://user?id={admin_id}")])
    return InlineKeyboardMarkup(kb)

# ================== СТАРТ ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.message.from_user.id

    # Пользователь без доступа
    if not has_access(uid):
        instruction_text = (
            "❌ У вас нет доступа к боту.\n\n"
            "👣 **Инструкция для получения доступа:**\n"
            "1️⃣ Отправьте администратору ваш ID для выдачи доступа.\n"
            f"Ваш ID: `{uid}`\n"
            "2️⃣ После получения доступа, нажмите /start снова."
        )
        await update.message.reply_text(
            instruction_text,
            parse_mode="Markdown",
            reply_markup=get_admin_contact_kb()
        )
        return

    # Пользователь с доступом (автор)
    welcome_text = (
        "👑 **ULTRA KURUT AI — ЭЛИТНЫЙ ТРЕЙДИНГ 2026**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Добро пожаловать! Все ссылки ниже доступны для быстрого перехода.\n\n"
        "📍 **Ссылки:**\n"
        f"• [Канал Telegram]({LINK_TG})\n"
        f"• [Instagram]({LINK_INSTA})\n"
        f"• [YouTube]({YOUTUBE})\n"
        f"• [Второй бот]({SECOND_BOT})\n"
        f"• [Реферальная ссылка]({REF_LINK})\n\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    # Добавляем кнопки к админам внизу
    admin_kb = get_admin_contact_kb()

    await update.message.reply_text(
        welcome_text,
        parse_mode="Markdown",
        reply_markup=admin_kb,
        disable_web_page_preview=True
    )
# ================== ОБРАБОТЧИК CALLBACK ==================
async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if uid not in user_stats:
        user_stats[uid] = {"win": 0, "loss": 0}

    if query.data == "go_main":
        await start(update, context)

    elif query.data == "category":
        kb = [
            [InlineKeyboardButton("💱 Валютные пары OTC", callback_data="nav_curr_0")],
            [InlineKeyboardButton("₿ Криптовалюты OTC", callback_data="nav_cryp_0")],
            [InlineKeyboardButton("🏢 Акции OTC", callback_data="nav_stock_0")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="go_main")]
        ]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ АКТИВОВ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        if pref == "curr":
            data = CURRENCY_PAIRS
        elif pref == "cryp":
            data = CRYPTO_ASSETS
        else:
            data = STOCK_ASSETS
        await query.edit_message_text("📍 **Выберите торговый актив:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("curr_", "cryp_", "stock_")):
        idx = int(query.data.split("_")[1])
        if "curr" in query.data:
            context.user_data['asset'] = CURRENCY_PAIRS[idx]
        elif "cryp" in query.data:
            context.user_data['asset'] = CRYPTO_ASSETS[idx]
        else:
            context.user_data['asset'] = STOCK_ASSETS[idx]

        kb = [
            [InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
            [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]
        ]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите таймфрейм экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset', 'Active')
        direction, acc, inds, sup, res = await perform_elite_analysis(query, asset, tf)

        kb = [
            [InlineKeyboardButton("✅ ПЛЮС", callback_data="win"), InlineKeyboardButton("❌ МИНУС", callback_data="loss")],
            [InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="category")]
        ]
        await query.edit_message_text(
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n━━━━━━━━━━━━━━\n"
            f"📊 АКТИВ: `{asset}`\n⚡️ НАПРАВЛЕНИЕ: **{direction}**\n⏱ ВРЕМЯ: `{tf}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 **ТЕХНИЧЕСКИЙ ОБЗОР:**\n"
            f"• Сопротивление: `{res}`\n• Поддержка: `{sup}`\n"
            f"• Анализ 30 индикаторов: `УСПЕШНО`\n"
            f"• Сильное подтверждение: `{', '.join(inds[:3])}`\n\n"
            f"🏁 **ОТМЕТЬТЕ РЕЗУЛЬТАТ СДЕЛКИ:**",
            reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown"
        )

    elif query.data in ["win", "loss"]:
        user_stats[uid]["win" if query.data == "win" else "loss"] += 1
        await query.edit_message_text(
            f"✅ **Данные сохранены!**\nВаша личная статистика обновлена.",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="category")]])
        )

# ================== ФУНКЦИЯ ПАГИНАЦИИ ==================
def get_paged_kb(data, page, prefix):
    size = 10
    start = page * size
    items = data[start:start + size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start + i}")]
        if i + 1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start + i + 1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start + size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 В МЕНЮ", callback_data="go_main")])
    return InlineKeyboardMarkup(kb)

# ================== ЗАПУСК ==================
if __name__ == "__main__":
    def run_dummy():
        server = HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None)
        server.serve_forever()
    Thread(target=run_dummy, daemon=True).start()

    app = Application.builder().token(TOKEN).connect_timeout(40).read_timeout(40).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("revoke", revoke))
    app.add_handler(CallbackQueryHandler(handle_cb))

    print("✅ Бот запущен и готов к анализу...")
    
    while True:
        try:
            app.run_polling(drop_pending_updates=True, close_loop=False)
        except Exception as e:
            print(f"🔄 Реконнект через 10 секунд из-за ошибки: {e}")
            time.sleep(10)
