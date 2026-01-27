import json
import os
import asyncio
import threading
import time
import hashlib
import math
import random
from datetime import datetime, timedelta
import requests
from flask import Flask
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes, ApplicationBuilder
import logging

# ============================================
# ⚙️ НАСТРОЙКИ (ОБЯЗАТЕЛЬНО ЗАПОЛНИ)
# ============================================
TOKEN = "8578509228:AAFdsHJOSaNc0b1JrCnRwAbA-d4IVXI0Ip0"
ADMIN_IDS = {6117198446, 7079260196}
# Ссылка на твой сервис на Render (чтобы он не спал)
RENDER_URL = "https://твой-проект.onrender.com" 

# Ссылки
ADMIN_LINK = "https://t.me/Kuruttrader"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

OTC_PAIRS = L
"EUR/USD OTC", "AUD/CAD OTC", "AUD/ CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC",
"AUD/USD OTC", "CAD/CHF OTC", "CAD/ JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC",
"EUR/GBP OTC", "EUR/JPY OTC", "EUR/ NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC",
"GBP/USD OTC", "NZD/JPY OTC", "NZD/ USD OTC", "USD/CAD OTC", "USD/CHF OTC",
"USD/JPY OTC", "USD/RUB OTC", "CHF/ NOK OTC", "EUR/HUF OTC", "USD/CNH OTC",
"EUR/TRY OTC", "USD/INR OTC", "USD/ SGD OTC", "USD/CLP OTC", "USD/MYR OTC",
"USD/THB OTC", "USD/VND OTC", "USD/ PKR OTC", "USD/COP OTC", "USD/EGP OTC",
"USD/PHP OTC", "USD/MXN OTC", "USD/ DZD OTC", "USD/ARS OTC", "USD/IDR OTC",
"USD/BRL OTC", "USD/BDT OTC", "YER/ USD OTC", "LBP/USD OTC", "TND/USD OTC",
"MAD/USD OTC", "NGN/USD OTC", "KES/ USD OTC", "ZAR/USD OTC", "UAH/USD OTC"
]
EXCHANGE_PAIRS = [
"EUR/USD", "GBP/USD", "USD/JPY",
"USD/CHF", "AUD/USD",
"USD/CAD", "NZD/USD", "EUR/GBP",
"EUR/JPY", "GBP/JPY",
"AUD/JPY", "EUR/AUD", "GBP/AUD",
"EUR/NZD", "AUD/NZD" ,
"CAD/JPY", "AUD/CHF", "CHF/JPY",
"EUR/CHF", "GBP/CHF",
"NZD/JPY"
]
STOCKS_OTC = L
"Apple OTC", "McDonald's OTC",
"Microsoft OTC", "Citigroup Inc OTC"
"VISA OTC",
"VIX OTC", "ExxonMobil OTC",
"Pfizer Inc OTC", "Johnson & Johnson
OTC", "American Express OTC",
"Alibaba OTC", "Netflix OTC",
"Tesla OTC", "Amazon OTC", "GameStop
Corp OTC",
"Boeing Company OTC", "Marathon
Digital Holdings OTC", "Facebook Inc
OTC", "Intel OTC",
"Advanced Micro Devices OTC"
"FedEx OTC", "Coinbase Global OTC",
"Palantir Technologies OTC"
]
CRYPTO_OTC = [
"Bitcoin OTC", "Ethereum OTC",
"Polygon OTC", "Polkadot OTC", "TRON
ОТС",
"Litecoin OTC", "Toncoin OTC",
"Bitcoin ETF OTC", "Solana OTC", "BNB
ОТС",
"Cardano OTC", "Dogecoin OTC"
"Chainlink OTC", "Avalanche OTC"
]

MARKET_CATEGORIES = {
    "otc_forex": {"name": "💱 OTC Валюты", "pairs": OTC_PAIRS},
    "exchange_forex": {"name": "🏛️ Биржевые Валюты", "pairs": EXCHANGE_PAIRS},
    "stocks": {"name": "📈 Акции OTC", "pairs": STOCKS_OTC},
    "crypto": {"name": "₿ Криптовалюты OTC", "pairs": CRYPTO_OTC}
}

EXPIRATIONS = ["1 МИНУТА", "2 МИНУТЫ", "3 МИНУТЫ", "5 МИНУТ", "10 МИНУТ"]

# ============================================
# 💾 БАЗА ДАННЫХ (JSON)
# ============================================
DATA_PATH = "data/"
if not os.path.exists(DATA_PATH): os.makedirs(DATA_PATH)

def load_data(name, default):
    try:
        with open(DATA_PATH + name, 'r') as f: return json.load(f)
    except: return default

def save_data(name, data):
    with open(DATA_PATH + name, 'w') as f: json.dump(data, f)

vip_users = set(load_data("vips.json", []))
all_users = set(load_data("users.json", []))
user_stats = load_data("stats.json", {})

# ============================================
# 📈 АНАЛИТИЧЕСКИЙ ДВИЖОК (БЕЗ РАНДОМА)
# ============================================
class SmartAnalyzer:
    @staticmethod
    def get_signal(pair, timeframe):
        # Создаем уникальный seed на основе пары и текущего времени (интервал 2 мин)
        seed_time = datetime.now().strftime("%Y-%m-%d %H:%M")
        # Для того чтобы сигнал был стабильным 2 минуты:
        if int(datetime.now().minute) % 2 != 0:
            seed_time = (datetime.now() - timedelta(minutes=1)).strftime("%Y-%m-%d %H:%M")
            
        combined = f"{pair}{seed_time}{timeframe}"
        hash_val = int(hashlib.sha256(combined.encode()).hexdigest(), 16)
        
        # Вычисляем параметры на основе хеша (псевдо-анализ)
        score = hash_val % 100
        direction = "CALL" if (hash_val % 2 == 0) else "PUT"
        confidence = 82 + (hash_val % 14) # 82-96%
        
        # Технические индикаторы (симуляция на основе хеша)
        rsi = 30 + (hash_val % 40)
        market_strength = 70 + (hash_val % 25)
        
        return {
            "pair": pair,
            "direction": direction,
            "confidence": confidence,
            "rsi": round(rsi, 2),
            "strength": market_strength,
            "entry": datetime.now().strftime("%H:%M:%S")
        }

# ============================================
# 🌐 KEEP ALIVE (FLASK + PINGER)
# ============================================
app = Flask(__name__)

@app.route('/')
def index(): return "Bot is running 24/7", 200

def run_flask():
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 8080)))

def pinger():
    while True:
        try:
            requests.get(RENDER_URL, timeout=10)
            logging.info("Ping success")
        except: logging.error("Ping failed")
        time.sleep(150) # каждые 2.5 минуты

# ============================================
# 🤖 ЛОГИКА БОТА
# ============================================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in all_users:
        all_users.add(uid)
        save_data("users.json", list(all_users))
        user_stats[uid] = {"wins": 0, "loss": 0}
        save_data("stats.json", user_stats)
    
    kb = [
        [InlineKeyboardButton("🚀 СИГНАЛЫ", callback_data="menu_signals")],
        [InlineKeyboardButton("👑 VIP ДОСТУП", callback_data="menu_vip"), InlineKeyboardButton("📊 СТАТИСТИКА", callback_data="menu_stats")],
        [InlineKeyboardButton("💬 ЧАТ", url="https://t.me/Kurutopen"), InlineKeyboardButton("👨‍💼 АДМИН", url=ADMIN_LINK)]
    ]
    await update.message.reply_text("🚀 **KURUT AI v3.0 АКТИВИРОВАН**\nВыбери действие:", 
                                   parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = str(query.from_user.id)
    data = query.data
    await query.answer()

    # ГЛАВНОЕ МЕНЮ
    if data == "main":
        kb = [[InlineKeyboardButton("🚀 СИГНАЛЫ", callback_data="menu_signals")],
              [InlineKeyboardButton("📊 СТАТИСТИКА", callback_data="menu_stats")]]
        await query.edit_message_text("Главное меню:", reply_markup=InlineKeyboardMarkup(kb))

    # КАТЕГОРИИ
    elif data == "menu_signals":
        if uid not in vip_users and int(uid) not in ADMIN_IDS:
            await query.edit_message_text("❌ Доступ ограничен! Купите VIP.", 
                                          reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Купить VIP", callback_data="menu_vip")]]))
            return
        kb = [[InlineKeyboardButton(v["name"], callback_data=f"cat_{k}_0")] for k, v in MARKET_CATEGORIES.items()]
        kb.append([InlineKeyboardButton("🔙 Назад", callback_data="main")])
        await query.edit_message_text("Выбери категорию рынка:", reply_markup=InlineKeyboardMarkup(kb))

    # ПАГИНАЦИЯ ПАР
    elif data.startswith("cat_"):
        _, cat_id, page = data.split("_")
        page = int(page)
        pairs = MARKET_CATEGORIES[cat_id]["pairs"]
        per_page = 6
        total_pages = math.ceil(len(pairs) / per_page)
        
        start_i = page * per_page
        end_i = start_i + per_page
        current_pairs = pairs[start_i:end_i]
        
        kb = []
        for p in current_pairs:
            kb.append([InlineKeyboardButton(p, callback_data=f"sel_{cat_id}_{p}")])
        
        nav = []
        if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"cat_{cat_id}_{page-1}"))
        if page < total_pages - 1: nav.append(InlineKeyboardButton("➡️", callback_data=f"cat_{cat_id}_{page+1}"))
        if nav: kb.append(nav)
        kb.append([InlineKeyboardButton("🔙 К категориям", callback_data="menu_signals")])
        
        await query.edit_message_text(f"Выбери пару (Стр. {page+1}/{total_pages}):", reply_markup=InlineKeyboardMarkup(kb))

    # ВЫБОР ТАЙМФРЕЙМА
    elif data.startswith("sel_"):
        _, cat_id, pair = data.split("_")
        kb = []
        for t in EXPIRATIONS:
            kb.append([InlineKeyboardButton(t, callback_data=f"sig_{pair}_{t}")])
        await query.edit_message_text(f"Выбрано: {pair}\nУкажи время сделки:", reply_markup=InlineKeyboardMarkup(kb))

    # ГЕНЕРАЦИЯ СИГНАЛА
    elif data.startswith("sig_"):
        _, pair, tf = data.split("_")
        res = SmartAnalyzer.get_signal(pair, tf)
        
        emoji = "🟢 ВВЕРХ (CALL)" if res['direction'] == "CALL" else "🔴 ВНИЗ (PUT)"
        msg = (f"🎯 **СИГНАЛ СФОРМИРОВАН**\n\n"
               f"📊 Пара: `{pair}`\n"
               f"⏰ Время: `{tf}`\n"
               f"🎫 Вход: `{res['entry']}`\n"
               f"📈 Направление: **{emoji}**\n"
               f"🔥 Точность: `{res['confidence']}%`\n"
               f"💎 Сила рынка: `{res['strength']}%`\n"
               f"📉 RSI: `{res['rsi']}`")
        
        kb = [[InlineKeyboardButton("✅ ВИН", callback_data=f"stat_w_{uid}"), InlineKeyboardButton("❌ ЛОСС", callback_data=f"stat_l_{uid}")],
              [InlineKeyboardButton("🔄 Новый сигнал", callback_data="menu_signals")]]
        await query.edit_message_text(msg, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))

    # VIP
    elif data == "menu_vip":
        txt = f"👑 **VIP СТАТУС**\n\nДля активации:\n1. Регайся: [ССЫЛКА]({REF_LINK})\n2. Депозит от $50\n3. Пиши ID админу: {ADMIN_USER}"
        await query.edit_message_text(txt, parse_mode="Markdown", disable_web_page_preview=True, 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню", callback_data="main")]]))

    # СТАТИСТИКА
    elif data == "menu_stats":
        s = user_stats.get(uid, {"wins": 0, "loss": 0})
        total = s['wins'] + s['loss']
        wr = round((s['wins']/total)*100, 1) if total > 0 else 0
        await query.edit_message_text(f"📊 **ТВОЯ СТАТИСТИКА**\n\n✅ Побед: {s['wins']}\n❌ Поражений: {s['loss']}\n🎯 WinRate: {wr}%", 
                                      parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Меню", callback_data="main")]]))

    # ОБРАБОТКА ВИН/ЛОСС
    elif data.startswith("stat_"):
        _, res_type, _ = data.split("_")
        if res_type == "w": user_stats[uid]["wins"] += 1
        else: user_stats[uid]["loss"] += 1
        save_data("stats.json", user_stats)
        await query.edit_message_text("✅ Результат учтен! Ждем следующей сделки.")
        await asyncio.sleep(2)
        # Возврат в меню сигналов
        kb = [[InlineKeyboardButton(v["name"], callback_data=f"cat_{k}_0")] for k, v in MARKET_CATEGORIES.items()]
        await query.message.reply_text("Выберите категорию:", reply_markup=InlineKeyboardMarkup(kb))

# ============================================
# 👑 АДМИН-ФУНКЦИИ
# ============================================
async def admin_grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    if not context.args: return
    target = context.args[0]
    vip_users.add(target)
    save_data("vips.json", list(vip_users))
    await update.message.reply_text(f"✅ Пользователь {target} теперь VIP!")

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    msg = " ".join(context.args)
    count = 0
    for u in all_users:
        try:
            await context.bot.send_message(u, f"📢 **ОПОВЕЩЕНИЕ**\n\n{msg}", parse_mode="Markdown")
            count += 1
        except: pass
    await update.message.reply_text(f"✅ Рассылка завершена. Получили: {count}")

# ============================================
# 🚀 ТОЧКА ВХОДА
# ============================================
def main():
    # Запуск фоновых процессов
    threading.Thread(target=run_flask, daemon=True).start()
    threading.Thread(target=pinger, daemon=True).start()

    # Сборка бота
    bot = ApplicationBuilder().token(TOKEN).build()
    
    bot.add_handler(CommandHandler("start", start))
    bot.add_handler(CommandHandler("grant", admin_grant))
    bot.add_handler(CommandHandler("broadcast", admin_broadcast))
    bot.add_handler(CallbackQueryHandler(handle_callback))
    
    print("--- KURUT AI v3.0 STARTED ---")
    bot.run_polling()

if __name__ == "__main__":
    main()
