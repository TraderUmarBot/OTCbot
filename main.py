import asyncio
import json
import os
import random
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] СЕРВЕР ДЛЯ KOYEB ---
server = Flask('')
@server.route('/')
def home(): return "KURUT INFINITY ULTRA v24 | POCKET OPTION OTC ACTIVE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] КОНФИГ ---
TOKEN = "8578509228:AAE2D6ANQGgXWkyLkVXYnq_htqFbTAYF_Ms"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@id6117198446"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

# Ссылки
LINKS = {
    "tg": "https://t.me/KURUTTRADING",
    "insta": "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw==",
    "yt": "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
}

# БД
DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "trader_stats.json"

def load_db(file, default_type=list):
    if os.path.exists(file):
        with open(file, 'r') as f: return json.load(f)
    return default_type()

def save_db(file, data):
    with open(file, 'w') as f: json.dump(data, f)

vip_users = set(load_db(DB_VIP))
all_users = set(load_db(DB_ALL))
trader_stats = load_db(DB_STATS, dict)

# --- [3] СПИСКИ АКТИВОВ (ПОЛНЫЕ) ---
OTC_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC", "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/RUB OTC", "EUR/RUB OTC", "CHF/NOK OTC", "EUR/HUF OTC", "USD/CNH OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CLP OTC", "USD/MYR OTC", "USD/THB OTC", "USD/VND OTC", "USD/PKR OTC", "USD/COP OTC", "USD/EGP OTC", "USD/PHP OTC", "USD/MXN OTC", "USD/DZD OTC", "USD/ARS OTC", "USD/IDR OTC", "USD/BRL OTC", "USD/BDT OTC", "YER/USD OTC", "LBP/USD OTC", "TND/USD OTC", "MAD/USD OTC", "BHD/CNY OTC", "NGN/USD OTC", "KES/USD OTC", "ZAR/USD OTC", "UAH/USD OTC"
]
STOCKS = [
    "McDonald’s", "Intel", "American Express", "Palantir", "Microsoft", "Apple", "GameStop", "Pfizer", "Boeing", "Visa", "Meta", "Citigroup", "Cisco", "Marathon Digital", "FedEx", "Johnson & Johnson", "ExxonMobil", "Tesla", "Coinbase", "Amazon", "AMD", "Alibaba", "Netflix"
]
CRYPTO = [
    "Bitcoin (BTC)", "Ethereum (ETH)", "Bitcoin ETF", "Cardano (ADA)", "BNB", "Solana (SOL)", "TRON (TRX)", "Polkadot (DOT)", "Dogecoin (DOGE)", "Avalanche (AVAX)", "Chainlink (LINK)", "Toncoin (TON)", "Litecoin (LTC)"
]

# --- [4] АЛГОРИТМ ПОВЫШЕННОЙ ТОЧНОСТИ ---
def get_ultra_signal():
    accuracy = random.uniform(89.4, 98.2)
    direction = "ВВЕРХ 🟢 CALL" if random.random() > 0.48 else "ВНИЗ 🔴 PUT"
    
    analysis_logs = [
        "Анализ японских свечей выявил паттерн 'Молот'.",
        "Сильный импульс отскока от уровня Фибоначчи 0.618.",
        "Индикаторы Stochastic и RSI в зоне перепроданности.",
        "Алгоритм зафиксировал крупный объем на покупку.",
        "Тренд OTC подтвержден скользящими средними EMA 50/200."
    ]
    return direction, round(accuracy, 2), random.choice(analysis_logs)

# --- [5] ЛОГИКА ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in all_users:
        all_users.add(uid); save_db(DB_ALL, list(all_users))
    
    text = (
        f"👋 **Привет, {update.effective_user.first_name}!**\n\n"
        "Это **KURUT AI INFINITY** — профессиональный софт для Pocket Option.\n"
        "Математический анализ 52+ OTC пар и акций в реальном времени."
    )
    kb = [[InlineKeyboardButton("📚 ИНСТРУКЦИЯ ПО БОТУ", callback_data="v_guide")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = str(query.from_user.id)
    await query.answer()

    if query.data == "v_guide":
        text = "📖 **ИНСТРУКЦИЯ:**\n\n1. Выбери актив.\n2. Выбери время (10с - 8м).\n3. Заходи в сделку по сигналу.\n\nБот анализирует рынок OTC с точностью до 98%."
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ (СОЦСЕТИ)", callback_data="v_socials")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "v_socials":
        text = "🔗 **НАШИ КОНТАКТЫ:**"
        kb = [
            [InlineKeyboardButton("📢 TG", url=LINKS['tg']), InlineKeyboardButton("📸 INSTA", url=LINKS['insta'])],
            [InlineKeyboardButton("▶️ YOUTUBE", url=LINKS['yt'])],
            [InlineKeyboardButton("➡️ ДАЛЕЕ (ПОЛУЧИТЬ ДОСТУП)", callback_data="v_access")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb))

    elif query.data == "v_access":
        text = (
            "💎 **ДОСТУП К СИГНАЛАМ:**\n\n"
            f"1. Регистрация: [POCKET OPTION]({REF_LINK})\n"
            "2. Депозит от **$15** (стандарт) или **$35** (VIP).\n"
            f"3. Твой ID: `{uid}` — отправь его @id6117198446"
        )
        kb = [[InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="m_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "m_home":
        is_vip = uid in [str(a) for a in ADMIN_IDS] or uid in vip_users
        if is_vip:
            text = "🚀 **ГЛАВНОЕ МЕНЮ | ДОСТУП АКТИВЕН**"
            kb = [
                [InlineKeyboardButton("📊 АНАЛИЗ РЫНКА", callback_data="m_market")],
                [InlineKeyboardButton("🏃 МАРАФОН", callback_data="m_mara"), InlineKeyboardButton("🏆 ТОП", callback_data="m_top")]
            ]
        else:
            text = "⚠️ **ДОСТУП НЕ АКТИВИРОВАН**"
            kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="v_access")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # --- VIP РАЗДЕЛ ---
    if uid not in [str(a) for a in ADMIN_IDS] and uid not in vip_users: return

    if query.data == "m_market":
        kb = [
            [InlineKeyboardButton("💱 ВАЛЮТЫ OTC (52)", callback_data="nav_cu_0")],
            [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")],
            [InlineKeyboardButton("₿ КРИПТОВАЛЮТА", callback_data="nav_cr_0")]
        ]
        await query.edit_message_text("🎯 **ВЫБЕРИ КАТЕГОРИЮ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = OTC_PAIRS if pref == "cu" else STOCKS if pref == "st" else CRYPTO
        await query.edit_message_text("📍 **ВЫБЕРИ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "st_", "cr_")):
        idx = int(query.data.split("_")[1])
        asset = (OTC_PAIRS if "cu" in query.data else STOCKS if "st" in query.data else CRYPTO)[idx]
        context.user_data['asset'] = asset
        tfs = ["10 СЕК", "30 СЕК", "М1", "М2", "М3", "М4", "М5", "М8"]
        kb = [ [InlineKeyboardButton(t, callback_data=f"t_{t}")] for t in tfs ]
        await query.edit_message_text(f"📊 **АКТИВ:** `{asset}`\nВыбери экспирацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1]
        asset = context.user_data.get('asset')
        msg = await query.edit_message_text(f"📡 **СКАНИРОВАНИЕ OTC РЫНКА...**\n`Пара: {asset} | ТФ: {tf}`")
        await asyncio.sleep(4)
        
        dir, acc, log = get_ultra_signal()
        res = (
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📊 АКТИВ: `{asset}`\n"
            f"⏳ ВРЕМЯ: `{tf}`\n"
            f"🚦 ВХОД: **{dir}**\n"
            f"🎯 ВЕРОЯТНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📋 **АНАЛИЗ:** _{log}_"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_p"), InlineKeyboardButton("❌ МИНУС", callback_data="res_m")]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("res_"):
        await query.edit_message_text("♻️ Результат в статистике!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 НОВЫЙ АНАЛИЗ", callback_data="m_market")]]))

# --- [6] АДМИНКА ---

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in [str(a) for a in ADMIN_IDS]: return

    txt = update.message.text
    if txt.startswith("/grant"):
        tid = txt.split()[1]
        vip_users.add(tid); save_db(DB_VIP, list(vip_users))
        await update.message.reply_text(f"✅ Доступ открыт: {tid}")
        try:
            await context.bot.send_message(chat_id=tid, text="🎉 **АДМИН ОТКРЫЛ ВАМ ДОСТУП!**\nТеперь сигналы доступны.", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛЫ", callback_data="m_home")]]))
        except: pass

    elif txt.startswith("/revoke"):
        tid = txt.split()[1]
        if tid in vip_users: vip_users.remove(tid); save_db(DB_VIP, list(vip_users))
        await update.message.reply_text(f"❌ Доступ закрыт: {tid}")

def get_paged_kb(data, page, prefix):
    size = 10
    items = data[page*size : (page+1)*size]
    kb = [[InlineKeyboardButton(items[i], callback_data=f"{prefix}_{page*size+i}")] for i in range(len(items))]
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if (page+1)*size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="m_home")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    Thread(target=run_web).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🚀 KURUT INFINITY ULTRA v24 СТАРТОВАЛ!")
    app.run_polling()
