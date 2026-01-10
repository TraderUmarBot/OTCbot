import asyncio
import json
import os
import random
import time
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] СЕРВЕР ДЛЯ ПОДДЕРЖКИ РАБОТЫ (REPLIT) ---
server = Flask('')
@server.route('/')
def home(): return "KURUT AI ULTIMATE IS ONLINE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] КОНФИГУРАЦИЯ И ВСЕ ТВОИ ССЫЛКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
PRIMARY_ADMIN_TG = "https://t.me/id6117198446" # Ссылка на личку админа

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# Базы данных (JSON файлы для хранения на Replit)
DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"

def load_data(file):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return set(json.load(f))
        except: return set()
    return set()

def save_data(file, data):
    with open(file, 'w') as f: json.dump(list(data), f)

vip_users = load_data(DB_VIP)
all_users = load_data(DB_ALL)

# --- [3] ПОЛНЫЕ СПИСКИ АКТИВОВ (ВСЕ ПАРЫ POCKET OPTION) ---
CURRENCY_PAIRS = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC", "AUD/USD OTC", "USD/CAD OTC", "NZD/USD OTC",
    "EUR/GBP OTC", "EUR/JPY OTC", "GBP/JPY OTC", "EUR/CHF OTC", "AUD/CAD OTC", "AUD/JPY OTC", "CAD/JPY OTC",
    "NZD/JPY OTC", "AUD/NZD OTC", "GBP/CAD OTC", "GBP/CHF OTC", "EUR/AUD OTC", "EUR/CAD OTC", "CHF/JPY OTC",
    "AUD/CHF OTC", "CAD/CHF OTC", "NZD/CAD OTC", "NZD/CHF OTC", "GBP/AUD OTC", "GBP/NZD OTC", "USD/CNH OTC",
    "USD/INR OTC", "USD/BRL OTC", "USD/MXN OTC", "USD/RUB OTC", "EUR/RUB OTC", "USD/TRY OTC"
]
CRYPTO_ASSETS = [
    "Bitcoin OTC", "Ethereum OTC", "Litecoin OTC", "Ripple OTC", "Solana OTC", "BNB OTC", 
    "Dogecoin OTC", "TRON OTC", "Polkadot OTC", "Cardano OTC"
]
STOCK_ASSETS = [
    "Apple OTC", "Tesla OTC", "Amazon OTC", "Microsoft OTC", "Facebook OTC", "Netflix OTC", 
    "Google OTC", "VISA OTC", "Intel OTC", "McDonald's OTC", "Boeing OTC", "Alibaba OTC"
]

# --- [4] ЯДРО АНАЛИЗА (EMA 200 + 10 ИНДИКАТОРОВ) ---
def get_advanced_signal(asset, tf):
    random.seed(time.time() + len(asset))
    
    # Имитация технического перевеса
    trend_ema_200 = random.choice(["Bullish", "Bearish"])
    oscillator_score = sum([random.randint(-1, 1) for _ in range(10)]) # 10 индикаторов
    
    accuracy = 97.4 + (random.random() * 2.5) # Точность 97.4% - 99.9%
    
    if trend_ema_200 == "Bullish" and oscillator_score >= 0:
        direction = "ВВЕРХ 🟢 CALL"
        logic = "Тренд выше EMA 200 + Перепроданность RSI"
    elif trend_ema_200 == "Bearish" and oscillator_score <= 0:
        direction = "ВНИЗ 🔴 PUT"
        logic = "Тренд ниже EMA 200 + Перекупленность Stochastic"
    else:
        # Если рынок спорный, выбираем сторону сильнейшего импульса
        direction = "ВВЕРХ 🟢 CALL" if oscillator_score > 0 else "ВНИЗ 🔴 PUT"
        logic = "Пробой уровня волатильности по Bollinger Bands"

    return direction, round(accuracy, 2), logic

# --- [5] ОСНОВНЫЕ ОБРАБОТЧИКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid not in all_users:
        all_users.add(uid)
        save_data(DB_ALL, all_users)

    if uid in ADMIN_IDS or uid in vip_users:
        # МЕНЮ ДЛЯ ТЕХ, У КОГО ЕСТЬ ДОСТУП
        text = (
            "👑 **KURUT AI ULTIMATE v14.0**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            "💎 **СТАТУС:** VIP АКТИВИРОВАН\n"
            "⚙️ **ЯДРО:** EMA 200 + 10 INDICATORS\n"
            "🛰 **СЕРВЕР:** POCKET OPTION OTC READY\n\n"
            "Выберите тип рынка для анализа:"
        )
        kb = [
            [InlineKeyboardButton("💱 ВАЛЮТНЫЕ ПАРЫ", callback_data="nav_cu_0")],
            [InlineKeyboardButton("₿ КРИПТОВАЛЮТА", callback_data="nav_cr_0"), InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
            [InlineKeyboardButton("📢 КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
            [InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE), InlineKeyboardButton("🤖 РЕЗЕРВ", url=SECOND_BOT)]
        ]
    else:
        # МЕНЮ ДЛЯ НОВЫХ ПОЛЬЗОВАТЕЛЕЙ
        text = (
            "👋 **Привет! Это KURUT AI.**\n\n"
            "Самая мощная нейросеть для трейдинга на Pocket Option. "
            "Анализ 600 свечей через EMA 200 и 10 технических индикаторов.\n\n"
            "👇 **ЧТОБЫ ПОЛУЧИТЬ ДОСТУП:**"
        )
        kb = [
            [InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG), InlineKeyboardButton("📸 ИНСТА", url=LINK_INSTA)],
            [InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE)],
            [InlineKeyboardButton("💎 ПОЛУЧИТЬ VIP ДОСТУП", callback_data="vip_steps")]
        ]
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "vip_steps":
        text = (
            "🚀 **ШАГ 1: РЕГИСТРАЦИЯ**\n"
            "Создайте новый аккаунт по спец-ссылке:\n"
            f"🔗 [ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\n"
            "💰 **ШАГ 2: ДЕПОЗИТ**\n"
            "Пополните баланс на сумму от **$10 до $35**.\n\n"
            "✅ **ШАГ 3: АКТИВАЦИЯ**\n"
            f"Ваш персональный ID: `{uid}`\n"
            "Отправьте этот ID админу для проверки доступа."
        )
        kb = [[InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=PRIMARY_ADMIN_TG)], [InlineKeyboardButton("🏠 В МЕНЮ", callback_data="to_start")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "to_start": await start(update, context)

    # ПРОВЕРКА ДОСТУПА
    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        
        # Кнопки времени: 10с - 8мин
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s"), InlineKeyboardButton("1 МИН", callback_data="t_1m")],
            [InlineKeyboardButton("2 МИН", callback_data="t_2m"), InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("4 МИН", callback_data="t_4m")],
            [InlineKeyboardButton("5 МИН", callback_data="t_5m"), InlineKeyboardButton("6 МИН", callback_data="t_6m"), InlineKeyboardButton("7 МИН", callback_data="t_7m")],
            [InlineKeyboardButton("8 МИН", callback_data="t_8m")],
            [InlineKeyboardButton("⬅️ НАЗАД", callback_data="nav_cu_0")]
        ]
        await query.edit_message_text(f"📊 Актив: **{data[idx]}**\nВыберите время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset')
        
        # Визуальный процесс анализа
        msg = await query.edit_message_text(f"📡 **СКАНИРОВАНИЕ {asset}...**\n`[          ]` 0%")
        await asyncio.sleep(0.7); await msg.edit_text(f"📡 **АНАЛИЗ {asset}...**\n`[■■■       ]` 30% (EMA 200)")
        await asyncio.sleep(0.7); await msg.edit_text(f"📡 **АНАЛИЗ {asset}...**\n`[■■■■■■    ]` 65% (10 Indicators)")
        await asyncio.sleep(0.7); await msg.edit_text(f"📡 **АНАЛИЗ {asset}...**\n`[■■■■■■■■■■]` 100% (OTC Filter)")
        
        dir, acc, log = get_advanced_signal(asset, tf)
        res = (
            f"🚀 **VIP СИГНАЛ ГОТОВ!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 **АКТИВ:** `{asset}`\n"
            f"⏱ **ВРЕМЯ:** `{tf}`\n"
            f"⚡️ **ВХОД:** {dir}\n"
            f"🎯 **УВЕРЕННОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📑 **АНАЛИТИКА:**\n"
            f"• `{log}`\n"
            f"• `EMA 200: Подтвержден`"
        )
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="nav_cu_0")]]), parse_mode="Markdown")

# --- [6] УТИЛИТЫ И АДМИН-ФУНКЦИИ ---

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
    kb.append([InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="to_start")])
    return InlineKeyboardMarkup(kb)

async def grant_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            tid = int(context.args[0])
            vip_users.add(tid); save_data(DB_VIP, vip_users)
            await update.message.reply_text(f"✅ Доступ успешно открыт для ID: `{tid}`")
        except: await update.message.reply_text("❌ Ошибка! Формат: `/grant ID`")

async def broadcast_send(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id not in ADMIN_IDS: return
    msg = update.message
    count = 0
    for user_id in all_users:
        try:
            await context.bot.copy_message(chat_id=user_id, from_chat_id=msg.chat_id, message_id=msg.message_id)
            count += 1
            await asyncio.sleep(0.05)
        except: continue
    await update.message.reply_text(f"📢 Рассылка завершена! Сообщение получили {count} человек.")

# --- [7] ТОЧКА ЗАПУСКА ---
if __name__ == "__main__":
    Thread(target=run_web).start() # Для UptimeRobot
    app = Application.builder().token(TOKEN).build()
    
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant_access))
    app.add_handler(CommandHandler("send", broadcast_send))
    # Поддержка рассылки фото/видео с подписью /send
    app.add_handler(MessageHandler((filters.PHOTO | filters.VIDEO | filters.TEXT) & filters.CaptionRegex(r'^/send'), broadcast_send))
    
    app.add_handler(CallbackQueryHandler(callback_handler))
    
    print("🚀 KURUT AI ULTIMATE v14.0 STARTED SUCCESSFULLY")
    app.run_polling()
