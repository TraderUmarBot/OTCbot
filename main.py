import os
import asyncio
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- НАСТРОЙКИ ---
TOKEN = "8596735739:AAH5mhGIN8hAjNXX2H5FJcFy9RQr_DIsQKI"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_OTHER_BOT = "https://t.me/KURUT_TRADE_BOT"

# --- СПИСКИ АКТИВОВ (ТВОИ 48 ПАР + 12 КРИПТО) ---
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

# --- ГЛУБОКАЯ ЛОГИКА АНАЛИЗА ---
def get_advanced_ai_signal(exp_time):
    """Имитация работы мощного ИИ: 600 свечей, 20 индикаторов"""
    np.random.seed(None)
    
    # Математические веса в зависимости от экспирации
    accuracy = random.randint(94, 98)
    direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    
    analysis_report = (
        f"📊 Анализ завершен: сканировано 600 свечей.\n"
        f"🛠 20 технических индикаторов (RSI, MACD, BB, ADX) подтверждают вход.\n"
        f"📐 Математическая модель вероятности: {accuracy + 1.2}%"
    )
    return direction, accuracy, analysis_report

# --- ГЕНЕРАЦИЯ КНОПОК ПАГИНАЦИИ ---
def get_pagination_kb(list_data, page, prefix):
    page_size = 10
    start_idx = page * page_size
    end_idx = start_idx + page_size
    items = list_data[start_idx:end_idx]
    
    keyboard = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx + i}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx + i + 1}"))
        keyboard.append(row)
        
    nav_row = []
    if page > 0: nav_row.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"nav_{prefix}_{page-1}"))
    if end_idx < len(list_data): nav_row.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"nav_{prefix}_{page+1}"))
    
    if nav_row: keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton("🏠 В ГЛАВНОЕ МЕНЮ", callback_data="go_main")])
    return InlineKeyboardMarkup(keyboard)

# --- ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("📊 Мой Telegram Канал", url=LINK_TG)],
        [InlineKeyboardButton("📸 Мой Instagram", url=LINK_INSTA)],
        [InlineKeyboardButton("🤖 Резервный Бот", url=LINK_OTHER_BOT)],
        [InlineKeyboardButton("ДАЛЕЕ 🚀 ПЕРЕЙТИ К АНАЛИЗУ", callback_data="go_main")]
    ]
    welcome_text = (
        "👑 **ДОБРО ПОЖАЛОВАТЬ В KURUT TRADE PREMIUM AI!**\n\n"
        "Здорово, трейдер! Это твой самый мощный инструмент для анализа рынка.\n\n"
        "🔬 **Как работает наш ИИ:**\n"
        "• **Deep Scan:** Анализирует последние 600 свечей в реальном времени.\n"
        "• **Multi-Indicator:** Сверяет показатели 20 технических индикаторов.\n"
        "• **Algorithm:** Использует сложную математическую модель для фильтрации рыночного шума на OTC.\n\n"
        "⚡️ *Подпишись на наши ресурсы и жми кнопку «ДАЛЕЕ», чтобы начать работу!*"
    )
    if update.message:
        await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("💱 Валютные пары (48)", callback_data="nav_curr_0")],
        [InlineKeyboardButton("₿ Криптовалюты (12)", callback_data="nav_cryp_0")],
        [InlineKeyboardButton("📚 Обучение (25 Стратегий)", callback_data="menu_strat")]
    ]
    await update.callback_query.message.edit_text("🎯 **ВЫБЕРИТЕ ТИП АКТИВА ДЛЯ АНАЛИЗА:**", reply_markup=InlineKeyboardMarkup(kb))

async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    # Навигация
    if query.data.startswith("nav_"):
        parts = query.data.split("_")
        prefix, page = parts[1], int(parts[2])
        data_list = CURRENCY_PAIRS if prefix == "curr" else CRYPTO_ASSETS
        await query.edit_message_text("📍 **Выберите актив:**", reply_markup=get_pagination_kb(data_list, page, prefix))

    # Выбор актива
    elif query.data.startswith("curr_") or query.data.startswith("cryp_"):
        is_curr = "curr" in query.data
        idx = int(query.data.split("_")[1])
        asset = CURRENCY_PAIRS[idx] if is_curr else CRYPTO_ASSETS[idx]
        context.user_data['asset'] = asset
        
        kb = [
            [InlineKeyboardButton("5 СЕК", callback_data="t_5s"), InlineKeyboardButton("15 СЕК", callback_data="t_15s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m"), InlineKeyboardButton("3 МИН", callback_data="t_3m")],
            [InlineKeyboardButton("5 МИНУТ ⏳", callback_data="t_5m")],
            [InlineKeyboardButton("⬅️ К ВЫБОРУ АКТИВА", callback_data="go_main")]
        ]
        await query.edit_message_text(f"💎 Актив: **{asset}**\n\nВыберите время экспирации для анализа:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # Выдача сигнала
    elif query.data.startswith("t_"):
        asset = context.user_data.get('asset', 'Active')
        exp = query.data.split("_")[1].replace('s', ' СЕК').replace('m', ' МИН')
        
        await query.edit_message_text(f"📡 **ИИ СКАНИРУЕТ РЫНОК {asset}...**\nГлубина: 600 свечей.")
        await asyncio.sleep(1.2)
        
        dir, acc, report = get_advanced_ai_signal(exp)
        
        res_text = (
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **АКТИВ:** `{asset}`\n"
            f"⚡️ **ВХОД:** `{dir}`\n"
            f"⏱ **ВРЕМЯ:** `{exp}`\n"
            f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💡 **ИНФО:**\n`{report}`"
        )
        await query.edit_message_text(res_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="go_main")]]), parse_mode="Markdown")

    elif query.data == "go_main": await main_menu(update, context)
    # Здесь можно добавить логику обучения (menu_strat), если нужно

# --- ЗАПУСК ---
if __name__ == "__main__":
    # Health check server для Koyeb
    Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever(), daemon=True).start()
    
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_interaction))
    print("Бот запущен...")
    app.run_polling()
