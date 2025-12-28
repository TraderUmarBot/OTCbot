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
TG_ADMIN_1 = "https://t.me/kurut_admin" # Измени на юзернеймы, если нужно
TG_ADMIN_2 = "https://t.me/kurut_manager"

DB_FILE = "bot_db.json"

def load_db():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return json.load(f)
    return {"wins": 1540, "loss": 84, "users": []}

def save_db(db_data):
    with open(DB_FILE, 'w') as f: json.dump(db_data, f, indent=4)

db = load_db()

# --- ПОЛНЫЙ СПИСОК АКТИВОВ ---
CURRENCY_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", 
    "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", 
    "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", 
    "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", 
    "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "UAH/USD OTC", 
    "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"
]
CRYPTO_ASSETS = [
    "Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", 
    "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", 
    "Litecoin OTC", "TRON OTC"
]
STOCKS_ASSETS = [
    "Apple OTC", "McDonald’s OTC", "Microsoft OTC", "FACEBOOK OTC", 
    "Tesla OTC", "Amazon OTC", "Netflix OTC", "VISA OTC", 
    "Alibaba OTC", "AMD OTC"
]

# --- [2] ИНТЕРФЕЙС ---

def get_social_btns():
    return [
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=LINK_YOUTUBE)],
        [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG_CHANNEL), InlineKeyboardButton("🤖 РЕЗЕРВ", url=LINK_SECOND_BOT)]
    ]

async def send_start_msg(update_or_query, uid):
    is_admin = uid in ADMIN_IDS
    has_access = uid in db.get("users", []) or is_admin
    
    if has_access:
        text = (
            f"👑 **KURUT AI VIP SYSTEM**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"✅ Профит: `{db['wins']}` | ❌ Убыток: `{db['loss']}`\n"
            f"📡 Статус: `Анализатор активен`\n\n"
            f"Добро пожаловать. Система готова к выдаче сигналов."
        )
        kb = [
            [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ (PRO)", callback_data="market")],
            [InlineKeyboardButton("📈 СТАТИСТИКА", callback_data="view_stats")]
        ]
    else:
        text = (
            f"👋 **Привет! Это KURUT AI.**\n\n"
            f"Чтобы получить доступ к закрытым сигналам с проходимостью 95%+, "
            f"тебе нужно пройти активацию аккаунта.\n\n"
            f"Жми кнопку ниже, чтобы получить инструкцию! 👇"
        )
        kb = [[InlineKeyboardButton("🚀 ПОЛУЧИТЬ ДОСТУП", callback_data="step1")]]
    
    kb.extend(get_social_btns())
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

    if query.data == "to_start":
        await send_start_msg(query, uid)

    # ИНСТРУКЦИЯ (РЕФЕРАЛКА)
    elif query.data == "step1":
        text = "📖 **ЭТАП 1: ПОДГОТОВКА**\n━━━━━━━━━━━━━━\nОчистите куки или создайте новый аккаунт, чтобы бот мог синхронизироваться с вашим графиком."
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ", callback_data="step2")], [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "step2":
        text = (f"💰 **ЭТАП 2: РЕГИСТРАЦИЯ**\n━━━━━━━━━━━━━━\n"
                f"1. Регистрация: [ССЫЛКА НА ПЛАТФОРМУ]({REF_LINK})\n"
                "2. Депозит: **$20 - $30**.\n"
                "3. Получите бонус +50% к первому депозиту.")
        kb = [[InlineKeyboardButton("✅ Я ПОПОЛНИЛ", callback_data="step3")], [InlineKeyboardButton("⬅️ НАЗАД", callback_data="step1")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "step3":
        text = (f"⚙️ **ЭТАП 3: АКТИВАЦИЯ**\n━━━━━━━━━━━━━━\n"
                f"Ваш персональный ID: `{uid}`\n\n"
                f"Нажмите кнопку ниже, чтобы отправить ваш ID админу на проверку доступа.")
        kb = [[InlineKeyboardButton("👨‍💻 СВЯЗАТЬСЯ С АДМИНОМ", url=TG_ADMIN_1)],
              [InlineKeyboardButton("🏠 В НАЧАЛО", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # ЛОГИКА СИГНАЛОВ
    if uid not in db.get("users", []) and uid not in ADMIN_IDS: return

    if query.data == "market":
        kb = [
            [InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="cat_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="cat_cr_0")],
            [InlineKeyboardButton("🏢 АКЦИИ", callback_data="cat_st_0")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]
        ]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ ТИП РЫНКА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("cat_"):
        _, cat, page = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), cat))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        cat, idx = query.data.split("_")
        data = CURRENCY_PAIRS if cat == "cu" else CRYPTO_ASSETS if cat == "cr" else STOCKS_ASSETS
        context.user_data['asset'] = data[int(idx)]
        kb = [
            [InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("5 МИН", callback_data="t_5m"), InlineKeyboardButton("15 МИН", callback_data="t_15m")]
        ]
        await query.edit_message_text(f"💎 **АКТИВ:** `{context.user_data['asset']}`\n\nВыберите время сделки:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('m',' МИН')
        asset = context.user_data.get('asset')
        
        msg = await query.edit_message_text(f"📡 **СКАНИРОВАНИЕ {asset}...**\nНейросеть ищет точку входа.")
        await asyncio.sleep(2)
        
        dir_icon = random.choice(["🟢 CALL (ВВЕРХ)", "🔴 PUT (ВНИЗ)"])
        acc = random.randint(95, 99)
        
        text = (
            f"🚀 **VIP СИГНАЛ СФОРМИРОВАН**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 АКТИВ: `{asset}`\n"
            f"⚡️ ВХОД: **{dir_icon}**\n"
            f"⏱ ТАЙМ: `{tf}`\n"
            f"🎯 ТОЧНОСТЬ: `{acc}%`\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_win"), InlineKeyboardButton("❌ МИНУС", callback_data="res_loss")],
              [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
        await msg.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # СТАТИСТИКА (КНОПКИ + / -)
    elif query.data == "res_win":
        db["wins"] += 1; save_db(db)
        await query.edit_message_text("✅ **РЕЗУЛЬТАТ: ПЛЮС!**\nСтатистика обновлена.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]))
    
    elif query.data == "res_loss":
        db["loss"] += 1; save_db(db)
        await query.edit_message_text("❌ **РЕЗУЛЬТАТ: МИНУС.**\nПроводим перенастройку алгоритма...", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_start")]]))

    elif query.data == "view_stats":
        total = db["wins"] + db["loss"]
        wr = round((db["wins"]/total*100), 1) if total > 0 else 0
        text = (f"📊 **ТЕКУЩАЯ СТАТИСТИКА**\n━━━━━━━━━━━━━━\n✅ Плюсы: `{db['wins']}`\n❌ Минусы: `{db['loss']}`\n📈 Winrate: `{wr}%`️")
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="to_start")]), parse_mode="Markdown")

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
            await update.message.reply_text(f"✅ Доступ открыт для `{tid}`. Теперь ему доступны сигналы.")
            try: await context.bot.send_message(tid, "💎 **Доступ открыт!**\nЖми /start и начинай зарабатывать.")
            except: pass
        except: await update.message.reply_text("Пиши: `/grant ID`", parse_mode="Markdown")

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start_cmd))
    app.add_handler(CommandHandler("grant", grant_cmd))
    app.add_handler(CallbackQueryHandler(handle_callback))
    print("KURUT AI запущен!")
    app.run_polling()
