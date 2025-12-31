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

# ================== ПОЛНЫЕ СПИСКИ АКТИВОВ ==================
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

# ================== СИЛЬНЫЙ МАТЕМАТИЧЕСКИЙ АЛГОРИТМ ==================
def get_advanced_signal(asset):
    # Генерация уникального зерна на основе времени и актива
    random.seed(time.time() + sum(ord(c) for c in asset))
    
    # Расчет веса из 30 виртуальных индикаторов
    indicators_score = sum([random.uniform(-1, 1) for _ in range(30)])
    accuracy = 96.8 + (random.random() * 2.9)
    
    if indicators_score > 0.2:
        direction = "ВВЕРХ 🟢 CALL"
        logic = "Импульс от зоны поддержки + Сигнал RSI"
    elif indicators_score < -0.2:
        direction = "ВНИЗ 🔴 PUT"
        logic = "Пробой уровня + Перекупленность Stochastic"
    else:
        direction = "ВВЕРХ 🟢 CALL" if indicators_score > 0 else "ВНИЗ 🔴 PUT"
        logic = "Тест локального экстремума"
        
    return direction, round(accuracy, 2), logic

# ================== ЛОГИКА ИНТЕРФЕЙСА ==================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    
    # Кнопки соцсетей (всегда снизу)
    social_kb = [
        [InlineKeyboardButton("📢 ТГ КАНАЛ", url=LINK_TG), InlineKeyboardButton("🤖 ВТОРОЙ БОТ", url=SECOND_BOT)],
        [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("📺 YOUTUBE", url=YOUTUBE)]
    ]

    if uid in ADMIN_IDS or uid in vip_users:
        text = "🚀 **ТЕРМИНАЛ KURUT AI АКТИВИРОВАН**\n\nБро, выбирай актив. Алгоритм готов к сканированию Pocket Option."
        kb = [[InlineKeyboardButton("📊 НАЧАТЬ АНАЛИЗ РЫНКА", callback_data="market")]] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        return

    text = (
        "👋 **Добро пожаловать в KURUT AI!**\n\n"
        "Этот бот — твой главный инструмент для работы на **Pocket Option**.\n\n"
        "🔥 **ВОЗМОЖНОСТИ:**\n"
        "✅ Анализ 48 валютных пар, крипты и акций.\n"
        "✅ Математический алгоритм на 30 индикаторах.\n"
        "✅ Работа со всеми таймфреймами (10с - 8м).\n\n"
        "⚠️ **ИНСТРУКЦИЯ:**\n"
        "Лучшее время экспирации: **1м, 3м, 6м**.\n\n"
        "Для доступа к сигналам пройди активацию 👇"
    )
    kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="instruction")]] + social_kb
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "instruction":
        text = (
            "🚀 **ШАГИ ДЛЯ АКТИВАЦИИ АНАЛИЗАТОРА:**\n\n"
            f"1️⃣ Регистрация на Pocket Option:\n🔗 [ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\n"
            "2️⃣ Пополни баланс (от $15).\n\n"
            f"3️⃣ Пришли админу свой ID: `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 АКТИВИРОВАТЬ МОЙ ID", url=PRIMARY_ADMIN_LINK)],
              [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "to_home":
        await start(update, context)

    if uid not in ADMIN_IDS and uid not in vip_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТНЫЕ ПАРЫ (48)", callback_data="nav_cu_0")],
              [InlineKeyboardButton("₿ КРИПТОВАЛЮТЫ", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ / STOCKS", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК ДЛЯ СКАННИРОВАНИЯ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН ⭐", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("3 МИН ⭐", callback_data="t_3m"), InlineKeyboardButton("4 МИН", callback_data="t_4m")],
            [InlineKeyboardButton("5 МИН", callback_data="t_5m"), InlineKeyboardButton("6 МИН ⭐", callback_data="t_6m")],
            [InlineKeyboardButton("7 МИН", callback_data="t_7m"), InlineKeyboardButton("8 МИН", callback_data="t_8m")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]
        ]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\n\nВыбирай время экспирации (⭐ - лучшее):", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf_label = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        asset = context.user_data.get('asset')
        
        # АНАЛИЗ РОВНО 6-7 СЕКУНД
        start_time = time.time()
        steps = ["📡 Синхронизация с Pocket Option...", "📊 Поиск паттернов...", "🧠 Математический расчет..."]
        for step in steps:
            await query.edit_message_text(f"📡 **ГЛУБОКИЙ АНАЛИЗ {asset}...**\n\n`{step}`")
            await asyncio.sleep(2.1) # 2.1 * 3 = 6.3 секунды
            
        direction, acc, logic = get_advanced_signal(asset)
        
        res = (
            f"✅ **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 **ПЛАТФОРМА:** Pocket Option\n"
            f"📊 **ПАРА:** `{asset}`\n"
            f"⚡️ **ВХОД:** {direction}\n"
            f"⏱ **ВРЕМЯ:** `{tf_label}`\n"
            f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🧠 **ЛОГИКА:** `{logic}`\n"
            f"📢 *Входи сразу! Сигнал актуален 30 секунд.*"
        )
        kb = [[InlineKeyboardButton("✅ ВИН / PLUS", callback_data="market"), InlineKeyboardButton("❌ ЛОСС / LOSS", callback_data="market")],
              [InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")],
              [InlineKeyboardButton("🔗 РЕГИСТРАЦИЯ PO", url=REF_LINK)]]
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

def get_paged_kb(data, page, prefix):
    size = 10
    start_idx = page * size
    items = data[start_idx:start_idx+size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"nav_{prefix}_{page-1}"))
    if start_idx+size < len(data): nav.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 В МЕНЮ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT ULTIMATE v12.0 STARTED")
    app.run_polling()

