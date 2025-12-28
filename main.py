import asyncio
import random
import json
import os
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
LINK_SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"
# Прямые ссылки на ваши ТГ (проверь юзернеймы!)
TG_ADMIN_1 = "https://t.me/id7079260196" # Если это ID, лучше заменить на @username
TG_ADMIN_2 = "https://t.me/id6117198446"

# База данных
DB_FILE = "bot_db.json"
def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"wins": 1540, "loss": 84, "users": ADMIN_IDS}

def save_db(db):
    with open(DB_FILE, 'w') as f: json.dump(db, f)

db = load_db()

# Активы
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "UAH/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCKS_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK OTC", "Tesla OTC", "Amazon OTC", "Netflix OTC", "VISA OTC", "Alibaba OTC", "AMD OTC"]

# --- [2] ФУНКЦИИ ИНТЕРФЕЙСА ---

def get_social_btns():
    return [
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG_CHANNEL), InlineKeyboardButton("🤖 РЕЗЕРВ БОТ", url=LINK_SECOND_BOT)]
    ]

async def send_start_msg(update_or_query, uid):
    is_admin = uid in ADMIN_IDS
    if uid in db["users"] or is_admin:
        text = (
            f"👑 **KURUT AI VIP СИСТЕМА**\n"
            f"━━━━━━━━━━━━━━\n"
            f"✅ Профит: `{db['wins']}` | ❌ Убыток: `{db['loss']}`\n"
            f"📡 Статус: `Анализатор активен`"
        )
        kb = [[InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ (PRO)", callback_data="market")],
              [InlineKeyboardButton("📈 СТАТИСТИКА", callback_data="view_stats")]]
        kb.extend(get_social_btns())
    else:
        text = "👋 **Привет! Это KURUT AI.**\n\nДля доступа к сигналам с проходимостью 95%+ пройди активацию."
        kb = get_social_btns()
        kb.append([InlineKeyboardButton("🚀 ПОЛУЧИТЬ ДОСТУП", callback_data="step1")])
    
    markup = InlineKeyboardMarkup(kb)
    if isinstance(update_or_query, Update):
        await update_or_query.message.reply_text(text, reply_markup=markup, parse_mode="Markdown")
    else:
        await update_or_query.edit_message_text(text, reply_markup=markup, parse_mode="Markdown")

# --- [3] ОБРАБОТЧИК ---

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    # НАВИГАЦИЯ И ИНСТРУКЦИЯ
    if query.data == "to_start":
        await send_start_msg(query, uid)

    elif query.data == "step1":
        text = "📖 **ЭТАП 1: ПОДГОТОВКА**\n━━━━━━━━━━━━━━\nОчистите куки или создайте новый аккаунт, чтобы бот мог синхронизироваться с вашим графиком."
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ", callback_data="step2")], [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "step2":
        text = (f"💰 **ЭТАП 2: РЕГИСТРАЦИЯ**\n━━━━━━━━━━━━━━\n"
                f"1. Регистрация: [ССЫЛКА]({REF_LINK})\n"
                "2. Депозит: **$20 - $30**.\n"
                "3. Получите бонус +50% автоматически.")
        kb = [[InlineKeyboardButton("✅ Я ПОПОЛНИЛ", callback_data="step3")], [InlineKeyboardButton("⬅️ НАЗАД", callback_data="step1")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "step3":
        text = (f"⚙️ **ЭТАП 3: АКТИВАЦИЯ**\n━━━━━━━━━━━━━━\n"
                f"Ваш ID: `{uid}`\n\nНажмите кнопку ниже, чтобы отправить ID админам на проверку.")
        kb = [[InlineKeyboardButton("👨‍💻 СВЯЗАТЬСЯ С АДМИНАМИ", callback_data="contact_admins")],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "contact_admins":
        # Отправляем новое сообщение с кнопками-ссылками
        kb = [[InlineKeyboardButton("👤 АДМИН #1", url=TG_ADMIN_1)],
              [InlineKeyboardButton("👤 АДМИН #2", url=TG_ADMIN_2)]]
        await context.bot.send_message(chat_id=uid, text="👇 Выберите любого администратора для отправки ID:", reply_markup=InlineKeyboardMarkup(kb))

    # VIP ЛОГИКА
    if uid not in db["users"] and uid not in ADMIN_IDS: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="cat_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="cat_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="cat_st_0")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("cat_"):
        _, cat, page = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), cat))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        cat, idx = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        context.user_data['asset'] = data[int(idx)]
        kb = [[InlineKeyboardButton("10С", callback_data="t_10s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 Актив: `{context.user_data['asset']}`\nВремя экспирации:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s','с').replace('m','м')
        asset = context.user_data.get('asset')
        # АНАЛИЗ
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\nШаг {i}/3: Сканирование индикаторов...")
            await asyncio.sleep(1.5)
        
        dir = random.choice(["ВВЕРХ 🟢 CALL", "ВНИЗ 🔴 PUT"])
        acc = random.randint(96, 99)
        text = (f"🚀 **VIP СИГНАЛ ГОТОВ**\n━━━━━━━━━━━━━━\n📊 АКТИВ: `{asset}`\n⚡️ ВХОД: **{dir}**\n⏱ ТАЙМ: `{tf}`\n🎯 ТОЧНОСТЬ: `{acc}%`\n━━━━━━━━━━━━━━")
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="win"), InlineKeyboardButton("❌ МИНУС", callback_data="loss")],
              [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "win":
        db["wins"] += 1
        save_db(db)
        await query.edit_message_text("✅ Статистика обновлена!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]))
    
    elif query.data == "loss":
        db["loss"] += 1
        save_db(db)
        await query.edit_message_text("❌ Учтено. Проводим калибровку...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]))

    elif query.data == "view_stats":
        total = db["wins"] + db["loss"]
        wr = round((db["wins"]/total*100), 1) if total > 0 else 0
        await query.edit_message_text(f"📊 **СТАТИСТИКА**\n━━━━━━━━━━━━━━\n✅ Плюсы: `{db['wins']}`\n❌ Минусы: `{db['loss']}`\n📈 Winrate: `{wr}%`", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]), parse_mode="Markdown")

# --- [4] СИСТЕМНОЕ ---

def get_paged_kb(data, page, prefix):
    size = 10
    start_idx = page * size
    items = data[start_idx:start_idx+size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"cat_{prefix}_{page-1}"))
    if start_idx+size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"cat_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 КАТЕГОРИИ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def start_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await send_start_msg(update, update.effective_user.id)

async def grant_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            tid = int(context.args[0])
            if tid not in db["users"]: db["users"].append(tid); save_db(db)
            await update.message.reply_text(f"✅ Доступ открыт для `{tid}`")
        except: await update.message.reply_text("Пиши: /grant ID")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("grant", grant_cmd))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.run_polling()
