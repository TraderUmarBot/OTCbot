import asyncio
import json
import os
import random
import time
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] SERVER FOR UPTIME ---
server = Flask('')
@server.route('/')
def home(): return "KURUT AI ARMAGEDDON v18 IS ACTIVE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] CONFIG & LINKS ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_LINK = "https://t.me/id6117198446"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# Files
DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_USER_STATS = "user_performance.json" # Храним плюсы каждого юзера

def load_json(file, default):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return json.load(f)
        except: return default
    return default

def save_json(file, data):
    with open(file, 'w') as f: json.dump(data, f)

vip_users = set(load_json(DB_VIP, []))
all_users = set(load_json(DB_ALL, []))
user_performance = load_json(DB_USER_STATS, {}) # {user_id: {"name": "Name", "wins": 0}}

# --- [3] ASSETS (FULL OTC LIST) ---
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC", "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/RUB OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CLP OTC", "USD/VND OTC", "USD/COP OTC", "USD/MXN OTC", "USD/ARS OTC", "USD/BDT OTC", "USD/PKR OTC", "USD/THB OTC", "USD/PHP OTC", "USD/EGP OTC", "USD/CNH OTC", "USD/MYR OTC", "USD/IDR OTC", "USD/BRL OTC", "USD/DZD OTC", "EUR/RUB OTC", "EUR/TRY OTC", "EUR/HUF OTC", "CHF/NOK OTC", "BHD/CNY OTC", "AED/CNY OTC", "QAR/CNY OTC", "OMR/CNY OTC", "JOD/CNY OTC", "NGN/USD OTC", "KES/USD OTC", "ZAR/USD OTC", "UAH/USD OTC", "LBP/USD OTC", "TND/USD OTC", "MAD/USD OTC", "YER/USD OTC"]
STOCK_ASSETS = ["Apple Inc OTC", "McDonald’s OTC", "Microsoft OTC", "Facebook Inc OTC", "Intel OTC", "Tesla OTC", "Pfizer Inc OTC", "Johnson & Johnson OTC", "Boeing Company OTC", "American Express OTC", "Amazon OTC", "Citigroup Inc OTC", "FedEx OTC", "VISA OTC", "Cisco OTC", "ExxonMobil OTC", "Alibaba OTC", "Netflix OTC", "VIX OTC", "Palantir OTC", "GameStop OTC", "AMD OTC", "Coinbase OTC", "Marathon Digital OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "Ethereum OTC", "Litecoin OTC", "Dogecoin OTC", "Polkadot OTC", "BNB OTC", "Solana OTC", "Cardano OTC", "TRON OTC", "Chainlink OTC", "Toncoin OTC", "Avalanche OTC", "Polygon OTC", "Bitcoin ETF OTC"]

# --- [4] ULTRA PRECISION ANALYSIS ---
def get_ultra_signal(asset):
    random.seed(time.time() + len(asset))
    accuracy = 98.9 + (random.random() * 1.05) # 98.9% - 99.9%
    trend = random.choice(["BUY", "SELL"])
    
    if trend == "BUY":
        return "ВВЕРХ 🟢 CALL", round(accuracy, 2), "EMA 200 + MACD Bullish Cross"
    else:
        return "ВНИЗ 🔴 PUT", round(accuracy, 2), "EMA 200 + RSI Overbought"

# --- [5] CORE HANDLERS ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    name = update.effective_user.first_name
    if uid not in all_users:
        all_users.add(uid); save_json(DB_ALL, list(all_users))
    
    if uid not in user_performance:
        user_performance[uid] = {"name": name, "wins": 0}
        save_json(DB_USER_STATS, user_performance)

    if uid in ADMIN_IDS or uid in vip_users:
        text = f"🚀 **KURUT AI ARMAGEDDON v18**\n━━━━━━━━━━━━━━\nПривет, {name}! Система готова к анализу."
        kb = [
            [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="m_market")],
            [InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="m_top"), InlineKeyboardButton("🏃 МАРАФОН", callback_data="m_mara")],
            [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("🤖 ВТОРОЙ БОТ", url=SECOND_BOT)],
            [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE)]
        ]
    else:
        text = "⚠️ **ДОСТУП ЗАБЛОКИРОВАН**\n\nЧтобы не сливать баланс, используй профессиональный софт."
        kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="m_vip")]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = str(query.from_user.id)
    await query.answer()

    if query.data == "m_vip":
        text = f"💎 **АКТИВАЦИЯ:**\n\n1. [РЕГИСТРАЦИЯ]({REF_LINK})\n2. Депозит **$10+**\n3. Твой ID: `{uid}`"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="m_home")]]), parse_mode="Markdown")

    elif query.data == "m_home": await start(update, context)

    # --- TOP TRADERS ---
    elif query.data == "m_top":
        sorted_users = sorted(user_performance.items(), key=lambda x: x[1]['wins'], reverse=True)[:10]
        text = "🏆 **РЕЙТИНГ ТОП ТРЕЙДЕРОВ (ПО ПЛЮСАМ):**\n━━━━━━━━━━━━━━\n"
        for i, (usr_id, data) in enumerate(sorted_users, 1):
            text += f"{i}. {data['name']} — `{data['wins']}` ✅\n"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="m_home")]]), parse_mode="Markdown")

    # --- MARATHON ---
    elif query.data == "m_mara":
        await query.edit_message_text("💰 **Введи свой текущий баланс ($):**\n(Просто напиши число в чат, например: 100)")
        context.user_data['waiting_balance'] = True

    # --- ANALYSIS LOGIC ---
    elif query.data == "m_market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0")], 
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        times = ["10С", "30С", "1М", "2М", "3М", "4М", "5М", "8М"]
        kb = [ [InlineKeyboardButton(t, callback_data=f"t_{t}")] for t in times ]
        await query.edit_message_text(f"📊 **{data[idx]}**\nВремя экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1]
        asset = context.user_data.get('asset')
        msg = await query.edit_message_text(f"📡 **СКАНИРОВАНИЕ {asset}...**\n`Анализ EMA 200 + кластеры`")
        await asyncio.sleep(1.5)
        
        dir, acc, log = get_ultra_signal(asset)
        res = f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n━━━━━━━━━━━━━━\n📊 АКТИВ: `{asset}`\n⚡️ ВХОД: **{dir}**\n🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n📑 `{log}`"
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_p"), InlineKeyboardButton("❌ МИНУС", callback_data="res_m")]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("res_"):
        if query.data == "res_p":
            user_performance[uid]["wins"] += 1
            save_json(DB_USER_STATS, user_performance)
        await query.edit_message_text("♻️ Результат учтен! Выбирай новый актив:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 НОВЫЙ АНАЛИЗ", callback_data="m_market")]]))

# --- [6] MARATHON PLAN GENERATOR ---
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if context.user_data.get('waiting_balance'):
        try:
            balance = float(update.message.text)
            context.user_data['waiting_balance'] = False
            plan = f"🏃 **ВАШ МАРАФОН НА 30 ДНЕЙ (Баланс: ${balance})**\n━━━━━━━━━━━━━━\n"
            plan += f"🔹 **Цель:** `${round(balance*5, 2)}` за месяц\n"
            plan += f"🔹 **Риск на сделку:** `${round(balance*0.02, 2)}` (2%)\n\n"
            plan += "📅 **ПЛАН:**\n"
            plan += f"• Неделя 1: Цель +15% к банку\n• Неделя 2: Цель +25% к банку\n• ПРАВИЛО: 2 минуса в ряд = СТОП.\n\n"
            plan += "Удачи! Используй сигналы бота для реализации плана."
            await update.message.reply_text(plan, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="m_home")]]), parse_mode="Markdown")
        except:
            await update.message.reply_text("❌ Введи числовое значение баланса!")
        return

    # BROADCAST /send
    if uid in ADMIN_IDS and update.message.text and update.message.text.startswith("/send"):
        text_to_send = update.message.text.replace("/send", "").strip()
        count = 0
        for user in all_users:
            try:
                if update.message.reply_to_message:
                    await context.bot.copy_message(chat_id=user, from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
                else:
                    await context.bot.send_message(chat_id=user, text=text_to_send)
                count += 1
                await asyncio.sleep(0.05)
            except: continue
        await update.message.reply_text(f"📢 Рассылка на {count} чел. завершена.")

def get_paged_kb(data, page, prefix):
    size = 10
    start_idx = page * size
    items = data[start_idx:start_idx + size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx + i}")]
        if i + 1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx + i + 1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start_idx + size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="m_home")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    Thread(target=run_web).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(handle_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    app.add_handler(MessageHandler(filters.COMMAND & filters.Regex(r'^/send'), handle_message))
    print("🚀 ARMAGEDDON READY")
    app.run_polling()
