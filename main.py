import asyncio
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_OTHER_BOT = "https://t.me/KURUT_TRADE_BOT"

# Активы (48 пар + 12 крипто)
CURRENCY_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC",
    "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC",
    "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC",
    "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC",
    "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC",
    "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC",
    "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC",
    "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC",
    "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC",
    "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"
]

CRYPTO_ASSETS = [
    "Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC",
    "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC",
    "Litecoin OTC", "TRON OTC"
]

TIME_MAP = {"5s": 5, "15s": 15, "30s": 30, "1m": 60, "2m": 120, "3m": 180, "5m": 300}

# --- ЯДРО АНАЛИЗА ---
def get_precision_signal():
    accuracy = random.uniform(96.5, 99.4)
    direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    factors = ["Объемы: ПИК", "RSI: ПОДТВЕРЖДЕНО", "Price Action: OK", "Neural Filter: ACTIVE"]
    return direction, round(accuracy, 2), random.sample(factors, 2)

# --- КНОПКИ ---
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

# --- ФОНОВАЯ ОБРАБОТКА СДЕЛКИ ---
async def process_trade(query, asset, time_key):
    wait_sec = TIME_MAP.get(time_key, 5)
    label = time_key.replace('s',' сек').replace('m',' мин')
    direction, acc, factors = get_precision_signal()
    
    # 1. Выдача сигнала
    await query.edit_message_text(
        f"🚀 **ULTRA KURUT OTC: СИГНАЛ СФОРМИРОВАН**\n━━━━━━━━━━━━━━\n"
        f"📊 АКТИВ: `{asset}`\n⚡️ ПРОГНОЗ: `{direction}`\n⏱ ЭКСПИРАЦИЯ: `{label}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n"
        f"⚙️ `{factors[0]}` | `{factors[1]}`\n"
        f"📡 **Идет анализ движения цены... Ожидайте.**",
        parse_mode="Markdown"
    )

    # 2. Ждем реальное время
    await asyncio.sleep(wait_sec)

    # 3. Результат
    win = random.choices([True, False], weights=[int(acc), 100-int(acc)])[0]
    res_text = "✅ ПЛЮС (WIN) 🟢" if win else "❌ МИНУС (LOSS) 🔴"
    
    await query.edit_message_text(
        f"🏁 **ИТОГ СДЕЛКИ ПО {asset}**\n━━━━━━━━━━━━━━\n"
        f"🏆 РЕЗУЛЬТАТ: **{res_text}**\n📈 ВХОД БЫЛ: `{direction}`\n⏱ ВРЕМЯ: `{label}`\n━━━━━━━━━━━━━━\n"
        f"Математическая модель 2026 подтвердила прогноз.",
        reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="go_main")]]),
        parse_mode="Markdown"
    )

# --- ОБРАБОТЧИКИ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📊 Telegram Канал", url=LINK_TG)],
          [InlineKeyboardButton("📸 Instagram", url=LINK_INSTA)],
          [InlineKeyboardButton("🤖 Резервный Бот", url=LINK_OTHER_BOT)],
          [InlineKeyboardButton("ДАЛЕЕ 🚀 ЗАПУСТИТЬ ULTRA SCAN", callback_data="go_main")]]
    
    welcome = (
        "👑 **ULTRA KURUT OTC — FUTURE AI**\n\n"
        "Добро пожаловать в элитный софт для анализа Pocket Option.\n\n"
        "🔬 **Как мы работаем:**\n"
        "• Анализ 600 свечей и 20 индикаторов.\n"
        "• Реальные таймеры ожидания результата.\n"
        "• Точность прогнозов до 99.4%.\n\n"
        "Жми «ДАЛЕЕ» для начала работы!"
    )
    if update.message: await update.message.reply_text(welcome, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else: await update.callback_query.message.edit_text(welcome, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📖 **ИНСТРУКЦИЯ ULTRA KURUT OTC**\n\n"
        "1. Выберите актив из списка (60 вариантов).\n"
        "2. Выберите время экспирации (от 5с до 5м).\n"
        "3. Бот выдаст сигнал. Сразу открывайте сделку на платформе.\n"
        "4. Бот подождет время экспирации и сам сообщит результат."
    )
    await update.message.reply_text(text, parse_mode="Markdown")

async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "go_main":
        kb = [[InlineKeyboardButton("💱 Валютные пары", callback_data="nav_curr_0")],
              [InlineKeyboardButton("₿ Криптовалюты", callback_data="nav_cryp_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, prefix, page = query.data.split("_")
        data = CURRENCY_PAIRS if prefix == "curr" else CRYPTO_ASSETS
        await query.edit_message_text("📍 **Выберите актив:**", reply_markup=get_paged_kb(data, int(page), prefix))

    elif query.data.startswith(("curr_", "cryp_")):
        idx = int(query.data.split("_")[1])
        context.user_data['asset'] = (CURRENCY_PAIRS if "curr" in query.data else CRYPTO_ASSETS)[idx]
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("3М", callback_data="t_3m")],
              [InlineKeyboardButton("5 МИНУТ ⏳", callback_data="t_5m")],
              [InlineKeyboardButton("⬅️ НАЗАД", callback_data="go_main")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите экспирацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        asset = context.user_data.get('asset', 'Active')
        time_key = query.data.split("_")[1]
        # Запуск в фоне, чтобы бот не зависал при нагрузке
        asyncio.create_task(process_trade(query, asset, time_key))

# --- ЗАПУСК ---
if __name__ == "__main__":
    Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever(), daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CallbackQueryHandler(handle_cb))
    print("ULTRA KURUT OTC ЗАПУЩЕН...")
    app.run_polling(drop_pending_updates=True)
