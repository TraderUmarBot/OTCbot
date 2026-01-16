# ==============================
# KURUT AI INFINITY | PRO EDITION
# OTC SIGNAL SYSTEM FOR POCKET OPTION
# ==============================

import asyncio
import json
import os
import time
import numpy as np
import pandas as pd
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# -----------------------------
# SERVER
# -----------------------------
server = Flask('')

@server.route('/')
def home():
    return "KURUT AI INFINITY | PRO ENGINE ACTIVE"

def run_web():
    server.run(host='0.0.0.0', port=8080)

# -----------------------------
# CONFIG
# -----------------------------
TOKEN = "ТВОЙ_BOT_TOKEN"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@id6117198446"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "trader_stats.json"
DB_LOGS = "admin_logs.json"

# -----------------------------
# STORAGE
# -----------------------------
def load_db(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r") as f:
                return json.load(f)
        except:
            return default
    return default

def save_db(file, data):
    with open(file, "w") as f:
        json.dump(data, f, indent=2)

vip_users = set(load_db(DB_VIP, []))
all_users = set(load_db(DB_ALL, []))
trader_stats = load_db(DB_STATS, {})
admin_logs = load_db(DB_LOGS, [])

# -----------------------------
# ASSETS
# -----------------------------
OTC_PAIRS = [
    "EUR/USD OTC","AUD/CAD OTC","AUD/CHF OTC","AUD/JPY OTC","AUD/NZD OTC","AUD/USD OTC",
    "CAD/CHF OTC","CAD/JPY OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC","EUR/JPY OTC",
    "EUR/NZD OTC","GBP/AUD OTC","GBP/JPY OTC","GBP/USD OTC","NZD/JPY OTC","NZD/USD OTC",
    "USD/CAD OTC","USD/CHF OTC","USD/JPY OTC","USD/RUB OTC","EUR/RUB OTC","CHF/NOK OTC",
    "EUR/HUF OTC","USD/CNH OTC","EUR/TRY OTC","USD/INR OTC","USD/SGD OTC","USD/CLP OTC",
    "USD/MYR OTC","USD/THB OTC","USD/VND OTC","USD/PKR OTC","USD/COP OTC","USD/EGP OTC",
    "USD/PHP OTC","USD/MXN OTC","USD/DZD OTC","USD/ARS OTC","USD/IDR OTC","USD/BRL OTC",
    "USD/BDT OTC","YER/USD OTC","LBP/USD OTC","TND/USD OTC","MAD/USD OTC","BHD/CNY OTC",
    "NGN/USD OTC","KES/USD OTC","ZAR/USD OTC","UAH/USD OTC"
]

STOCKS = [
    "McDonald’s","Intel","American Express","Palantir","Microsoft","Apple","GameStop",
    "Pfizer","Boeing","Visa","Meta","Citigroup","Cisco","FedEx","Tesla","Coinbase",
    "Amazon","AMD","Netflix"
]

CRYPTO = ["Bitcoin (BTC)","Ethereum (ETH)","Solana (SOL)","Toncoin (TON)","Litecoin (LTC)","Dogecoin (DOGE)"]

# -----------------------------
# MARKET SIMULATION (замени API при желании)
# -----------------------------
def generate_candles(n=120):
    price = 100
    data = []
    for _ in range(n):
        open_p = price
        close_p = open_p + np.random.randn() * 0.3
        high = max(open_p, close_p) + abs(np.random.randn() * 0.2)
        low = min(open_p, close_p) - abs(np.random.randn() * 0.2)
        data.append({"open": open_p, "high": high, "low": low, "close": close_p})
        price = close_p
    return pd.DataFrame(data)

# -----------------------------
# INDICATORS
# -----------------------------
def ema(series, period):
    return series.ewm(span=period).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series):
    fast = ema(series, 12)
    slow = ema(series, 26)
    return fast - slow

def atr(df, period=14):
    high_low = df['high'] - df['low']
    high_close = abs(df['high'] - df['close'].shift())
    low_close = abs(df['low'] - df['close'].shift())
    ranges = pd.concat([high_low, high_close, low_close], axis=1)
    return ranges.max(axis=1).rolling(period).mean()

def adx(df, period=14):
    return atr(df, period) * 2  # упрощённая версия

# -----------------------------
# AI ENGINE
# -----------------------------
def analyze_market():
    df = generate_candles()
    close = df["close"]

    score = 0
    reasons = []

    ema20 = ema(close, 20).iloc[-1]
    ema50 = ema(close, 50).iloc[-1]
    ema200 = ema(close, 200).iloc[-1]
    rsi_val = rsi(close).iloc[-1]
    macd_val = macd(close).iloc[-1]
    atr_val = atr(df).iloc[-1]
    adx_val = adx(df).iloc[-1]

    if ema20 > ema50 > ema200:
        score += 2
        reasons.append("Сильный восходящий тренд (EMA)")
    elif ema20 < ema50 < ema200:
        score -= 2
        reasons.append("Сильный нисходящий тренд (EMA)")

    if rsi_val < 30:
        score += 1
        reasons.append("RSI перепроданность")
    elif rsi_val > 70:
        score -= 1
        reasons.append("RSI перекупленность")

    if macd_val > 0:
        score += 1
        reasons.append("MACD подтверждает рост")
    else:
        score -= 1
        reasons.append("MACD подтверждает падение")

    if atr_val > close.mean() * 0.002:
        score += 1
        reasons.append("Хорошая волатильность")

    if adx_val > 0.4:
        score += 1
        reasons.append("Сильное движение OTC")

    probability = min(99, max(55, 50 + score * 7))
    direction = "ВВЕРХ 🟢 CALL" if score >= 1 else "ВНИЗ 🔴 PUT"

    return direction, probability, " | ".join(reasons[:3])

# -----------------------------
# ACCESS CONTROL
# -----------------------------
def is_admin(uid):
    return str(uid) in [str(a) for a in ADMIN_IDS]

def is_vip(uid):
    return str(uid) in vip_users or is_admin(uid)

def log_admin(action, target, admin):
    admin_logs.append({
        "time": int(time.time()),
        "admin": admin,
        "action": action,
        "target": target
    })
    save_db(DB_LOGS, admin_logs)

# -----------------------------
# UI
# -----------------------------
async def show_menu(update, context):
    text = "🚀 **KURUT AI INFINITY | PRO MENU**"
    kb = [
        [InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛ", callback_data="market")],
        [InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="top")],
        [InlineKeyboardButton("📚 ИНСТРУКЦИЯ", callback_data="guide")]
    ]
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# -----------------------------
# START
# -----------------------------
async def start(update: Update, context):
    uid = str(update.effective_user.id)
    all_users.add(uid)
    save_db(DB_ALL, list(all_users))

    if is_vip(uid):
        await show_menu(update, context)
    else:
        text = (
            "👋 **Добро пожаловать в KURUT AI INFINITY**\n\n"
            "Для доступа:\n"
            f"1️⃣ Зарегистрируйся: [Pocket Option]({REF_LINK})\n"
            "2️⃣ Пополни баланс от $15\n"
            f"3️⃣ Отправь ID: `{uid}` админу {ADMIN_USER}"
        )
        await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)

# -----------------------------
# CALLBACKS
# -----------------------------
async def callback_handler(update: Update, context):
    q = update.callback_query
    uid = str(q.from_user.id)
    await q.answer()

    if not is_vip(uid):
        return

    if q.data == "market":
        kb = [
            [InlineKeyboardButton("💱 OTC", callback_data="cu_0")],
            [InlineKeyboardButton("🏢 АКЦИИ", callback_data="st_0")],
            [InlineKeyboardButton("₿ КРИПТО", callback_data="cr_0")]
        ]
        await q.edit_message_text("Выбери рынок:", reply_markup=InlineKeyboardMarkup(kb))

    elif q.data.startswith(("cu_", "st_", "cr_")):
        pref, page = q.data.split("_")
        data = OTC_PAIRS if pref == "cu" else STOCKS if pref == "st" else CRYPTO
        page = int(page)
        await q.edit_message_text("Выбери актив:", reply_markup=get_paged_kb(data, page, pref))

    elif q.data.startswith("asset_"):
        idx = int(q.data.split("_")[1])
        asset = context.user_data["assets"][idx]
        context.user_data["asset"] = asset

        msg = await q.edit_message_text(f"📡 Анализируем {asset}...")
        await asyncio.sleep(3)

        direction, prob, reason = analyze_market()
        res = (
            f"✨ **СИГНАЛ**\n\n"
            f"📊 Актив: `{asset}`\n"
            f"🚦 Направление: **{direction}**\n"
            f"🎯 Вероятность: `{prob}%`\n\n"
            f"📋 Причины:\n_{reason}_"
        )

        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_plus"),
               InlineKeyboardButton("❌ МИНУС", callback_data="res_minus")]]

        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# -----------------------------
# PAGINATION
# -----------------------------
def get_paged_kb(data, page, prefix):
    size = 8
    start = page * size
    chunk = data[start:start + size]

    kb = []
    for i, item in enumerate(chunk):
        kb.append([InlineKeyboardButton(item, callback_data=f"asset_{start+i}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"{prefix}_{page-1}"))
    if start + size < len(data):
        nav.append(InlineKeyboardButton("➡️", callback_data=f"{prefix}_{page+1}"))

    if nav:
        kb.append(nav)

    return InlineKeyboardMarkup(kb)

# -----------------------------
# ADMIN COMMANDS
# -----------------------------
async def admin_commands(update: Update, context):
    uid = str(update.effective_user.id)
    if not is_admin(uid):
        return

    txt = update.message.text.split()
    cmd = txt[0]

    if cmd == "/grant" and len(txt) > 1:
        tid = txt[1]
        vip_users.add(tid)
        save_db(DB_VIP, list(vip_users))
        log_admin("GRANT", tid, uid)
        await update.message.reply_text(f"✅ Доступ выдан: {tid}")

    elif cmd == "/revoke" and len(txt) > 1:
        tid = txt[1]
        vip_users.discard(tid)
        save_db(DB_VIP, list(vip_users))
        log_admin("REVOKE", tid, uid)
        await update.message.reply_text(f"❌ Доступ снят: {tid}")

# -----------------------------
# RUN
# -----------------------------
if __name__ == "__main__":
    Thread(target=run_web).start()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.Regex(r"^/(grant|revoke)"), admin_commands))

    print("🚀 KURUT AI INFINITY | PRO ENGINE ONLINE")
    app.run_polling()
