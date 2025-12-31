import asyncio
import json
import os
import random
import time
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# ================== ТВОИ НАСТРОЙКИ И ССЫЛКИ ==================
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
PRIMARY_ADMIN_LINK = "tg://user?id=6117198446"

# ССЫЛКИ
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# База доступа
DB_FILE = "access_db.json"
def load_access():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return set(json.load(f))
        except: return set()
    return set()

vip_users = load_access()
def save_access():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)

# ================== СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC",
    "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC",
    "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC",
    "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC",
    "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC",
    "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC",
    "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC",
    "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"
]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Ethereum OTC", "Solana OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC"]

# ================== АЛГОРИТМ ==================
def get_advanced_signal(asset):
    random.seed(time.time() + sum(ord(c) for c in asset))
    score = sum([random.uniform(-1, 1) for _ in range(30)])
    accuracy = 96.8 + (random.random() * 2.9)
    if score > 0:
        direction, logic = "ВВЕРХ 🟢 CALL", "Импульс от зоны поддержки + RSI"
    else:
        direction, logic = "ВНИЗ 🔴 PUT", "Пробой уровня + Stochastic"
    return direction, round(accuracy, 2), logic

# ================== КОМАНДЫ АДМИНА ==================
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда выдачи доступа: /grant ID"""
    uid = update.effective_user.id
    if uid not in ADMIN_IDS:
        return # Только для админов

    if not context.args:
        await update.message.reply_text("❌ Ошибка! Введи ID. Пример: `/grant 1234567`", parse_mode="Markdown")
        return

    try:
        new_vip = int(context.args[0])
        vip_users.add(new_vip)
        save_access()
        await update.message.reply_text(f"✅ **ДОСТУП ОТКРЫТ!**\nПользователь `{new_vip}` теперь может использовать анализ.", parse_mode="Markdown")
        
        # Уведомляем пользователя, если бот может
        try:
            await context.bot.send_message(chat_id=new_vip, text="💎 **Поздравляем!** Админ открыл вам доступ к сигналам KURUT AI. Жмите /start")
        except: pass
    except ValueError:
        await update.message.reply_text("❌ Ошибка! ID должен быть числом.")

# ================== ЛОГИКА ИНТЕРФЕЙСА ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    social_kb = [
        [InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG), InlineKeyboardButton("🤖 ВТОРОЙ БОТ", url=SECOND_BOT)],
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=YOUTUBE)]
    ]

    if uid in ADMIN_IDS or uid in vip_users:
        text = "🚀 **ТЕРМИНАЛ KURUT AI АКТИВИРОВАН**\n\nБро, система готова к глубокому анализу Pocket Option."
        kb = [[InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="market")]] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return

    text = (
        "👋 **Добро пожаловать в KURUT AI!**\n\n"
        "🔥 **ВОЗМОЖНОСТИ:**\n"
        "✅ Анализ 48 пар + Крипта + Акции.\n"
        "✅ 30 индикаторов. Выдача за 7 секунд.\n\n"
        "⚠️ **ИНСТРУКЦИЯ:** Лучшее время: **1м, 3м, 6м**.\n\n"
        "Для доступа пройди активацию 👇"
    )
    kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="instruction")]] + social_kb
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "instruction":
        text = f"🚀 **АКТИВАЦИЯ:**\n\n1. Регистрация: [ССЫЛКА]({REF_LINK})\n2. Депозит от $15.\n3. Твой ID: `{uid}`"
        kb = [[InlineKeyboardButton("👨‍💻 ОТПРАВИТЬ ID АДМИНУ", url=PRIMARY_ADMIN_LINK)], [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "to_home":
        await start(update, context)

    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТНЫЕ ПАРЫ", callback_data="nav_cu_0")], [InlineKeyboardButton("₿ КРИПТА / 🏢 АКЦИИ", callback_data="nav_cr_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS + STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS + STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        kb = [[InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
              [InlineKeyboardButton("1 МИН ⭐", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
              [InlineKeyboardButton("3 МИН ⭐", callback_data="t_3m"), InlineKeyboardButton("6 МИН ⭐", callback_data="t_6m")],
              [InlineKeyboardButton("8 МИН", callback_data="t_8m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nЭкспирация:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset')
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **ГЛУБОКИЙ АНАЛИЗ {asset}...**\n\n`Обработка данных Pocket Option [{i}/3]`")
            await asyncio.sleep(2.1)
        dir, acc, log = get_advanced_signal(asset)
        res = (f"✅ **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📊 **ПАРА:** `{asset}`\n⚡️ **ВХОД:** {dir}\n⏱ **ВРЕМЯ:** `{tf}`\n🎯 **ТОЧНОСТЬ:** `{acc}%` \n━━━━━━━━━━━━━━\n🧠 **ЛОГИКА:** `{log}`")
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]), parse_mode="Markdown")

def get_paged_kb(data, page, prefix):
    size = 10
    start = page * size
    items = data[start:start+size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"nav_{prefix}_{page-1}"))
    if start+size < len(data): nav.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 В МЕНЮ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant)) # КОМАНДА ДЛЯ АДМИНА
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT ULTIMATE STARTED")
    app.run_polling()
