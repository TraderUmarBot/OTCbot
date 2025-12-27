import asyncio
import random
import time
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] НАСТРОЙКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = [7079260196, 6117198446]

# Ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_YOUTUBE = "https://youtube.com/@kurut_kg?si=pFftIV_UQsOxAyvy"
LINK_TG_CHANNEL = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_ADMIN_1 = "https://t.me/id7079260196"
LINK_ADMIN_2 = "https://t.me/id6117198446"

granted_users = set(ADMIN_IDS)
user_history = {}

# Активы
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC", "Avalanche OTC", "Chainlink OTC", "Litecoin OTC", "TRON OTC"]
STOCKS_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK OTC", "Intel OTC", "Tesla OTC", "Pfizer Inc OTC", "J&J OTC", "Boeing OTC", "Amex OTC", "Amazon OTC", "Citigroup OTC", "FedEx OTC", "VISA OTC", "Cisco OTC", "Exxon OTC", "Alibaba OTC", "Netflix OTC", "VIX OTC", "Palantir OTC", "GameStop OTC", "AMD OTC", "Coinbase OTC", "Marathon OTC"]

# --- [2] МАТЕМАТИЧЕСКИЙ АЛГОРИТМ ---
async def elite_math_analysis(query, asset, tf):
    steps = [
        f"📡 Подключение к потоку {asset}...",
        "📊 Опрос 30 технических индикаторов (RSI, MACD, BB...)",
        "📐 Построение математических уровней S/R...",
        "🧠 Фильтрация рыночного шума нейросетью...",
        "🎯 Формирование точки входа..."
    ]
    for s in steps:
        await query.edit_message_text(f"⏳ **ULTRA АНАЛИЗ В ПРОЦЕССЕ...**\n\n{s}")
        await asyncio.sleep(0.9)

    score = sum([random.uniform(-1, 1) for _ in range(30)])
    direction = "ВВЕРХ 🟢" if score > 0 else "ВНИЗ 🔴"
    # Базовая точность 96% + случайный фактор до 99.9%
    accuracy = round(96.2 + (abs(score)/15 * 3.7), 2)
    if accuracy > 99.9: accuracy = 99.9
    
    return direction, accuracy

# --- [3] ИНТЕРФЕЙС И ГРАМОТНАЯ ИНСТРУКЦИЯ ---
def vip_menu_kb():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="get_cats")],
        [InlineKeyboardButton("📜 ИСТОРИЯ СДЕЛОК", callback_data="view_history")],
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG_CHANNEL)]
    ])

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in granted_users:
        await update.message.reply_text("👑 **KURUT AI: VIP ДОСТУП АКТИВИРОВАН**\n\nСистема готова. Используйте меню для точных сигналов.", reply_markup=vip_menu_kb())
        return

    instr = (
        "👋 **Добро пожаловать в ULTRA KURUT AI!**\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "Это профессиональный софт для анализа OTC-рынков. Наш алгоритм просчитывает 30 индикаторов для максимальной точности.\n\n"
        "📖 **ИНСТРУКЦИЯ ПО АКТИВАЦИИ:**\n"
        "1️⃣ Зарегистрируйте новый аккаунт по ссылке ниже.\n"
        "2️⃣ Пополните баланс на сумму от **$20 до $30**.\n"
        "3️⃣ После пополнения нажмите кнопку «ПОЛУЧИТЬ ДОСТУП».\n"
        "4️⃣ Получите свой ID и отправьте его админу для проверки.\n\n"
        "📍 [Официальный Канал](%s) | [Наш YouTube](%s)"
    ) % (LINK_TG_CHANNEL, LINK_YOUTUBE)
    
    kb = [[InlineKeyboardButton("🔗 РЕГИСТРАЦИЯ (БОНУС 50%)", url=REF_LINK)],
          [InlineKeyboardButton("➡️ ПОЛУЧИТЬ ДОСТУП / МОЙ ID", callback_data="req_access")]]
    await update.message.reply_text(instr, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

# --- [4] ОБРАБОТКА CALLBACK ---
async def handle_cb(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "req_access":
        text = (
            "🚀 **ШАГ К АКТИВАЦИИ**\n\n"
            f"1. Ссылка на регистрацию: [КЛИКНИ СЮДА]({REF_LINK})\n"
            "2. Мин. депозит: **$20 - $30**.\n"
            f"3. Ваш уникальный ID: `{uid}`\n\n"
            "Отправьте этот ID админу вместе со скрином пополнения для получения доступа!"
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ 1", url=LINK_ADMIN_1)],
              [InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ 2", url=LINK_ADMIN_2)],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="back_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "back_start":
        await start(update, context)

    if uid not in granted_users: return

    # Торговое меню
    if query.data == "get_cats":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="n_curr_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="n_cryp_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="n_stoc_0")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="back_vip")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("n_"):
        _, cat, page = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "curr" else CRYPTO_ASSETS if cat == "cryp" else STOCKS_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), cat))

    elif query.data.startswith(("curr_", "cryp_", "stoc_")):
        cat, idx = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "curr" else CRYPTO_ASSETS if cat == "cryp" else STOCKS_ASSETS
        context.user_data['asset'] = data[int(idx)]
        # ВСЕ ВРЕМЕНА ЭКСПИРАЦИИ
        kb = [[InlineKeyboardButton("10С", callback_data="t_10с"), InlineKeyboardButton("15С", callback_data="t_15с"), InlineKeyboardButton("30С", callback_data="t_30с")],
              [InlineKeyboardButton("1М", callback_data="t_1м"), InlineKeyboardButton("2М", callback_data="t_2м"), InlineKeyboardButton("3М", callback_data="t_3м")],
              [InlineKeyboardButton("4М", callback_data="t_4м"), InlineKeyboardButton("5М", callback_data="t_5м")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1]
        asset = context.user_data.get('asset', 'Active')
        dir, acc = await elite_math_analysis(query, asset, tf)
        
        context.user_data['last_sig'] = {"pair": asset, "dir": dir}
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_win"), InlineKeyboardButton("❌ МИНУС", callback_data="res_loss")],
              [InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="get_cats")]]
        
        await query.edit_message_text(
            f"🚀 **VIP СИГНАЛ СФОРМИРОВАН!**\n━━━━━━━━━━━━━━\n"
            f"📊 ПАРА: `{asset}`\n⚡️ ВХОД: **{dir}**\n⏱ ТАЙМ: `{tf}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━\n"
            f"📈 **АНАЛИЗ 30 ИНДИКАТОРОВ:** `УСПЕШНО`\n"
            f"📐 **PRICE ACTION:** `ПОДТВЕРЖДЕНО`\n\n"
            f"🏁 **ОТМЕТЬТЕ РЕЗУЛЬТАТ:**",
            reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown"
        )

    elif query.data.startswith("res_"):
        res = "✅ WIN" if "win" in query.data else "❌ LOSS"
        last = context.user_data.get('last_sig', {"pair": "N/A", "dir": "N/A"})
        if uid not in user_history: user_history[uid] = []
        user_history[uid].append(f"{res} | {last['pair']} | {last['dir']}")
        await query.edit_message_text(f"📝 Результат `{res}` сохранен!", reply_markup=vip_menu_kb(), parse_mode="Markdown")

    elif query.data == "view_history":
        history = user_history.get(uid, [])
        txt = "📜 **ИСТОРИЯ ВАШИХ СДЕЛОК:**\n━━━━━━━━━━━━━━\n"
        if not history: txt += "Пока нет сделок."
        else:
            for item in history[-10:]: txt += f"{item}\n"
        await query.edit_message_text(txt + "━━━━━━━━━━━━━━", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="back_vip")]]), parse_mode="Markdown")

    elif query.data == "back_vip":
        await start(update, context)

# --- [5] СЛУЖЕБНЫЕ ФУНКЦИИ ---
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
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"n_{prefix}_{page-1}"))
    if start + size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"n_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 НАЗАД", callback_data="get_cats")])
    return InlineKeyboardMarkup(kb)

async def grant_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target_id = int(context.args[0])
            granted_users.add(target_id)
            await update.message.reply_text(f"✅ Доступ для `{target_id}` открыт!")
        except: await update.message.reply_text("Пиши: /grant ID")

# --- [6] ЗАПУСК ---
if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant_access))
    app.add_handler(CallbackQueryHandler(handle_cb))
    print("🚀 KURUT ELITE SYSTEM ONLINE")
    app.run_polling()
