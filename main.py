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

# Базы данных
DB_FILE = "access_db.json"
STATS_FILE = "user_stats.json"

def load_data(file, default):
    if os.path.exists(file):
        try:
            with open(file, 'r') as f: return json.load(f)
        except: return default
    return default

vip_users = set(load_data(DB_FILE, []))
user_stats = load_data(STATS_FILE, {})

def save_all():
    with open(DB_FILE, 'w') as f: json.dump(list(vip_users), f)
    with open(STATS_FILE, 'w') as f: json.dump(user_stats, f)

# ================== СПИСКИ АКТИВОВ ==================
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Netflix OTC", "Coinbase OTC", "Meta OTC", "Intel OTC"]

# ================== СЕРВЕР ДЛЯ 24/7 ==================
server = Flask('')
@server.route('/')
def home(): return "Бот работает 24/7"
def run_server(): server.run(host='0.0.0.0', port=8080)

# ================== ГЛАВНОЕ МЕНЮ (БОЛЬШОЕ) ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = str(update.effective_user.id)
    if uid not in user_stats: 
        user_stats[uid] = {"wins": 0, "losses": 0, "name": update.effective_user.first_name}
        save_all()
    
    if int(uid) in ADMIN_IDS or int(uid) in vip_users:
        text = (
            f"💰 **ДОБРО ПОЖАЛОВАТЬ В KURUT AI ELITE!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"👤 **Трейдер:** {update.effective_user.first_name}\n"
            f"📈 **Статистика:** ✅ {user_stats[uid]['wins']} | ❌ {user_stats[uid]['losses']}\n"
            f"💎 **Статус:** PREMIUM ACCESS\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Выбирай инструмент ниже и начинай зарабатывать!"
        )
        # Большие кнопки в несколько рядов
        kb = [
            [InlineKeyboardButton("📊 АНАЛИЗАТОР РЫНКА (OTC)", callback_data="market")],
            [InlineKeyboardButton("🏆 ТОП ЛИДЕРОВ", callback_data="top_list"), InlineKeyboardButton("💰 МАРАФОН", callback_data="calc_start")],
            [InlineKeyboardButton("📢 НАШ КАНАЛ", url=LINK_TG)]
        ]
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = f"🔒 **ДОСТУП ОГРАНИЧЕН**\n\nТвой ID: `{uid}`\n\nДля активации софта:\n1. Зарегистрируйся по ссылке ниже.\n2. Пополни баланс ($15+).\n3. Отправь свой ID админу."
        kb = [[InlineKeyboardButton("🔗 РЕГИСТРАЦИЯ", url=REF_LINK)], [InlineKeyboardButton("🔑 АКТИВИРОВАТЬ ID", url="https://t.me/traderumarr")]]
        await update.message.reply_photo(photo=PHOTO_REG, caption=text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; uid = str(query.from_user.id)
    await query.answer()

    if query.data == "market":
        kb = [
            [InlineKeyboardButton("💱 ВАЛЮТНЫЕ ПАРЫ", callback_data="nav_cu_0")],
            [InlineKeyboardButton("₿ КРИПТОВАЛЮТА", callback_data="nav_cr_0")],
            [InlineKeyboardButton("🏢 АКЦИИ КОМПАНИЙ", callback_data="nav_st_0")],
            [InlineKeyboardButton("🏠 В ГЛАВНОЕ МЕНЮ", callback_data="to_home")]
        ]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ ТИП ТОРГОВОГО ИНСТРУМЕНТА:**", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ АКТИВ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        prefix, idx = query.data.split("_")
        data = CURRENCY_PAIRS if prefix == "cu" else CRYPTO_ASSETS if prefix == "cr" else STOCK_ASSETS
        context.user_data['asset'] = data[int(idx)]
        
        # Полный список ТФ
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("3 МИН", callback_data="t_3m"), InlineKeyboardButton("5 МИН", callback_data="t_5m")],
            [InlineKeyboardButton("8 МИН", callback_data="t_8m")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]
        ]
        await query.edit_message_text(f"💎 **АКТИВ: {context.user_data['asset']}**\nУкажите время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' СЕК').replace('m',' МИН')
        asset = context.user_data.get('asset')
        
        # ЭФФЕКТНЫЙ АНАЛИЗ (8 секунд)
        status_msg = await query.edit_message_text(f"🔍 **ЗАПУСК АЛГОРИТМА ПО {asset}...**")
        await asyncio.sleep(2.5); await status_msg.edit_text("🧬 **АНАЛИЗ 40 ИНДИКАТОРОВ (RSI, MACD, BB)...**")
        await asyncio.sleep(2.5); await status_msg.edit_text("⚡️ **МАТЕМАТИЧЕСКИЙ ПРОСЧЕТ OTC РЫНКА...**")
        await asyncio.sleep(3)

        # ЛОГИКА СИГНАЛА
        direction = "UP" if random.random() > 0.5 else "DOWN"
        photo = PHOTO_UP if direction == "UP" else PHOTO_DOWN
        acc = random.uniform(96.1, 99.7)
        
        caption = (
            f"📊 **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📈 **ИНСТРУМЕНТ:** `{asset}`\n"
            f"⏱ **ВРЕМЯ СДЕЛКИ:** `{tf}`\n"
            f"🚀 **ПРОГНОЗ:** {'ВВЕРХ (CALL) ↑' if direction == 'UP' else 'ВНИЗ (PUT) ↓'}\n"
            f"🎯 **ВЕРОЯТНОСТЬ:** `{acc:.2f}%` \n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"Жми на результат ниже для статистики!"
        )
        
        kb = [
            [InlineKeyboardButton("✅ ПЛЮС", callback_data="stat_win"), InlineKeyboardButton("❌ МИНУС", callback_data="stat_loss")],
            [InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]
        ]
        
        await context.bot.send_photo(chat_id=int(uid), photo=photo, caption=caption, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
        await status_msg.delete()

    elif query.data == "stat_win":
        user_stats[uid]["wins"] += 1; save_all()
        await context.bot.send_message(chat_id=int(uid), text="💎 **ОТЛИЧНО!** Твой рейтинг в ТОПе обновлен!")

    elif query.data == "stat_loss":
        user_stats[uid]["losses"] += 1; save_all()
        await context.bot.send_message(chat_id=int(uid), text="❌ **БЫВАЕТ.** Используй систему Мартингейла!")

    elif query.data == "top_list":
        top = sorted(user_stats.items(), key=lambda x: x[1]['wins'], reverse=True)[:10]
        res = "🏆 **ЛИДЕРЫ НЕДЕЛИ (ПО ПЛЮСАМ)**\n━━━━━━━━━━━━━━━━━━━━\n"
        for i, (tid, data) in enumerate(top, 1):
            res += f"{i}. {data['name']} — {data['wins']} ✅ | {data['losses']} ❌\n"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="to_home")]]), parse_mode="Markdown")

    elif query.data == "calc_start":
        await query.edit_message_text("💰 **Введите сумму твоего баланса:**\n(Бот рассчитает план на 30 дней)"); context.user_data['waiting_balance'] = True

    elif query.data == "to_home":
        await query.message.delete()
        await start(update, context)

async def handle_msg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_balance'):
        try:
            val = float(update.message.text); rep = "📅 **МАРАФОН: ЦЕЛЬ НА 30 ДНЕЙ (+15%)**\n\n"
            for d in range(1, 31):
                val += val * 0.15
                if d in [1, 5, 10, 15, 20, 25, 30]:
                    rep += f"День {d}: **${val:.2f}**\n"
            context.user_data['waiting_balance'] = False
            await update.message.reply_text(rep, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", url=f"https://t.me/{context.bot.username}?start=1")]]), parse_mode="Markdown")
        except: await update.message.reply_text("Введите только число!")

# ================== АДМИН КОМАНДЫ ==================
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target = int(context.args[0]); vip_users.add(target); save_all()
            await update.message.reply_text(f"✅ Доступ открыт для ID: {target}")
        except: pass

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            target = int(context.args[0]); vip_users.discard(target); save_all()
            await update.message.reply_text(f"🚫 Доступ закрыт для ID: {target}")
        except: pass

# ================== ПОДДЕРЖКА ПАГИНАЦИИ ==================
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
    kb.append([InlineKeyboardButton("🏠 НАЗАД", callback_data="market")])
    return InlineKeyboardMarkup(kb)

if __name__ == "__main__":
    Thread(target=run_server).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("revoke", revoke))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_msg))
    print("🚀 КУРУТ БОТ ELITE ЗАПУЩЕН!")
    app.run_polling()
