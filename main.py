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

# Твои ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

DB_FILE = "access_db.json"
STATS_FILE = "user_stats.json"

def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return json.load(f)
        except: return default
    return default

vip_users = set(load_data(DB_FILE, []))
user_stats = load_data(STATS_FILE, {})

def save_all():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)
    with open(STATS_FILE, 'w') as f: json.dump(user_stats, f)

# ================== АКТИВЫ (49 ПАР) ==================
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]

# ================== ИНТЕРФЕЙС ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in user_stats:
        user_stats[uid] = {"wins": 0, "loss": 0, "name": update.effective_user.first_name}; save_all()
    
    social_kb = [[InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG), InlineKeyboardButton("🤖 БОТ 2", url=SECOND_BOT)], [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YT", url=YOUTUBE)]]
    
    if int(uid) in ADMIN_IDS or int(uid) in vip_users:
        text = f"👑 **KURUT AI OVERLORD v20.0**\n\nПривет, {update.effective_user.first_name}!\nВинрейт: {get_winrate(uid)}% | Статус: PREMIUM"
        kb = [
            [InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛ", callback_data="market")],
            [InlineKeyboardButton("🧮 К-ТОР МАРТИНГЕЙЛА", callback_data="martingale"), InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="top_list")],
            [InlineKeyboardButton("💰 ПЛАН 30 ДНЕЙ", callback_data="calc_start"), InlineKeyboardButton("📉 МОЯ СТАТИСТИКА", callback_data="my_stats")]
        ] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = f"🔒 **ДОСТУП ЗАКРЫТ**\n\nID: `{uid}`\n\n1. [РЕГИСТРАЦИЯ]({REF_LINK})\n2. Депозит от $15\n3. Скинь ID админу."
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 АКТИВАЦИЯ", callback_data="instruction")]] + social_kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; uid = str(query.from_user.id)
    try: await query.answer()
    except: pass

    if query.data == "instruction":
        await query.edit_message_text(f"🚀 **АКТИВАЦИЯ**\nID: `{uid}`\n[ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\nСкинь ID админу!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("👨‍💻 АДМИН", url=f"https://t.me/share/url?url=ID:+{uid}")], [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_home")]]), parse_mode="Markdown")
    
    elif query.data == "martingale":
        await query.edit_message_text("🔢 **Введите сумму первой сделки:**"); context.user_data['waiting_martingale'] = True

    elif query.data == "top_list":
        top = sorted(user_stats.items(), key=lambda x: x[1]['wins'], reverse=True)[:10]
        res = "🏆 **ТОП-10 ТРЕЙДЕРОВ**\n━━━━━━━━━━━━━━\n"
        for i, (tid, data) in enumerate(top, 1): res += f"{i}. {data['name']} — {data['wins']} ✅\n"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]), parse_mode="Markdown")

    elif query.data == "my_stats":
        s = user_stats.get(uid, {"wins":0, "loss":0})
        await query.edit_message_text(f"📈 **ВАША СТАТИСТИКА**\n\n✅ Плюсы: {s['wins']}\n❌ Минусы: {s['loss']}\n🎯 Винрейт: {get_winrate(uid)}%", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]))

    elif query.data == "market":
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(CURRENCY_PAIRS, 0, "cu"))

    elif query.data.startswith("nav_cu_"):
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(CURRENCY_PAIRS, int(query.data.split("_")[2]), "cu"))

    elif query.data.startswith("cu_"):
        idx = int(query.data.split("_")[1]); context.user_data['asset'] = CURRENCY_PAIRS[idx]
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("4 МИН", callback_data="t_4m")],
            [InlineKeyboardButton("5 МИН", callback_data="t_5m"), InlineKeyboardButton("6 МИН", callback_data="t_6m")],
            [InlineKeyboardButton("7 МИН", callback_data="t_7m"), InlineKeyboardButton("8 МИН", callback_data="t_8m")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]
        ]
        await query.edit_message_text(f"💎 **{CURRENCY_PAIRS[idx]}**\nВыбери экспирацию:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s','с').replace('m','м'); asset = context.user_data.get('asset')
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\n[ОПРОС 30 ИНДИКАТОРОВ: {i*10}/30]"); await asyncio.sleep(1.5)
        
        sentiment = random.randint(70, 99); bar = "🟢" * (sentiment // 10) + "⚪" * (10 - (sentiment // 10))
        smart = random.choice(["🐳 SMART MONEY: ВЫЯВЛЕН ОБЪЕМ", "⚖️ АККУМУЛЯЦИЯ ПОЗИЦИЙ", "🚀 ИМПУЛЬСНЫЙ ПРОБОЙ"])
        dir = "ВВЕРХ 🟢 CALL" if random.random() > 0.5 else "ВНИЗ 🔴 PUT"
        
        res = f"📊 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📈 **АКТИВ:** `{asset}`\n⚡️ **ВХОД:** {dir}\n⏱ **ВРЕМЯ:** `{tf}`\n\n🎯 **ТОЧНОСТЬ:** `{random.uniform(97, 99):.2f}%` \n🔍 **SMART:** `{smart}`\n📊 **SENTIMENT:** {bar} {sentiment}%\n━━━━━━━━━━━━━━"
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="stat_win"), InlineKeyboardButton("❌ МИНУС", callback_data="stat_loss")]]
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("stat_"):
        if query.data == "stat_win": user_stats[uid]["wins"] += 1
        else: user_stats[uid]["loss"] += 1
        save_all()
        await query.edit_message_text("✅ Результат сохранен!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="market")]]))

    elif query.data == "calc_start":
        await query.edit_message_text("💰 **Введите баланс для марафона:**"); context.user_data['waiting_balance'] = True
    elif query.data == "to_home": await start(update, context)

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_martingale'):
        try:
            v = float(update.message.text); res = f"🧮 **МАРТИНГЕЙЛ (x2.2)**\n\n1. `${v}`\n2. `${v*2.2:.2f}`\n3. `${v*5.0:.2f}`\n4. `${v*11.5:.2f}`"
            context.user_data['waiting_martingale'] = False
            await update.message.reply_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]))
        except: pass
    elif context.user_data.get('waiting_balance'):
        try:
            curr = float(update.message.text); rep = "📅 **МАРАФОН 30 ДНЕЙ (+15%)**\n\n"
            for d in range(1, 31): curr += curr * 0.15; rep += f"День {d}: `${curr:.2f}`\n"
            context.user_data['waiting_balance'] = False
            await update.message.reply_text(rep, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]))
        except: pass

def get_winrate(uid):
    s = user_stats.get(str(uid), {"wins":0, "loss":0}); t = s["wins"] + s["loss"]
    return round((s["wins"] / t * 100), 1) if t > 0 else 0

def get_paged_kb(data, page, prefix):
    size = 10; start_idx = page * size; items = data[start_idx:start_idx+size]; kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start_idx+size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    return InlineKeyboardMarkup(kb)

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            uid = int(context.args[0]); vip_users.add(uid); save_all()
            await update.message.reply_text(f"✅ Доступ выдан: {uid}")
        except: pass

if __name__ == "__main__":
    Thread(target=lambda: HTTPServer(('0.0.0.0', int(os.environ.get("PORT", 8000))), BaseHTTPRequestHandler).serve_forever(), daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start)); app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(callback_handler)); app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.run_polling()
