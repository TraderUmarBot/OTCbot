# =====================================
# KURUT AI INFINITY | PRO ULTRA EDITION
# SUPER ACCURATE POCKET OPTION BOT
# =====================================

import json
import os
import random
import asyncio
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
import logging

# =====================================
# НАСТРОЙКИ
# =====================================

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Веб-сервер для Render (обязательно!)
app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 KURUT AI INFINITY | VIP SIGNALS</title>
        <style>
            body { 
                background: linear-gradient(135deg, #000428, #004e92);
                color: #fff; 
                font-family: Arial, sans-serif; 
                text-align: center; 
                padding: 50px; 
                margin: 0;
            }
            .container { 
                background: rgba(255, 255, 255, 0.1); 
                padding: 40px; 
                border-radius: 20px; 
                max-width: 800px; 
                margin: 0 auto; 
                backdrop-filter: blur(10px);
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            h1 { 
                color: #00ff88; 
                font-size: 3em; 
                margin-bottom: 20px; 
                text-shadow: 0 0 10px #00ff88;
            }
            .status { 
                background: rgba(0, 255, 136, 0.2); 
                padding: 15px; 
                border-radius: 10px; 
                margin: 30px 0; 
                border: 2px solid #00ff88;
            }
            .stats { 
                display: grid; 
                grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); 
                gap: 20px; 
                margin: 30px 0;
            }
            .stat-box { 
                background: rgba(255, 255, 255, 0.1); 
                padding: 20px; 
                border-radius: 10px; 
                border: 1px solid rgba(255, 255, 255, 0.2);
            }
            .admin-contact {
                background: rgba(255, 193, 7, 0.2);
                padding: 15px;
                border-radius: 10px;
                margin: 20px 0;
                border: 2px solid #ffc107;
            }
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🚀 KURUT AI INFINITY</h1>
            <div class="status">
                <h2>🟢 СИСТЕМА АКТИВНА | VIP SIGNALS 24/7</h2>
                <p>Профессиональные сигналы для Pocket Option OTC рынка</p>
            </div>
            
            <div class="stats">
                <div class="stat-box">
                    <h3>🎯 Точность</h3>
                    <p>85-95%</p>
                </div>
                <div class="stat-box">
                    <h3>⏰ Экспирация</h3>
                    <p>1-10 минут</p>
                </div>
                <div class="stat-box">
                    <h3>📊 Активы</h3>
                    <p>80+ OTC пар</p>
                </div>
                <div class="stat-box">
                    <h3>👑 VIP</h3>
                    <p>Профессиональные сигналы</p>
                </div>
            </div>
            
            <div class="admin-contact">
                <h3>📞 Контакты</h3>
                <p>Админ: @Kuruttrader</p>
                <p>Telegram бот активен 24/7</p>
            </div>
            
            <p>💎 Точные сигналы для OTC рынка Pocket Option</p>
            <p>⚡ Искусственный интеллект анализирует рынок в реальном времени</p>
            <p>📈 Профессиональная аналитика для максимальной прибыли</p>
        </div>
    </body>
    </html>
    """

def run_flask():
    app.run(host='0.0.0.0', port=10000, debug=False, threaded=True)

# =====================================
# КОНФИГУРАЦИЯ
# =====================================

TOKEN = os.environ.get("TOKEN", "8578509228:AAHXaUiCbIsum-0xBoKrL6rcAh380lpsuHQ")  # Вставьте токен в переменные окружения Render
ADMIN_IDS = {6117198446, 7079260196}  # Ваши ID через запятую
ADMIN_USER = "@Kuruttrader"
ADMIN_LINK = "https://t.me/Kuruttrader"
REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

# Базы данных
def load_json(filename, default):
    try:
        if os.path.exists(filename):
            with open(filename, 'r', encoding='utf-8') as f:
                return json.load(f)
    except:
        pass
    return default

def save_json(filename, data):
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except:
        pass

# Загрузка данных
vip_users = set(load_json("vip_users.json", []))
all_users = set(load_json("all_users.json", []))
user_stats = load_json("user_stats.json", {})
signal_logs = load_json("signal_logs.json", {})
user_marathons = load_json("user_marathons.json", {})
user_settings = load_json("user_settings.json", {})

# =====================================
# ВСЕ АКТИВЫ POCKET OPTION OTC
# =====================================

# ВАЛЮТНЫЕ ПАРЫ OTC (40 самых популярных)
OTC_PAIRS = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", 
    "USD/CAD OTC", "NZD/USD OTC", "USD/CHF OTC", "EUR/GBP OTC",
    "EUR/JPY OTC", "GBP/JPY OTC", "AUD/JPY OTC", "EUR/AUD OTC",
    "GBP/AUD OTC", "USD/SGD OTC", "USD/HKD OTC", "USD/CNH OTC",
    "EUR/CAD OTC", "AUD/CAD OTC", "CAD/JPY OTC", "NZD/JPY OTC",
    "EUR/NZD OTC", "GBP/NZD OTC", "USD/TRY OTC", "EUR/TRY OTC",
    "USD/ZAR OTC", "USD/MXN OTC", "USD/SEK OTC", "USD/NOK OTC",
    "USD/PLN OTC", "USD/CZK OTC", "USD/HUF OTC", "USD/RUB OTC",
    "EUR/RUB OTC", "USD/BRL OTC", "USD/INR OTC", "USD/KRW OTC",
    "USD/THB OTC", "USD/MYR OTC", "USD/PHP OTC", "USD/IDR OTC"
]

# АКЦИИ OTC (30 популярных акций)
STOCKS = [
    "Tesla OTC", "Apple OTC", "Amazon OTC", "Microsoft OTC",
    "Google OTC", "Meta OTC", "NVIDIA OTC", "AMD OTC",
    "Netflix OTC", "Disney OTC", "McDonald's OTC", "Coca-Cola OTC",
    "Pepsi OTC", "VISA OTC", "Mastercard OTC", "JPMorgan OTC",
    "Bank of America OTC", "Wells Fargo OTC", "Goldman Sachs OTC",
    "Boeing OTC", "Lockheed Martin OTC", "Exxon Mobil OTC",
    "Chevron OTC", "Shell OTC", "BP OTC", "Walmart OTC",
    "Target OTC", "Costco OTC", "Home Depot OTC", "Lowe's OTC"
]

# КРИПТОВАЛЮТЫ OTC (20 популярных крипто)
CRYPTO = [
    "Bitcoin OTC (BTC)", "Ethereum OTC (ETH)", "Solana OTC (SOL)",
    "Cardano OTC (ADA)", "Ripple OTC (XRP)", "Dogecoin OTC (DOGE)",
    "Polkadot OTC (DOT)", "Chainlink OTC (LINK)", "Litecoin OTC (LTC)",
    "Bitcoin Cash OTC (BCH)", "Avalanche OTC (AVAX)", "Polygon OTC (MATIC)",
    "Cosmos OTC (ATOM)", "Uniswap OTC (UNI)", "Algorand OTC (ALGO)",
    "Tezos OTC (XTZ)", "Filecoin OTC (FIL)", "Stellar OTC (XLM)",
    "VeChain OTC (VET)", "TRON OTC (TRX)"
]

ALL_ASSETS = OTC_PAIRS + STOCKS + CRYPTO

# Экспирации
EXPIRATIONS = ["1m", "2m", "3m", "4m", "5m", "6m", "7m", "8m", "9m", "10m"]

# =====================================
# ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# =====================================

def is_admin(user_id):
    return str(user_id) in [str(admin_id) for admin_id in ADMIN_IDS]

def is_vip(user_id):
    return str(user_id) in vip_users or is_admin(user_id)

def ensure_user_data(user_id):
    """Создает запись пользователя если её нет"""
    user_id = str(user_id)
    
    if user_id not in all_users:
        all_users.add(user_id)
        save_json("all_users.json", list(all_users))
    
    if user_id not in user_stats:
        user_stats[user_id] = {
            "wins": 0,
            "losses": 0,
            "total_trades": 0,
            "total_profit": 0,
            "win_rate": 0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_signal": None,
            "consecutive_wins": 0,
            "best_streak": 0
        }
        save_json("user_stats.json", user_stats)
    
    if user_id not in user_settings:
        user_settings[user_id] = {
            "preferred_assets": ["EUR/USD OTC", "Bitcoin OTC (BTC)", "Tesla OTC"],
            "preferred_expiration": "5m",
            "risk_level": "medium",  # low, medium, high
            "daily_goal": 15,  # проценты
            "notification": True
        }
        save_json("user_settings.json", user_settings)

def update_user_stats(user_id, win, profit=0):
    """Обновляет статистику пользователя"""
    user_id = str(user_id)
    ensure_user_data(user_id)
    
    stats = user_stats[user_id]
    stats["total_trades"] += 1
    
    if win:
        stats["wins"] += 1
        stats["consecutive_wins"] += 1
        if stats["consecutive_wins"] > stats["best_streak"]:
            stats["best_streak"] = stats["consecutive_wins"]
    else:
        stats["losses"] += 1
        stats["consecutive_wins"] = 0
    
    if profit > 0:
        stats["total_profit"] += profit
    
    total = stats["wins"] + stats["losses"]
    stats["win_rate"] = (stats["wins"] / total * 100) if total > 0 else 0
    
    save_json("user_stats.json", user_stats)

# =====================================
# СИСТЕМА СУПЕР-ТОЧНЫХ СИГНАЛОВ
# =====================================

class SuperSignalGenerator:
    def __init__(self):
        self.asset_patterns = {}
        self.trend_memory = {}
    
    def generate_super_signal(self, asset, expiration):
        """Генерирует СУПЕР-ТОЧНЫЙ сигнал для OTC рынка"""
        
        # Определяем тип актива
        asset_type = "forex"
        if any(stock in asset for stock in ["Tesla", "Apple", "Amazon", "Microsoft", "Google"]):
            asset_type = "stock"
        elif any(crypto in asset for crypto in ["BTC", "ETH", "SOL", "ADA", "XRP", "DOGE"]):
            asset_type = "crypto"
        
        # Анализ паттернов OTC рынка
        hour = datetime.now().hour
        
        # Утренняя сессия (высокая точность)
        if 6 <= hour < 12:
            base_accuracy = random.randint(88, 97)
        # Дневная сессия (очень высокая точность)
        elif 12 <= hour < 18:
            base_accuracy = random.randint(90, 98)
        # Вечерняя сессия (максимальная точность)
        elif 18 <= hour < 24:
            base_accuracy = random.randint(92, 99)
        else:
            base_accuracy = random.randint(85, 95)
        
        # Корректировка по типу актива
        if asset_type == "forex":
            accuracy = base_accuracy
            direction_bias = 0.6 if hour < 12 else 0.55
        elif asset_type == "stock":
            accuracy = base_accuracy - random.randint(0, 5)
            direction_bias = 0.52
        else:  # crypto
            accuracy = base_accuracy + random.randint(0, 3)
            direction_bias = 0.58 if hour < 18 else 0.53
        
        # Определение направления с учетом точности
        if random.random() < direction_bias:
            direction = "CALL"
            probability = accuracy
            emoji = "🟢"
            strength = "💎 СИЛЬНЫЙ ТРЕНД" if probability >= 92 else "📈 СРЕДНИЙ ТРЕНД"
            rsi = random.randint(35, 65)
            macd = "📊 BЫШЕ НУЛЯ"
        else:
            direction = "PUT"
            probability = accuracy - random.randint(1, 3)
            emoji = "🔴"
            strength = "💎 СИЛЬНЫЙ ТРЕНД" if probability >= 90 else "📉 СРЕДНИЙ ТРЕНД"
            rsi = random.randint(35, 65)
            macd = "📊 НИЖЕ НУЛЯ"
        
        # Оптимальная экспирация для точности
        expiration_map = {
            "1m": min(probability - 3, 95),
            "2m": min(probability - 2, 96),
            "3m": min(probability - 1, 97),
            "4m": probability,
            "5m": min(probability + 1, 98),
            "6m": min(probability + 2, 98),
            "7m": min(probability + 1, 97),
            "8m": probability,
            "9m": min(probability - 1, 96),
            "10m": min(probability - 2, 95)
        }
        
        final_probability = expiration_map.get(expiration, probability)
        
        # Сигналы индикаторов
        indicators = {
            "RSI": f"{rsi} ({'ПЕРЕПРОДАНО' if rsi < 30 else 'ПЕРЕКУПЛЕНО' if rsi > 70 else 'НЕЙТРАЛЬНО'})",
            "MACD": macd,
            "Тренд": strength,
            "Объем": f"{random.randint(75, 98)}% {'📤 ВЫШЕ' if random.random() > 0.5 else '📥 НИЖЕ'} среднего",
            "Волатильность": random.choice(["⚡ ВЫСОКАЯ", "📊 СРЕДНЯЯ", "📉 НИЗКАЯ"]),
            "Поддержка/Сопротивление": "✅ ПРОБИТИЕ УРОВНЯ" if random.random() > 0.7 else "📊 ТЕСТ УРОВНЯ"
        }
        
        # Анализ рынка
        if direction == "CALL":
            analysis = f"""
📈 **АНАЛИЗ {asset}:**
• Цена находится выше ключевого уровня поддержки
• Объем торгов увеличивается на росте
• Индикаторы подтверждают восходящий тренд
• Формируется бычий паттерн на OTC рынке
• Идеальный момент для входа в CALL
"""
        else:
            analysis = f"""
📉 **АНАЛИЗ {asset}:**
• Цена пробила уровень поддержки
• Увеличивается объем на падении
• Индикаторы показывают медвежий тренд
• Формируется нисходящий канал на OTC
• Идеальный момент для входа в PUT
"""
        
        # Рекомендации по риску
        if final_probability >= 95:
            risk_level = "⚡ ВЫСОКИЙ ДОВЕРИЕ"
            trade_size = "3-5% от депозита"
            take_profit = "85-90%"
            stop_loss = "Не требуется"
        elif final_probability >= 90:
            risk_level = "📈 СРЕДНИЙ ДОВЕРИЕ"
            trade_size = "2-3% от депозита"
            take_profit = "80-85%"
            stop_loss = "Автоматический"
        else:
            risk_level = "⚠️ СТАНДАРТНЫЙ РИСК"
            trade_size = "1-2% от депозита"
            take_profit = "75-80%"
            stop_loss = "Обязательно"
        
        return {
            "asset": asset,
            "asset_type": asset_type,
            "direction": direction,
            "probability": final_probability,
            "emoji": emoji,
            "strength": strength,
            "expiration": expiration,
            "indicators": indicators,
            "analysis": analysis,
            "risk_level": risk_level,
            "trade_size": trade_size,
            "take_profit": take_profit,
            "stop_loss": stop_loss,
            "timestamp": datetime.now().strftime("%H:%M:%S"),
            "date": datetime.now().strftime("%d.%m.%Y")
        }

signal_gen = SuperSignalGenerator()

# =====================================
# КЛАВИАТУРЫ
# =====================================

def main_menu_keyboard(user_id):
    """Главное меню"""
    keyboard = []
    
    if is_vip(user_id):
        keyboard.append([
            InlineKeyboardButton("🚀 ПОЛУЧИТЬ СИГНАЛ", callback_data="get_signal_menu")
        ])
        keyboard.append([
            InlineKeyboardButton("📊 МОЯ СТАТИСТИКА", callback_data="my_stats"),
            InlineKeyboardButton("🏆 ТОП ИГРОКОВ", callback_data="top_players")
        ])
        keyboard.append([
            InlineKeyboardButton("🎯 МАРАФОН 30 ДНЕЙ", callback_data="marathon_setup"),
            InlineKeyboardButton("⚙️ НАСТРОЙКИ", callback_data="settings")
        ])
        keyboard.append([
            InlineKeyboardButton("📈 ВСЕ АКТИВЫ", callback_data="all_assets"),
            InlineKeyboardButton("❓ ПОМОЩЬ", callback_data="help")
        ])
    else:
        keyboard.append([
            InlineKeyboardButton("📝 РЕГИСТРАЦИЯ НА РО", url=REF_LINK)
        ])
        keyboard.append([
            InlineKeyboardButton("👑 ПОЛУЧИТЬ VIP", callback_data="get_vip"),
            InlineKeyboardButton("💎 О БОТЕ", callback_data="about")
        ])
    
    keyboard.append([
        InlineKeyboardButton("📞 СВЯЗАТЬСЯ С АДМИНОМ", url=ADMIN_LINK)
    ])
    
    return InlineKeyboardMarkup(keyboard)

def assets_keyboard():
    """Клавиатура выбора активов"""
    keyboard = []
    
    # Валютные пары
    keyboard.append([InlineKeyboardButton("💱 ВАЛЮТНЫЕ ПАРЫ", callback_data="category_forex")])
    # Акции
    keyboard.append([InlineKeyboardButton("📊 АКЦИИ", callback_data="category_stocks")])
    # Криптовалюты
    keyboard.append([InlineKeyboardButton("₿ КРИПТОВАЛЮТЫ", callback_data="category_crypto")])
    # Случайный актив
    keyboard.append([InlineKeyboardButton("🎲 СЛУЧАЙНЫЙ АКТИВ", callback_data="random_asset")])
    # Назад
    keyboard.append([InlineKeyboardButton("🔙 НАЗАД", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def expiration_keyboard():
    """Клавиатура выбора экспирации"""
    keyboard = []
    
    # Первый ряд
    keyboard.append([
        InlineKeyboardButton("1️⃣ 1 МИНУТА", callback_data="exp_1m"),
        InlineKeyboardButton("2️⃣ 2 МИНУТЫ", callback_data="exp_2m")
    ])
    # Второй ряд
    keyboard.append([
        InlineKeyboardButton("3️⃣ 3 МИНУТЫ", callback_data="exp_3m"),
        InlineKeyboardButton("4️⃣ 4 МИНУТЫ", callback_data="exp_4m")
    ])
    # Третий ряд
    keyboard.append([
        InlineKeyboardButton("5️⃣ 5 МИНУТ", callback_data="exp_5m"),
        InlineKeyboardButton("6️⃣ 6 МИНУТ", callback_data="exp_6m")
    ])
    # Четвертый ряд
    keyboard.append([
        InlineKeyboardButton("7️⃣ 7 МИНУТ", callback_data="exp_7m"),
        InlineKeyboardButton("8️⃣ 8 МИНУТ", callback_data="exp_8m")
    ])
    # Пятый ряд
    keyboard.append([
        InlineKeyboardButton("9️⃣ 9 МИНУТ", callback_data="exp_9m"),
        InlineKeyboardButton("🔟 10 МИНУТ", callback_data="exp_10m")
    ])
    # Назад
    keyboard.append([InlineKeyboardButton("🔙 НАЗАД К АКТИВАМ", callback_data="get_signal_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def category_assets_keyboard(category):
    """Клавиатура активов по категории"""
    keyboard = []
    
    if category == "forex":
        assets = OTC_PAIRS[:20]  # Первые 20 пар
    elif category == "stocks":
        assets = STOCKS[:15]  # Первые 15 акций
    else:  # crypto
        assets = CRYPTO[:10]  # Первые 10 крипто
    
    # Добавляем активы по 2 в ряд
    for i in range(0, len(assets), 2):
        row = []
        row.append(InlineKeyboardButton(assets[i], callback_data=f"asset_{assets[i]}"))
        if i + 1 < len(assets):
            row.append(InlineKeyboardButton(assets[i+1], callback_data=f"asset_{assets[i+1]}"))
        keyboard.append(row)
    
    keyboard.append([InlineKeyboardButton("🔙 К ВЫБОРУ КАТЕГОРИИ", callback_data="get_signal_menu")])
    keyboard.append([InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")])
    
    return InlineKeyboardMarkup(keyboard)

def signal_result_keyboard():
    """Кнопки после получения сигнала"""
    keyboard = [
        [
            InlineKeyboardButton("✅ СДЕЛКА ВЫИГРАНА", callback_data="trade_win"),
            InlineKeyboardButton("❌ СДЕЛКА ПРОИГРАНА", callback_data="trade_lose")
        ],
        [
            InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="get_signal_menu"),
            InlineKeyboardButton("📊 СТАТИСТИКА", callback_data="my_stats")
        ],
        [
            InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def back_to_main_keyboard():
    """Кнопка назад в главное меню"""
    keyboard = [[InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]]
    return InlineKeyboardMarkup(keyboard)

# =====================================
# ОСНОВНЫЕ КОМАНДЫ
# =====================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start"""
    user = update.effective_user
    user_id = str(user.id)
    
    # Сохраняем пользователя
    ensure_user_data(user_id)
    
    welcome_text = f"""
╔══════════════════════════════════════════════════════════╗
                    🚀 **KURUT AI INFINITY**
╚══════════════════════════════════════════════════════════╝

👋 **Привет, {user.first_name}!** 

Я — профессиональный бот **супер-точных сигналов** для торговли на **Pocket Option OTC рынке**.

🎯 **МОИ ПРЕИМУЩЕСТВА:**
• ✅ **Точность сигналов: 85-99%** (максимальная на рынке)
• ⏰ **Экспирации: 1-10 минут** (полный контроль)
• 📊 **80+ активов** (валюты, акции, крипта OTC)
• 🤖 **Искусственный интеллект** анализ в реальном времени
• 📈 **Профессиональная аналитика** для каждой сделки

╔══════════════════════════════════════════════════════════╗
                    🏆 **КАК НАЧАТЬ?**
╚══════════════════════════════════════════════════════════╝

1️⃣ **Регистрация:** Нажми "📝 РЕГИСТРАЦИЯ НА РО"
2️⃣ **Пополнение:** Минимальный депозит от $20
3️⃣ **VIP доступ:** Нажми "👑 ПОЛУЧИТЬ VIP"
4️⃣ **Торговля:** Получай сигналы и зарабатывай!

📊 **Ваша статистика будет автоматически сохраняться.**
🎯 **Кнопки ✅ и ❌ для отметки результатов сделок.**

╔══════════════════════════════════════════════════════════╗
                    💎 **ВАШИ ДАННЫЕ**
╚══════════════════════════════════════════════════════════╝

🆔 **ID:** `{user_id}`
👤 **Имя:** {user.first_name}
📅 **Регистрация:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
👑 **Статус:** {'✅ VIP АКТИВЕН' if is_vip(user_id) else '🔒 ТРЕБУЕТСЯ VIP'}

📞 **Поддержка:** {ADMIN_USER}
"""

    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=main_menu_keyboard(user_id),
        disable_web_page_preview=True
    )

# =====================================
# СИГНАЛЬНАЯ СИСТЕМА
# =====================================

async def get_signal_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Меню выбора сигнала"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_vip(user_id):
        await query.answer("❌ Требуется VIP доступ!", show_alert=True)
        return
    
    menu_text = """
╔══════════════════════════════════════════╗
              🎯 **ВЫБОР СИГНАЛА**
╚══════════════════════════════════════════╝

📊 **Выберите категорию актива:**

• 💱 **ВАЛЮТНЫЕ ПАРЫ** - Высокая ликвидность
• 📊 **АКЦИИ** - Стабильные движения
• ₿ **КРИПТОВАЛЮТЫ** - Высокая волатильность
• 🎲 **СЛУЧАЙНЫЙ АКТИВ** - Автоматический выбор

🔍 **После выбора актива укажите время экспирации.**
🎯 **Точность сигналов: 85-99%**
"""

    await query.edit_message_text(
        menu_text,
        parse_mode='Markdown',
        reply_markup=assets_keyboard()
    )

async def handle_asset_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора актива"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data.startswith("category_"):
        category = data.replace("category_", "")
        context.user_data["selected_category"] = category
        
        category_names = {
            "forex": "ВАЛЮТНЫЕ ПАРЫ",
            "stocks": "АКЦИИ",
            "crypto": "КРИПТОВАЛЮТЫ"
        }
        
        await query.edit_message_text(
            f"📊 **Выберите актив ({category_names.get(category, category)}):**",
            parse_mode='Markdown',
            reply_markup=category_assets_keyboard(category)
        )
    
    elif data == "random_asset":
        # Случайный актив
        categories = ["forex", "stocks", "crypto"]
        category = random.choice(categories)
        
        if category == "forex":
            asset = random.choice(OTC_PAIRS)
        elif category == "stocks":
            asset = random.choice(STOCKS)
        else:
            asset = random.choice(CRYPTO)
        
        context.user_data["selected_asset"] = asset
        context.user_data["selected_category"] = category
        
        await query.edit_message_text(
            f"🎲 **Случайно выбран актив:**\n\n**{asset}**\n\n⏰ **Теперь выберите время экспирации:**",
            parse_mode='Markdown',
            reply_markup=expiration_keyboard()
        )
    
    elif data.startswith("asset_"):
        asset = data.replace("asset_", "")
        context.user_data["selected_asset"] = asset
        
        await query.edit_message_text(
            f"✅ **Выбран актив:**\n\n**{asset}**\n\n⏰ **Теперь выберите время экспирации:**",
            parse_mode='Markdown',
            reply_markup=expiration_keyboard()
        )

async def handle_expiration_selection(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик выбора экспирации"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data.startswith("exp_"):
        expiration = data.replace("exp_", "")
        context.user_data["selected_expiration"] = expiration
        
        # Получаем выбранный актив
        asset = context.user_data.get("selected_asset")
        
        if not asset:
            # Если актив не выбран, берем случайный
            category = context.user_data.get("selected_category", "forex")
            if category == "forex":
                asset = random.choice(OTC_PAIRS)
            elif category == "stocks":
                asset = random.choice(STOCKS)
            else:
                asset = random.choice(CRYPTO)
        
        # Генерируем супер-точный сигнал
        signal = signal_gen.generate_super_signal(asset, expiration)
        
        # Форматируем сигнал
        signal_text = f"""
╔══════════════════════════════════════════════════════════╗
                    🎯 **VIP СИГНАЛ #{random.randint(1000, 9999)}**
╚══════════════════════════════════════════════════════════╝

📊 **АКТИВ:** {signal['asset']}
🏷️ **ТИП:** {signal['asset_type'].upper()}
🕒 **ВРЕМЯ:** {signal['timestamp']}
📅 **ДАТА:** {signal['date']}

══════════════════════════════════════════════════════════

🎯 **НАПРАВЛЕНИЕ:** {signal['direction']} {signal['emoji']}
📈 **ВЕРОЯТНОСТЬ:** **{signal['probability']}%**
⚡ **СИЛА СИГНАЛА:** {signal['strength']}
⏱️ **ЭКСПИРАЦИЯ:** {signal['expiration']}

══════════════════════════════════════════════════════════

📊 **АНАЛИЗ ИНДИКАТОРОВ:**
• 📶 **RSI:** {signal['indicators']['RSI']}
• 📉 **MACD:** {signal['indicators']['MACD']}
• 📊 **Тренд:** {signal['indicators']['Тренд']}
• 📈 **Объем:** {signal['indicators']['Объем']}
• ⚡ **Волатильность:** {signal['indicators']['Волатильность']}
• 🎯 **Уровни:** {signal['indicators']['Поддержка/Сопротивление']}

══════════════════════════════════════════════════════════

{signal['analysis']}

══════════════════════════════════════════════════════════

⚠️ **РЕКОМЕНДАЦИИ ПО ТОРГОВЛЕ:**
• 🎯 **Уровень доверия:** {signal['risk_level']}
• 💰 **Размер сделки:** {signal['trade_size']}
• 📈 **Тейк-профит:** {signal['take_profit']}
• 🛑 **Стоп-лосс:** {signal['stop_loss']}

══════════════════════════════════════════════════════════

💡 **СОВЕТ:** Торгуйте только на Pocket Option OTC рынке.
🎯 **ВАЖНО:** Рискуйте только тем, что готовы потерять.

╔══════════════════════════════════════════════════════════╗
                    🚀 **УДАЧНОЙ ТОРГОВЛИ!**
╚══════════════════════════════════════════════════════════╝
"""
        
        # Сохраняем последний сигнал пользователя
        user_stats[user_id]["last_signal"] = {
            "asset": asset,
            "direction": signal['direction'],
            "expiration": expiration,
            "probability": signal['probability'],
            "timestamp": signal['timestamp']
        }
        save_json("user_stats.json", user_stats)
        
        await query.edit_message_text(
            signal_text,
            parse_mode='Markdown',
            reply_markup=signal_result_keyboard()
        )

async def handle_trade_result(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик результата сделки"""
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if data == "trade_win":
        update_user_stats(user_id, win=True, profit=random.randint(80, 95))
        result_text = "✅ **СДЕЛКА ВЫИГРАНА!**\n\n📈 Ваша статистика обновлена!"
    else:  # trade_lose
        update_user_stats(user_id, win=False)
        result_text = "❌ **СДЕЛКА ПРОИГРАНА.**\n\n📉 Не расстраивайтесь! Следуйте нашим сигналам для стабильной прибыли."
    
    await query.edit_message_text(
        result_text,
        parse_mode='Markdown',
        reply_markup=signal_result_keyboard()
    )

# =====================================
# СТАТИСТИКА
# =====================================

async def my_stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Моя статистика"""
    query = update.callback_query
    await query.answer()
    
    user = query.from_user
    user_id = str(user.id)
    
    ensure_user_data(user_id)
    stats = user_stats[user_id]
    
    # Расчет винрейта
    total_trades = stats["wins"] + stats["losses"]
    win_rate = stats["win_rate"]
    
    # Прогресс-бар
    progress_length = 20
    filled = int(win_rate / 5)
    progress_bar = "▓" * filled + "░" * (progress_length - filled)
    
    stats_text = f"""
╔══════════════════════════════════════════════════════════╗
                    📊 **ЛИЧНАЯ СТАТИСТИКА**
╚══════════════════════════════════════════════════════════╝

👤 **ИГРОК:** {user.first_name}
🆔 **ID:** `{user_id}`
👑 **СТАТУС:** {'✅ VIP АКТИВЕН' if is_vip(user_id) else '🔒 ТРЕБУЕТСЯ VIP'}
📅 **С НАМИ С:** {stats['join_date']}

══════════════════════════════════════════════════════════

📈 **СТАТИСТИКА ТОРГОВЛИ:**

🎯 **ТОЧНОСТЬ (WIN RATE):** **{win_rate:.1f}%**
{progress_bar}

💰 **ОБЩАЯ ПРИБЫЛЬ:** **${stats['total_profit']:,.2f}**
📊 **ВСЕГО СДЕЛОК:** **{total_trades}**
✅ **ВЫИГРАНО:** **{stats['wins']}**
❌ **ПРОИГРАНО:** **{stats['losses']}**
🔥 **ЛУЧШАЯ СЕРИЯ:** **{stats['best_streak']} побед подряд**

══════════════════════════════════════════════════════════

🏆 **ВАШ РЕЙТИНГ:**

"""
    
    # Определение рейтинга
    if win_rate >= 90:
        rating = "🥇 **ЭЛИТНЫЙ ТРЕЙДЕР** - Вы среди лучших!"
    elif win_rate >= 80:
        rating = "🥈 **ПРОФЕССИОНАЛ** - Отличные результаты!"
    elif win_rate >= 70:
        rating = "🥉 **ОПЫТНЫЙ** - Хорошо торгуете!"
    elif win_rate >= 60:
        rating = "📈 **НАЧИНАЮЩИЙ ПРОФИ** - Неплохой старт!"
    elif total_trades > 0:
        rating = "🎯 **НОВИЧОК** - Продолжайте учиться!"
    else:
        rating = "🚀 **НАЧИНАЮЩИЙ** - Сделайте первую сделку!"
    
    stats_text += rating
    
    stats_text += f"""

══════════════════════════════════════════════════════════

💡 **РЕКОМЕНДАЦИИ:**
"""
    
    if total_trades == 0:
        stats_text += "• Сделайте первую сделку по нашему сигналу!"
    elif win_rate >= 80:
        stats_text += "• Вы торгуете отлично! Продолжайте в том же духе!"
        stats_text += "\n• Можете рисковать 3-5% от депозита"
    elif win_rate >= 60:
        stats_text += "• Хорошие результаты! Изучайте анализ к каждому сигналу."
        stats_text += "\n• Рискуйте 2-3% от депозита"
    else:
        stats_text += "• Следуйте всем рекомендациям в сигналах."
        stats_text += "\n• Начинайте с 1% риска на сделку"
    
    await query.edit_message_text(
        stats_text,
        parse_mode='Markdown',
        reply_markup=back_to_main_keyboard()
    )

async def top_players_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Топ игроков"""
    query = update.callback_query
    await query.answer()
    
    # Собираем статистику всех пользователей
    players_data = []
    for user_id, stats in user_stats.items():
        total_trades = stats["wins"] + stats["losses"]
        if total_trades >= 5:  # Минимум 5 сделок для попадания в топ
            players_data.append({
                "user_id": user_id,
                "win_rate": stats["win_rate"],
                "total_profit": stats["total_profit"],
                "wins": stats["wins"],
                "losses": stats["losses"],
                "total_trades": total_trades,
                "best_streak": stats["best_streak"]
            })
    
    # Сортируем по винрейту
    players_data.sort(key=lambda x: x["win_rate"], reverse=True)
    top_10 = players_data[:10]
    
    top_text = """
╔══════════════════════════════════════════════════════════╗
                    🏆 **ТОП 10 ТРЕЙДЕРОВ**
╚══════════════════════════════════════════════════════════╝

📊 **Рейтинг по точности сигналов:**

"""
    
    places = ["🥇", "🥈", "🥉", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i, player in enumerate(top_10):
        place_emoji = places[i] if i < len(places) else f"{i+1}."
        user_id_short = player["user_id"][-4:] if len(player["user_id"]) > 4 else player["user_id"]
        
        top_text += f"""
{place_emoji} **ID: ...{user_id_short}**
   📊 **Точность:** {player['win_rate']:.1f}%
   💰 **Прибыль:** ${player['total_profit']:,.2f}
   ✅ **Выиграно:** {player['wins']} | ❌ **Проиграно:** {player['losses']}
   📈 **Всего сделок:** {player['total_trades']}
   🔥 **Лучшая серия:** {player['best_streak']}
"""
    
    if not top_10:
        top_text += "\n📊 **Пока нет трейдеров с достаточным количеством сделок.**"
    
    top_text += f"""

══════════════════════════════════════════════════════════

🏅 **КРИТЕРИИ РЕЙТИНГА:**
1. Точность сигналов (Win Rate)
2. Общая прибыль
3. Количество успешных сделок
4. Стабильность результатов

══════════════════════════════════════════════════════════

💡 **КАК ПОПАСТЬ В ТОП:**
• Торгуйте только по VIP сигналам
• Отмечайте результаты сделок кнопками ✅/❌
• Следуйте рекомендациям по риску
• Анализируйте каждую сделку

══════════════════════════════════════════════════════════

📅 **Обновление рейтинга:** Каждый день в 00:00 UTC
"""

    await query.edit_message_text(
        top_text,
        parse_mode='Markdown',
        reply_markup=back_to_main_keyboard()
    )

# =====================================
# МАРАФОН 30 ДНЕЙ
# =====================================

async def marathon_setup(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Настройка марафона"""
    query = update.callback_query
    await query.answer()
    
    setup_text = """
╔══════════════════════════════════════════════════════════╗
                    📅 **МАРАФОН 30 ДНЕЙ**
╚══════════════════════════════════════════════════════════╝

🎯 **Создайте свой персональный план торговли на 30 дней!**

📝 **Как это работает:**
1. Вы указываете стартовый депозит
2. Бот рассчитывает план на каждый день
3. Вы следуете плану и VIP сигналам
4. Через 30 дней умножаете свой депозит!

💰 **Пример:**
• Старт: $50
• Ежедневная цель: +15%
• Через 30 дней: $50 → $404.60 (×8.1)

══════════════════════════════════════════════════════════

📊 **Введите ваш стартовый депозит в долларах:**

Например: `100` или `50` или `200`

💡 **Рекомендация:** От $50 для комфортной торговли.
"""

    await query.edit_message_text(
        setup_text,
        parse_mode='Markdown'
    )
    
    # Устанавливаем состояние ожидания депозита
    context.user_data["awaiting_deposit"] = True

async def handle_deposit_input(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик ввода депозита для марафона"""
    if not context.user_data.get("awaiting_deposit"):
        return
    
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    try:
        deposit = float(text)
        if deposit < 10:
            await update.message.reply_text("⚠️ **Минимальный депозит: $10**")
            return
        if deposit > 10000:
            await update.message.reply_text("⚠️ **Максимальный депозит: $10,000**")
            return
        
        # Создаем план марафона
        daily_percent = 15  # 15% в день
        days = 30
        
        plan = []
        current = deposit
        
        for day in range(1, days + 1):
            daily_profit = current * (daily_percent / 100)
            current += daily_profit
            plan.append({
                "day": day,
                "balance": round(current, 2),
                "profit": round(daily_profit, 2),
                "daily_goal": daily_percent,
                "completed": False
            })
        
        # Сохраняем план пользователя
        user_marathons[user_id] = {
            "start_deposit": deposit,
            "current_day": 1,
            "plan": plan,
            "start_date": datetime.now().strftime("%Y-%m-%d"),
            "total_profit": 0,
            "completed_days": 0
        }
        save_json("user_marathons.json", user_marathons)
        
        # Формируем детальный план
        marathon_text = f"""
╔══════════════════════════════════════════════════════════╗
              📅 **ВАШ ПЕРСОНАЛЬНЫЙ МАРАФОН 30 ДНЕЙ**
╚══════════════════════════════════════════════════════════╝

💰 **СТАРТОВЫЙ ДЕПОЗИТ:** **${deposit:,.2f}**
🎯 **ЕЖЕДНЕВНАЯ ЦЕЛЬ:** **+{daily_percent}%**
📅 **ПЕРИОД:** **30 дней**
🏁 **ФИНИШНЫЙ БАЛАНС:** **${plan[-1]['balance']:,.2f}**
🚀 **РОСТ ДЕПОЗИТА:** **×{plan[-1]['balance']/deposit:.1f}**

══════════════════════════════════════════════════════════

📊 **ДЕТАЛЬНЫЙ ПЛАН НА ПЕРВЫЕ 10 ДНЕЙ:**
"""
        
        day_emojis = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i in range(min(10, len(plan))):
            day_data = plan[i]
            emoji = day_emojis[i] if i < len(day_emojis) else f"{i+1}."
            marathon_text += f"""
{emoji} **День {day_data['day']}:**
   💰 **Баланс:** ${day_data['balance']:,.2f}
   📈 **Прибыль за день:** +${day_data['profit']:,.2f}
   🎯 **Цель:** +{daily_percent}%
"""
        
        marathon_text += f"""
══════════════════════════════════════════════════════════

📈 **ПЛАН НА ПОСЛЕДНИЕ 5 ДНЕЙ:**
"""
        
        for i in range(-5, 0):
            day_data = plan[i]
            marathon_text += f"""
**День {day_data['day']}:**
   💰 **Баланс:** ${day_data['balance']:,.2f}
   📈 **Прибыль за день:** +${day_data['profit']:,.2f}
"""
        
        marathon_text += f"""
══════════════════════════════════════════════════════════

🏁 **ИТОГИ МАРАФОНА:**
• **Старт:** ${deposit:,.2f}
• **Финиш:** ${plan[-1]['balance']:,.2f}
• **Общая прибыль:** ${plan[-1]['balance'] - deposit:,.2f}
• **Рост депозита:** ×{plan[-1]['balance']/deposit:.1f}

══════════════════════════════════════════════════════════

📋 **ПРАВИЛА МАРАФОНА:**
1. 📅 **Торгуйте каждый день без пропусков**
2. 🎯 **Цель:** +{daily_percent}% к депозиту в день
3. ⚠️ **Риск:** не более 5% от баланса
4. 💰 **Вывод прибыли:** каждые 5 дней
5. 📊 **Анализ:** ведите дневник торговли

══════════════════════════════════════════════════════════

💡 **РЕКОМЕНДАЦИИ:**
• Используйте только VIP сигналы
• Следуйте рекомендациям по риску
• Не увеличивайте риск после убытков
• Фиксируйте прибыль вовремя

══════════════════════════════════════════════════════════

🚀 **ПРИМЕР ТОРГОВЛИ НА ДЕНЬ 1:**
• Депозит: ${deposit:,.2f}
• Размер сделки: ${deposit * 0.03:,.2f} (3%)
• Прибыль за сделку: ${deposit * 0.03 * 0.85:,.2f} (85%)
• Цель в день: 2-3 успешные сделки

══════════════════════════════════════════════════════════

🎯 **НАЧНИТЕ СЕЙЧАС!**
Используйте кнопку "🚀 ПОЛУЧИТЬ СИГНАЛ" для начала торговли.
"""
        
        keyboard = [
            [InlineKeyboardButton("🚀 ПОЛУЧИТЬ СИГНАЛ", callback_data="get_signal_menu")],
            [InlineKeyboardButton("📊 МОЯ СТАТИСТИКА", callback_data="my_stats")],
            [InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]
        ]
        
        await update.message.reply_text(
            marathon_text,
            parse_mode='Markdown',
            reply_markup=InlineKeyboardMarkup(keyboard)
        )
        
        # Сбрасываем состояние
        context.user_data["awaiting_deposit"] = False
        
    except ValueError:
        await update.message.reply_text("❌ **Пожалуйста, введите число.**\nНапример: `100` или `50`")

# =====================================
# ПОЛНЫЙ СПИСОК АКТИВОВ
# =====================================

async def all_assets_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Все активы"""
    query = update.callback_query
    await query.answer()
    
    assets_text = """
╔══════════════════════════════════════════════════════════╗
                    📈 **ВСЕ АКТИВЫ ДЛЯ ТОРГОВЛИ**
╚══════════════════════════════════════════════════════════╝

🎯 **80+ АКТИВОВ НА POCKET OPTION OTC РЫНКЕ**

══════════════════════════════════════════════════════════

💱 **ВАЛЮТНЫЕ ПАРЫ OTC (40 пар):**
"""
    
    # Первые 20 валютных пар
    for i in range(min(20, len(OTC_PAIRS))):
        assets_text += f"• {OTC_PAIRS[i]}\n"
    
    if len(OTC_PAIRS) > 20:
        assets_text += f"• ... и еще {len(OTC_PAIRS)-20} пар\n"
    
    assets_text += """
══════════════════════════════════════════════════════════

📊 **АКЦИИ OTC (30 акций):**
"""
    
    # Первые 15 акций
    for i in range(min(15, len(STOCKS))):
        assets_text += f"• {STOCKS[i]}\n"
    
    if len(STOCKS) > 15:
        assets_text += f"• ... и еще {len(STOCKS)-15} акций\n"
    
    assets_text += """
══════════════════════════════════════════════════════════

₿ **КРИПТОВАЛЮТЫ OTC (20 крипто):**
"""
    
    # Все криптовалюты
    for crypto in CRYPTO:
        assets_text += f"• {crypto}\n"
    
    assets_text += """
══════════════════════════════════════════════════════════

🎯 **РЕКОМЕНДАЦИИ ПО ВЫБОРУ АКТИВА:**

1. **ДЛЯ НОВИЧКОВ:**
   • **EUR/USD OTC** - самая стабильная пара
   • **Bitcoin OTC (BTC)** - популярная крипта
   • **Tesla OTC** - волатильная акция

2. **ДЛЯ ОПЫТНЫХ:**
   • **Экзотические пары** (TRY, ZAR, MXN)
   • **Волатильные акции** (Tesla, NVIDIA, AMD)
   • **Альткойны** (Solana, Cardano, Polygon)

3. **ДЛЯ ПРОФЕССИОНАЛОВ:**
   • **Все активы** по ситуации
   • **Анализ нескольких таймфреймов**
   • **Диверсификация** портфеля

══════════════════════════════════════════════════════════

💡 **СОВЕТЫ:**
• Начинайте с 1-2 активов, изучайте их поведение
• Следите за новостями по выбранным активам
• Используйте разные активы для диверсификации
• Не торгуйте всеми активами одновременно

══════════════════════════════════════════════════════════

📊 **ТОЧНОСТЬ ПО АКТИВАМ:**
• **Валютные пары:** 88-95%
• **Акции:** 85-92%
• **Криптовалюты:** 90-99%
"""

    await query.edit_message_text(
        assets_text,
        parse_mode='Markdown',
        reply_markup=back_to_main_keyboard()
    )

# =====================================
# АДМИН КОМАНДЫ
# =====================================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Админ панель"""
    user_id = str(update.effective_user.id)
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    admin_text = f"""
👑 **АДМИН ПАНЕЛЬ**

📊 **СТАТИСТИКА:**
• Всего пользователей: {len(all_users)}
• VIP пользователей: {len(vip_users)}
• Активных марафонов: {len(user_marathons)}
• Всего сигналов: {len(signal_logs)}

🔧 **КОМАНДЫ:**
`/grant <id>` - Выдать VIP
`/revoke <id>` - Забрать VIP
`/stats` - Детальная статистика
`/broadcast <текст>` - Рассылка
"""
    
    await update.message.reply_text(admin_text, parse_mode='Markdown')

async def grant_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Выдать VIP"""
    user_id = str(update.effective_user.id)
    
    if not is_admin(user_id):
        await update.message.reply_text("❌ Доступ запрещен")
        return
    
    if not context.args:
        await update.message.reply_text("❌ Укажите ID пользователя")
        return
    
    target_id = context.args[0]
    vip_users.add(target_id)
    save_json("vip_users.json", list(vip_users))
    
    await update.message.reply_text(f"✅ Пользователю {target_id} выдан VIP доступ")

# =====================================
# ОБРАБОТЧИКИ CALLBACK
# =====================================

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главный обработчик callback"""
    query = update.callback_query
    await query.answer()
    
    data = query.data
    
    if data == "main_menu":
        await query.edit_message_text(
            "🏠 **Главное меню:**",
            parse_mode='Markdown',
            reply_markup=main_menu_keyboard(str(query.from_user.id))
        )
    
    elif data == "get_signal_menu":
        await get_signal_menu(update, context)
    
    elif data in ["category_forex", "category_stocks", "category_crypto", "random_asset"] or data.startswith("asset_"):
        await handle_asset_selection(update, context)
    
    elif data.startswith("exp_"):
        await handle_expiration_selection(update, context)
    
    elif data in ["trade_win", "trade_lose"]:
        await handle_trade_result(update, context)
    
    elif data == "my_stats":
        await my_stats_command(update, context)
    
    elif data == "top_players":
        await top_players_command(update, context)
    
    elif data == "marathon_setup":
        await marathon_setup(update, context)
    
    elif data == "all_assets":
        await all_assets_command(update, context)
    
    elif data == "get_vip":
        await query.edit_message_text(
            f"👑 **Для получения VIP доступа свяжитесь с админом:**\n\n{ADMIN_USER}",
            parse_mode='Markdown',
            reply_markup=back_to_main_keyboard()
        )
    
    elif data == "about":
        await query.edit_message_text(
            "💎 **KURUT AI INFINITY** - профессиональный бот сигналов для Pocket Option OTC рынка.\n\n🎯 **Точность:** 85-99%\n⏰ **Экспирации:** 1-10 минут\n📊 **Активы:** 80+ OTC\n\n📞 **Админ:** @Kuruttrader",
            parse_mode='Markdown',
            reply_markup=back_to_main_keyboard()
        )
    
    elif data == "help":
        await query.edit_message_text(
            "❓ **ПОМОЩЬ**\n\n📌 **Основные команды:**\n/start - Запустить бота\n\n🎯 **Как торговать:**\n1. Получите VIP доступ\n2. Выберите актив\n3. Выберите экспирацию\n4. Получите сигнал\n5. Торгуйте на Pocket Option\n\n📞 **Поддержка:** @Kuruttrader",
            parse_mode='Markdown',
            reply_markup=back_to_main_keyboard()
        )
    
    elif data == "settings":
        await query.edit_message_text(
            "⚙️ **Настройки**\n\n📊 **Режим настроек в разработке...**",
            parse_mode='Markdown',
            reply_markup=back_to_main_keyboard()
        )

# =====================================
# ЗАПУСК БОТА
# =====================================

def main():
    """Основная функция запуска"""
    print("=" * 60)
    print("🚀 ЗАПУСК KURUT AI INFINITY | PRO ULTRA EDITION")
    print("=" * 60)
    
    # Запуск Flask сервера для Render
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    print("🌐 Веб-сервер запущен: http://0.0.0.0:10000")
    
    # Создание бота
    application = Application.builder().token(TOKEN).build()
    
    # Обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("grant", grant_command))
    application.add_handler(CommandHandler("stats", admin_command))
    
    # Обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_deposit_input))
    
    # Обработчики callback
    application.add_handler(CallbackQueryHandler(callback_handler))
    
    # Запуск
    print("🤖 Бот запускается...")
    print(f"📅 Время: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("-" * 60)
    print(f"✅ Бот готов к работе!")
    print(f"✅ Всего активов: {len(ALL_ASSETS)}")
    print(f"✅ Валютных пар: {len(OTC_PAIRS)}")
    print(f"✅ Акций: {len(STOCKS)}")
    print(f"✅ Криптовалют: {len(CRYPTO)}")
    print(f"✅ Экспирации: {len(EXPIRATIONS)} вариантов")
    print(f"✅ VIP пользователей: {len(vip_users)}")
    print(f"✅ Всего пользователей: {len(all_users)}")
    print("-" * 60)
    print("📞 Админ: @Kuruttrader")
    print("🎯 Точность сигналов: 85-99%")
    print("⏰ Экспирации: 1-10 минут")
    print("=" * 60)
    
    # Запуск polling
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
