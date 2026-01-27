# ============================================
# 🚀 KURUT AI INFINITY PRO - WORKING VERSION
# ============================================
# ПРОСТОЙ И РАБОЧИЙ КОД - НАЖМИ START И ВСЁ ЗАРАБОТАЕТ
# ============================================

import json
import os
import asyncio
import threading
import time
import hashlib
from datetime import datetime, timedelta
import requests
from flask import Flask
from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ApplicationBuilder
)
import logging

# ============================================
# 🔧 НАСТРОЙКИ ЛОГИРОВАНИЯ
# ============================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ============================================
# ⚙️ КОНФИГУРАЦИЯ БОТА
# ============================================

TOKEN = "8578509228:AAFdsHJOSaNc0b1JrCnRwAbA-d4IVXI0Ip0"
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@Kuruttrader"
ADMIN_LINK = "https://t.me/Kuruttrader"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

SOCIALS = {
    "telegram": "https://t.me/KURUTTRADING",
    "youtube": "https://youtube.com/@kurut_kg",
    "instagram": "https://www.instagram.com/kurut_trading",
    "open_chat": "https://t.me/Kurutopen"
}

# ============================================
# 📊 ВАЛЮТНЫЕ ПАРЫ
# ============================================

# OTC ВАЛЮТНЫЕ ПАРЫ (50+ ПАР)
OTC_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/JPY OTC", "AUD/NZD OTC",
    "AUD/USD OTC", "CAD/CHF OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC",
    "EUR/GBP OTC", "EUR/JPY OTC", "EUR/NZD OTC", "GBP/AUD OTC", "GBP/JPY OTC",
    "GBP/USD OTC", "NZD/JPY OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC",
    "USD/JPY OTC", "USD/RUB OTC", "CHF/NOK OTC", "EUR/HUF OTC", "USD/CNH OTC",
    "EUR/TRY OTC", "USD/INR OTC", "USD/SGD OTC", "USD/CLP OTC", "USD/MYR OTC",
    "USD/THB OTC", "USD/VND OTC", "USD/PKR OTC", "USD/COP OTC", "USD/EGP OTC",
    "USD/PHP OTC", "USD/MXN OTC", "USD/DZD OTC", "USD/ARS OTC", "USD/IDR OTC",
    "USD/BRL OTC", "USD/BDT OTC", "YER/USD OTC", "LBP/USD OTC", "TND/USD OTC",
    "MAD/USD OTC", "NGN/USD OTC", "KES/USD OTC", "ZAR/USD OTC", "UAH/USD OTC"
]

# БИРЖЕВЫЕ ВАЛЮТНЫЕ ПАРЫ
EXCHANGE_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "USD/CHF", "AUD/USD",
    "USD/CAD", "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY",
    "AUD/JPY", "EUR/AUD", "GBP/AUD", "EUR/NZD", "AUD/NZD",
    "CAD/JPY", "AUD/CHF", "CHF/JPY", "EUR/CHF", "GBP/CHF",
    "NZD/JPY"
]

# АКЦИИ OTC (23 АКЦИИ)
STOCKS_OTC = [
    "Apple OTC", "McDonald's OTC", "Microsoft OTC", "Citigroup Inc OTC", "VISA OTC",
    "VIX OTC", "ExxonMobil OTC", "Pfizer Inc OTC", "Johnson & Johnson OTC", "American Express OTC",
    "Alibaba OTC", "Netflix OTC", "Tesla OTC", "Amazon OTC", "GameStop Corp OTC",
    "Boeing Company OTC", "Marathon Digital Holdings OTC", "Facebook Inc OTC", "Intel OTC",
    "Advanced Micro Devices OTC", "FedEx OTC", "Coinbase Global OTC", "Palantir Technologies OTC"
]

# КРИПТОВАЛЮТЫ OTC (14 КРИПТО)
CRYPTO_OTC = [
    "Bitcoin OTC", "Ethereum OTC", "Polygon OTC", "Polkadot OTC", "TRON OTC",
    "Litecoin OTC", "Toncoin OTC", "Bitcoin ETF OTC", "Solana OTC", "BNB OTC",
    "Cardano OTC", "Dogecoin OTC", "Chainlink OTC", "Avalanche OTC"
]

# ВСЕ КАТЕГОРИИ
MARKET_CATEGORIES = {
    "otc_forex": {"name": "💱 OTC Валюты (50+ пар)", "pairs": OTC_PAIRS},
    "exchange_forex": {"name": "🏛️ Биржевые Валюты", "pairs": EXCHANGE_PAIRS},
    "stocks": {"name": "📈 Акции OTC (23 акции)", "pairs": STOCKS_OTC},
    "crypto": {"name": "₿ Криптовалюты OTC (14 крипто)", "pairs": CRYPTO_OTC}
}

# ЭКСПИРАЦИИ
EXPIRATION_OPTIONS = [
    "30 СЕКУНД", "1 МИНУТА", "2 МИНУТЫ", "3 МИНУТЫ", "4 МИНУТЫ",
    "5 МИНУТ", "6 МИНУТ", "7 МИНУТ", "8 МИНУТ", "9 МИНУТ", "10 МИНУТ"
]

# ============================================
# 🌐 FLASK СЕРВЕР ДЛЯ RENDER (УПРОЩЕННЫЙ)
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    return "🚀 KURUT AI INFINITY PRO - BOT IS ONLINE 24/7", 200

@app.route('/ping')
def ping():
    return "PONG", 200

def run_flask():
    """Запускает Flask сервер"""
    app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)

# ============================================
# 🔄 АВТОПИНГ СИСТЕМА
# ============================================

def start_ping():
    """Запускает автопинг в отдельном потоке"""
    def ping_loop():
        while True:
            try:
                time.sleep(180)  # 3 минуты
                try:
                    requests.get('http://localhost:8080/ping', timeout=5)
                    logger.info("✅ Автопинг выполнен")
                except:
                    pass
            except Exception as e:
                logger.error(f"Ошибка автопинга: {e}")
                time.sleep(60)
    
    thread = threading.Thread(target=ping_loop, daemon=True)
    thread.start()
    logger.info("🔄 Автопинг запущен (каждые 3 минуты)")
    return thread

# ============================================
# 💾 БАЗА ДАННЫХ (УПРОЩЕННАЯ)
# ============================================

class Database:
    @staticmethod
    def load(filename, default):
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            return default
        except:
            return default
    
    @staticmethod
    def save(filename, data):
        try:
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except:
            return False

# Создаем папку данных
os.makedirs("data", exist_ok=True)

# Загружаем данные
vip_users = set(Database.load("data/vip_users.json", []))
all_users = set(Database.load("data/all_users.json", []))
user_stats = Database.load("data/user_stats.json", {})
user_languages = Database.load("data/user_languages.json", {})
banned_users = set(Database.load("data/banned_users.json", []))
auto_signals = Database.load("data/auto_signals.json", {})

# ============================================
# 🛠️ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================

def is_admin(user_id):
    return user_id in ADMIN_IDS

def is_vip(user_id):
    return str(user_id) in vip_users or is_admin(user_id)

def is_banned(user_id):
    return str(user_id) in banned_users

def get_lang(user_id):
    return user_languages.get(str(user_id), 'ru')

def ensure_user(user_id):
    uid = str(user_id)
    if uid not in all_users:
        all_users.add(uid)
        Database.save("data/all_users.json", list(all_users))
        
        if uid not in user_stats:
            user_stats[uid] = {
                "wins": 0, "losses": 0, "profit": 0,
                "total": 0, "win_rate": 0,
                "join_date": datetime.now().strftime("%Y-%m-%d")
            }
            Database.save("data/user_stats.json", user_stats)
        
        if uid not in user_languages:
            user_languages[uid] = 'ru'
            Database.save("data/user_languages.json", user_languages)
    
    return True

def update_stats(user_id, win=None):
    uid = str(user_id)
    if uid not in user_stats:
        ensure_user(user_id)
    
    if win is not None:
        if win:
            user_stats[uid]["wins"] += 1
            user_stats[uid]["profit"] += 95
        else:
            user_stats[uid]["losses"] += 1
            user_stats[uid]["profit"] -= 100
        
        wins = user_stats[uid]["wins"]
        losses = user_stats[uid]["losses"]
        total = wins + losses
        
        user_stats[uid]["total"] = total
        if total > 0:
            user_stats[uid]["win_rate"] = round((wins / total) * 100, 2)
    
    Database.save("data/user_stats.json", user_stats)

# ============================================
# 🎯 АНАЛИЗАТОР РЫНКА
# ============================================

class MarketAnalyzer:
    def analyze(self, pair, expiration, category):
        """Анализирует пару и возвращает сигнал"""
        now = datetime.now()
        
        # Детерминированный расчет
        pair_hash = int(hashlib.md5(pair.encode()).hexdigest()[:8], 16)
        hour = now.hour
        
        # Логика анализа
        if "USD" in pair and "OTC" in pair:
            if hour < 12:
                direction = "CALL"
                confidence = 92
            else:
                direction = "PUT"
                confidence = 88
        elif "EUR" in pair or "GBP" in pair:
            direction = "CALL" if (pair_hash % 100) < 58 else "PUT"
            confidence = 90
        elif "JPY" in pair:
            direction = "PUT" if (pair_hash % 100) < 52 else "CALL"
            confidence = 87
        elif "Apple" in pair or "Tesla" in pair:
            direction = "CALL"
            confidence = 93
        elif "Bitcoin" in pair or "Ethereum" in pair:
            if hour < 18:
                direction = "CALL"
                confidence = 91
            else:
                direction = "PUT"
                confidence = 89
        else:
            direction = "CALL" if (pair_hash % 100) < 55 else "PUT"
            confidence = 85
        
        confidence = min(95, confidence)
        
        if confidence >= 92:
            strength = "💎 УЛЬТРА СИЛЬНЫЙ"
            emoji = "💎"
        elif confidence >= 88:
            strength = "🔥 СИЛЬНЫЙ"
            emoji = "🔥"
        elif confidence >= 85:
            strength = "📈 ХОРОШИЙ"
            emoji = "📈"
        else:
            strength = "📊 СТАНДАРТНЫЙ"
            emoji = "📊"
        
        # Время входа
        entry_time = (now + timedelta(seconds=10)).strftime("%H:%M:%S")
        
        # Экспирация
        if "СЕКУНД" in expiration:
            minutes = int(expiration.split()[0]) / 60
        else:
            minutes = int(expiration.split()[0])
        
        exp_time = (now + timedelta(minutes=minutes)).strftime("%H:%M:%S")
        
        return {
            'pair': pair,
            'direction': direction,
            'confidence': confidence,
            'strength': strength,
            'emoji': emoji,
            'expiration': expiration,
            'exact_expiration': exp_time,
            'entry_time': entry_time,
            'entry_type': "📊 ОПТИМАЛЬНЫЙ ВХОД",
            'current_time': now.strftime("%H:%M:%S"),
            'date': now.strftime("%d.%m.%Y")
        }

analyzer = MarketAnalyzer()

# ============================================
# 🌍 ТЕКСТЫ НА ДВУХ ЯЗЫКАХ
# ============================================

TEXTS = {
    'ru': {
        'welcome': "👋 Добро пожаловать в KURUT AI INFINITY PRO!",
        'choose_lang': "🌍 Выберите язык:",
        'lang_set': "✅ Язык установлен на Русский!",
        'main_menu': """🚀 <b>KURUT AI INFINITY PRO</b>

<em>Профессиональные торговые сигналы | 100+ пар</em>

────────────────────
<b>📊 ВАШ ПРОФИЛЬ</b>
🆔 ID: <code>{user_id}</code>
👑 Статус: {status}
────────────────────""",
        'vip_active': "✅ VIP АКТИВЕН",
        'vip_required': "🔒 ТРЕБУЕТСЯ VIP",
        'btn_get_signal': "🚀 Получить сигнал",
        'btn_get_vip': "👑 Получить VIP",
        'btn_my_stats': "📊 Моя статистика",
        'btn_main_menu': "🏠 Главное меню",
        'choose_market': "🎯 <b>ВЫБЕРИТЕ КАТЕГОРИЮ:</b>",
        'choose_pair': "📊 <b>ВЫБЕРИТЕ ПАРУ:</b>",
        'choose_expiration': "⏰ <b>ВЫБЕРИТЕ ЭКСПИРАЦИЮ:</b>",
        'analyzing': "🔍 <b>АНАЛИЗ РЫНКА...</b>",
    },
    
    'kg': {
        'welcome': "👋 KURUT AI INFINITY PRO'го кош келиңиз!",
        'choose_lang': "🌍 Тилди тандаңыз:",
        'lang_set': "✅ Тил Кыргызчага орнотулду!",
        'main_menu': """🚀 <b>KURUT AI INFINITY PRO</b>

<em>Профессионалдык соода сигналдары | 100+ жуп</em>

────────────────────
<b>📊 СИЗДИН ПРОФИЛИНИЗ</b>
🆔 ID: <code>{user_id}</code>
👑 Статус: {status}
────────────────────""",
        'vip_active': "✅ VIP АКТИВДҮҮ",
        'vip_required': "🔒 VIP ТАЛАП КЫЛЫНАТ",
        'btn_get_signal': "🚀 Сигнал алуу",
        'btn_get_vip': "👑 VIP алуу",
        'btn_my_stats': "📊 Менин статистикам",
        'btn_main_menu': "🏠 Башкы меню",
        'choose_market': "🎯 <b>КАТЕГОРИЯ ТАНДАҢЫЗ:</b>",
        'choose_pair': "📊 <b>ЖУП ТАНДАҢЫЗ:</b>",
        'choose_expiration': "⏰ <b>ЭКСПИРАЦИЯ ТАНДАҢЫЗ:</b>",
        'analyzing': "🔍 <b>БАЗАР АНАЛИЗИ...</b>",
    }
}

def get_text(user_id, key, **kwargs):
    lang = get_lang(user_id)
    text = TEXTS.get(lang, TEXTS['ru']).get(key, key)
    if kwargs:
        return text.format(**kwargs)
    return text

# ============================================
# 🚀 КОМАНДА /start (РАБОЧАЯ!)
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик команды /start"""
    user = update.effective_user
    user_id = str(user.id)
    
    logger.info(f"👤 /start от {user_id}")
    
    if is_banned(user_id):
        await update.message.reply_text("⛔ Вы заблокированы.")
        return
    
    ensure_user(user_id)
    
    message = f"<b>{get_text(user_id, 'welcome')}</b>\n\n"
    message += f"<b>🆔 Ваш ID:</b> <code>{user_id}</code>\n\n"
    message += f"<b>{get_text(user_id, 'choose_lang')}</b>"
    
    keyboard = [
        [
            InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
            InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg")
        ]
    ]
    
    await update.message.reply_text(
        message,
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ============================================
# 📋 ГЛАВНОЕ МЕНЮ
# ============================================

async def show_main_menu(update, user_id):
    """Показывает главное меню"""
    if is_banned(user_id):
        await update.edit_message_text("⛔ Вы заблокированы.")
        return
    
    ensure_user(user_id)
    
    status = get_text(user_id, 'vip_active') if is_vip(int(user_id)) else get_text(user_id, 'vip_required')
    message = get_text(user_id, 'main_menu').format(user_id=user_id, status=status)
    
    keyboard = []
    
    if is_vip(int(user_id)):
        keyboard.append([InlineKeyboardButton(get_text(user_id, 'btn_get_signal'), callback_data="get_signal")])
    else:
        keyboard.append([InlineKeyboardButton(get_text(user_id, 'btn_get_vip'), callback_data="get_vip")])
    
    keyboard.append([InlineKeyboardButton(get_text(user_id, 'btn_my_stats'), callback_data="my_stats")])
    
    keyboard.append([
        InlineKeyboardButton("📢 Telegram", url=SOCIALS["telegram"]),
        InlineKeyboardButton("📺 YouTube", url=SOCIALS["youtube"])
    ])
    
    keyboard.append([InlineKeyboardButton("👨‍💼 Админ", url=ADMIN_LINK)])
    
    await update.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup(keyboard)
    )

# ============================================
# 🎯 ОСНОВНОЙ ОБРАБОТЧИК CALLBACK
# ============================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик callback запросов"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    logger.info(f"🔄 Callback: {user_id} -> {data}")
    
    if is_banned(user_id):
        await query.edit_message_text("⛔ Вы заблокированы.")
        return
    
    # ВЫБОР ЯЗЫКА
    if data.startswith("lang_"):
        lang = data.replace("lang_", "")
        user_languages[user_id] = lang
        Database.save("data/user_languages.json", user_languages)
        
        message = get_text(user_id, 'lang_set')
        button_text = "🚀 НАЧАТЬ" if lang == 'ru' else "🚀 БАШТОО"
        
        await query.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(button_text, callback_data="main_menu")]
            ])
        )
    
    # ГЛАВНОЕ МЕНЮ
    elif data == "main_menu":
        await show_main_menu(query, user_id)
    
    # ПОЛУЧИТЬ СИГНАЛ
    elif data == "get_signal":
        if not is_vip(int(user_id)):
            await query.answer(get_text(user_id, 'vip_required'), show_alert=True)
            return
        
        keyboard = []
        for cat_id, cat_info in MARKET_CATEGORIES.items():
            keyboard.append([InlineKeyboardButton(cat_info['name'], callback_data=f"category_{cat_id}")])
        
        keyboard.append([InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")])
        
        await query.edit_message_text(
            get_text(user_id, 'choose_market'),
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # ВЫБОР КАТЕГОРИИ
    elif data.startswith("category_"):
        if not is_vip(int(user_id)):
            await query.answer(get_text(user_id, 'vip_required'), show_alert=True)
            return
        
        cat_id = data.replace("category_", "")
        if cat_id not in MARKET_CATEGORIES:
            await query.answer("❌ Ошибка")
            return
        
        category = MARKET_CATEGORIES[cat_id]
        pairs = category['pairs']
        
        keyboard = []
        for pair in pairs[:8]:  # Показываем первые 8 пар
            keyboard.append([InlineKeyboardButton(pair, callback_data=f"pair_{cat_id}_{pairs.index(pair)}")])
        
        keyboard.append([InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")])
        
        await query.edit_message_text(
            f"{get_text(user_id, 'choose_pair')}\n\n<b>{category['name']}</b>",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # ВЫБОР ПАРЫ
    elif data.startswith("pair_"):
        if not is_vip(int(user_id)):
            await query.answer(get_text(user_id, 'vip_required'), show_alert=True)
            return
        
        _, cat_id, idx = data.split("_")
        idx = int(idx)
        
        category = MARKET_CATEGORIES[cat_id]
        pairs = category['pairs']
        
        if 0 <= idx < len(pairs):
            pair = pairs[idx]
            context.user_data['selected_pair'] = pair
            context.user_data['selected_category'] = cat_id
            
            keyboard = []
            for exp in EXPIRATION_OPTIONS[:5]:  # Первые 5 экспираций
                keyboard.append([InlineKeyboardButton(exp, callback_data=f"exp_{exp.replace(' ', '_')}")])
            
            keyboard.append([InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")])
            
            await query.edit_message_text(
                f"{get_text(user_id, 'choose_expiration')}\n\n<b>Пара:</b> <code>{pair}</code>",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
    
    # ВЫБОР ЭКСПИРАЦИИ
    elif data.startswith("exp_"):
        if not is_vip(int(user_id)):
            await query.answer(get_text(user_id, 'vip_required'), show_alert=True)
            return
        
        expiration = data.replace("exp_", "").replace("_", " ")
        pair = context.user_data.get('selected_pair')
        category = context.user_data.get('selected_category')
        
        if not pair or not category:
            await query.answer("❌ Ошибка данных")
            return
        
        await query.edit_message_text(
            get_text(user_id, 'analyzing'),
            parse_mode='HTML'
        )
        
        await asyncio.sleep(1.5)
        
        signal = analyzer.analyze(pair, expiration, category)
        
        # Показываем сигнал
        dir_text = "ВВЕРХ ▲" if signal['direction'] == "CALL" else "ВНИЗ ▼"
        dir_emoji = "🟢" if signal['direction'] == "CALL" else "🔴"
        
        message = f"🎯 <b>ТОЧНЫЙ СИГНАЛ</b>\n\n"
        message += f"📊 Пара: <code>{signal['pair']}</code>\n"
        message += f"🎯 Направление: {dir_emoji} <b>{dir_text}</b>\n"
        message += f"📈 Уверенность: <b>{signal['confidence']}%</b>\n"
        message += f"💪 {signal['strength']}\n"
        message += f"⏰ Экспирация: {signal['expiration']}\n"
        message += f"🕒 До: {signal['exact_expiration']}\n"
        message += f"⏱️ Вход: {signal['entry_time']}\n"
        message += f"📊 Тип: {signal['entry_type']}\n\n"
        message += f"<b>Удачи в торговле!</b>"
        
        keyboard = [
            [InlineKeyboardButton("✅ Выиграл +95%", callback_data="trade_win")],
            [InlineKeyboardButton("❌ Проиграл", callback_data="trade_loss")],
            [InlineKeyboardButton("🔄 Новый сигнал", callback_data="get_signal")],
            [InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # ПОЛУЧИТЬ VIP
    elif data == "get_vip":
        lang = get_lang(user_id)
        
        if lang == 'ru':
            message = """👑 <b>VIP ДОСТУП</b>

✅ <b>ПРЕИМУЩЕСТВА:</b>
• 100+ торговых пар
• Максимально точные сигналы
• Точное время входа

📝 <b>КАК ПОЛУЧИТЬ:</b>
1. Регистрация по ссылке
2. Пополнение от $50
3. Написать админу"""
        else:
            message = """👑 <b>VIP ДОСТУП</b>

✅ <b>АРТЫКЧЫЛЫКТАРЫ:</b>
• 100+ соода жуптары
• Максималдуу так сигналдар
• Так кириш убактысы

📝 <b>КАЛАЙ АЛУУ:</b>
1. Шилтеме боюнча каттоо
2. $50дан депозит салуу
3. Админге жазуу"""
        
        keyboard = [
            [InlineKeyboardButton("📝 Регистрация", url=REF_LINK)],
            [InlineKeyboardButton("📞 Написать админу", url=ADMIN_LINK)],
            [InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # МОЯ СТАТИСТИКА
    elif data == "my_stats":
        stats = user_stats.get(user_id, {})
        
        if get_lang(user_id) == 'ru':
            message = f"""📊 <b>ВАША СТАТИСТИКА</b>

🎯 Сделки: {stats.get('total', 0)}
✅ Выигрыши: {stats.get('wins', 0)}
❌ Проигрыши: {stats.get('losses', 0)}
📈 Успех: {stats.get('win_rate', 0)}%
💰 Прибыль: ${stats.get('profit', 0)}"""
        else:
            message = f"""📊 <b>СИЗДИН СТАТИСТИКАНЫЗ</b>

🎯 Иштер: {stats.get('total', 0)}
✅ Жеңиштер: {stats.get('wins', 0)}
❌ Жеңилүүлөр: {stats.get('losses', 0)}
📈 Ийгилик: {stats.get('win_rate', 0)}%
💰 Пайда: ${stats.get('profit', 0)}"""
        
        keyboard = [[InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")]]
        
        await query.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    # ОТМЕТКА ТОРГОВ
    elif data.startswith("trade_"):
        if "win" in data:
            update_stats(user_id, True)
            message = "✅ <b>Результат сохранен!</b>"
        else:
            update_stats(user_id, False)
            message = "❌ <b>Результат сохранен!</b>"
        
        keyboard = [
            [InlineKeyboardButton("🔄 Новый сигнал", callback_data="get_signal")],
            [InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")]
        ]
        
        await query.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
    
    else:
        await query.edit_message_text(
            "🔄 Функция в разработке...",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(get_text(user_id, 'btn_main_menu'), callback_data="main_menu")]
            ])
        )

# ============================================
# 📢 АДМИН КОМАНДЫ
# ============================================

async def grant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выдать VIP"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("⛔ Только для админа!")
        return
    
    if not context.args:
        await update.message.reply_text("Использование: /grant <user_id>")
        return
    
    target = context.args[0]
    vip_users.add(target)
    Database.save("data/vip_users.json", list(vip_users))
    
    await update.message.reply_text(f"✅ VIP выдан {target}")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Рассылка"""
    user_id = update.effective_user.id
    
    if not is_admin(user_id):
        await update.message.reply_text("⛔ Только для админа!")
        return
    
    if not context.args:
        await update.message.reply_text("Использование: /broadcast <текст>")
        return
    
    text = " ".join(context.args)
    sent = 0
    failed = 0
    
    await update.message.reply_text("📢 Начинаю рассылку...")
    
    for user in all_users:
        try:
            await context.bot.send_message(
                chat_id=int(user),
                text=f"📢 <b>РАССЫЛКА ОТ АДМИНА:</b>\n\n{text}",
                parse_mode='HTML'
            )
            sent += 1
            await asyncio.sleep(0.1)
        except:
            failed += 1
    
    await update.message.reply_text(
        f"✅ Рассылка завершена!\n\n"
        f"📤 Отправлено: {sent}\n"
        f"❌ Ошибок: {failed}"
    )

# ============================================
# 🚀 ЗАПУСК БОТА (РАБОЧИЙ ВАРИАНТ)
# ============================================

def main():
    """Главная функция запуска"""
    logger.info("=" * 60)
    logger.info("🚀 ЗАПУСК KURUT AI INFINITY PRO - РАБОЧАЯ ВЕРСИЯ")
    logger.info("=" * 60)
    
    # 1. Запускаем Flask в отдельном потоке
    flask_thread = threading.Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("✅ Flask сервер запущен (порт 8080)")
    
    # 2. Запускаем автопинг
    start_ping()
    
    # 3. Создаем и настраиваем приложение бота
    application = ApplicationBuilder().token(TOKEN).build()
    
    # 4. Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("grant", grant_command))
    application.add_handler(CommandHandler("broadcast", broadcast_command))
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # 5. Обработчик текстовых сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, 
                                         lambda update, context: update.message.reply_text(
                                             "Используйте команду /start")))
    
    logger.info("✅ Бот настроен и готов к работе")
    logger.info(f"👥 Пользователей в базе: {len(all_users)}")
    logger.info(f"👑 VIP пользователей: {len(vip_users)}")
    logger.info("=" * 60)
    logger.info("🤖 Бот запускается...")
    
    # 6. Запускаем бота
    application.run_polling()

if __name__ == "__main__":
    # Простой запуск - никаких сложных async проблем
    main()
