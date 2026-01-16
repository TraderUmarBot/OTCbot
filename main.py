# =====================================
# KURUT AI INFINITY | COIP PRO EDITION
# OTC SIGNAL SYSTEM FOR POCKET OPTION
# FULL ADMIN / VIP / MARATHON / TOP / SEND
# =====================================

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
from telegram.error import BadRequest

# ---------------- SERVER ----------------
server = Flask('')

@server.route('/')
def home():
    return "KURUT AI INFINITY | COIP PRO ACTIVE"

def run_web():
    server.run(host='0.0.0.0', port=8080)

# ---------------- CONFIG ----------------
TOKEN = "ВСТАВЬ_СВОЙ_BOT_TOKEN"

ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@id6117198446"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

INSTAGRAM = "https://instagram.com/ТВОЙ_ИНСТА"
TELEGRAM = "https://t.me/ТВОЙ_ТГ"
YOUTUBE = "https://youtube.com/@ТВОЙ_YT"
BLOG = "https://ТВОЙ_БЛОГ"

DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "trader_stats.json"
DB_LOGS = "admin_logs.json"

# ---------------- STORAGE ----------------
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

# ---------------- ASSETS ----------------
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

# ---------------- UTILS ----------------
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

# ---------------- SAFE EDIT ----------------
async def safe_edit(query, text, reply_markup=None, parse_mode=None):
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            raise

# ---------------- MARKET DATA (SIM / API READY) ----------------
def generate_candles(n=120):
    price = 100
    data = []
    for _ in range(n):
        o = price
        c = o + np.random.randn() * 0.3
        h = max(o, c) + abs(np.random.randn() * 0.2)
        l = min(o, c) - abs(np.random.randn() * 0.2)
        data.append({"open": o, "high": h, "low": l, "close": c})
        price = c
    return pd.DataFrame(data)

# ---------------- INDICATORS ----------------
def ema(series, period):
    return series.ewm(span=period).mean()

def rsi(series, period=14):
    delta = series.diff()
    gain = delta.clip(lower=0).rolling(period).mean()
    loss = -delta.clip(upper=0).rolling(period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

def macd(series):
    return ema(series, 12) - ema(series, 26)

def atr(df, period=14):
    hl = df["high"] - df["low"]
    hc = abs(df["high"] - df["close"].shift())
    lc = abs(df["low"] - df["close"].shift())
    return pd.concat([hl, hc, lc], axis=1).max(axis=1).rolling(period).mean()

# ---------------- AI ENGINE ----------------
def analyze_market():
    df = generate_candles()
    close = df["close"]

    score = 0
    reasons = []

    ema20 = ema(close, 20).iloc[-1]
    ema50 = ema(close, 50).iloc[-1]
    ema200 = ema(close, 200).iloc[-1]
    rsi_v = rsi(close).iloc[-1]
    macd_v = macd(close).iloc[-1]
    atr_v = atr(df).iloc[-1]

    if ema20 > ema50 > ema200:
        score += 2
        reasons.append("EMA тренд вверх")
    elif ema20 < ema50 < ema200:
        score -= 2
        reasons.append("EMA тренд вниз")

    if rsi_v < 30:
        score += 1
        reasons.append("RSI перепроданность")
    elif rsi_v > 70:
        score -= 1
        reasons.append("RSI перекупленность")

    if macd_v > 0:
        score += 1
        reasons.append("MACD подтверждает рост")
    else:
        score -= 1
        reasons.append("MACD подтверждает падение")

    if atr_v > close.mean() * 0.002:
        score += 1
        reasons.append("Хорошая волатильность OTC")

    probability = min(99, max(55, 50 + score * 7))
    direction = "ВВЕРХ 🟢 CALL" if score >= 1 else "ВНИЗ 🔴 PUT"

    return direction, probability, " | ".join(reasons[:3])

# ---------------- UI ----------------
async def show_menu(update, context):
    text = "🚀 **KURUT AI INFINITY | PRO MENU**"
    kb = [
        [InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛ", callback_data="market")],
        [InlineKeyboardButton("🏃 МАРАФОН 30 ДНЕЙ", callback_data="marathon")],
        [InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="top")],
        [InlineKeyboardButton("📚 ИНСТРУКЦИЯ", callback_data="guide")]
    ]

    if update.callback_query:
        await safe_edit(update.callback_query, text, InlineKeyboardMarkup(kb), "Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# ---------------- START ----------------
async def start(update: Update, context):
    uid = str(update.effective_user.id)
    all_users.add(uid)
    save_db(DB_ALL, list(all_users))

    if is_vip(uid):
        await show_menu(update, context)
    else:
        text = (
            "👋 **Добро пожаловать в KURUT AI INFINITY**\n\n"
            "🔓 Для доступа:\n"
            f"1️⃣ Регистрация: [Pocket Option]({REF_LINK})\n"
            "2️⃣ Пополни баланс от $15\n"
            f"3️⃣ Отправь ID: `{uid}` админу {ADMIN_USER}\n\n"
            "🌐 **Наши соцсети:**\n"
            f"📸 Instagram: {INSTAGRAM}\n"
            f"💬 Telegram: {TELEGRAM}\n"
            f"▶️ YouTube: {YOUTUBE}\n"
            f"📝 Блог: {BLOG}"
        )
        await update.message.reply_text(text, parse_mode="Markdown", disable_web_page_preview=True)

# ---------------- CALLBACKS ----------------
async def callback_handler(update: Update, context):
    q = update.callback_query
    uid = str(q.from_user.id)
    await q.answer()

    if not is_vip(uid):
        return

    if q.data == "guide":
        await safe_edit(q, "📚 Используй сигналы с риск-менеджментом\nРекомендуемый риск: 1–5% от депозита")

    elif q.data == "market":
        kb = [
            [InlineKeyboardButton("💱 OTC", callback_data="cu_0")],
            [InlineKeyboardButton("🏢 АКЦИИ", callback_data="st_0")],
            [InlineKeyboardButton("₿ КРИПТО", callback_data="cr_0")]
        ]
        await safe_edit(q, "Выбери рынок:", InlineKeyboardMarkup(kb))

    elif q.data.startswith(("cu_", "st_", "cr_")):
        pref, page = q.data.split("_")
        data = OTC_PAIRS if pref == "cu" else STOCKS if pref == "st" else CRYPTO
        context.user_data["assets"] = data
        await safe_edit(q, "Выбери актив:", get_paged_kb(data, int(page), pref))

    elif q.data.startswith("asset_"):
        idx = int(q.data.split("_")[1])
        asset = context.user_data["assets"][idx]

        msg = await q.edit_message_text(f"📡 Анализируем {asset}...")
        await asyncio.sleep(3)

        direction, prob, reason = analyze_market()
        res = (
            f"✨ **СИГНАЛ**\n\n"
            f"📊 Актив: `{asset}`\n"
            f"🚦 Вход: **{direction}**\n"
            f"🎯 Вероятность: `{prob}%`\n\n"
            f"📋 Анализ:\n_{reason}_"
        )

        kb = [[
            InlineKeyboardButton("✅ ПЛЮС", callback_data="res_plus"),
            InlineKeyboardButton("❌ МИНУС", callback_data="res_minus")
        ]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif q.data == "top":
        top = sorted(trader_stats.items(), key=lambda x: x[1]["plus"], reverse=True)[:10]
        text = "🏆 **ТОП ТРЕЙДЕРОВ**\n\n"
        for i, (uid, d) in enumerate(top, 1):
            text += f"{i}. {d['name']} | ✅ {d['plus']} | ❌ {d['minus']}\n"
        await safe_edit(q, text, None, "Markdown")

    elif q.data == "marathon":
        await safe_edit(q, "💰 Введи стартовый баланс ($):")
        context.user_data["wait_balance"] = True

    elif q.data.startswith("res_"):
        if uid not in trader_stats:
            trader_stats[uid] = {"name": q.from_user.first_name, "plus": 0, "minus": 0}
        if q.data == "res_plus":
            trader_stats[uid]["plus"] += 1
        else:
            trader_stats[uid]["minus"] += 1

        save_db(DB_STATS, trader_stats)
        await safe_edit(q, "♻️ Результат сохранён")

# ---------------- MARATHON INPUT ----------------
async def message_handler(update: Update, context):
    if context.user_data.get("wait_balance"):
        try:
            bal = float(update.message.text.replace(",", "."))
            context.user_data["wait_balance"] = False

            text = f"🏃 **МАРАФОН НА 30 ДНЕЙ | Старт ${bal}**\n\n"
            curr = bal
            for d in range(1, 31):
                profit = round(curr * 0.15, 2)
                curr = round(curr + profit, 2)
                text += f"День {d}: ${curr} (+15%)\n"

            text += f"\n🏆 **ИТОГ: ${curr}**"
            await update.message.reply_text(text, parse_mode="Markdown")
        except:
            await update.message.reply_text("❌ Введи число!")

# ---------------- PAGINATION ----------------
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

# ---------------- ADMIN ----------------
async def admin_commands(update: Update, context):
    uid = str(update.effective_user.id)
    if not is_admin(uid):
        return

    parts = update.message.text.split()
    cmd = parts[0]

    if cmd == "/grant" and len(parts) > 1:
        tid = parts[1]
        vip_users.add(tid)
        save_db(DB_VIP, list(vip_users))
        log_admin("GRANT", tid, uid)
        await update.message.reply_text(f"✅ Доступ выдан: {tid}")

    elif cmd == "/revoke" and len(parts) > 1:
        tid = parts[1]
        vip_users.discard(tid)
        save_db(DB_VIP, list(vip_users))
        log_admin("REVOKE", tid, uid)
        await update.message.reply_text(f"❌ Доступ снят: {tid}")

    elif cmd == "/send":
        count = 0
        for user in all_users:
            try:
                if update.message.reply_to_message:
                    await context.bot.copy_message(
                        chat_id=user,
                        from_chat_id=update.message.chat_id,
                        message_id=update.message.reply_to_message.message_id
                    )
                else:
                    msg = update.message.text.replace("/send", "").strip()
                    await context.bot.send_message(chat_id=user, text=msg)
                count += 1
                await asyncio.sleep(0.05)
            except:
                continue
        await update.message.reply_text(f"📢 Отправлено: {count} пользователей")

# ---------------- RUN ----------------
if __name__ == "__main__":
    Thread(target=run_web).start()

    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.Regex(r"^/(grant|revoke|send)"), admin_commands))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))

    print("🚀 KURUT AI INFINITY | COIP PRO ONLINE")
    app.run_polling()
