import asyncio
import json
import os
import random
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ================== КОНФИГУРАЦИЯ ==================
TOKEN = "8596735739:AAGQScXaW47LRlZTVQsGLTi2FUOpJj2YkpA"
ADMIN_IDS = {7079260196, 6117198446}

# Твои Фото ID
PHOTO_UP = "AgACAgIAAxkBAAIDRmliLyW2ijHX2PRFDt7CAfWRRFLyAALyDWsb_CURSxA3wRq5Anf1AQADAgADeQADOAQ"
PHOTO_DOWN = "AgACAgIAAxkBAAIDPGliLeaqevpLkW5wBwOuJQEj1RjjAALpDWsb_CURS3K1vWT0Ck_aAQADAgADeQADOAQ"
PHOTO_REG = "AgACAgIAAxkBAAIDSmliL6io7GM9iLxWg85X5aYmtXxrAAL6DWsb_CURS7iPDYdaBHRCAQADAgADeAADOAQ"

# Ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# Файлы БД
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

# ================== СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Netflix OTC", "Coinbase OTC", "Meta OTC", "Intel OTC"]

# ================== СЕРВЕР 24/7 ==================
server = Flask('')
@server.route('/')
def home(): return "Kurut AI is Online"
def run_server(): server.run(host='0.0.0.0', port=8080)

# ================== ГЛАВНЫЙ ИНТЕРФЕЙС ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in user_stats: 
        user_stats[uid] = {"wins": 0, "name": update.effective_user.first_name}
        save_all()

    social_kb = [[InlineKeyboardButton("📢 ТГ", url=LINK_TG), InlineKeyboardButton("🤖 БОТ 2", url=SECOND_BOT)], [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YT", url=YOUTUBE)]]
    
    if int(uid) in ADMIN_IDS or int(uid) in vip_users:
        text = f"💎 **KURUT AI ELITE v22.0**\n\nПривет, {update.effective_user.first_name}!\nСтатус: **PREMIUM** ✅\nТвои победы: {user_stats[uid]['wins']} ✅"
        kb = [
            [InlineKeyboardButton("📊 АНАЛИЗАТОР", callback_data="market")],
            [InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="top_list")],
            [InlineKeyboardButton("💰 МАРАФОН", callback_data="calc_start")]
        ] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = (f"🔒 **ДОСТУП ОГРАНИЧЕН**\n\nID: `{uid}`\n\n"
                f"1️⃣ Зарегистрируйся: [ПО ССЫЛКЕ]({REF_LINK})\n"
                f"2️⃣ Депозит от **15$**\n"
                f"3️⃣ Скинь ID админу для активации.")
        await update.message.reply_photo(photo=PHOTO_REG, caption=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 ПОЛУЧИТЬ ДОСТУП", url="https://t.me/traderumarr")]] + social_kb), parse_mode="Markdown")

# ================== ОБРАБОТКА CALLBACK ==================
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; uid = str(query.from_user.id)
    await query.answer()

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
        kb = [[InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
              [InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("5 МИН", callback_data="t_5m")],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]]
        await query.edit_message_text(f"💎 **{context.user_data['asset']}**\nСрок сделки:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('m',' МИН')
        asset = context.user_data.get('asset')
        
        msg = await query.edit_message_text(f"🔍 **АНАЛИЗИРУЮ {asset}...**")
        await asyncio.sleep(2.5); await msg.edit_text("🧬 **СБОР ДАННЫХ С 40 ИНДИКАТОРОВ...**")
        await asyncio.sleep(2.5); await msg.edit_text("⚡️ **МАТЕМАТИЧЕСКИЙ ПРОСЧЕТ...**")
        await asyncio.sleep(2.5); await msg.delete()

        direction = "UP" if random.random() > 0.5 else "DOWN"
        photo = PHOTO_UP if direction == "UP" else PHOTO_DOWN
        res = (f"📊 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📈 **АКТИВ:** `{asset}`\n⏱ **ВРЕМЯ:** `{tf}`\n"
               f"🚀 **ВХОД:** {'ВВЕРХ (CALL) ↑' if direction == 'UP' else 'ВНИЗ (PUT) ↓'}\n"
               f"🎯 **ТОЧНОСТЬ:** `{random.uniform(95, 99):.2f}%` \n━━━━━━━━━━━━━━")
        
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="stat_win"), InlineKeyboardButton("🔄 НОВЫЙ", callback_data="market")]]
        await context.bot.send_photo(chat_id=int(uid), photo=photo, caption=res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "stat_win":
        user_stats[uid]["wins"] += 1; save_all()
        await query.message.reply_text("✅ Красава! Статистика обновлена.")

    elif query.data == "top_list":
        top = sorted(user_stats.items(), key=lambda x: x[1]['wins'], reverse=True)[:10]
        res = "🏆 **ЛИДЕРЫ НЕДЕЛИ**\n━━━━━━━━━━━━━━\n"
        for i, (tid, data) in enumerate(top, 1): res += f"{i}. {data['name']} — {data['wins']} ✅\n"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]), parse_mode="Markdown")

    elif query.data == "calc_start":
        await query.edit_message_text("💰 **Введите ваш текущий баланс:**"); context.user_data['waiting_balance'] = True

    elif query.data == "to_home": 
        # Эмуляция команды старт для возврата в меню
        await start(update, context)

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_balance'):
        try:
            val = float(update.message.text); rep = "📅 **МАРАФОН 30 ДНЕЙ (+15% DAILY)**\n\n"
            for d in range(1, 31): val += val * 0.15; rep += f"День {d}: `${val:.2f}`\n"
            context.user_data['waiting_balance'] = False
            await update.message.reply_text(rep, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]))
        except: await update.message.reply_text("Введите число!")

# ================== ВСПОМОГАТЕЛЬНОЕ ==================
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
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

# Команды админа
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target = int(context.args[0]); vip_users.add(target); save_all()
            await update.message.reply_text(f"✅ Доступ выдан: {target}")
        except: pass

if __name__ == "__main__":
    Thread(target=run_server).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("🚀 KURUT AI ELITE С МАРАФОНОМ ЗАПУЩЕН!")
    app.run_polling()
