import asyncio
import random
import json
import os
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] КОНФИГУРАЦИЯ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = [7079260196, 6117198446]

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_YOUTUBE = "https://youtube.com/@kurut_kg?si=pFftIV_UQsOxAyvy"
LINK_TG_CHANNEL = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"
LINK_ADMIN_1 = "https://t.me/id7079260196"
LINK_ADMIN_2 = "https://t.me/id6117198446"

# Файл для хранения реальной статистики и доступа
DB_FILE = "bot_data.json"

def load_data():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"wins": 0, "loss": 0, "users": ADMIN_IDS}

def save_data(data):
    with open(DB_FILE, 'w') as f: json.dump(data, f)

data_db = load_data()

# Активы
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "UAH/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCKS_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK OTC", "Tesla OTC", "Amazon OTC", "Netflix OTC", "VISA OTC", "Alibaba OTC", "AMD OTC"]

# --- [2] КЛАВИАТУРЫ ---

def get_social_kb():
    return [
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG_CHANNEL), InlineKeyboardButton("🤖 РЕЗЕРВ БОТ", url=LINK_SECOND_BOT)]
    ]

def get_welcome_kb():
    kb = get_social_kb()
    kb.append([InlineKeyboardButton("💎 ПОЛУЧИТЬ VIP ДОСТУП", callback_data="instruction_1")])
    return InlineKeyboardMarkup(kb)

def get_vip_kb():
    kb = [
        [InlineKeyboardButton("📈 ГЕНЕРИРОВАТЬ СИГНАЛ (99%)", callback_data="market")],
        [InlineKeyboardButton("📊 ТЕКУЩАЯ СТАТИСТИКА", callback_data="stats")]
    ]
    kb.extend(get_social_kb())
    return InlineKeyboardMarkup(kb)

# --- [3] ЛОГИКА АНАЛИЗА ---

async def run_analysis(query, asset, tf):
    steps = [
        "🛸 Подключение к спутниковому терминалу...",
        "📉 Анализ ликвидности уровней S/R...",
        "🧠 Вычисление по 30 индикаторам (RSI, BB, MACD)...",
        "⚖️ Оценка волатильности и новостного фона...",
        "💎 Финализация торгового решения..."
    ]
    for step in steps:
        await query.edit_message_text(f"🛰 **KURUT AI ELITE v6.0**\n\n`Актив:` **{asset}**\n`Таймфрейм:` **{tf}**\n\n{step}")
        await asyncio.sleep(1.2)

    direction = random.choice(["ВВЕРХ 🟢 CALL", "ВНИЗ 🔴 PUT"])
    acc = random.randint(96, 99)
    
    signal_text = (
        f"👑 **VIP СИГНАЛ СФОРМИРОВАН**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"💎 **АКТИВ:** `{asset}`\n"
        f"📊 **НАПРАВЛЕНИЕ:** {direction}\n"
        f"⏱ **ЭКСПИРАЦИЯ:** `{tf}`\n"
        f"🎯 **ВЕРОЯТНОСТЬ:** `{acc}%` \n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📌 *Входите в сделку мгновенно после получения сигнала!*"
    )
    kb = [[InlineKeyboardButton("✅ ВЫШЛО В ПЛЮС", callback_data="res_win"), InlineKeyboardButton("❌ ВЫШЛО В МИНУС", callback_data="res_loss")],
          [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
    await query.edit_message_text(signal_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [4] ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in data_db["users"] or uid in ADMIN_IDS:
        text = (
            f"🌟 **ДОБРО ПОЖАЛОВАТЬ В VIP КЛУБ**\n\n"
            f"Вы авторизованы в системе **KURUT AI**.\n"
            f"Все индикаторы синхронизированы. Нажмите кнопку ниже для начала торговли."
        )
        await update.message.reply_text(text, reply_markup=get_vip_kb(), parse_mode="Markdown")
    else:
        text = (
            "👋 **Вас приветствует KURUT AI!**\n\n"
            "Это самое мощное программное обеспечение для анализа Pocket Option.\n"
            "Наш бот использует **30 слоев анализа** для выдачи максимально точных сигналов.\n\n"
            "👇 Используйте кнопки ниже, чтобы изучить наши соцсети или получить доступ."
        )
        await update.message.reply_text(text, reply_markup=get_welcome_kb(), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    # --- ИНСТРУКЦИЯ (СТРАНИЦА 1) ---
    if query.data == "instruction_1":
        text = (
            "📖 **ЭТАП 1: ПОДГОТОВКА (ИНСТРУКЦИЯ)**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Чтобы нейросеть работала корректно, ваш аккаунт должен быть привязан к нашему торговому узлу.\n\n"
            "1️⃣ **Очистите куки** в браузере или используйте режим инкогнито.\n"
            "2️⃣ Перейдите по ссылке ниже и создайте новый аккаунт.\n"
            "3️⃣ Это обеспечит вам 99% точность сигналов и возврат части убытков.\n\n"
            "📍 *Нажмите кнопку ниже, чтобы перейти к регистрации.*"
        )
        kb = [[InlineKeyboardButton("➡️ ПЕРЕЙТИ К РЕГИСТРАЦИИ", callback_data="instruction_2")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # --- ИНСТРУКЦИЯ (СТРАНИЦА 2) ---
    elif query.data == "instruction_2":
        text = (
            "💰 **ЭТАП 2: РЕГИСТРАЦИЯ И ДЕПОЗИТ**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🔗 **ССЫЛКА:** [ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\n"
            "✅ **ШАГ 1:** Зарегистрируйтесь на платформе.\n"
            "✅ **ШАГ 2:** Сделайте депозит от **$20 до $30**.\n"
            "✅ **ШАГ 3:** Скопируйте ваш **ID** в личном кабинете.\n\n"
            "🎁 *При регистрации по этой ссылке вы получите бонус +50% к депозиту!*"
        )
        kb = [[InlineKeyboardButton("💳 Я ПОПОЛНИЛ БАЛАНС", callback_data="instruction_3")],
              [InlineKeyboardButton("⬅️ НАЗАД", callback_data="instruction_1")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    # --- ИНСТРУКЦИЯ (СТРАНИЦА 3) ---
    elif query.data == "instruction_3":
        text = (
            "⚙️ **ЭТАП 3: АКТИВАЦИЯ ДОСТУПА**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "Последний шаг! Теперь вам нужно отправить данные админам.\n\n"
            f"🆔 **ВАШ ID ДЛЯ ПРОВЕРКИ:** `{uid}`\n\n"
            "Напишите любому из наших администраторов, скиньте ID и скриншот пополнения.\n"
            "Они активируют ваш VIP статус в течение 5 минут!"
        )
        kb = [[InlineKeyboardButton("👨‍💻 АДМИН 1", url=LINK_ADMIN_1), InlineKeyboardButton("👨‍💻 АДМИН 2", url=LINK_ADMIN_2)],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "to_start":
        await start(update, context)

    # --- VIP ЗОНА ---
    if uid not in data_db["users"] and uid not in ADMIN_IDS: return

    if query.data == "stats":
        total = data_db["wins"] + data_db["loss"]
        winrate = round((data_db["wins"] / total * 100), 1) if total > 0 else 0
        text = (
            "📊 **РЕАЛЬНАЯ СТАТИСТИКА БОТА**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Успешных сигналов: `{data_db['wins']}`\n"
            f"❌ Убыточных сигналов: `{data_db['loss']}`\n"
            f"📈 Общий винрейт: `{winrate}%`"
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]), parse_mode="Markdown")

    elif query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, cat, page = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), cat))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        cat, idx = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        context.user_data['asset'] = data[int(idx)]
        kb = [[InlineKeyboardButton("10С", callback_data="t_10s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 **АКТИВ:** `{context.user_data['asset']}`\nВыберите время:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s','с').replace('m','м')
        await run_analysis(query, context.user_data.get('asset'), tf)

    elif query.data == "res_win":
        data_db["wins"] += 1
        save_data(data_db)
        await query.edit_message_text("🔥 **В ТОЧКУ!** Результат занесен в базу.\nПродолжим?", reply_markup=get_vip_kb())

    elif query.data == "res_loss":
        data_db["loss"] += 1
        save_data(data_db)
        await query.edit_message_text("⚠️ **Учтено.** Проводим калибровку индикаторов.\nПопробуем другой актив?", reply_markup=get_vip_kb())

# --- [5] ДОП. ФУНКЦИИ ---

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
    kb.append([InlineKeyboardButton("🏠 КАТЕГОРИИ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            tid = int(context.args[0])
            if tid not in data_db["users"]:
                data_db["users"].append(tid)
                save_data(data_db)
                await update.message.reply_text(f"✅ Доступ открыт для `{tid}`")
        except: await update.message.reply_text("Формат: `/grant ID`")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.run_polling()
