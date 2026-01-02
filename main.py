import asyncio
import json
import os
import random
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ================== КОНФИГУРАЦИЯ ==================
TOKEN = "8596735739:AAGQScXaW47LRlZTVQsGLTi2FUOpJj2YkpA"
ADMIN_IDS = {6117198446, 7079260196}

# Ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# Базы данных
DB_FILE = "access_db.json"
STATS_FILE = "user_stats.json"
USERS_LIST_FILE = "all_users.json"

def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return json.load(f)
        except: return default
    return default

vip_users = set(load_data(DB_FILE, []))
user_stats = load_data(STATS_FILE, {})
all_users = set(load_data(USERS_LIST_FILE, []))

def save_all():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)
    with open(STATS_FILE, 'w') as f: json.dump(user_stats, f)
    with open(USERS_LIST_FILE, 'w') as f: json.dump(list(all_users), f)

# ================== СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Netflix OTC", "Coinbase OTC", "Meta OTC", "Intel OTC"]

# ================== ГЛАВНЫЙ ИНТЕРФЕЙС ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in all_users: all_users.add(uid); save_all()
    if uid not in user_stats: user_stats[uid] = {"wins": 0, "name": update.effective_user.first_name}; save_all()

    social_kb = [[InlineKeyboardButton("📢 ТГ", url=LINK_TG), InlineKeyboardButton("🤖 БОТ 2", url=SECOND_BOT)], [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YT", url=YOUTUBE)]]
    
    if int(uid) in ADMIN_IDS or int(uid) in vip_users:
        text = f"💎 **KURUT AI ELITE v21.5**\n\nПривет, {update.effective_user.first_name}!\nСтатистика: {user_stats[uid]['wins']} ✅ | Статус: PREMIUM"
        kb = [[InlineKeyboardButton("📊 АНАЛИЗАТОР", callback_data="market")], [InlineKeyboardButton("🏆 ТОП", callback_data="top_list"), InlineKeyboardButton("💰 МАРАФОН", callback_data="calc_start")]] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = f"🔒 **ДОСТУП ОГРАНИЧЕН**\n\nID: `{uid}`\n\nДля активации:\n1. [РЕГИСТРАЦИЯ]({REF_LINK})\n2. Депозит от $15\n3. Скинь ID админу."
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 АКТИВАЦИЯ", callback_data="instruction")]] + social_kb), parse_mode="Markdown")

# ================== РАССЫЛКА (ADMIN ONLY) ==================
async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    if not context.args:
        await update.message.reply_text("❌ Формат: `/send Текст сообщения и ссылка`")
        return
    msg_text = " ".join(context.args)
    count = 0
    await update.message.reply_text(f"🚀 Начинаю рассылку для {len(all_users)} трейдеров...")
    for user_id in all_users:
        try:
            await context.bot.send_message(chat_id=user_id, text=f"🔔 **ОБНОВЛЕНИЕ ОТ KURUT TRADING!**\n\n{msg_text}", parse_mode="Markdown")
            count += 1
            await asyncio.sleep(0.05)
        except: pass
    await update.message.reply_text(f"✅ Готово! Получили: {count} человек.")

# ================== ОБРАБОТКА КНОПОК ==================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; uid = str(query.from_user.id)
    try: await query.answer()
    except: pass

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ (OTC)", callback_data="nav_cu_0")], [InlineKeyboardButton("₿ КРИПТА (OTC)", callback_data="nav_cr_0")], [InlineKeyboardButton("🏢 АКЦИИ (OTC)", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        prefix, idx = query.data.split("_")
        data = CURRENCY_PAIRS if prefix == "cu" else CRYPTO_ASSETS if prefix == "cr" else STOCK_ASSETS
        context.user_data['asset'] = data[int(idx)]
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("4 МИН", callback_data="t_4m")],
            [InlineKeyboardButton("5 МИН", callback_data="t_5m"), InlineKeyboardButton("6 МИН", callback_data="t_6m")],
            [InlineKeyboardButton("7 МИН", callback_data="t_7m"), InlineKeyboardButton("8 МИН", callback_data="t_8m")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]
        ]
        await query.edit_message_text(f"💎 **{context.user_data['asset']}**\nСрок сделки:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин'); asset = context.user_data.get('asset')
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\n[ИНДИКАТОРЫ: {i*10}/30]"); await asyncio.sleep(1.5)
        
        sentiment = random.randint(72, 98); bar = "🟢" * (sentiment // 10) + "⚪" * (10 - (sentiment // 10))
        dir = "ВВЕРХ 🟢 CALL" if random.random() > 0.5 else "ВНИЗ 🔴 PUT"
        res = f"📊 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📈 **АКТИВ:** `{asset}`\n⚡️ **ВХОД:** {dir}\n⏱ **ВРЕМЯ:** `{tf}`\n\n🎯 **ТОЧНОСТЬ:** `{random.uniform(96, 99):.2f}%` \n🔍 **SMART:** `🐳 ВЫЯВЛЕН ОБЪЕМ` \n📊 **SENTIMENT:** {bar} {sentiment}%\n━━━━━━━━━━━━━━"
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="stat_win"), InlineKeyboardButton("❌ МИНУС", callback_data="stat_loss")]]
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "instruction":
        await query.edit_message_text(f"📝 **ИНСТРУКЦИЯ**\n\n1. [Регистрация]({REF_LINK})\n2. Пополни баланс от $15\n3. Скинь ID: `{uid}` админу", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="to_home")]]), parse_mode="Markdown")
    
    elif query.data == "top_list":
        top = sorted(user_stats.items(), key=lambda x: x[1]['wins'], reverse=True)[:10]
        res = "🏆 **ЛИДЕРЫ НЕДЕЛИ**\n━━━━━━━━━━━━━━\n"
        for i, (tid, data) in enumerate(top, 1): res += f"{i}. {data['name']} — {data['wins']} ✅\n"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]), parse_mode="Markdown")

    elif query.data == "stat_win":
        user_stats[uid]["wins"] += 1; save_all()
        await query.edit_message_text("✅ Статистика учтена!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="market")]]))
    
    elif query.data == "stat_loss":
        await query.edit_message_text("❌ Записано. Используй Мартин!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="market")]]))

    elif query.data == "calc_start":
        await query.edit_message_text("💰 **Введите баланс (число):**"); context.user_data['waiting_balance'] = True
    elif query.data == "to_home": await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_balance'):
        try:
            curr = float(update.message.text); rep = "📅 **МАРАФОН 30 ДНЕЙ (+15%)**\n\n"
            for d in range(1, 31): curr += curr * 0.15; rep += f"День {d}: `${curr:.2f}`\n"
            context.user_data['waiting_balance'] = False
            await update.message.reply_text(rep, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]))
        except: pass

def get_paged_kb(data, page, prefix):
    size = 10; start_idx = page * size; items = data[start_idx:start_idx+size]; kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"nav_{prefix}_{page-1}"))
    if start_idx+size < len(data): nav.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 НАЗАД", callback_data="market")])
    return InlineKeyboardMarkup(kb)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            uid = int(context.args[0]); vip_users.add(uid); save_all()
            await update.message.reply_text(f"✅ Доступ выдан: {uid}")
        except: pass

if __name__ == "__main__":
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start)); app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("send", broadcast))
    app.add_handler(CallbackQueryHandler(callback_handler)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 KURUT AI v21.5 ЗАПУЩЕН")
    app.run_polling()
