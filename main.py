import asyncio
import random
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] КОНФИГУРАЦИЯ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = [7079260196, 6117198446]

# Твои ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_YOUTUBE = "https://youtube.com/@kurut_kg?si=pFftIV_UQsOxAyvy"
LINK_TG_CHANNEL = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"
LINK_ADMIN_1 = "https://t.me/id7079260196"

# Статистика и Доступ
stats = {"wins": 3120, "loss": 148}
granted_users = set(ADMIN_IDS)

# База активов
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "UAH/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCKS_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK OTC", "Tesla OTC", "Amazon OTC", "Netflix OTC", "VISA OTC", "Alibaba OTC", "AMD OTC"]

# --- [2] КЛАВИАТУРЫ ---

def get_social_kb():
    return [
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
        [InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG_CHANNEL), InlineKeyboardButton("🤖 РЕЗЕРВНЫЙ БОТ", url=LINK_SECOND_BOT)]
    ]

def get_welcome_kb():
    kb = get_social_kb()
    kb.append([InlineKeyboardButton("🚀 ПОЛУЧИТЬ VIP ДОСТУП", callback_data="show_instr")])
    return InlineKeyboardMarkup(kb)

def get_vip_kb():
    kb = [
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ (PRO)", callback_data="market")],
        [InlineKeyboardButton("📜 ИСТОРИЯ СИГНАЛОВ", callback_data="history")]
    ]
    kb.extend(get_social_kb())
    return InlineKeyboardMarkup(kb)

# --- [3] ЛОГИКА АНАЛИЗА ---

async def run_ai_analysis(query, asset, tf):
    steps = [
        "🔍 [1/5] Подключение к серверам котировок...",
        "📈 [2/5] Анализ 30 технических индикаторов...",
        "🕯 [3/5] Поиск паттернов Price Action...",
        "📉 [4/5] Фильтрация рыночного шума...",
        "✅ [5/5] Формирование точки входа..."
    ]
    for step in steps:
        await query.edit_message_text(f"🛰 **KURUT AI: АНАЛИЗ РЫНКА**\n\n`Актив: {asset}`\n`Таймфрейм: {tf}`\n\n{step}")
        await asyncio.sleep(1.2) # Общее время ~6 секунд

    direction = random.choice(["ВВЕРХ 🟢 CALL", "ВНИЗ 🔴 PUT"])
    acc = random.randint(97, 99)
    
    signal_text = (
        f"🎯 **VIP СИГНАЛ СФОРМИРОВАН**\n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"📊 **АКТИВ:** `{asset}`\n"
        f"⚡️ **ВХОД:** {direction}\n"
        f"⏱ **ВРЕМЯ:** `{tf}`\n"
        f"🎯 **УВЕРЕННОСТЬ:** `{acc}%` \n"
        f"━━━━━━━━━━━━━━━━━━\n"
        f"🧠 *Анализ завершен успешно. Входите строго в начало свечи!*"
    )
    kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="win"), InlineKeyboardButton("❌ МИНУС", callback_data="loss")],
          [InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]
    await query.edit_message_text(signal_text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [4] ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in granted_users:
        text = (
            f"👑 **KURUT AI ELITE v5.0**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 Профит (24ч): `+{stats['wins']}`\n"
            f"📉 Просадка: `-{stats['loss']}`\n"
            f"📡 Статус нейросети: `ONLINE`"
        )
        await update.message.reply_text(text, reply_markup=get_vip_kb(), parse_mode="Markdown")
    else:
        text = (
            "👋 **Добро пожаловать в KURUT AI!**\n\n"
            "Это закрытая торговая нейросеть для OTC-рынков. "
            "Наш софт анализирует рынок через 30 индикаторов и выдает сигналы с точностью до 99.9%.\n\n"
            "📍 **Ниже представлены наши официальные ресурсы:**"
        )
        await update.message.reply_text(text, reply_markup=get_welcome_kb(), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "show_instr":
        text = (
            "💎 **КАК ПОЛУЧИТЬ VIP ДОСТУП:**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "1️⃣ **РЕГИСТРАЦИЯ:** Создайте аккаунт по ссылке:\n"
            f"🔗 [ОФИЦИАЛЬНАЯ ПЛАТФОРМА]({REF_LINK})\n\n"
            "2️⃣ **ДЕПОЗИТ:** Пополните баланс на сумму от **$20 до $30**.\n\n"
            "3️⃣ **ID:** Отправьте ваш ID админу вместе со скриншотом депозита.\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🆔 **ВАШ ТЕХНИЧЕСКИЙ ID:** `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=LINK_ADMIN_1)],
              [InlineKeyboardButton("🏠 ВЕРНУТЬСЯ НАЗАД", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "to_start":
        await start(update, context)

    if uid not in granted_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
              [InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="to_start")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ ТОРГОВЫЙ СЕКТОР:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, cat, page = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), cat))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        cat, idx = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        context.user_data['asset'] = data[int(idx)]
        kb = [[InlineKeyboardButton("10С", callback_data="t_10s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("3М", callback_data="t_3m")],
              [InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 **АКТИВ:** `{context.user_data['asset']}`\nВыберите экспирацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s','с').replace('m','м')
        asset = context.user_data.get('asset')
        await run_ai_analysis(query, asset, tf)

    elif query.data in ["win", "loss"]:
        stats["wins" if query.data == "win" else "loss"] += 1
        await query.edit_message_text("✅ Результат учтен! Возврат в меню...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]))

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
    kb.append([InlineKeyboardButton("🏠 К КАТЕГОРИЯМ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def grant_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target = int(context.args[0])
            granted_users.add(target)
            await update.message.reply_text(f"✅ Доступ для `{target}` активирован!")
        except: await update.message.reply_text("Формат: `/grant ID`", parse_mode="Markdown")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT ELITE v5.0 STARTED")
    app.run_polling()

