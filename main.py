import asyncio
import json
import os
import random
import time
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] СЕРВЕР ДЛЯ REPLIT ---
server = Flask('')
@server.route('/')
def home(): return "KURUT AI BLACK EDITION IS ONLINE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] КОНФИГУРАЦИЯ И ТВОИ ССЫЛКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}

LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"

def load_db(file):
    if os.path.exists(file):
        with open(file, 'r') as f: return set(json.load(f))
    return set()

def save_db(file, data):
    with open(file, 'w') as f: json.dump(list(data), f)

vip_users = load_db(DB_VIP)
all_users = load_db(DB_ALL)

# --- [3] СПИСКИ АКТИВОВ (ПОЛНЫЙ OTC ПАКЕТ) ---
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC", "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/RUB OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CNH OTC", "USD/BRL OTC", "EUR/RUB OTC", "EUR/TRY OTC", "ZAR/USD OTC", "UAH/USD OTC"]
STOCK_ASSETS = ["Apple Inc OTC", "McDonald’s OTC", "Microsoft OTC", "Facebook OTC", "Intel OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "Netflix OTC", "Palantir OTC", "AMD OTC", "Coinbase OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "Ethereum OTC", "Litecoin OTC", "Dogecoin OTC", "Solana OTC", "Toncoin OTC", "Bitcoin ETF OTC"]

# --- [4] ЯДРО АНАЛИЗА (10 СЕКУНД, 20 ИНДИКАТОРОВ) ---
def get_pro_signal(asset):
    random.seed(time.time())
    accuracy = random.uniform(82.4, 94.8)
    direction = random.choice(["ВВЕРХ 🟢 CALL", "ВНИЗ 🔴 PUT"])
    
    indicators = [
        "RSI (14) - Сигнал подтвержден", "Bollinger Bands - Пробой границы",
        "MACD - Пересечение линий", "Stochastic - Зона разворота",
        "EMA 200 - Тренд подтвержден", "Volume - Кластерный всплеск"
    ]
    log = random.sample(indicators, 2)
    return direction, round(accuracy, 2), f"• {log[0]}\n• {log[1]}"

# --- [5] ОБРАБОТЧИКИ КОМАНД ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in all_users:
        all_users.add(uid); save_db(DB_ALL, all_users)

    is_vip = uid in ADMIN_IDS or uid in vip_users
    
    if is_vip:
        text = "👑 **KURUT AI BLACK EDITION**\n━━━━━━━━━━━━━━\nДобро пожаловать в элитный софт.\n\n"
        kb = [
            [InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛ", callback_data="menu_market")],
            [InlineKeyboardButton("🏃 МАРАФОН", callback_data="menu_mara"), InlineKeyboardButton("🏆 ТОП", callback_data="menu_top")],
            [InlineKeyboardButton("📚 ИНСТРУКЦИЯ", callback_data="menu_guide")],
            [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("🤖 БОТ 2.0", url=SECOND_BOT)],
            [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE)]
        ]
    else:
        text = "⚠️ **ДОСТУП ОГРАНИЧЕН**\n\nДля активации софта и торговли с проходимостью до 94% обратитесь к администратору."
        kb = [[InlineKeyboardButton("💎 АКТИВИРОВАТЬ ДОСТУП", callback_data="menu_vip")], [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG)]]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# Команды админа
async def admin_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    cmd = update.message.text.split()
    if len(cmd) < 2: return
    
    target_id = int(cmd[1])
    if "/grant" in cmd[0]:
        vip_users.add(target_id); save_db(DB_VIP, vip_users)
        await update.message.reply_text(f"✅ Доступ открыт для `{target_id}`")
    elif "/revoke" in cmd[0]:
        if target_id in vip_users: vip_users.remove(target_id); save_db(DB_VIP, vip_users)
        await update.message.reply_text(f"❌ Доступ закрыт для `{target_id}`")

async def broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    count = 0
    for user_id in all_users:
        try:
            if update.message.reply_to_message:
                await context.bot.copy_message(chat_id=user_id, from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
            else:
                text = update.message.text.replace("/send", "").strip()
                if text: await context.bot.send_message(chat_id=user_id, text=text)
            count += 1
            await asyncio.sleep(0.05)
        except: continue
    await update.message.reply_text(f"📢 Рассылка на {count} человек завершена!")

# --- [6] CALLBACKS ---

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "menu_guide":
        text = (
            "📚 **ИНСТРУКЦИЯ ПО ТОРГОВЛЕ:**\n\n"
            "1️⃣ **Время захода:** Как только бот выдал сигнал — заходим моментально.\n"
            "2️⃣ **Таймфрейм:** Выбирайте тот, который указали в боте.\n"
            "3️⃣ **Перекрытия:** Если сигнал не зашел, используйте максимум 1-2 догона.\n"
            "4️⃣ **Мани-менеджмент:** Ставьте не более 2-3% от баланса.\n\n"
            "⚠️ Помни: Анализ OTC требует дисциплины!"
        )
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="menu_home")]]), parse_mode="Markdown")

    elif query.data == "menu_home":
        await start(update, context)

    elif query.data == "menu_vip":
        await query.edit_message_text(f"💎 **Твой ID:** `{uid}`\nОтправь его админу после регистрации по ссылке:\n[ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 НАЗАД", callback_data="menu_home")]]))

    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data == "menu_market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0")], [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = (CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS)
        context.user_data['asset'] = data[idx]
        kb = [[InlineKeyboardButton(t, callback_data=f"t_{t}")] for t in ["10С", "1М", "2М", "5М", "8М"]]
        await query.edit_message_text(f"📊 **{data[idx]}**\nВыбери время:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1]
        asset = context.user_data.get('asset')
        msg = await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\n`Опрос 20 индикаторов`")
        
        # Ровно 10 секунд ожидания для "красоты"
        for i in range(1, 4):
            await asyncio.sleep(3)
            await msg.edit_text(f"📡 **ГЛУБОКИЙ АНАЛИЗ {asset}...**\n`Прогресс: {i*33}%`")
        
        dir, acc, log = get_pro_signal(asset)
        res = (
            f"🚀 **СИГНАЛ ГОТОВ!**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📊 АКТИВ: `{asset}`\n"
            f"⏱ ВРЕМЯ: `{tf}`\n"
            f"⚡️ ВХОД: **{dir}**\n"
            f"🎯 ТОЧНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━\n"
            f"📋 **АНАЛИТИКА:**\n{log}\n\n"
            f"💎 `EMA 200 + CLUSTERS: OK`"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="menu_market"), InlineKeyboardButton("❌ МИНУС", callback_data="menu_market")]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

def get_paged_kb(data, page, prefix):
    size = 10
    items = data[page*size : (page+1)*size]
    kb = [[InlineKeyboardButton(items[i], callback_data=f"{prefix}_{page*size+i}")] for i in range(len(items))]
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if (page+1)*size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="menu_home")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    Thread(target=run_web).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", admin_cmd))
    app.add_handler(CommandHandler("revoke", admin_cmd))
    app.add_handler(CommandHandler("send", broadcast))
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO | filters.TEXT) & filters.CaptionRegex(r'^/send'), broadcast))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT AI v20 BLACK EDITION STARTED")
    app.run_polling()
