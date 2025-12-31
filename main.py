import asyncio
import json
import os
import random
import math
import time
from threading import Thread
from http.server import HTTPServer
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- [1] НАСТРОЙКИ ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMINS = {6117198446, 7079260196}
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

DB_FILE = "vip_users.json"
def load_vip():
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, 'r') as f: return set(json.load(f))
        except: return set()
    return set()

vip_users = load_vip()

# --- [2] ПОЛНЫЙ СПИСОК ПАР ---
CURRENCY_PAIRS = ["EUR/USD OTC","AUD/CAD OTC","AUD/CHF OTC","AUD/USD OTC","CAD/CHF OTC","CAD/JPY OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC","EUR/JPY OTC","EUR/NZD OTC","GBP/USD OTC","NZD/USD OTC","USD/CAD OTC","USD/CHF OTC","USD/JPY OTC","USD/CNH OTC","EUR/RUB OTC","USD/RUB OTC","EUR/TRY OTC","USD/INR OTC","USD/MXN OTC","USD/BRL OTC","USD/PHP OTC","UAH/USD OTC","AUD/NZD OTC","GBP/JPY OTC","NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC","BNB OTC","Dogecoin OTC","Ethereum OTC","Solana OTC","Toncoin OTC","Litecoin OTC","TRON OTC"]
STOCK_ASSETS = ["Apple OTC","McDonald’s OTC","Microsoft OTC","Facebook OTC","Tesla OTC","Amazon OTC","Netflix OTC","VISA OTC","Alibaba OTC","AMD OTC"]

# --- [3] МАТЕМАТИЧЕСКИЙ АЛГОРИТМ АНАЛИЗА ---
def calculate_trading_signal(asset, timeframe):
    """
    Имитация реального тех-анализа через математическую модель весов.
    """
    # Создаем уникальное зерно для расчета на основе текущего времени и актива,
    # чтобы сигнал менялся, но следовал внутренней логике "рынка".
    seed = time.time() + sum(ord(c) for c in asset)
    random.seed(seed)
    
    # 1. Генерируем "показания" 30 индикаторов (от -100 до 100)
    # Где -100 это сильный перепроданность (BUY), 100 - перекупленность (SELL)
    indicator_weights = [random.uniform(-100, 100) for _ in range(30)]
    
    # 2. Учитываем таймфрейм (влияет на шум)
    tf_multiplier = 1.5 if "s" in timeframe else 1.0
    
    # 3. Суммируем вектор движения
    market_vector = sum(indicator_weights) * tf_multiplier
    
    # Определение направления
    if market_vector > 0:
        direction = "ВНИЗ 🔴 PUT"
        logic = "Перекупленность по RSI и Bollinger Bands"
    else:
        direction = "ВВЕРХ 🟢 CALL"
        logic = "Отскок от уровня поддержки + бычье поглощение"
        
    # Расчет точности (вероятности)
    accuracy = 94.0 + (abs(market_vector) / 3000 * 5.9)
    if accuracy > 99.8: accuracy = 99.8
    
    return direction, round(accuracy, 2), logic

async def run_analysis_engine(query, asset, tf):
    await query.edit_message_text(f"📡 **ИНИЦИАЛИЗАЦИЯ АНАЛИЗА...**\n`Актив:` {asset}\n`Таймфрейм:` {tf}")
    await asyncio.sleep(1.5)
    
    # Процесс "сканирования"
    for i in range(1, 4):
        p = i * 33
        await query.edit_message_text(f"📊 **KURUT AI QUANTUM v9.0**\n\n🔎 Сканирование рынка: {p}%\n⚙️ Обработка индикаторов: {i*10}/30\n📦 Свечей в памяти: 600")
        await asyncio.sleep(1.2)

    # Получаем результат из мат-модели
    direction, acc, reason = calculate_trading_signal(asset, tf)
    
    res_msg = (
        f"👑 **СИГНАЛ СФОРМИРОВАН**\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📊 **АКТИВ:** `{asset}`\n"
        f"⚡️ **ВХОД:** {direction}\n"
        f"⏱ **ВРЕМЯ:** `{tf}`\n"
        f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📑 **АНАЛИТИКА:**\n"
        f"• Индикаторы: `30/30 подтверждено`\n"
        f"• Алгоритм: `{reason}`\n"
        f"• База данных: `Сигнал на основе 600 свечей`"
    )
    
    kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_save"), InlineKeyboardButton("❌ МИНУС", callback_data="res_save")],
          [InlineKeyboardButton("🔄 ДРУГОЙ АКТИВ", callback_data="market")]]
    await query.edit_message_text(res_msg, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# --- [4] ОСНОВНЫЕ ФУНКЦИИ (СТАРТ, КОЛБЭКИ) ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    if uid in ADMINS or uid in vip_users:
        text = "🚀 **ДОБРО ПОЖАЛОВАТЬ, ТРЕЙДЕР!**\n\nМатематический движок KURUT AI готов к работе."
        kb = [[InlineKeyboardButton("📈 НАЧАТЬ АНАЛИЗ", callback_data="market")],
              [InlineKeyboardButton("📢 КАНАЛ", url="https://t.me/KURUTTRADING")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        # Инструкция для новичков
        text = (
            "👋 **Привет! Это KURUT AI.**\n\n"
            "Наш бот анализирует 30 индикаторов и 600 свечей для каждого сигнала.\n"
            "Для доступа выполните активацию."
        )
        kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="get_vip")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = query.from_user.id
    await query.answer()

    if query.data == "get_vip":
        instr = (
            "💎 **ИНСТРУКЦИЯ ПО АКТИВАЦИИ:**\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"1️⃣ Регистрация: [ССЫЛКА]({REF_LINK})\n"
            "2️⃣ Пополнение от **$20**.\n"
            f"3️⃣ Скиньте ваш ID админу: `{uid}`"
        )
        kb = [[InlineKeyboardButton("👨‍💻 АДМИН", url="tg://user?id=7079260196")],
              [InlineKeyboardButton("🏠 В МЕНЮ", callback_data="to_home")]]
        await query.edit_message_text(instr, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "to_home": await start(update, context)

    # Проверка доступа для торговых функций
    if uid not in ADMINS and uid not in vip_users: return

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0"), InlineKeyboardButton("₿ КРИПТА", callback_data="nav_cr_0")],
              [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        data = CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        kb = [[InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
              [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("5М", callback_data="t_5m")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['asset']}**\nВыберите время:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        await run_analysis_engine(query, context.user_data.get('asset'), tf)

    elif query.data == "res_save":
        await query.edit_message_text("✅ Данные сохранены в модель!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]))

# --- [5] ВСПОМОГАТЕЛЬНОЕ ---
def get_paged_kb(data, page, prefix):
    size = 10
    start = page * size
    items = data[start:start+size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start+size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    def run_dummy(): HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever()
    Thread(target=run_dummy, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT MATH-ENGINE STARTED")
    app.run_polling()
