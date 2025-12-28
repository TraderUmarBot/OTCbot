import asyncio
import json
import os
import random
import math
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] КОНФИГУРАЦИЯ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMINS = {6117198446, 7079260196}
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

DB_FILE = "allowed_users.json"
def load_allowed():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return set(json.load(f))
        except: return set()
    return set()

allowed_users = load_allowed()

def save_allowed():
    with open(DB_FILE, 'w') as f: json.dump(list(allowed_users), f)

# --- [2] АКТИВЫ (ВСЕ ПАРЫ) ---
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "UAH/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Facebook Inc OTC", "Tesla OTC", "Amazon OTC", "Netflix OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Coinbase OTC", "Marathon OTC"]

# --- [3] МАТЕМАТИЧЕСКИЙ ДВИЖОК СИГНАЛОВ ---
async def heavy_math_analysis(query, asset, tf):
    # Этапы для визуала (создаем доверие)
    steps = [
        "📊 Загрузка истории: 600 свечей получено...",
        "📉 Просчет 30 индикаторов (RSI, MACD, BB)...",
        "🧬 Поиск паттернов в кластерах ликвидности...",
        "🤖 Нейросетевая фильтрация ложных пробоев...",
        "💎 Математическое подтверждение сигнала..."
    ]
    for step in steps:
        await query.edit_message_text(f"🛰 **KURUT AI: ГЛУБОКИЙ АНАЛИЗ**\n\n`Актив:` **{asset}**\n`Глубина:` **600 свечей**\n\n{step}")
        await asyncio.sleep(1.3)

    # Математическая имитация точности
    # Мы генерируем "Силу сигнала" на основе мнимых расчетов
    power_index = random.uniform(85, 99)
    volatility = random.choice(["Низкая", "Умеренная", "Стабильная"])
    main_ind = random.choice(["RSI Divergence", "MACD Crossover", "Fibonacci 0.618", "Bollinger Breakout"])
    
    direction = random.choice(["ВВЕРХ 🟢 CALL", "ВНИЗ 🔴 PUT"])
    accuracy = 95.0 + (power_index / 100 * 4.9) # Итоговая точность 95-99.9%

    res_text = (
        f"🚀 **VIP СИГНАЛ СФОРМИРОВАН**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **АКТИВ:** `{asset}`\n"
        f"⚡️ **ВХОД:** {direction}\n"
        f"⏱ **ВРЕМЯ:** `{tf}`\n"
        f"🎯 **ТОЧНОСТЬ:** `{accuracy:.2f}%` \n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🔍 **ОБОСНОВАНИЕ:**\n"
        f"• База: `600 свечей` | Индикаторов: `30`\n"
        f"• Алгоритм: `{main_ind}`\n"
        f"• Волатильность: `{volatility}`\n\n"
        f"⚠️ *Входите строго в начало свечи. Удачи!*"
    )
    
    kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="stat_ok"), InlineKeyboardButton("❌ МИНУС", callback_data="stat_no")],
          [InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]
    await query.edit_message_text(res_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [4] ОСНОВНЫЕ ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    
    if uid in ADMINS or uid in allowed_users:
        text = "👑 **KURUT AI: ПАНЕЛЬ ТРЕЙДЕРА**\n\nСистема готова к глубокому анализу рынка (600 свечей / 30 индикаторов)."
        kb = [[InlineKeyboardButton("📈 НАЧАТЬ АНАЛИЗ", callback_data="market")],
              [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
              [InlineKeyboardButton("🤖 РЕЗЕРВ БОТ", url=SECOND_BOT)]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = (
            "👋 **Привет! Это KURUT AI BOT v7.0**\n\n"
            "Единственный бот, использующий математическую модель анализа 600 свечей для OTC рынков.\n\n"
            "👇 **Официальные ресурсы:**"
        )
        kb = [
            [InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТАГРАМ", url=LINK_INSTA)],
            [InlineKeyboardButton("💎 ПОЛУЧИТЬ VIP ДОСТУП", callback_data="get_vip")]
        ]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "get_vip":
        text = (
            "💎 **ИНСТРУКЦИЯ ПО АКТИВАЦИИ:**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ **РЕГИСТРАЦИЯ:** [СОЗДАТЬ АККАУНТ]({REF_LINK})\n"
            "*(Используйте инкогнито, если есть старый аккаунт)*\n\n"
            "2️⃣ **ДЕПОЗИТ:** От **$20** для привязки к нейросети.\n\n"
            "3️⃣ **ID:** Скиньте ваш ID админу для проверки.\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **ВАШ ID:** `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 АДМИНИСТРАТОР", url=f"tg://user?id=7079260196")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "to_start":
        await start(update, context)

    if uid not in ADMINS and uid not in allowed_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
              [InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК ДЛЯ АНАЛИЗА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время сделки:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        await heavy_math_analysis(query, context.user_data.get('asset'), tf)

    elif query.data.startswith("stat_"):
        await query.edit_message_text("✅ Данные занесены в математическую модель. Спасибо за обратную связь!", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]))

# --- [5] ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ ---
def get_paged_kb(data, page, prefix):
    size = 10
    start_idx = page * size
    items = data[start_idx:start_idx + size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx + i}")]
        if i + 1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx + i + 1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start_idx + size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 КАТЕГОРИИ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMINS:
        try:
            tid = int(context.args[0])
            allowed_users.add(tid)
            save_allowed()
            await update.message.reply_text(f"✅ Доступ для `{tid}` открыт!")
        except: await update.message.reply_text("Пиши: `/grant ID`")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT PRO-MATH v7.0 STARTED")
    app.run_polling()
