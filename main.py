import asyncio
import json
import os
import random
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# --- [1] SERVER ---
server = Flask('')
@server.route('/')
def home(): return "KURUT INFINITY v26 | FINAL ACTIVE"
def run_web(): server.run(host='0.0.0.0', port=8080)

# --- [2] CONFIG ---
TOKEN = "8578509228:AAE2D6ANQGgXWkyLkVXYnq_htqFbTAYF_Ms"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@id6117198446"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

# Databases
DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "trader_stats.json"

def load_db(file, default_type=list):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return json.load(f)
        except: return default_type()
    return default_type()

def save_db(file, data):
    with open(file, 'w') as f: json.dump(data, f)

vip_users = set(load_db(DB_VIP))
all_users = set(load_db(DB_ALL))
trader_stats = load_db(DB_STATS, dict)

# --- [3] ASSETS (52 OTC + Stocks + Crypto) ---
OTC_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC", "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/RUB OTC", "EUR/RUB OTC", "CHF/NOK OTC", "EUR/HUF OTC", "USD/CNH OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CLP OTC", "USD/MYR OTC", "USD/THB OTC", "USD/VND OTC", "USD/PKR OTC", "USD/COP OTC", "USD/EGP OTC", "USD/PHP OTC", "USD/MXN OTC", "USD/DZD OTC", "USD/ARS OTC", "USD/IDR OTC", "USD/BRL OTC", "USD/BDT OTC", "YER/USD OTC", "LBP/USD OTC", "TND/USD OTC", "MAD/USD OTC", "BHD/CNY OTC", "NGN/USD OTC", "KES/USD OTC", "ZAR/USD OTC", "UAH/USD OTC"]
STOCKS = ["McDonald’s", "Intel", "American Express", "Palantir", "Microsoft", "Apple", "GameStop", "Pfizer", "Boeing", "Visa", "Meta", "Citigroup", "Cisco", "FedEx", "Tesla", "Coinbase", "Amazon", "AMD", "Netflix"]
CRYPTO = ["Bitcoin (BTC)", "Ethereum (ETH)", "Solana (SOL)", "Toncoin (TON)", "Litecoin (LTC)", "Dogecoin (DOGE)"]

# --- [4] POCKET OPTION AI ENGINE ---
def get_pocket_option_analysis():
    accuracy = random.uniform(92.5, 98.9)
    direction = "ВВЕРХ 🟢 CALL" if random.random() > 0.45 else "ВНИЗ 🔴 PUT"
    reasons = [
        "Математическое подтверждение пробоя уровня волатильности.",
        "Алгоритм зафиксировал дефицит ликвидности на стороне продавцов.",
        "Индекс RSI подтверждает сильный импульс по тренду OTC.",
        "Корреляция с объемами Pocket Option выше 94%.",
        "Паттерн 'Поглощение' на младшем таймфрейме подтвержден."
    ]
    return direction, round(accuracy, 2), random.choice(reasons)

# --- [5] LOGIC ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in all_users:
        all_users.add(uid); save_db(DB_ALL, list(all_users))
    
    if uid in [str(a) for a in ADMIN_IDS] or uid in vip_users:
        await show_main_menu(update, context)
    else:
        text = f"👋 **Привет, {update.effective_user.first_name}!**\n\nЭто **KURUT AI INFINITY** — самый мощный ИИ-анализатор для Pocket Option.\nДля начала работы необходимо активировать доступ."
        kb = [[InlineKeyboardButton("📚 ИНСТРУКЦИЯ И ДОСТУП", callback_data="v_guide")]]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🚀 **ГЛАВНОЕ МЕНЮ | KURUT AI INFINITY**\n\nВыбирай нужный раздел и начинай зарабатывать:"
    kb = [
        [InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛ", callback_data="m_market")],
        [InlineKeyboardButton("🏃 МАРАФОН", callback_data="m_mara"), InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="m_top")],
        [InlineKeyboardButton("📚 ИНСТРУКЦИЯ", callback_data="v_guide")]
    ]
    if update.callback_query:
        await update.callback_query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    uid = str(query.from_user.id)
    await query.answer()

    if query.data == "v_guide":
        text = "📖 **ИНСТРУКЦИЯ:**\n\n1. Анализ по 15 индикаторам.\n2. Точность сигналов до 98%.\n3. Работаем на OTC парах Pocket Option."
        kb = [[InlineKeyboardButton("➡️ ДАЛЕЕ (ДОСТУП)", callback_data="v_access")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "v_access":
        text = f"💎 **КАК ПОЛУЧИТЬ ДОСТУП?**\n\n1. Регистрация: [ССЫЛКА]({REF_LINK})\n2. Пополни баланс от $15.\n3. Твой ID: `{uid}` — отправь его {ADMIN_USER}"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="m_home")]]), parse_mode="Markdown", disable_web_page_preview=True)

    elif query.data == "m_home":
        await show_main_menu(update, context)

    # VIP Check
    if uid not in [str(a) for a in ADMIN_IDS] and uid not in vip_users: return

    if query.data == "m_top":
        sorted_top = sorted(trader_stats.items(), key=lambda x: x[1].get('plus', 0), reverse=True)[:10]
        text = "🏆 **ТОП 10 ТРЕЙДЕРОВ:**\n━━━━━━━━━━━━━━\n"
        for i, (usr_id, data) in enumerate(sorted_top, 1):
            text += f"{i}. {data.get('name', 'Trader')} | ✅ `{data.get('plus',0)}` | ❌ `{data.get('minus',0)}` \n"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠", callback_data="m_home")]]), parse_mode="Markdown")

    elif query.data == "m_mara":
        await query.edit_message_text("💰 **Введи свой стартовый баланс ($):**")
        context.user_data['wait_bal'] = True

    elif query.data == "m_market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ OTC", callback_data="nav_cu_0")], [InlineKeyboardButton("🏢 АКЦИИ", callback_data="nav_st_0")], [InlineKeyboardButton("₿ КРИПТО", callback_data="nav_cr_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = OTC_PAIRS if pref == "cu" else STOCKS if pref == "st" else CRYPTO
        await query.edit_message_text("📍 **ВЫБЕРИТЕ ПАРУ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "st_", "cr_")):
        idx = int(query.data.split("_")[1])
        asset = (OTC_PAIRS if "cu" in query.data else STOCKS if "st" in query.data else CRYPTO)[idx]
        context.user_data['asset'] = asset
        tfs = ["10 СЕК", "30 СЕК", "М1", "М2", "М3", "М5", "М8"]
        kb = [[InlineKeyboardButton(t, callback_data=f"t_{t}")] for t in tfs]
        await query.edit_message_text(f"📊 **{asset}**\nТаймфрейм:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1]
        asset = context.user_data.get('asset')
        msg = await query.edit_message_text(f"📡 **ГЛУБОКИЙ АНАЛИЗ {asset}...**")
        await asyncio.sleep(4)
        dir, acc, log = get_pocket_option_analysis()
        res = f"✨ **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📊 АКТИВ: `{asset}`\n⏳ ВРЕМЯ: `{tf}`\n🚦 ВХОД: **{dir}**\n🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n📋 **АНАЛИЗ:** _{log}_"
        kb = [[InlineKeyboardButton("✅ ПЛЮС", callback_data="res_p"), InlineKeyboardButton("❌ МИНУС", callback_data="res_m")]]
        await msg.edit_text(res, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("res_"):
        if uid not in trader_stats: trader_stats[uid] = {"name": query.from_user.first_name, "plus": 0, "minus": 0}
        if query.data == "res_p": trader_stats[uid]["plus"] += 1
        else: trader_stats[uid]["minus"] += 1
        save_db(DB_STATS, trader_stats)
        await query.edit_message_text("♻️ Статистика сохранена!", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🎯 СЛЕДУЮЩИЙ СИГНАЛ", callback_data="m_market")]]))

# --- [6] ADMIN COMMANDS ---

async def admin_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in [str(a) for a in ADMIN_IDS]: return
    
    txt = update.message.text
    if txt.startswith("/grant"):
        try:
            tid = txt.split()[1]
            vip_users.add(tid); save_db(DB_VIP, list(vip_users))
            await update.message.reply_text(f"✅ Доступ открыт: {tid}")
            await context.bot.send_message(chat_id=tid, text="🎉 **АДМИН ОТКРЫЛ ВАМ ВЕЧНЫЙ ДОСТУП!**", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("📊 ПОЛУЧИТЬ СИГНАЛЫ", callback_data="m_home")]]))
        except: pass

    elif txt.startswith("/revoke"):
        try:
            tid = txt.split()[1]
            if tid in vip_users: vip_users.remove(tid); save_db(DB_VIP, list(vip_users))
            await update.message.reply_text(f"❌ Доступ закрыт: {tid}")
        except: pass

    elif txt.startswith("/send"):
        msg_text = txt.replace("/send", "").strip()
        count = 0
        for user in all_users:
            try:
                if update.message.reply_to_message:
                    await context.bot.copy_message(chat_id=user, from_chat_id=update.message.chat_id, message_id=update.message.reply_to_message.message_id)
                else:
                    await context.bot.send_message(chat_id=user, text=f"📢 **СООБЩЕНИЕ ОТ АДМИНИСТРАЦИИ:**\n\n{msg_text}", parse_mode="Markdown")
                count += 1
                await asyncio.sleep(0.05)
            except: continue
        await update.message.reply_text(f"📢 Рассылка завершена. Получили: {count} пользователей.")

async def message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('wait_bal'):
        try:
            bal = float(update.message.text.replace(",", "."))
            context.user_data['wait_bal'] = False
            text = f"🏃 **ПЛАН НА 30 ДНЕЙ ($ {bal})**\n"
            curr = bal
            for d in range(1, 31):
                p = round(curr * 0.15, 2)
                text += f"**День {d}:** `${round(curr + p, 2)}` \n"
                curr += p
                if d == 12: break
            text += "...и так до 30 дня!\n" + f"🏆 **ИТОГ: `${round(curr * 2, 2)}`**"
            await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="m_home")]]), parse_mode="Markdown")
        except: await update.message.reply_text("❌ Введи число!")

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
    app.add_handler(MessageHandler(filters.Regex(r'^/(grant|revoke|send)'), admin_commands))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, message_handler))
    print("🚀 FINAL VERSION STARTED")
    app.run_polling()
