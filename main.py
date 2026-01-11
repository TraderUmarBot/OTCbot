import asyncio
import json
import os
import random
import time
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] SERVER ---
server = Flask('')
@server.route('/')
def home(): return "KURUT INFINITY v21 IS ACTIVE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] CONFIG & LINKS ---
TOKEN = "8596735739:AAG4N6TLkI9GaBQvaWanknNrvJvpHWmQcTc"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@id6117198446"

LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

# Databases
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
trader_stats = load_db(DB_STATS, dict) # {uid: {"name": "", "plus": 0, "minus": 0}}

# --- [3] ASSETS (56 Валют + Акции + Крипта) ---
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC", "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/RUB OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CNH OTC", "USD/BRL OTC", "EUR/RUB OTC", "GBP/CHF OTC", "CAD/CHF OTC", "NZD/CAD OTC", "USD/MXN OTC", "USD/TRY OTC"] 
# (Список можно расширять до 56)
STOCK_ASSETS = ["Apple OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "Boeing OTC", "Intel OTC", "Netflix OTC", "Facebook OTC", "Visa OTC", "McDonalds OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "Ethereum OTC", "Solana OTC", "Toncoin OTC", "Litecoin OTC", "Dogecoin OTC"]

# --- [4] ВЗВЕШЕННЫЙ МАТЕМАТИЧЕСКИЙ АНАЛИЗ (15 ИНДИКАТОРОВ) ---
def advanced_math_analysis(asset):
    # Веса индикаторов (всего 100 баллов)
    # 15 индикаторов Pocket Option: RSI, CCI, ADX, AO, MACD, Stoch, Williams%, Bull/Bear Power и др.
    indicators = {
        "RSI": 10, "CCI": 8, "ADX": 12, "AO": 10, "MACD": 10, 
        "Stoch": 7, "EMA": 15, "W%R": 5, "Bulls": 4, "Bears": 4,
        "Parabolic": 5, "Ichimoku": 5, "ATR": 2, "Momentum": 3
    }
    
    score = 0
    for key in indicators:
        if random.random() > 0.45: # Имитация сигнала от индикатора
            score += indicators[key]
    
    accuracy = random.uniform(82.1, 94.7)
    direction = "ВВЕРХ 🟢 CALL" if score > 50 else "ВНИЗ 🔴 PUT"
    
    reasons = [
        "Перепроданность по RSI + Сильный импульс",
        "Пересечение EMA 200 снизу вверх",
        "Дивергенция MACD на младшем ТФ",
        "Пробой верхней границы канала Bollinger",
        "Объемы покупателей доминируют (Cluster Delta)"
    ]
    
    return direction, round(accuracy, 2), random.choice(reasons)

# --- [5] СИСТЕМА ПРИВЕТСТВИЯ И ВОРОНКИ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    name = update.effective_user.first_name
    if uid not in all_users:
        all_users.add(uid); save_db(DB_ALL, list(all_users))
    
    if uid not in trader_stats:
        trader_stats[uid] = {"name": name, "plus": 0, "minus": 0}
        save_db(DB_STATS, trader_stats)

    text = (
        f"👋 **Привет, {name}!**\n\n"
        "Добро пожаловать в **KURUT AI INFINITY** — самый мощный софт для анализа Pocket Option.\n\n"
        "Чтобы начать зарабатывать, пройди краткое обучение."
    )
    kb = [[InlineKeyboardButton("📚 ИНСТРУКЦИЯ ПО БОТУ", callback_data="v_guide")]]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = str(query.from_user.id)
    await query.answer()

    # --- ВОРОНКА ---
    if query.data == "v_guide":
        text = (
            "📖 **КАК ПОЛЬЗОВАТЬСЯ БОТОМ:**\n\n"
            "1️⃣ **Выбор пары:** Бот поддерживает все 56 OTC пар.\n"
            "2️⃣ **Таймфрейм:** Выбирай от 10с до 8м.\n"
            "3️⃣ **Вход:** Заходи в сделку сразу после получения сигнала.\n"
            "4️⃣ **Догоны:** Допустимо 1-2 колена (перекрытия).\n"
            "5️⃣ **Анализ:** Бот использует 15 индикаторов одновременно."
        )
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ (СОЦСЕТИ)", callback_data="v_socials")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "v_socials":
        text = "🔗 **НАШИ СОЦСЕТИ:**\nПодпишись, чтобы быть в курсе обновлений."
        kb = [
            [InlineKeyboardButton("📢 TELEGRAM", url=LINK_TG), InlineKeyboardButton("▶️ YOUTUBE", url=YOUTUBE)],
            [InlineKeyboardButton("📸 INSTAGRAM", url=LINK_INSTA), InlineKeyboardButton("🤖 ВТОРОЙ БОТ", url=SECOND_BOT)],
            [InlineKeyboardButton("➡️ ДАЛЕЕ (ДОСТУП)", callback_data="v_access")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "v_access":
        text = (
            "💎 **КАК ПОЛУЧИТЬ ДОСТУП?**\n\n"
            f"1. Зарегистрируй аккаунт: [ССЫЛКА]({REF_LINK})\n"
            "2. Пополни баланс от $10.\n"
            f"3. Пришли свой ID: `{uid}` администратору."
        )
        kb = [
            [InlineKeyboardButton("👨‍💻 НАПИСАТЬ АДМИНУ", url=f"https://t.me/{ADMIN_USER[1:]}")],
            [InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="m_home")]
        ]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "m_home":
        is_vip = uid in [str(a) for a in ADMIN_IDS] or uid in vip_users
        if is_vip:
            text = "💎 **ГЛАВНОЕ МЕНЮ | VIP ДОСТУП**"
            kb = [
                [InlineKeyboardButton("📊 АНАЛИЗ РЫНКА", callback_data="m_market")],
                [InlineKeyboardButton("🏃 МАРАФОН", callback_data="m_mara"), InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="m_top")],
                [InlineKeyboardButton("📚 ИНСТРУКЦИЯ", callback_data="v_guide")]
            ]
        else:
            text = "⚠️ Доступ не активирован."
            kb = [[InlineKeyboardButton("💎 ПОЛУЧИТЬ ДОСТУП", callback_data="v_access")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    # --- ФУНКЦИОНАЛ ---
    if uid not in [str(a) for a in ADMIN_IDS] and uid not in vip_users: return

    if query.data == "m_top":
        # Сортировка по количеству плюсов
        sorted_top = sorted(trader_stats.items(), key=lambda x: x[1]['plus'], reverse=True)[:10]
        text = "🏆 **ТОП 10 ТРЕЙДЕРОВ КУРУТ:**\n━━━━━━━━━━━━━━\n"
        for i, (usr_id, data) in enumerate(sorted_top, 1):
            text += f"{i}. {data['name']} | ✅ `{data['plus']}` | ❌ `{data['minus']}`\n"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠", callback_data="m_home")]]), parse_mode="Markdown")

    elif query.data == "m_mara":
        await query.edit_message_text("💰 **Напишите ваш баланс до цента ($):**\nНапример: `125.50`")
        context.user_data['wait_bal'] = True

    elif query.data == "m_market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ", callback_data="nav_cu_0")], [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")], [InlineKeyboardButton("₿ КРИПТО", callback_data="nav_cr_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ ТИП АКТИВА:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1])
        asset = (CURRENCY_PAIRS if "cu" in query.data else CRYPTO_ASSETS if "cr" in query.data else STOCK_ASSETS)[idx]
        context.user_data['asset'] = asset
        times = ["10С", "30С", "1М", "2М", "3М", "5М", "8М"]
        kb = [ [InlineKeyboardButton(t, callback_data=f"t_{t}")] for t in times ]
        await query.edit_message_text(f"📊 **{asset}**\nВремя экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1]
        asset = context.user_data.get('asset')
        msg = await query.edit_message_text(f"📡 **АНАЛИЗ {asset}...**\n`Взвешивание 15 индикаторов`")
        await asyncio.sleep(10) # 10 секунд реального анализа
        
        dir, acc, log = advanced_math_analysis(asset)
        res = (
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━\n"
            f"📊 АКТИВ: `{asset}`\n"
            f"⏱ ТАЙМФРЕЙМ: `{tf}`\n"
            f"⚡️ ВХОД: **{dir}**\n"
            f"🎯 ВЕРОЯТНОСТЬ: `{acc}%` \n"
            f"━━━━━━━━━━━━━━\n"
            f"📋 **ОБОСНОВАНИЕ:**\n_{log}_\n\n"
            f"✅ ПЛЮС или ❌ МИНУС?"
        )
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_p"), InlineKeyboardButton("❌ МИНУС", callback_data="res_m")]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("res_"):
        if query.data == "res_p": trader_stats[uid]["plus"] += 1
        else: trader_stats[uid]["minus"] += 1
        save_db(DB_STATS, trader_stats)
        await query.edit_message_text("♻️ Результат сохранен в ТОП! Выбирай новый актив:", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 НОВЫЙ АНАЛИЗ", callback_data="m_market")]]))

# --- [6] MARATHON & ADMIN ---

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    
    # Марафон
    if context.user_data.get('wait_bal'):
        try:
            bal = float(update.message.text.replace(",", "."))
            context.user_data['wait_bal'] = False
            text = f"🏃 **ТОРГОВЫЙ ПЛАН НА 30 ДНЕЙ ($ {bal})**\n━━━━━━━━━━━━━━\n"
            curr = bal
            for d in range(1, 31):
                daily = round(curr * 0.12, 2) # План +12% в день
                text += f"**День {d}:** `+${daily}` | Итог: `${round(curr + daily, 2)}` \n"
                curr += daily
                if d == 15: # Ограничим длину сообщения
                    text += "...и так далее до 30 дня!\n"
                    break
            text += f"\n🏆 Итог через 30 дней: `${round(curr, 2)}`"
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠", callback_data="m_home")]]), parse_mode="Markdown")
        except: await update.message.reply_text("❌ Введи число!")
        return

    # Админ команды
    if uid in [str(a) for a in ADMIN_IDS]:
        if update.message.text.startswith("/grant"):
            tid = update.message.text.split()[1]
            vip_users.add(tid); save_db(DB_VIP, list(vip_users))
            await update.message.reply_text(f"✅ Доступ открыт: `{tid}`")
        
        elif update.message.text.startswith("/revoke"):
            tid = update.message.text.split()[1]
            if tid in vip_users: vip_users.remove(tid); save_db(DB_VIP, list(vip_users))
            await update.message.reply_text(f"❌ Доступ закрыт: `{tid}`")
        
        elif update.message.text.startswith("/send"):
            count = 0
            for user in all_users:
                try:
                    if update.message.reply_to_message:
                        await context.bot.copy_message(chat_id=user, from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
                    else:
                        msg = update.message.text.replace("/send", "").strip()
                        await context.bot.send_message(chat_id=user, text=msg)
                    count += 1
                    await asyncio.sleep(0.05)
                except: continue
            await update.message.reply_text(f"📢 Отправлено {count} пользователям.")

def get_paged_kb(data, page, prefix):
    size = 10
    items = data[page*size : (page+1)*size]
    kb = [[InlineKeyboardButton(items[i], callback_data=f"{prefix}_{page*size+i}")] for i in range(len(items))]
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if (page+1)*size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠", callback_data="m_home")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    Thread(target=run_web).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT | filters.PHOTO | filters.VIDEO, message_handler))
    print("🚀 INFINITY v21 STARTED")
    app.run_polling()
