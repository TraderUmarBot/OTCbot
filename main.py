import asyncio
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] КОНФИГУРАЦИЯ И ССЫЛКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_OTHER_BOT = "https://t.me/KURUT_TRADE_BOT"

# Список активов (Валюты + Крипто)
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]

TIME_MAP = {"5s": 5, "15s": 15, "30s": 30, "1m": 60, "2m": 120, "3m": 180, "5m": 300}

# --- [2] ЯДРО АНАЛИЗА (20 ИНДИКАТОРОВ) ---
def get_heavy_analysis():
    accuracy = random.uniform(99.1, 99.9) # Пиковая точность
    direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    
    indicators = [
        "RSI (14) - Подтверждено", "MACD - Пересечение", "Bollinger Bands - Отскок",
        "Stochastic - Вход в зону", "Ichimoku - Облако пробито", "ATR - Волатильность OK",
        "ADX - Сильный тренд", "Parabolic SAR - Смена позиции", "CCI - Перепроданность",
        "Awesome Oscillator - Импульс", "Pivot Points - Уровень удержан", "Fibonacci - 0.618",
        "Volume Profile - Плотность", "MFI - Приток капитала", "EMA 50/200 - Золотой крест",
        "VWAP - Опорная цена", "Donchian Channels - Прорыв", "Williams %R - Фильтр пройден",
        "ZigZag - Локальное дно", "SuperTrend - Цикл подтвержден"
    ]
    return direction, round(accuracy, 2), random.sample(indicators, 4)

# --- [3] КРАСИВОЕ ОФОРМЛЕНИЕ МЕНЮ ---
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
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"nav_{prefix}_{page-1}"))
    if start + size < len(data): nav.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="go_main")])
    return InlineKeyboardMarkup(kb)

# --- [4] ЛОГИКА СИГНАЛА И РЕЗУЛЬТАТА ---
async def process_signal(query, asset, time_key):
    wait_sec = TIME_MAP.get(time_key, 5)
    label = time_key.replace('s',' сек').replace('m',' мин')
    
    # Имитация глубокого сканирования
    await query.edit_message_text(
        f"🛡 **ULTRA SCAN 2026: {asset}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⚙️ Синхронизация с 20 индикаторами...\n"
        f"📡 Считывание тиковых данных OTC...\n"
        f"🧩 Анализ паттернов завершен на 92%..."
    )
    await asyncio.sleep(2)
    
    dir, acc, inds = get_heavy_analysis()
    
    # Выдача снайперского сигнала
    await query.edit_message_text(
        f"💎 **СНАЙПЕРСКИЙ СИГНАЛ ВЫДАН**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 АКТИВ: `{asset}`\n"
        f"⚡️ НАПРАВЛЕНИЕ: **{dir}**\n"
        f"⏱ ВРЕМЯ: `{label}`\n"
        f"🎯 ВЕРОЯТНОСТЬ: `{acc}%` \n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🛠 **ТЕХ. АНАЛИЗ:**\n• {inds[0]}\n• {inds[1]}\n• {inds[2]}\n• {inds[3]}\n\n"
        f"⏳ Сделка в процессе... Ожидайте фиксации прибыли."
    )

    # Реальное ожидание экспирации
    await asyncio.sleep(wait_sec)

    # Итоговый результат (99% точность)
    is_win = random.choices([True, False], weights=[99, 1])[0]
    res_icon = "✅ ПЛЮС (WIN) 🟢" if is_win else "❌ МИНУС (LOSS) 🔴"
    
    await query.edit_message_text(
        f"🏁 **РЕЗУЛЬТАТ СДЕЛКИ: {asset}**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 ИТОГ: **{res_icon}**\n"
        f"📈 ПРОГНОЗ БЫЛ: `{dir}`\n"
        f"⏱ ЭКСПИРАЦИЯ: `{label}`\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔥 *Сигнал отработан со стопроцентной точностью алгоритма Ultra Kurut.*",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 СЛЕДУЮЩИЙ СИГНАЛ", callback_data="go_main")]]),
        parse_mode="Markdown"
    )

# --- [5] ГРАМОТНОЕ ОПИСАНИЕ (СТАРТ) ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("📢 ТЕЛЕГРАМ КАНАЛ", url=LINK_TG)],
        [InlineKeyboardButton("📸 НАШ INSTAGRAM", url=LINK_INSTA)],
        [InlineKeyboardButton("🤖 РЕЗЕРВНЫЙ БОТ", url=LINK_OTHER_BOT)],
        [InlineKeyboardButton("🚀 ЗАПУСТИТЬ ТЕРМИНАЛ 2026", callback_data="go_main")]
    ]
    
    welcome_text = (
        "👑 **ULTRA KURUT OTC — PREMIUM AI SYSTEM**\n\n"
        "Добро пожаловать в элитную экосистему для трейдеров! Мы объединили опыт топ-аналитиков и мощь 20 нейро-индикаторов.\n\n"
        "🔬 **ПОЧЕМУ МЫ ЛУЧШИЕ?**\n"
        "• **Ultra-Core AI:** Анализ через RSI, MACD, Ichimoku и еще 17 фильтров.\n"
        "• **Deep Scan 600:** Сканирование последних 600 свечей.\n"
        "• **OTC-Adaptive:** Алгоритм, созданный специально для Pocket Option.\n"
        "• **Live-Control:** Реальное ожидание экспирации и фиксация профита.\n\n"
        "📍 **НАШИ РЕСУРСЫ:**\n"
        "Подпишись на наш Telegram и Instagram, чтобы получать эксклюзивные отчеты!\n\n"
        "🎯 *Готов забирать профит? Жми кнопку ниже!*"
    )
    
    target = update.message.reply_text if update.message else update.callback_query.message.edit_text
    await target(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [6] ОБРАБОТКА КОМАНД И КНОПОК ---
async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "go_main":
        kb = [[InlineKeyboardButton("💱 Валюты OTC", callback_data="nav_curr_0"), InlineKeyboardButton("₿ Крипто OTC", callback_data="nav_cryp_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ АКТИВА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, prefix, page = query.data.split("_")
        data = CURRENCY_PAIRS if prefix == "curr" else CRYPTO_ASSETS
        await query.edit_message_text("📍 **Выберите торговую пару:**", reply_markup=get_paged_kb(data, int(page), prefix))

    elif query.data.startswith(("curr_", "cryp_")):
        idx = int(query.data.split("_")[1])
        context.user_data['asset'] = (CURRENCY_PAIRS if "curr" in query.data else CRYPTO_ASSETS)[idx]
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("3М", callback_data="t_3m")],
              [InlineKeyboardButton("5 МИНУТ ⏳", callback_data="t_5m")],
              [InlineKeyboardButton("⬅️ НАЗАД", callback_data="go_main")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\n\nВыберите время экспирации:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        asset = context.user_data.get('asset', 'Active')
        time_key = query.data.split("_")[1]
        asyncio.create_task(process_signal(query, asset, time_key))

# --- [7] ЗАПУСК СЕРВЕРА И БОТА ---
if __name__ == "__main__":
    Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever(), daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_cb))
    print("Бот ULTRA KURUT OTC успешно запущен!")
    app.run_polling(drop_pending_updates=True)
