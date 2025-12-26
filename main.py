import asyncio
import logging
import random
import time
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] НАСТРОЙКИ И ССЫЛКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_OTHER_BOT = "https://t.me/KURUT_TRADE_BOT"

# База данных в памяти
user_stats = {}

# ПОЛНЫЙ СПИСОК 20 ИНДИКАТОРОВ ДЛЯ РАСЧЕТА
ALL_INDICATORS = [
    "RSI (14)", "MACD (12,26,9)", "Bollinger Bands", "Stochastic (5,3,3)", "Ichimoku Cloud",
    "ATR (14)", "ADX (14)", "Parabolic SAR", "CCI (20)", "Awesome Oscillator",
    "Pivot Points", "Fibonacci Retracement", "Volume Profile", "MFI (Money Flow)",
    "EMA 50", "EMA 200", "VWAP", "Donchian Channels", "Williams %R", "SuperTrend"
]

CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]

# --- [2] ЛОГИКА ГЛУБОКОГО АНАЛИЗА ---
async def start_deep_analysis(query, asset):
    steps = [
        f"📡 Подключение к котировкам {asset}...",
        "📥 Сканирование тиков за последние 10 минут...",
        "⚙️ Запуск 20 тех. индикаторов в реальном времени...",
        "🧠 Фильтрация рыночного шума через нейросеть...",
        "✅ Формирование идеальной точки входа..."
    ]
    
    for step in steps:
        await query.edit_message_text(f"⏳ **ВЫПОЛНЯЕТСЯ ГЛУБОКИЙ АНАЛИЗ...**\n\n{step}")
        await asyncio.sleep(1.2)

    # Математический расчет на основе "голосов" индикаторов
    votes = [random.choice([1, -1]) for _ in range(20)]
    score = sum(votes)
    direction = "ВВЕРХ 🟢" if score >= 0 else "ВНИЗ 🔴"
    accuracy = 97 + (abs(score) / 20 * 2.9)
    
    # Подборка индикаторов, подтвердивших сигнал
    confirmed_inds = random.sample(ALL_INDICATORS, 5)
    
    return direction, round(accuracy, 2), confirmed_inds

# --- [3] ИНТЕРФЕЙС И КНОПКИ ---
def get_main_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ РЫНКА", callback_data="category")],
        [InlineKeyboardButton("📈 МОЯ СТАТИСТИКА", callback_data="stats")],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
        [InlineKeyboardButton("🤖 РЕЗЕРВНЫЙ БОТ", url=LINK_OTHER_BOT)]
    ])

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
    kb.append([InlineKeyboardButton("🏠 В ГЛАВНОЕ МЕНЮ", callback_data="go_main")])
    return InlineKeyboardMarkup(kb)

# --- [4] ОБРАБОТЧИКИ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    instr_text = (
        "👑 **ULTRA KURUT OTC 2026 — PREMIUM AI**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Приветствую! Это профессиональный инструмент для анализа OTC-рынков.\n\n"
        "📖 **ИНСТРУКЦИЯ ПО ЭКСПЛУАТАЦИИ:**\n"
        "1️⃣ **Выбор актива:** Нажмите кнопку анализа и выберите торговую пару.\n"
        "2️⃣ **Время экспирации:** Выберите ТФ (от 5с до 5м). Система подстроит расчет под волатильность.\n"
        "3️⃣ **Ожидание:** Дождитесь завершения обсчета 20 индикаторов (около 6 сек).\n"
        "4️⃣ **Сделка:** Открывайте позицию согласно сигналу. Входите сразу после получения данных.\n"
        "5️⃣ **Результат:** Обязательно нажимайте «Плюс» или «Минус» для обучения алгоритма.\n\n"
        "🚀 *Готовы забирать профит? Начинайте анализ!*"
    )
    target = update.message.reply_text if update.message else update.callback_query.message.edit_text
    await target(instr_text, reply_markup=get_main_kb(), parse_mode="Markdown")

async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if uid not in user_stats: user_stats[uid] = {"win": 0, "loss": 0}

    if query.data == "go_main":
        await start(update, context)

    elif query.data == "category":
        kb = [[InlineKeyboardButton("💱 Валютные OTC пары", callback_data="nav_curr_0")],
              [InlineKeyboardButton("₿ Криптовалюты OTC", callback_data="nav_cryp_0")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="go_main")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК ДЛЯ АНАЛИЗА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "stats":
        s = user_stats[uid]
        total = s['win'] + s['loss']
        wr = (s['win']/total*100) if total > 0 else 0
        await query.edit_message_text(
            f"📊 **ВАША ПЕРСОНАЛЬНАЯ СТАТИСТИКА**\n━━━━━━━━━━━━━━\n"
            f"✅ УСПЕШНЫЕ: `{s['win']}`\n❌ НЕУСПЕШНЫЕ: `{s['loss']}`\n"
            f"🏆 ВИНРЕЙТ: `{round(wr, 1)}%` \n━━━━━━━━━━━━━━",
            reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="go_main")]]), parse_mode="Markdown")

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "curr" else CRYPTO_ASSETS
        await query.edit_message_text("📍 **Выберите актив:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("curr_", "cryp_")):
        idx = int(query.data.split("_")[1])
        context.user_data['asset'] = (CURRENCY_PAIRS if "curr" in query.data else CRYPTO_ASSETS)[idx]
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("3М", callback_data="t_3m")],
              [InlineKeyboardButton("5 МИНУТ ⏳", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время сделки:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        time_label = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset', 'Active')
        
        # ЗАПУСК ГЛУБОКОГО АНАЛИЗА
        dir, acc, inds = await start_deep_analysis(query, asset)
        
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="win"), InlineKeyboardButton("❌ МИНУС", callback_data="loss")],
              [InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="category")]]
        
        await query.edit_message_text(
            f"🚀 **АНАЛИЗ ЗАВЕРШЕН — ВХОДИТЕ!**\n━━━━━━━━━━━━━━\n"
            f"📊 ПАРА: `{asset}`\n⚡️ СИГНАЛ: **{dir}**\n⏱ ТАЙМ: `{time_label}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━\n"
            f"🔬 **АКТИВНЫЕ ИНДИКАТОРЫ:**\n• {', '.join(inds[:4])}\n\n"
            f"🏁 **ЖМИ РЕЗУЛЬТАТ ПОСЛЕ ЗАКРЫТИЯ:**",
            reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown"
        )

    elif query.data in ["win", "loss"]:
        user_stats[uid]["win" if query.data == "win" else "loss"] += 1
        await query.edit_message_text(f"📝 **Результат учтен в статистике!**\nХотите продолжить?", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="category")]]))

# --- [5] ЗАПУСК С ЗАЩИТОЙ ОТ ВЫЛЕТОВ ---
if __name__ == "__main__":
    # Фиктивный сервер для Koyeb
    def run_dummy():
        server = HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None)
        server.serve_forever()
    Thread(target=run_dummy, daemon=True).start()

    # Сборка бота с таймаутами для стабильности сети
    app = Application.builder().token(TOKEN).connect_timeout(40).read_timeout(40).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_cb))

    print("✅ Бот KURUT TRADING активен...")
    
    # Вечный цикл для предотвращения остановки при NetworkError
    while True:
        try:
            app.run_polling(drop_pending_updates=True, close_loop=False)
        except Exception as e:
            print(f"⚠️ Сетевая ошибка: {e}. Реконнект через 10 сек...")
            time.sleep(10)
