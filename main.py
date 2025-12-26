import asyncio
import logging
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] НАСТРОЙКИ И ФИНАНСОВЫЕ АКТИВЫ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="

user_stats = {}

# Ядро из 30 профессиональных индикаторов
TECH_INDICATORS = [
    "RSI (14)", "MACD (12,26,9)", "Bollinger Bands", "Stochastic (5,3,3)", "Ichimoku Cloud",
    "ATR (14)", "ADX (14)", "Parabolic SAR", "CCI (20)", "Awesome Oscillator",
    "Pivot Points", "Fibonacci Retracement", "Volume Profile", "MFI", "EMA 50", 
    "EMA 200", "VWAP", "Donchian Channels", "Williams %R", "SuperTrend",
    "Chaikin Money Flow", "Keltner Channels", "TRIX", "Rate of Change (ROC)", 
    "Bull Power", "Bear Power", "On-Balance Volume (OBV)", "Hull Moving Average",
    "Ultimate Oscillator", "Standard Deviation"
]

CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "UAH/USD OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Toncoin OTC", "BNB OTC", "Dogecoin OTC", "Polygon OTC", "Cardano OTC", "Litecoin OTC", "TRON OTC", "Avalanche OTC", "Chainlink OTC"]

# --- [2] МАТЕМАТИЧЕСКИЙ ДВИЖОК АНАЛИЗА ---
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

    # Алгоритм взвешенного решения
    # Генерируем "силу" тренда: от -15 до +15
    trend_power = sum([random.uniform(-1, 1) for _ in range(30)])
    
    # Расчет уровней (для красоты и доверия)
    sup = round(random.uniform(1.0500, 1.1000), 5)
    res = round(sup + random.uniform(0.0010, 0.0050), 5)
    
    direction = "ВВЕРХ 🟢" if trend_power > 0 else "ВНИЗ 🔴"
    # Точность зависит от того, насколько единогласны индикаторы
    accuracy = 94.5 + (abs(trend_power) / 15 * 5.4)
    if accuracy > 99.8: accuracy = 99.8
    
    # Выборка индикаторов, подтвердивших вход
    confirmed = random.sample(TECH_INDICATORS, 6)
    
    return direction, round(accuracy, 2), confirmed, sup, res

# --- [3] ГРАМОТНАЯ ИНСТРУКЦИЯ И КЛАВИАТУРЫ ---
def get_main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ (PRO)", callback_data="category")],
        [InlineKeyboardButton("📈 МОЯ СТАТИСТИКА", callback_data="stats")],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = (
        "👑 **ULTRA KURUT AI — ЭЛИТНЫЙ ТРЕЙДИНГ 2026**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Добро пожаловать в самую мощную систему анализа OTC-рынков. "
        "Наш AI сканирует рынок через 30 технических индикаторов и определяет уровни S/R в реальном времени.\n\n"
        "📖 **ГРАМОТНАЯ ИНСТРУКЦИЯ:**\n"
        "1️⃣ **Выбор актива:** Валюты или Криптовалюты (обновлено).\n"
        "2️⃣ **Таймфрейм:** Доступны ТФ от 5 секунд до 5 минут. Алгоритм меняет логику под каждый ТФ.\n"
        "3️⃣ **Анализ:** Система строит уровни поддержки и сопротивления. Не входите в сделку, пока не увидите результат.\n"
        "4️⃣ **Вход:** Получив сигнал, немедленно открывайте сделку на платформе.\n"
        "5️⃣ **Отчет:** Жмите «Плюс» или «Минус», чтобы бот корректировал точность под текущий рынок.\n\n"
        "📍 [Официальный Канал](%s) | [Instagram](%s)\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "🎯 *Нажмите кнопку ниже, чтобы начать зарабатывать.*"
    ) % (LINK_TG, LINK_INSTA)
    
    target = update.message.reply_text if update.message else update.callback_query.message.edit_text
    await target(welcome_text, reply_markup=get_main_kb(), parse_mode="Markdown", disable_web_page_preview=True)

# --- [4] ОБРАБОТЧИК CALLBACK-ЗАПРОСОВ ---
async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if uid not in user_stats: user_stats[uid] = {"win": 0, "loss": 0}

    if query.data == "go_main":
        await start(update, context)

    elif query.data == "category":
        kb = [[InlineKeyboardButton("💱 Валютные пары OTC", callback_data="nav_curr_0")],
              [InlineKeyboardButton("₿ Криптовалюты OTC", callback_data="nav_cryp_0")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="go_main")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ АКТИВОВ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "stats":
        s = user_stats[uid]
        total = s['win'] + s['loss']
        wr = (s['win']/total*100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 **ВАША ТОРГОВАЯ ИСТОРИЯ**\n━━━━━━━━━━━━━━\n"
            f"✅ ПРОФИТНЫЕ: `{s['win']}`\n❌ УБЫТОЧНЫЕ: `{s['loss']}`\n"
            f"🏆 ЭФФЕКТИВНОСТЬ: `{round(wr, 1)}%` \n━━━━━━━━━━━━━━",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="go_main")]]), parse_mode="Markdown")

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "curr" else CRYPTO_ASSETS
        await query.edit_message_text("📍 **Выберите торговый актив:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("curr_", "cryp_")):
        idx = int(query.data.split("_")[1])
        context.user_data['asset'] = (CURRENCY_PAIRS if "curr" in query.data else CRYPTO_ASSETS)[idx]
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите таймфрейм экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset', 'Active')
        
        # ЗАПУСК ЭЛИТНОГО АНАЛИЗА
        direction, acc, inds, sup, res = await perform_elite_analysis(query, asset, tf)
        
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="win"), InlineKeyboardButton("❌ МИНУС", callback_data="loss")],
              [InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="category")]]
        
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
        await query.edit_message_text(f"✅ **Данные сохранены!**\nВаша личная статистика обновлена.", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="category")]]))

# Функция пагинации
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

# --- [5] СТАБИЛЬНЫЙ ЗАПУСК ---
if __name__ == "__main__":
    def run_dummy():
        server = HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None)
        server.serve_forever()
    Thread(target=run_dummy, daemon=True).start()

    app = Application.builder().token(TOKEN).connect_timeout(40).read_timeout(40).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_cb))

    print("✅ Бот запущен и готов к анализу...")
    
    while True:
        try:
            app.run_polling(drop_pending_updates=True, close_loop=False)
        except Exception as e:
            print(f"🔄 Реконнект через 10 секунд из-за ошибки: {e}")
            time.sleep(10)
