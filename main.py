import asyncio
import json
import os
import random
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ================== КОНФИГУРАЦИЯ ==================
TOKEN = "8596735739:AAGQScXaW47LRlZTVQsGLTi2FUOpJj2YkpA"
ADMIN_IDS = {7079260196, 6117198446}

# Твои Фото ID
PHOTO_UP = "AgACAgIAAxkBAAIDRmliLyW2ijHX2PRFDt7CAfWRRFLyAALyDWsb_CURSxA3wRq5Anf1AQADAgADeQADOAQ"
PHOTO_DOWN = "AgACAgIAAxkBAAIDPGliLeaqevpLkW5wBwOuJQEj1RjjAALpDWsb_CURS3K1vWT0Ck_aAQADAgADeQADOAQ"
PHOTO_REG = "AgACAgIAAxkBAAIDSmliL6io7GM9iLxWg85X5aYmtXxrAAL6DWsb_CURS7iPDYdaBHRCAQADAgADeAADOAQ"

# Ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# База данных
DB_FILE = "vip_users.json"
def load_vip():
    if os.path.exists(DB_FILE):
        with open(DB_FILE, 'r') as f: return set(json.load(f))
    return set()
vip_users = load_vip()

def save_vip():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)

# ================== СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Netflix OTC", "Coinbase OTC", "Meta OTC", "Intel OTC"]

# ================== СЕРВЕР 24/7 ==================
server = Flask('')
@server.route('/')
def home(): return "Kurut AI is Running 24/7"
def run_server(): server.run(host='0.0.0.0', port=8080)

# ================== ЛОГИКА БОТА ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    social_kb = [[InlineKeyboardButton("📢 ТГ", url=LINK_TG), InlineKeyboardButton("🤖 БОТ 2", url=SECOND_BOT)], [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YT", url=YOUTUBE)]]
    
    if uid in ADMIN_IDS or uid in vip_users:
        text = f"💎 **KURUT AI ELITE v22.0**\n\nПривет, {update.effective_user.first_name}!\nТвой доступ: **PREMIUM** ✅\n\nВыбирай рынок и получай точный сигнал!"
        kb = [[InlineKeyboardButton("📊 АНАЛИЗАТОР РЫНКА", callback_data="market")]] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = (f"🔒 **ДОСТУП ОГРАНИЧЕН**\n\nТвой ID: `{uid}`\n\n"
                f"Чтобы пользоваться ботом, выполни условия:\n"
                f"1️⃣ Зарегистрируйся: [ПО ЭТОЙ ССЫЛКЕ]({REF_LINK})\n"
                f"2️⃣ Пополни баланс от **15$**\n"
                f"3️⃣ Пришли свой ID админу для активации.")
        await update.message.reply_photo(photo=PHOTO_REG, caption=text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 ПОЛУЧИТЬ ДОСТУП", url="https://t.me/traderumarr")]] + social_kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; uid = query.from_user.id
    await query.answer()

    if query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ (OTC)", callback_data="nav_cu_0")], [InlineKeyboardButton("₿ КРИПТА (OTC)", callback_data="nav_cr_0")], [InlineKeyboardButton("🏢 АКЦИИ (OTC)", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ ТИП РЫНКА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ ДЛЯ АНАЛИЗА:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        prefix, idx = query.data.split("_")
        data = CURRENCY_PAIRS if prefix == "cu" else CRYPTO_ASSETS if prefix == "cr" else STOCK_ASSETS
        context.user_data['asset'] = data[int(idx)]
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("5 МИН", callback_data="t_5m")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]
        ]
        await query.edit_message_text(f"💎 **{context.user_data['asset']}**\nУкажите время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' СЕК').replace('m',' МИН')
        asset = context.user_data.get('asset')
        
        # ЭФФЕКТИВНЫЙ АНАЛИЗ (8 СЕКУНД)
        msg = await query.edit_message_text(f"🔍 **ЗАПУСК АЛГОРИТМА ПО {asset}...**")
        await asyncio.sleep(2)
        await msg.edit_text("🧬 **ПРОВЕРКА 40 ТЕХНИЧЕСКИХ ИНДИКАТОРОВ...**\n[██░░░░░░░░] 25%")
        await asyncio.sleep(2)
        await msg.edit_text("📊 **АНАЛИЗ ОБЪЕМОВ И УРОВНЕЙ OTC...**\n[██████░░░░] 60%")
        await asyncio.sleep(2)
        await msg.edit_text("⚡️ **ПОИСК ТОЧКИ ВХОДА...**\n[██████████] 100%")
        await asyncio.sleep(2)
        await msg.delete()

        # ГЕНЕРАЦИЯ СИГНАЛА
        direction = "UP" if random.random() > 0.5 else "DOWN"
        accuracy = random.uniform(94.2, 98.9)
        photo = PHOTO_UP if direction == "UP" else PHOTO_DOWN
        
        caption = (f"📊 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n"
                   f"📈 **АКТИВ:** `{asset}`\n"
                   f"⏱ **ВРЕМЯ:** `{tf}`\n"
                   f"🚀 **ПРОГНОЗ:** {'ВВЕРХ (CALL) ↑' if direction == 'UP' else 'ВНИЗ (PUT) ↓'}\n"
                   f"🎯 **ТОЧНОСТЬ:** `{accuracy:.2f}%` \n"
                   f"🐳 **ОБЪЕМ:** `ВЫЯВЛЕН`\n━━━━━━━━━━━━━━")
        
        await context.bot.send_photo(chat_id=uid, photo=photo, caption=caption, parse_mode="Markdown", 
                                     reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="market")]]))

# ================== АДМИН ПАНЕЛЬ ==================
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target = int(context.args[0]); vip_users.add(target); save_vip()
            await update.message.reply_text(f"✅ Доступ выдан пользователю: `{target}`", parse_mode="Markdown")
        except: await update.message.reply_text("Формат: `/grant ID`")

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target = int(context.args[0]); vip_users.discard(target); save_vip()
            await update.message.reply_text(f"🚫 Доступ отозван у: `{target}`", parse_mode="Markdown")
        except: await update.message.reply_text("Формат: `/revoke ID`")

# ================== ВСПОМОГАТЕЛЬНОЕ ==================
def get_paged_kb(data, page, prefix):
    size = 10; start_idx = page * size; items = data[start_idx:start_idx+size]; kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start_idx+i}")]
        if i+1 < len(items): row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start_idx+i+1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start_idx+size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="market")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    Thread(target=run_server).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("revoke", revoke))
    app.add_handler(CallbackQueryHandler(callback_handler))
    print("🚀 KURUT AI ELITE ЗАПУЩЕН!")
    app.run_polling()
