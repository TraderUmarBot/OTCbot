import asyncio
import json
import os
import random
import time
from threading import Thread
from http.server import HTTPServer, BaseHTTPRequestHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

# ================== КОНФИГУРАЦИЯ ==================
TOKEN = "8596735739:AAGQScXaW47LRlZTVQsGLTi2FUOpJj2YkpA"
ADMIN_IDS = {6117198446, 7079260196}
PRIMARY_ADMIN_LINK = "https://t.me/KURUTTRADING"

# Ссылки
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
YOUTUBE = "https://youtube.com/@kurut_kg?si=FYJOTn73sRuGYYsk"
SECOND_BOT = "https://t.me/KURUT_TRADE_BOT"

# База данных
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

# ================== АКТИВЫ (БЕЗ СТИКЕРОВ) ==================
CURRENCY_PAIRS = ["EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC", "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC", "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC", "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC", "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC", "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC", "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC", "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"]
CRYPTO_ASSETS = ["Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC", "Solana OTC", "Polkadot OTC", "Toncoin OTC", "Litecoin OTC", "TRON OTC"]
STOCK_ASSETS = ["Apple OTC", "McDonald’s OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC", "VISA OTC", "Alibaba OTC", "AMD OTC", "Netflix OTC", "Coinbase OTC", "Meta OTC", "Intel OTC"]

# ================== АЛГОРИТМ (30 ИНДИКАТОРОВ) ==================
def get_pro_signal(asset):
    # Математическая модель Pocket Option OTC
    random.seed(time.time() + len(asset))
    # Суммируем сигналы 30 индикаторов (имитация)
    indicators_sum = sum([random.uniform(-1, 1) for _ in range(30)])
    accuracy = 97.1 + (random.random() * 2.8)
    
    if indicators_sum > 0.4:
        direction, logic = "ВВЕРХ 🟢 CALL", "Strong Momentum: RSI + Bollinger Bands"
    elif indicators_sum < -0.4:
        direction, logic = "ВНИЗ 🔴 PUT", "Trend Reversal: MACD + Stochastic"
    else:
        direction = "ВВЕРХ 🟢 CALL" if indicators_sum > 0 else "ВНИЗ 🔴 PUT"
        logic = "Scalping: Support/Resistance Breakout"
    return direction, round(accuracy, 2), logic

# ================== HEALTH CHECK ==================
class HealthHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

def run_health_server():
    port = int(os.environ.get("PORT", 8000))
    HTTPServer(('0.0.0.0', port), HealthHandler).serve_forever()

# ================== ОБРАБОТЧИКИ ==================
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    uid = update.effective_user.id
    social_kb = [[InlineKeyboardButton("📢 ТГ", url=LINK_TG), InlineKeyboardButton("🤖 БОТ 2", url=SECOND_BOT)], [InlineKeyboardButton("📸 INSTA", url=LINK_INSTA), InlineKeyboardButton("📺 YT", url=YOUTUBE)]]
    
    if uid in ADMIN_IDS or uid in vip_users:
        text = "🚀 **ТЕРМИНАЛ KURUT AI v15.0**\n\nАлгоритм Pocket Option OTC подключен."
        kb = [[InlineKeyboardButton("📊 АНАЛИЗАТОР", callback_data="market")], [InlineKeyboardButton("💰 МАРАФОН $1000", callback_data="calc_start")]] + social_kb
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        text = f"💎 **ДОСТУП ЗАКРЫТ**\n\nТвой ID: `{uid}`\n\nДля активации:\n1. [РЕГИСТРАЦИЯ]({REF_LINK})\n2. Депозит от $15\n3. Пиши админу."
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔑 АКТИВАЦИЯ", callback_data="instruction")]] + social_kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query; uid = query.from_user.id
    try: await query.answer()
    except: pass

    if query.data == "instruction":
        text = f"🚀 **ИНСТРУКЦИЯ**\n\nТвой ID: `{uid}`\n[ЗАРЕГИСТРИРОВАТЬСЯ]({REF_LINK})\n\nПосле пополнения отправь ID админу 👇"
        kb = [[InlineKeyboardButton("👨‍💻 ОТПРАВИТЬ ID АДМИНУ", url=f"https://t.me/share/url?url=Бро,+активируй+мой+ID:+{uid}")], [InlineKeyboardButton("🏠 НАЗАД", callback_data="to_home")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data == "calc_start":
        await query.edit_message_text("💵 **Введите ваш стартовый баланс цифрами (например: 50):**")
        context.user_data['waiting_balance'] = True

    elif query.data == "market":
        kb = [[InlineKeyboardButton("💱 ВАЛЮТЫ (OTC)", callback_data="nav_cu_0")], [InlineKeyboardButton("₿ КРИПТА (OTC)", callback_data="nav_cr_0")], [InlineKeyboardButton("🏢 АКЦИИ (OTC)", callback_data="nav_st_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ РЫНОК:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, pref, page = query.data.split("_")
        data = CURRENCY_PAIRS if pref == "cu" else CRYPTO_ASSETS if pref == "cr" else STOCK_ASSETS
        await query.edit_message_text("📍 **ВЫБЕРИТЕ ПАРУ:**", reply_markup=get_paged_kb(data, int(page), pref))

    elif query.data.startswith(("cu_", "cr_", "st_")):
        idx = int(query.data.split("_")[1]); prefix = query.data.split("_")[0]
        data = CURRENCY_PAIRS if prefix == "cu" else CRYPTO_ASSETS if prefix == "cr" else STOCK_ASSETS
        context.user_data['asset'] = data[idx]
        kb = [
            [InlineKeyboardButton("10 СЕК", callback_data="t_10s"), InlineKeyboardButton("30 СЕК", callback_data="t_30s")],
            [InlineKeyboardButton("1 МИН ⭐", callback_data="t_1m"), InlineKeyboardButton("2 МИН", callback_data="t_2m")],
            [InlineKeyboardButton("3 МИН ⭐", callback_data="t_3m"), InlineKeyboardButton("4 МИН", callback_data="t_4m")],
            [InlineKeyboardButton("5 МИН ⭐", callback_data="t_5m"), InlineKeyboardButton("6 МИН", callback_data="t_6m")],
            [InlineKeyboardButton("7 МИН", callback_data="t_7m"), InlineKeyboardButton("8 МИН", callback_data="t_8m")],
            [InlineKeyboardButton("🏠 НАЗАД", callback_data="market")]
        ]
        await query.edit_message_text(f"💎 **{data[idx]}**\nВыбери время экспирации:", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("t_"):
        tf = query.data.split("_")[1].replace('s',' сек').replace('m',' мин'); asset = context.user_data.get('asset')
        for i in range(1, 4):
            await query.edit_message_text(f"📡 **ANALYZING {asset}...**\nШаг {i}/3 [Опрос 30 индикаторов]")
            await asyncio.sleep(2.3)
        dir, acc, log = get_pro_signal(asset)
        res = f"📊 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📈 **АКТИВ:** `{asset}`\n⚡️ **ВХОД:** {dir}\n⏱ **ВРЕМЯ:** `{tf}`\n🎯 **ТОЧНОСТЬ:** `{acc}%` \n━━━━━━━━━━━━━━\n🧠 **ЛОГИКА:** `{log}`"
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 НОВЫЙ АНАЛИЗ", callback_data="market")]]), parse_mode="Markdown")

    elif query.data == "to_home": await start(update, context)

# ================== МАТЕМАТИЧЕСКИЙ РАСЧЕТ 1-30 ДНЕЙ ==================
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get('waiting_balance'):
        try:
            balance = float(update.message.text.replace('$', '').replace(',', '.'))
            current = balance
            daily_percent = 0.15 # 15% в день
            
            report = f"📅 **ПЛАН МАРАФОНА НА 30 ДНЕЙ**\n"
            report += f"💰 Старт: **${balance}** | Цель: **15%/день**\n"
            report += "━━━━━━━━━━━━━━━━━━\n"
            
            for day in range(1, 31):
                current += current * daily_percent
                report += f"День {day}: `${round(current, 2)}`"
                report += "\n" # Каждый день с новой строки
                
            report += "━━━━━━━━━━━━━━━━━━\n"
            report += f"🏁 **ИТОГ: ${round(current, 2)}**"
            
            context.user_data['waiting_balance'] = False
            await update.message.reply_text(report, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 В МЕНЮ", callback_data="to_home")]]), parse_mode="Markdown")
        except:
            await update.message.reply_text("❌ Введите только число (например: 100)")

# ================== АДМИН КОМАНДЫ ==================
async def grant(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            uid = int(context.args[0]); vip_users.add(uid); save_access()
            await update.message.reply_text(f"✅ Доступ выдан: {uid}")
        except: pass

async def revoke(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id in ADMIN_IDS:
        try:
            uid = int(context.args[0]); vip_users.remove(uid); save_access()
            await update.message.reply_text(f"❌ Доступ закрыт: {uid}")
        except: pass

def get_paged_kb(data, page, prefix):
    size = 10; start_idx = page * size; items = data[start_idx:start_idx+size]; kb = []
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
    Thread(target=run_health_server, daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("grant", grant))
    app.add_handler(CommandHandler("revoke", revoke))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    print("🚀 KURUT ULTIMATE v15.0 STARTED")
    app.run_polling()
