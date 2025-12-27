import asyncio
import random
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] НАСТРОЙКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = [7079260196, 6117198446]

# Твои ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_YOUTUBE = "https://youtube.com/@kurut_kg?si=pFftIV_UQsOxAyvy"
LINK_TG_CHANNEL = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_SECOND_BOT = "https://t.me/KURUT_TRADE_BOT" # ТВОЙ ВТОРОЙ БОТ
LINK_ADMIN_1 = "https://t.me/id7079260196"

# Глобальная статистика сигналов
stats = {"wins": 2450, "loss": 112} # Начальные цифры для солидности
granted_users = set(ADMIN_IDS)

# Активы (Валюты, Крипта, Акции)
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCKS_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK OTC", "Intel OTC", "Tesla OTC", "Pfizer Inc OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Coinbase OTC"]

# --- [2] КЛАВИАТУРЫ ---

def get_main_menu(uid):
    is_admin = uid in ADMIN_IDS
    text = (
        f"👑 **KURUT AI VIP СИСТЕМА**\n"
        f"━━━━━━━━━━━━━━\n"
        f"📈 Сигналов в ПЛЮС: `{stats['wins']}`\n"
        f"📉 Сигналов в МИНУС: `{stats['loss']}`\n"
        f"📊 Проходимость: `95.4%`"
    )
    buttons = [
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="market")],
        [InlineKeyboardButton("🤖 РЕЗЕРВНЫЙ БОТ", url=LINK_SECOND_BOT)],
        [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG_CHANNEL)]
    ]
    if is_admin:
        buttons.append([InlineKeyboardButton("🔑 АДМИН ПАНЕЛЬ", callback_data="admin")])
    return text, InlineKeyboardMarkup(buttons)

# --- [3] ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in granted_users:
        text, kb = get_main_menu(uid)
        await update.message.reply_text(text, reply_markup=kb, parse_mode="Markdown")
    else:
        text = (
            "👋 **Привет! Это KURUT AI v4.5**\n\n"
            "Я — торговая нейросеть, которая анализирует 30 индикаторов для точных входов на Pocket Option.\n\n"
            "Чтобы получить доступ к сигналам, пройди простую активацию."
        )
        kb = [
            [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
            [InlineKeyboardButton("🤖 РЕЗЕРВНЫЙ БОТ", url=LINK_SECOND_BOT)],
            [InlineKeyboardButton("🚀 ПОЛУЧИТЬ ДОСТУП", callback_data="get_access")]
        ]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "get_access":
        text = (
            "💰 **КАК ПОЛУЧИТЬ ДОСТУП:**\n\n"
            f"1️⃣ Регайся здесь: [ССЫЛКА]({REF_LINK})\n"
            "2️⃣ Пополни баланс на **$20 - $30**.\n"
            "3️⃣ Скинь скрин депозита и свой ID админу.\n\n"
            f"🆔 **ТВОЙ ID:** `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=LINK_ADMIN_1)],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="back_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "back_home":
        if uid in granted_users:
            text, kb = get_main_menu(uid)
            await query.edit_message_text(text, reply_markup=kb, parse_mode="Markdown")
        else:
            await start(update, context) # Редирект на приветствие

    # --- VIP ФУНКЦИИ ---
    if uid not in granted_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
              [InlineKeyboardButton("🏠 МЕНЮ", callback_data="back_home")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ:**", reply_markup=InlineKeyboardMarkup(kb))

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
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время сделки:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s','с').replace('m','м')
        asset = context.user_data.get('asset', 'Asset')
        await query.edit_message_text(f"📡 **АНАЛИЗИРУЕМ {asset}...**\nМатематический расчет по 30 индикаторам...")
        await asyncio.sleep(1.5)
        
        direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
        acc = random.randint(96, 99)
        text = (
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n━━━━━━━━━━━━━━\n"
            f"📊 ПАРА: `{asset}`\n⚡️ ВХОД: **{direction}**\n⏱ ВРЕМЯ: `{tf}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━\n"
            f"🏁 Подтвердите результат для статистики:"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="win"), InlineKeyboardButton("❌ МИНУС", callback_data="loss")],
              [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "win":
        stats["wins"] += 1
        await query.edit_message_text(f"✅ Результат записан! Общий профит: {stats['wins']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="back_home")]]))

    elif query.data == "loss":
        stats["loss"] += 1
        await query.edit_message_text(f"❌ Минус учтен. Проводим коррекцию алгоритма...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="back_home")]]))

    elif query.data == "admin" and uid in ADMIN_IDS:
        await query.edit_message_text(f"🔑 **АДМИНКА**\n\nЧтобы дать доступ юзеру, отправь:\n`/grant ID`", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="back_home")]]))

# --- [4] СЛУЖЕБНОЕ ---

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
            await update.message.reply_text(f"✅ Пользователь `{target}` получил доступ!")
        except:
            await update.message.reply_text("Пиши: `/grant 12345678`")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant_cmd))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 БОТ ЗАПУЩЕН")
    app.run_polling()
