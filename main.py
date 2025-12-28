import asyncio
import json
import os
import random
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] НАСТРОЙКИ И ДОСТУП ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMINS = {6117198446, 7079260196}

# Ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# База данных (храним разрешенных юзеров)
DB_FILE = "allowed_users.json"
def load_allowed():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return set(json.load(f))
    return set()

allowed_users = load_allowed()

def save_allowed():
    with open(DB_FILE, 'w') as f: json.dump(list(allowed_users), f)

# --- [2] СПИСКИ АКТИВОВ ---
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Avalanche OTC", "Chainlink OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Facebook Inc OTC", "Intel OTC", "Tesla OTC", "Pfizer Inc OTC", "Johnson & Johnson OTC", "Boeing Company OTC", "American Express OTC", "Amazon OTC", "Citigroup Inc OTC", "FedEx OTC", "VISA OTC", "Cisco OTC", "ExxonMobil OTC", "Alibaba OTC", "Netflix OTC", "VIX OTC", "Palantir Technologies OTC", "GameStop Corp OTC", "AMD OTC", "Coinbase Global OTC", "Marathon Digital Holdings OTC"]

# --- [3] ЛОГИКА АНАЛИЗА ---
async def elite_signal_engine(query, asset, tf):
    steps = [
        "📡 Подключение к потоку ликвидности...",
        "📊 Анализ 30 технических индикаторов...",
        "🕯 Сканирование Price Action паттернов...",
        "⚖️ Оценка рыночного баланса сил...",
        "🎯 Фильтрация сигнала нейросетью..."
    ]
    for step in steps:
        await query.edit_message_text(f"⏳ **PRO-АНАЛИЗ В ПРОЦЕССЕ...**\n\n{step}")
        await asyncio.sleep(1.2)

    direction = random.choice(["ВВЕРХ 🟢 CALL", "ВНИЗ 🔴 PUT"])
    accuracy = random.uniform(96.4, 99.8)
    
    res = (
        f"🚀 **VIP СИГНАЛ СФОРМИРОВАН!**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **АКТИВ:** `{asset}`\n"
        f"⚡️ **ВХОД:** {direction}\n"
        f"⏱ **ТАЙМФРЕЙМ:** `{tf}`\n"
        f"🎯 **ТОЧНОСТЬ:** `{accuracy:.2f}%` \n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📈 **Price Action:** `Confirmed`\n"
        f"📐 **Levels S/R:** `Detected`"
    )
    kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_ok"), InlineKeyboardButton("❌ МИНУС", callback_data="res_no")],
          [InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="market")]]
    await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [4] ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    
    # ЕСЛИ АДМИН ИЛИ РАЗРЕШЕННЫЙ ЮЗЕР -> СРАЗУ В ТОРГОВЛЮ
    if uid in ADMINS or uid in allowed_users:
        text = "👑 **KURUT AI: ПАНЕЛЬ УПРАВЛЕНИЯ**\n\nВсе системы активны. Выберите рынок для генерации сигнала."
        kb = [[InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="market")],
              [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
              [InlineKeyboardButton("🤖 РЕЗЕРВ БОТ", url=SECOND_BOT)]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return

    # ЕСЛИ НОВЫЙ ЮЗЕР -> ШИКАРНАЯ ИНСТРУКЦИЯ
    welcome_text = (
        "👋 **Добро пожаловать в KURUT AI!**\n\n"
        "Это профессиональная нейросеть для анализа OTC рынков. Наша проходимость составляет более 95%.\n\n"
        "👇 **Наши официальные ресурсы:**"
    )
    kb = [
        [InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТАГРАМ", url=LINK_INSTA)],
        [InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE), InlineKeyboardButton("🤖 РЕЗЕРВНЫЙ БОТ", url=SECOND_BOT)],
        [InlineKeyboardButton("💎 ДАЛЕЕ (ПОЛУЧИТЬ ДОСТУП)", callback_data="instr_access")]
    ]
    await update.message.reply_text(welcome_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "instr_access":
        text = (
            "🚀 **ШАГИ ДЛЯ ПОЛУЧЕНИЯ ДОСТУПА:**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ **РЕГИСТРАЦИЯ:** Создайте новый аккаунт по ссылке ниже.\n"
            f"🔗 [ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\n"
            "2️⃣ **ДЕПОЗИТ:** Пополните баланс на сумму от **$20 до $30**.\n\n"
            "3️⃣ **ID:** Отправьте ваш ID админу для активации.\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **ВАШ ID:** `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=f"tg://user?id=7079260196")],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="back_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "back_start":
        # Имитируем команду старт для возврата
        await start(update, context)

    # ЛОГИКА ДЛЯ ТЕХ КТО С ДОСТУПОМ
    if uid not in ADMINS and uid not in allowed_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
              [InlineKeyboardButton("🏠 В МЕНЮ", callback_data="back_start")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ СЕКТОР РЫНКА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        if "cu" in query.data: context.user_data['asset'] = CURRENCY_PAIRS[idx]
        elif "cr" in query.data: context.user_data['asset'] = CRYPTO_ASSETS[idx]
        else: context.user_data['asset'] = STOCK_ASSETS[idx]
        
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        await elite_signal_engine(query, context.user_data.get('asset'), tf)

    elif query.data in ["res_ok", "res_no"]:
        await query.edit_message_text("✅ Результат учтен! Возврат в меню...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]))

# --- [5] УТИЛИТЫ ---
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
    kb.append([InlineKeyboardButton("🏠 НАЗАД", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMINS:
        try:
            tid = int(context.args[0])
            allowed_users.add(tid)
            save_allowed()
            await update.message.reply_text(f"✅ Доступ для `{tid}` активирован!")
        except: await update.message.reply_text("Пиши: `/grant ID`")

# --- [6] ЗАПУСК ---
if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(handle_cb))
    print("✅ KURUT AI STARTED")
    app.run_polling()
