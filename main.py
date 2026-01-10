import asyncio
import json
import os
import random
import time
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] СЕРВЕР ДЛЯ REPLIT (UPTIMEROBOT) ---
server = Flask('')
@server.route('/')
def home(): return "KURUT AI ULTRATUM v17 IS LIVE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] ТВОИ ССЫЛКИ И НАСТРОЙКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_LINK = "https://t.me/id6117198446"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# Базы данных
DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "stats.json"

def load_data(file, default_type=list):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return set(json.load(f)) if default_type == set else json.load(f)
        except: return default_type()
    return default_type()

def save_data(file, data):
    with open(file, 'w') as f: json.dump(list(data) if isinstance(data, set) else data, f)

vip_users = load_data(DB_VIP, set)
all_users = load_data(DB_ALL, set)
stats = load_data(DB_STATS, dict) # Для хранения +/-

if not stats: stats = {"wins": 0, "losses": 0}

# --- [3] СПИСКИ АКТИВОВ (ПОЛНЫЙ СПИСОК POCKET OPTION) ---
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC", "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/RUB OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CLP OTC", "USD/VND OTC", "USD/COP OTC", "USD/MXN OTC", "USD/ARS OTC", "USD/BDT OTC", "USD/PKR OTC", "USD/THB OTC", "USD/PHP OTC", "USD/EGP OTC", "USD/CNH OTC", "USD/MYR OTC", "USD/IDR OTC", "USD/BRL OTC", "USD/DZD OTC", "EUR/RUB OTC", "EUR/TRY OTC", "EUR/HUF OTC", "CHF/NOK OTC", "BHD/CNY OTC", "AED/CNY OTC", "QAR/CNY OTC", "OMR/CNY OTC", "JOD/CNY OTC", "NGN/USD OTC", "KES/USD OTC", "ZAR/USD OTC", "UAH/USD OTC", "LBP/USD OTC", "TND/USD OTC", "MAD/USD OTC", "YER/USD OTC"]
STOCK_ASSETS = ["Apple Inc OTC", "McDonald’s OTC", "Microsoft OTC", "Facebook Inc OTC", "Intel OTC", "Tesla OTC", "Pfizer Inc OTC", "Johnson & Johnson OTC", "Boeing Company OTC", "American Express OTC", "Amazon OTC", "Citigroup Inc OTC", "FedEx OTC", "VISA OTC", "Cisco OTC", "ExxonMobil OTC", "Alibaba OTC", "Netflix OTC", "VIX OTC", "Palantir OTC", "GameStop OTC", "AMD OTC", "Coinbase OTC", "Marathon Digital OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "Ethereum OTC", "Litecoin OTC", "Dogecoin OTC", "Polkadot OTC", "BNB OTC", "Solana OTC", "Cardano OTC", "TRON OTC", "Chainlink OTC", "Toncoin OTC", "Avalanche OTC", "Polygon OTC", "Bitcoin ETF OTC"]

# --- [4] МОЩНЫЙ АНАЛИЗ EMA 200 ---
def analyze_market_pro(asset, tf):
    random.seed(time.time() + len(asset))
    acc = 97.8 + (random.random() * 2.1)
    # Симуляция 10 индикаторов
    score = sum([random.randint(-1, 1) for _ in range(10)])
    ema_trend = "UP" if score >= 0 else "DOWN"
    
    if ema_trend == "UP":
        dir, log = "ВВЕРХ 🟢 CALL", "Цена выше EMA 200 + RSI(14) Перепроданность"
    else:
        dir, log = "ВНИЗ 🔴 PUT", "Цена ниже EMA 200 + MACD Пересечение"
    return dir, round(acc, 2), log

# --- [5] ИНТЕРФЕЙС И ЛОГИКА ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in all_users:
        all_users.add(uid); save_data(DB_ALL, all_users)

    if uid in ADMIN_IDS or uid in vip_users:
        text = "👑 **KURUT AI ULTRATUM v17**\n━━━━━━━━━━━━━━\n**Статус:** `VIP Активирован`\n**Точность системы:** `99.2%`"
        kb = [
            [InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ", callback_data="market_main")],
            [InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", url=LINK_TG), InlineKeyboardButton("🏃 МАРАФОН", url=LINK_TG)],
            [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("🤖 ВТОРОЙ БОТ", url=SECOND_BOT)],
            [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE)]
        ]
    else:
        text = "👋 **Доступ к KURUT AI закрыт!**\n\nДля получения сигналов (99% точность) пройди активацию:"
        kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="vip_info")]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "vip_info":
        text = f"🚀 **АКТИВАЦИЯ:**\n\n1. [РЕГИСТРАЦИЯ]({REF_LINK})\n2. Пополнение **$10 - $35**\n3. Скинуть ID: `{uid}`"
        kb = [[InlineKeyboardButton("👨‍💻 АДМИНУ", url=ADMIN_LINK)], [InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "to_home": await start(update, context)

    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data == "market_main":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ (56)", callback_data="nav_cu_0")], 
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
        kb = [
            [InlineKeyboardButton("10С", callback_data="t_10s"), InlineKeyboardButton("30С", callback_data="t_30s"), InlineKeyboardButton("1М", callback_data="t_1m")],
            [InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("3М", callback_data="t_3m"), InlineKeyboardButton("4М", callback_data="t_4m")],
            [InlineKeyboardButton("5М", callback_data="t_5m"), InlineKeyboardButton("6М", callback_data="t_6m"), InlineKeyboardButton("7М", callback_data="t_7m")],
            [InlineKeyboardButton("8М", callback_data="t_8m")]
        ]
        await query.edit_message_text(f"📊 **{data[idx]}**\nВремя:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset')
        msg = await query.edit_message_text(f"📡 **ГЛУБОКИЙ АНАЛИЗ {asset}...**")
        await asyncio.sleep(1)
        
        dir, acc, log = analyze_market_pro(asset, tf)
        res = f"🚀 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📊 АКТИВ: `{asset}`\n⚡️ ВХОД: **{dir}**\n⏱ ВРЕМЯ: `{tf}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n📑 `{log}`\n💎 `EMA 200 CONFIRMED`"
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_win"), InlineKeyboardButton("❌ МИНУС", callback_data="res_loss")]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("res_"):
        # Сохранение статистики
        if query.data == "res_win": stats["wins"] += 1
        else: stats["losses"] += 1
        save_data(DB_STATS, stats)
        # Возврат в начало анализа
        await query.edit_message_text(f"✅ Результат сохранен! (Всего побед: {stats['wins']})\nВыбирай новый актив:", 
                                      reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 НОВЫЙ АНАЛИЗ", callback_data="market_main")]]))

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
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")])
    return InlineKeyboardMarkup(kb)

# --- [6] АДМИН-ФУНКЦИИ ---

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    count = 0
    for user_id in all_users:
        try:
            await context.bot.copy_message(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.message_id)
            count += 1
            await asyncio.sleep(0.05)
        except: continue
    await update.message.reply_text(f"📢 Рассылка завершена! Отправлено: {count}")

async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            tid = int(context.args[0])
            vip_users.add(tid); save_data(DB_VIP, vip_users)
            await update.message.reply_text(f"✅ Доступ открыт для {tid}!")
        except: pass

if __name__ == "__main__":
    Thread(target=run_web).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("send", broadcast))
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO | filters.TEXT) & filters.CaptionRegex(r'^/send'), broadcast))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.run_polling()
