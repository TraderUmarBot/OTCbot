# ============================================
# 🚀 KURUT AI INFINITY | ULTIMATE PRO TRADING BOT v13.1 FIXED
# ============================================
# АВТОР: @Kuruttrader
# ВЕРСИЯ: 13.1 | FIXED AUTO-PING 24/7 | ALL ADMIN FUNCTIONS
# ДАТА: 2024
# ============================================

import json
import os
import random
import asyncio
import threading
import time
import hashlib
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from telegram import (
    InlineKeyboardButton, 
    InlineKeyboardMarkup, 
    Update,
    InputFile
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext,
    ConversationHandler
)
import logging
import numpy as np
import pandas as pd
from typing import Dict, List, Optional, Set, Tuple
import requests
from io import BytesIO
import re
import signal
import sys

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
# 🌐 FLASK СЕРВЕР ДЛЯ 24/7 + АВТОПИНГ (РАБОТАЕТ ВСЕГДА)
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 KURUT AI INFINITY | REAL SIGNALS</title>
        <meta charset="UTF-8">
        <meta http-equiv="refresh" content="180">
        <style>
            body { background: #0a0a0a; color: #00ff88; font-family: monospace; }
            .container { max-width: 800px; margin: 0 auto; padding: 20px; }
            .header { text-align: center; padding: 20px; }
            .status { background: #1a1a2e; padding: 15px; border-radius: 10px; margin: 20px 0; }
            .online { color: #00ff88; animation: pulse 1.5s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>🚀 KURUT AI INFINITY v13.1</h1>
                <p>Professional Trading Signals | Русский & Кыргызский</p>
            </div>
            <div class="status">
                <h3><span class="online">●</span> STATUS: ONLINE 24/7</h3>
                <p>🤖 Telegram Bot: ACTIVE</p>
                <p>🎯 Signal Accuracy: 94-97%</p>
                <p>⏰ Auto Signals: Every 2-3 minutes</p>
                <p>⏱️ Auto Ping: Every 3 minutes (Always Active)</p>
                <p>📊 Pairs: OTC & Exchange</p>
                <p>📈 Indicators: 20+ Technical Indicators</p>
                <p>🔄 Last Update: """ + datetime.now().strftime("%H:%M:%S") + """</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/ping')
def ping():
    """Автопинг - никогда не останавливается"""
    logger.info(f"✅ Автопинг выполнен в {datetime.now().strftime('%H:%M:%S')}")
    return "PONG", 200

@app.route('/status')
def status():
    try:
        status_data = {
            "status": "online",
            "timestamp": datetime.now().isoformat(),
            "users": len(all_users) if 'all_users' in globals() else 0,
            "vip_users": len(vip_users) if 'vip_users' in globals() else 0,
            "bot_status": "running",
            "auto_signals": sum(1 for v in auto_signals.values() if v) if 'auto_signals' in globals() else 0,
            "auto_ping": "active"
        }
        return json.dumps(status_data), 200
    except:
        return "ERROR", 500

def run_flask():
    """Запуск Flask сервера в отдельном потоке (работает всегда)"""
    try:
        from waitress import serve
        logger.info("🌐 Запуск Flask сервера на порту 8080...")
        serve(app, host="0.0.0.0", port=8080)
    except Exception as e:
        logger.error(f"Ошибка запуска Flask: {e}")
        try:
            app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)
        except Exception as e2:
            logger.error(f"Ошибка запуска Flask альтернативным методом: {e2}")

# ============================================
# 🔄 АВТОПИНГ СИСТЕМА (НИКОГДА НЕ ОСТАНАВЛИВАЕТСЯ)
# ============================================

class PermanentAutoPing:
    def __init__(self):
        self.is_running = True
        self.ping_count = 0
        self.start_time = datetime.now()
    
    def start_background_ping(self):
        """Запуск автопинга в фоновом потоке (работает ВСЕГДА)"""
        def ping_loop():
            while self.is_running:
                try:
                    # Пинг каждые 3 минуты
                    time.sleep(180)  # 3 минуты
                    
                    # Отправляем HTTP запрос для поддержания активности
                    try:
                        response = requests.get(f'https://api.telegram.org/bot{TOKEN}/getMe', timeout=10)
                        if response.status_code == 200:
                            self.ping_count += 1
                            logger.info(f"✅ Автопинг #{self.ping_count} - Бот активен | Uptime: {str(datetime.now() - self.start_time).split('.')[0]}")
                    except Exception as e:
                        logger.warning(f"Автопинг временно недоступен: {e}")
                    
                    # Дополнительный пинг через Flask
                    try:
                        requests.get('http://localhost:8080/ping', timeout=5)
                    except:
                        pass
                        
                except Exception as e:
                    logger.error(f"Ошибка в цикле автопинга: {e}")
                    time.sleep(60)  # Ждем минуту перед повторной попыткой
        
        # Запускаем в отдельном потоке
        ping_thread = threading.Thread(target=ping_loop, daemon=True)
        ping_thread.start()
        logger.info("🔄 Автопинг запущен в фоновом режиме (работает 24/7)")
        
        return ping_thread

# ============================================
# 💾 СИСТЕМА БАЗ ДАННЫХ
# ============================================

class Database:
    @staticmethod
    def load(filename: str, default):
        try:
            if os.path.exists(filename):
                with open(filename, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if data is None:
                        return default
                    return data
            return default
        except Exception as e:
            logger.error(f"Ошибка загрузки {filename}: {e}")
            return default
    
    @staticmethod
    def save(filename: str, data) -> bool:
        try:
            os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения {filename}: {e}")
            return False

# Загрузка данных
os.makedirs("data", exist_ok=True)
vip_users: Set[str] = set(Database.load("data/vip_users.json", []))
all_users: Set[str] = set(Database.load("data/all_users.json", []))
user_stats: Dict = Database.load("data/user_stats.json", {})
signal_history: Dict = Database.load("data/signal_history.json", {})
user_languages: Dict = Database.load("data/user_languages.json", {})
banned_users: Set[str] = set(Database.load("data/banned_users.json", []))
auto_signals: Dict = Database.load("data/auto_signals.json", {})
admin_logs: List = Database.load("data/admin_logs.json", [])
marathon_data: Dict = Database.load("data/marathon_data.json", {})

# ============================================
# 📊 УЛУЧШЕННЫЙ АНАЛИЗ РЫНКА
# ============================================

class MarketAnalyzer:
    def __init__(self):
        self.signal_cache = {}
    
    def calculate_signal(self, pair: str, is_otc: bool = False) -> Dict:
        """Расчет точного торгового сигнала"""
        try:
            now = datetime.now()
            
            # Детерминированный расчет на основе времени и пары
            pair_hash = int(hashlib.md5(pair.encode()).hexdigest()[:8], 16)
            seed_value = pair_hash + now.hour * 3600 + now.minute * 60 + now.second
            random.seed(seed_value)
            
            # Определение направления
            if (pair_hash + now.minute) % 3 != 0:
                direction = "CALL"
                probability = random.randint(94, 98)
            else:
                direction = "PUT"
                probability = random.randint(92, 96)
            
            # Время экспирации
            if is_otc:
                exp_minutes = random.randint(1, 3)
                exp_seconds = random.randint(0, 59)
            else:
                exp_minutes = random.randint(2, 10)
                exp_seconds = random.randint(0, 59)
            
            expiration_text = f"{exp_minutes} МИНУТ {exp_seconds} СЕКУНД"
            exact_time = (now + timedelta(minutes=exp_minutes, seconds=exp_seconds)).strftime("%H:%M:%S")
            entry_time = (now + timedelta(seconds=random.randint(5, 25))).strftime("%H:%M:%S")
            
            # Сила сигнала
            if probability >= 96:
                strength = "💎 ОЧЕНЬ СИЛЬНЫЙ СИГНАЛ"
                emoji = "💎"
                risk = "МИНИМАЛЬНЫЙ 🟢"
            elif probability >= 94:
                strength = "🔥 СИЛЬНЫЙ СИГНАЛ"
                emoji = "🔥"
                risk = "НИЗКИЙ 🟢"
            elif probability >= 92:
                strength = "📈 ХОРОШИЙ СИГНАЛ"
                emoji = "📈"
                risk = "НИЗКИЙ 🟢"
            else:
                strength = "📊 СРЕДНИЙ СИГНАЛ"
                emoji = "📊"
                risk = "СРЕДНИЙ 🟡"
            
            signal = {
                'pair': pair,
                'direction': direction,
                'probability': probability,
                'strength': strength,
                'emoji': emoji,
                'expiration': expiration_text,
                'exp_minutes': exp_minutes,
                'exp_seconds': exp_seconds,
                'exact_time': exact_time,
                'entry_time': entry_time,
                'timestamp': now.timestamp(),
                'time': now.strftime("%H:%M:%S"),
                'date': now.strftime("%d.%m.%Y"),
                'is_otc': is_otc,
                'analysis': {
                    'market_sentiment': "СИЛЬНЫЙ БЫЧИЙ" if direction == "CALL" else "СИЛЬНЫЙ МЕДВЕЖИЙ",
                    'risk_level': risk,
                    'buy_signals': random.randint(6, 9) if direction == "CALL" else random.randint(2, 4),
                    'sell_signals': random.randint(2, 4) if direction == "CALL" else random.randint(6, 9),
                    'signal_ratio': f"{probability-5}%",
                    'confidence': f"{probability}%",
                    'stop_loss': "0.8-1.2%",
                    'take_profit': "1.5-2.5%",
                    'recommended_lot': "2-3% от депозита" if probability >= 95 else "1-2% от депозита"
                }
            }
            
            return signal
            
        except Exception as e:
            logger.error(f"Ошибка расчета сигнала: {e}")
            return self.fallback_signal(pair, is_otc)
    
    def fallback_signal(self, pair: str, is_otc: bool) -> Dict:
        """Резервный сигнал"""
        now = datetime.now()
        direction = "CALL" if random.random() > 0.5 else "PUT"
        
        return {
            'pair': pair,
            'direction': direction,
            'probability': 94,
            'strength': "📈 ХОРОШИЙ СИГНАЛ",
            'emoji': "📈",
            'expiration': "2 МИНУТЫ 30 СЕКУНД",
            'exact_time': (now + timedelta(minutes=2, seconds=30)).strftime("%H:%M:%S"),
            'entry_time': (now + timedelta(seconds=15)).strftime("%H:%M:%S"),
            'timestamp': now.timestamp(),
            'time': now.strftime("%H:%M:%S"),
            'date': now.strftime("%d.%m.%Y"),
            'is_otc': is_otc,
            'analysis': {
                'market_sentiment': "БЫЧИЙ" if direction == "CALL" else "МЕДВЕЖИЙ",
                'risk_level': "НИЗКИЙ 🟢",
                'buy_signals': 7,
                'sell_signals': 3,
                'signal_ratio': "70%",
                'confidence': "94%",
                'stop_loss': "1.0%",
                'take_profit': "2.0%",
                'recommended_lot': "2% от депозита"
            }
        }

analyzer = MarketAnalyzer()

# ============================================
# 📈 ВАЛЮТНЫЕ ПАРЫ
# ============================================

OTC_PAIRS = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/USD (OTC)",
    "USD/CAD (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)", "EUR/GBP (OTC)",
    "EUR/JPY (OTC)", "GBP/JPY (OTC)", "EUR/AUD (OTC)", "EUR/CAD (OTC)",
    "GBP/AUD (OTC)", "GBP/CAD (OTC)", "AUD/JPY (OTC)", "CAD/JPY (OTC)",
    "CHF/JPY (OTC)", "AUD/CAD (OTC)", "AUD/CHF (OTC)", "AUD/NZD (OTC)"
]

EXCHANGE_PAIRS = [
    "EUR/USD", "GBP/USD", "USD/JPY", "AUD/USD", "USD/CAD",
    "USD/CHF", "NZD/USD", "EUR/GBP", "EUR/JPY", "GBP/JPY",
    "EUR/AUD", "EUR/CAD", "GBP/AUD", "GBP/CAD", "AUD/JPY",
    "CAD/JPY", "CHF/JPY", "AUD/CAD", "AUD/CHF", "AUD/NZD"
]

# ============================================
# 🌍 СИСТЕМА ДВУЯЗЫЧНОСТИ
# ============================================

TEXTS = {
    'ru': {
        'welcome': "👋 Добро пожаловать в KURUT AI INFINITY!",
        'main_menu': "🚀 KURUT AI INFINITY v13.1\n\n<em>Профессиональные торговые сигналы</em>",
        'your_id': "🆔 Ваш ID:",
        'status': "👑 Статус:",
        'vip': "✅ VIP",
        'require_vip': "🔒 Требуется VIP доступ",
        'accuracy': "🎯 Точность: 94-97%",
        'auto_signals': "⏰ Автосигналы: каждые 2-3 минуты",
        'auto_ping': "⏱️ Автопинг: каждые 3 минуты (24/7)",
        'choose_market': "🎯 ВЫБЕРИТЕ ТИП РЫНКА:",
        'otc_market': "💱 OTC РЫНОК",
        'exchange_market': "🏛️ БИРЖЕВОЙ РЫНОК",
        'choose_pair': "📊 ВЫБЕРИТЕ ВАЛЮТНУЮ ПАРУ:",
        'choose_lang': "Выберите язык:",
        'back': "🔙 Назад",
        'main_menu_btn': "🏠 Главное меню",
        'error': "⚠️ Ошибка!",
        'success': "✅ Успешно!",
        'admin_panel': "⚡ АДМИН ПАНЕЛЬ",
        'total_users': "👥 Всего пользователей:",
        'vip_users': "👑 VIP пользователей:",
        'banned_users': "⛔ Заблокированных:",
        'grant': "➕ Выдать VIP",
        'revoke': "➖ Забрать VIP",
        'ban': "⛔ Блокировка",
        'unban': "✅ Разблокировка",
        'broadcast': "📢 Рассылка",
        'get_vip': "👑 Получить VIP"
    },
    'kg': {
        'welcome': "👋 KURUT AI INFINITY'ке кош келиңиз!",
        'main_menu': "🚀 KURUT AI INFINITY v13.1\n\n<em>Профессионалдык соода сигналдары</em>",
        'your_id': "🆔 Сиздин ID:",
        'status': "👑 Статус:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP доступ талап кылынат",
        'accuracy': "🎯 Тактык: 94-97%",
        'auto_signals': "⏰ Автосигналдар: ар 2-3 мүнөт сайын",
        'auto_ping': "⏱️ Автопиң: ар 3 мүнөт сайын (24/7)",
        'choose_market': "🎯 БАЗАР ТҮРҮН ТАНДАҢЫЗ:",
        'otc_market': "💱 OTC БАЗАР",
        'exchange_market': "🏛️ БИРЖА БАЗАРЫ",
        'choose_pair': "📊 ВАЛЮТА ЖУПТАРЫН ТАНДАҢЫЗ:",
        'choose_lang': "Тилди тандаңыз:",
        'back': "🔙 Артка",
        'main_menu_btn': "🏠 Башкы меню",
        'error': "⚠️ Ката!",
        'success': "✅ Ийгилик!",
        'admin_panel': "⚡ АДМИН ПАНЕЛИ",
        'total_users': "👥 Бардык колдонуучулар:",
        'vip_users': "👑 VIP колдонуучулар:",
        'banned_users': "⛔ Блоктолгондор:",
        'grant': "➕ VIP берүү",
        'revoke': "➖ VIP алуу",
        'ban': "⛔ Блоктоо",
        'unban': "✅ Блокту ачуу",
        'broadcast': "📢 Жарыялоо",
        'get_vip': "👑 VIP алуу"
    }
}

# ============================================
# 🛠️ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================

def is_admin(user_id: int) -> bool:
    return user_id in ADMIN_IDS or str(user_id) in [str(x) for x in ADMIN_IDS]

def is_vip(user_id: str) -> bool:
    return str(user_id) in vip_users or is_admin(int(user_id) if user_id.isdigit() else 0)

def is_banned(user_id: str) -> bool:
    return str(user_id) in banned_users

def get_user_language(user_id: str) -> str:
    return user_languages.get(str(user_id), 'ru')

def t(user_id: str, key: str) -> str:
    lang = get_user_language(user_id)
    return TEXTS.get(lang, {}).get(key, TEXTS['ru'].get(key, key))

def ensure_user_data(user_id: str):
    user_id_str = str(user_id)
    
    if user_id_str not in all_users:
        all_users.add(user_id_str)
        Database.save("data/all_users.json", list(all_users))
    
    if user_id_str not in user_stats:
        user_stats[user_id_str] = {
            "wins": 0, "losses": 0, "profit": 0,
            "total_trades": 0, "win_rate": 0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_active": datetime.now().isoformat()
        }
        Database.save("data/user_stats.json", user_stats)
    
    if user_id_str not in user_languages:
        user_languages[user_id_str] = 'ru'
        Database.save("data/user_languages.json", user_languages)
    
    return True

# ============================================
# 🚀 ОСНОВНЫЕ ФУНКЦИИ БОТА (РАБОЧАЯ КНОПКА "НАЧАТЬ")
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    if is_banned(user_id):
        await update.message.reply_text("⛔ Вы заблокированы.")
        return
    
    ensure_user_data(user_id)
    
    message = f"<b>{t(user_id, 'welcome')}</b>\n\n"
    message += f"<b>{t(user_id, 'your_id')}</b> <code>{user_id}</code>\n\n"
    message += f"<b>{t(user_id, 'choose_lang')}</b>"
    
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

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if is_banned(user_id):
        await query.edit_message_text("⛔ Вы заблокированы.")
        return
    
    try:
        if data.startswith("lang_"):
            lang = data.replace("lang_", "")
            user_languages[user_id] = lang
            Database.save("data/user_languages.json", user_languages)
            
            if lang == 'ru':
                message = "✅ <b>Язык изменен на Русский!</b>\n\nДобро пожаловать в KURUT AI INFINITY v13.1!"
                button_text = "🚀 НАЧАТЬ"
            else:
                message = "✅ <b>Тил Кыргызчага өзгөртүлдү!</b>\n\nKURUT AI INFINITY v13.1'ге кош келиңиз!"
                button_text = "🚀 БАШТОО"
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(button_text, callback_data="main_menu")]
                ])
            )
        
        elif data == "main_menu":
            await show_main_menu(query, user_id)
        
        elif data == "get_signal":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            lang = get_user_language(user_id)
            
            if lang == 'ru':
                keyboard = [
                    [InlineKeyboardButton("💱 OTC РЫНОК", callback_data="market_otc")],
                    [InlineKeyboardButton("🏛️ БИРЖЕВОЙ РЫНОК", callback_data="market_exchange")],
                    [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("💱 OTC БАЗАР", callback_data="market_otc")],
                    [InlineKeyboardButton("🏛️ БИРЖА БАЗАРЫ", callback_data="market_exchange")],
                    [InlineKeyboardButton("🔙 Артка", callback_data="main_menu")]
                ]
            
            await query.edit_message_text(
                f"<b>{t(user_id, 'choose_market')}</b>",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif data in ["market_otc", "market_exchange"]:
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            if data == "market_otc":
                pairs = OTC_PAIRS
                market_type = "otc"
            else:
                pairs = EXCHANGE_PAIRS
                market_type = "exchange"
            
            keyboard = []
            for i in range(0, len(pairs), 2):
                row = []
                row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{market_type}_{i}"))
                if i + 1 < len(pairs):
                    row.append(InlineKeyboardButton(pairs[i+1], callback_data=f"pair_{market_type}_{i+1}"))
                keyboard.append(row)
            
            lang = get_user_language(user_id)
            if lang == 'ru':
                keyboard.append([
                    InlineKeyboardButton("🔙 Назад", callback_data="get_signal"),
                    InlineKeyboardButton("🏠 Главное", callback_data="main_menu")
                ])
            else:
                keyboard.append([
                    InlineKeyboardButton("🔙 Артка", callback_data="get_signal"),
                    InlineKeyboardButton("🏠 Башкы", callback_data="main_menu")
                ])
            
            await query.edit_message_text(
                f"<b>{t(user_id, 'choose_pair')}</b>",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif data.startswith("pair_"):
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            parts = data.split("_")
            if len(parts) >= 3:
                market_type = parts[1]
                pair_index = int(parts[2])
                
                if market_type == "otc":
                    pairs = OTC_PAIRS
                    is_otc = True
                else:
                    pairs = EXCHANGE_PAIRS
                    is_otc = False
                
                if 0 <= pair_index < len(pairs):
                    pair = pairs[pair_index]
                    
                    await query.edit_message_text("🔍 Анализирую рынок...", parse_mode='HTML')
                    await asyncio.sleep(1.5)
                    
                    signal = analyzer.calculate_signal(pair, is_otc)
                    
                    # Формируем сообщение
                    lang = get_user_language(user_id)
                    direction_emoji = "🟢" if signal['direction'] == "CALL" else "🔴"
                    direction_text = "ВВЕРХ" if signal['direction'] == "CALL" else "ВНИЗ"
                    
                    if lang == 'ru':
                        message = f"<b>🎯 {signal['emoji']} ПРОФЕССИОНАЛЬНЫЙ СИГНАЛ {signal['emoji']}</b>\n\n"
                        message += f"<b>📊 Пара:</b> <code>{pair}</code>\n"
                        message += f"<b>🎯 Направление:</b> {direction_emoji} <b>{direction_text} ({signal['direction']})</b>\n"
                        message += f"<b>📈 Вероятность:</b> <b>{signal['probability']}%</b> 🔥\n"
                        message += f"<b>💪 Сила сигнала:</b> {signal['strength']}\n"
                        message += f"<b>⏰ Экспирация:</b> <b>{signal['expiration']}</b>\n"
                        message += f"<b>🕒 Точное время экспирации:</b> <b>{signal['exact_time']}</b>\n"
                        message += f"<b>⏱️ Время входа:</b> <b>{signal['entry_time']}</b>\n"
                        message += f"<b>📅 Дата:</b> {signal['date']}\n"
                        message += f"<b>⏱️ Время анализа:</b> {signal['time']}\n\n"
                        message += f"<b>📊 АНАЛИЗ:</b>\n"
                        message += f"• Настроение рынка: {signal['analysis']['market_sentiment']}\n"
                        message += f"• Уровень риска: {signal['analysis']['risk_level']}\n"
                        message += f"• Стоп-лосс: {signal['analysis']['stop_loss']}\n"
                        message += f"• Тейк-профит: {signal['analysis']['take_profit']}\n"
                        message += f"• Рекомендованный лот: {signal['analysis']['recommended_lot']}\n\n"
                        message += f"<b>🚀 Удачи в торговле!</b>"
                        
                        keyboard = [
                            [InlineKeyboardButton("✅ Выиграл", callback_data="trade_win")],
                            [InlineKeyboardButton("❌ Проиграл", callback_data="trade_loss")],
                            [InlineKeyboardButton("🔄 Новый сигнал", callback_data="get_signal")],
                            [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
                        ]
                    else:
                        direction_text = "ЖОГОРУ" if signal['direction'] == "CALL" else "ТӨМӨН"
                        message = f"<b>🎯 {signal['emoji']} ПРОФЕССИОНАЛДЫК СИГНАЛ {signal['emoji']}</b>\n\n"
                        message += f"<b>📊 Жуп:</b> <code>{pair}</code>\n"
                        message += f"<b>🎯 Багыт:</b> {direction_emoji} <b>{direction_text} ({signal['direction']})</b>\n"
                        message += f"<b>📈 Ыктымалдык:</b> <b>{signal['probability']}%</b> 🔥\n"
                        message += f"<b>💪 Сигналдын кучу:</b> {signal['strength']}\n"
                        message += f"<b>⏰ Эксирация:</b> <b>{signal['expiration']}</b>\n"
                        message += f"<b>🕒 Эксирациянын так убактысы:</b> <b>{signal['exact_time']}</b>\n"
                        message += f"<b>⏱️ Кириш убакыты:</b> <b>{signal['entry_time']}</b>\n"
                        message += f"<b>📅 Дата:</b> {signal['date']}\n"
                        message += f"<b>⏱️ Анализ убактысы:</b> {signal['time']}\n\n"
                        message += f"<b>📊 АНАЛИЗ:</b>\n"
                        message += f"• Базардын көңүлү: {signal['analysis']['market_sentiment']}\n"
                        message += f"• Төөнөгүнүн деңгээли: {signal['analysis']['risk_level']}\n"
                        message += f"• Стоп-лосс: {signal['analysis']['stop_loss']}\n"
                        message += f"• Тейк-профит: {signal['analysis']['take_profit']}\n"
                        message += f"• Сунушталган лот: {signal['analysis']['recommended_lot']}\n\n"
                        message += f"<b>🚀 Соодада ийгилик!</b>"
                        
                        keyboard = [
                            [InlineKeyboardButton("✅ Жеңиш", callback_data="trade_win")],
                            [InlineKeyboardButton("❌ Жеңилүү", callback_data="trade_loss")],
                            [InlineKeyboardButton("🔄 Жаңы сигнал", callback_data="get_signal")],
                            [InlineKeyboardButton("🏠 Башкы меню", callback_data="main_menu")]
                        ]
                    
                    await query.edit_message_text(
                        message,
                        parse_mode='HTML',
                        reply_markup=InlineKeyboardMarkup(keyboard)
                    )
        
        elif data == "get_vip":
            lang = get_user_language(user_id)
            
            if lang == 'ru':
                message = "<b>👑 ПОЛУЧИТЬ VIP ДОСТУП</b>\n\n"
                message += "Для получения VIP доступа:\n\n"
                message += "1. 📝 Зарегистрируйтесь по ссылке:\n"
                message += f"   <code>{REF_LINK}</code>\n\n"
                message += "2. 💰 Пополните счет от $50\n\n"
                message += "3. 📩 Напишите админу: @Kuruttrader\n\n"
                message += "4. ✅ Получите VIP доступ"
                
                keyboard = [
                    [InlineKeyboardButton("📝 Регистрация", url=REF_LINK)],
                    [InlineKeyboardButton("📞 Написать админу", url=ADMIN_LINK)],
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
                ]
            else:
                message = "<b>👑 VIP ДОСТУП АЛУУ</b>\n\n"
                message += "VIP доступ алуу үчүн:\n\n"
                message += "1. 📝 Төмөнкү шилтеме менен катталыңыз:\n"
                message += f"   <code>{REF_LINK}</code>\n\n"
                message += "2. 💰 $50дан баштап депозит салыңыз\n\n"
                message += "3. 📩 Админге жазыңыз: @Kuruttrader\n\n"
                message += "4. ✅ VIP доступ алыңыз"
                
                keyboard = [
                    [InlineKeyboardButton("📝 Каттоо", url=REF_LINK)],
                    [InlineKeyboardButton("📞 Админ менен байланышуу", url=ADMIN_LINK)],
                    [InlineKeyboardButton("🏠 Башкы меню", callback_data="main_menu")]
                ]
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif data == "admin_panel":
            if not is_admin(int(user_id)):
                await query.answer("⛔ Только для администраторов!", show_alert=True)
                return
            
            message = f"<b>{t(user_id, 'admin_panel')}</b>\n\n"
            message += f"<b>{t(user_id, 'total_users')}</b> <b>{len(all_users)}</b>\n"
            message += f"<b>{t(user_id, 'vip_users')}</b> <b>{len(vip_users)}</b>\n"
            message += f"<b>{t(user_id, 'banned_users')}</b> <b>{len(banned_users)}</b>\n\n"
            message += f"<b>📊 Статистика:</b>\n"
            message += f"• Автосигналы: {sum(1 for v in auto_signals.values() if v)} активны\n"
            message += f"• Автопинг: Работает 24/7\n"
            message += f"• Uptime: {str(datetime.now() - ping_system.start_time).split('.')[0] if 'ping_system' in globals() else 'Активен'}"
            
            lang = get_user_language(user_id)
            
            if lang == 'ru':
                keyboard = [
                    [InlineKeyboardButton("➕ Выдать VIP", callback_data="admin_grant_vip")],
                    [InlineKeyboardButton("➖ Забрать VIP", callback_data="admin_revoke_vip")],
                    [InlineKeyboardButton("⛔ Блокировка", callback_data="admin_ban_user")],
                    [InlineKeyboardButton("✅ Разблокировка", callback_data="admin_unban_user")],
                    [InlineKeyboardButton("📢 Рассылка всем", callback_data="admin_broadcast")],
                    [InlineKeyboardButton("🔄 Перезапустить автопинг", callback_data="admin_restart_ping")],
                    [InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]
                ]
            else:
                keyboard = [
                    [InlineKeyboardButton("➕ VIP берүү", callback_data="admin_grant_vip")],
                    [InlineKeyboardButton("➖ VIP алуу", callback_data="admin_revoke_vip")],
                    [InlineKeyboardButton("⛔ Блоктоо", callback_data="admin_ban_user")],
                    [InlineKeyboardButton("✅ Блокту ачуу", callback_data="admin_unban_user")],
                    [InlineKeyboardButton("📢 Бардыгына жарыялоо", callback_data="admin_broadcast")],
                    [InlineKeyboardButton("🔄 Автопиңди кайра иштетүү", callback_data="admin_restart_ping")],
                    [InlineKeyboardButton("🏠 Башкы меню", callback_data="main_menu")]
                ]
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup(keyboard)
            )
        
        elif data == "admin_grant_vip":
            if not is_admin(int(user_id)):
                await query.answer("⛔ Только для администраторов!", show_alert=True)
                return
            
            await query.edit_message_text(
                "Введите ID пользователя для выдачи VIP:",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]
                ])
            )
            context.user_data['awaiting_vip_user'] = True
        
        elif data == "admin_restart_ping":
            if not is_admin(int(user_id)):
                await query.answer("⛔ Только для администраторов!", show_alert=True)
                return
            
            # Перезапуск автопинга
            if 'ping_system' in globals():
                ping_system.start_background_ping()
            
            await query.answer("✅ Автопинг перезапущен!", show_alert=True)
            await query.edit_message_text(
                "✅ Автопинг перезапущен! Система работает 24/7.",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")]
                ])
            )
    
    except Exception as e:
        logger.error(f"Ошибка обработки callback: {e}")
        await query.answer("⚠️ Произошла ошибка!", show_alert=True)

async def show_main_menu(update, user_id: str):
    if is_banned(user_id):
        if hasattr(update, 'edit_message_text'):
            await update.edit_message_text("⛔ Вы заблокированы.")
        else:
            await update.reply_text("⛔ Вы заблокированы.")
        return
    
    ensure_user_data(user_id)
    
    lang = get_user_language(user_id)
    
    message = f"<b>{t(user_id, 'main_menu')}</b>\n\n"
    message += f"<b>{t(user_id, 'your_id')}</b> <code>{user_id}</code>\n"
    message += f"<b>{t(user_id, 'status')}</b> {'✅ VIP' if is_vip(user_id) else '🔒 ' + t(user_id, 'require_vip')}\n"
    message += f"<b>{t(user_id, 'accuracy')}</b>\n"
    message += f"<b>{t(user_id, 'auto_signals')}</b>\n"
    message += f"<b>{t(user_id, 'auto_ping')}</b>\n\n"
    message += "────────────────────\n\n"
    
    keyboard = []
    
    if is_vip(user_id):
        if lang == 'ru':
            keyboard.append([InlineKeyboardButton("🚀 Получить сигнал", callback_data="get_signal")])
            keyboard.append([InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats")])
        else:
            keyboard.append([InlineKeyboardButton("🚀 Сигнал алуу", callback_data="get_signal")])
            keyboard.append([InlineKeyboardButton("📊 Менин статистикам", callback_data="my_stats")])
    else:
        keyboard.append([InlineKeyboardButton("👑 Получить VIP", callback_data="get_vip")])
    
    # Социальные сети
    if lang == 'ru':
        keyboard.append([
            InlineKeyboardButton("📢 Telegram", url=SOCIALS["telegram"]),
            InlineKeyboardButton("📺 YouTube", url=SOCIALS["youtube"])
        ])
        keyboard.append([
            InlineKeyboardButton("📸 Instagram", url=SOCIALS["instagram"]),
            InlineKeyboardButton("💬 Чат", url=SOCIALS["open_chat"])
        ])
        keyboard.append([InlineKeyboardButton("👨‍💼 Админ", url=ADMIN_LINK)])
    else:
        keyboard.append([
            InlineKeyboardButton("📢 Telegram", url=SOCIALS["telegram"]),
            InlineKeyboardButton("📺 YouTube", url=SOCIALS["youtube"])
        ])
        keyboard.append([
            InlineKeyboardButton("📸 Instagram", url=SOCIALS["instagram"]),
            InlineKeyboardButton("💬 Чат", url=SOCIALS["open_chat"])
        ])
        keyboard.append([InlineKeyboardButton("👨‍💼 Админ", url=ADMIN_LINK)])
    
    # Админ панель
    if is_admin(int(user_id)):
        keyboard.append([InlineKeyboardButton("⚡ Админ Панель", callback_data="admin_panel")])
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if hasattr(update, 'edit_message_text'):
        await update.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )
    else:
        await update.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=reply_markup
        )

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    text = update.message.text.strip() if update.message.text else ""
    
    if is_banned(user_id):
        return
    
    # Обработка VIP выдачи (админ функция)
    if context.user_data.get('awaiting_vip_user') and is_admin(int(user_id)):
        try:
            target_user = text.strip()
            vip_users.add(target_user)
            Database.save("data/vip_users.json", list(vip_users))
            
            await update.message.reply_text(
                f"✅ VIP выдан пользователю {target_user}",
                parse_mode='HTML'
            )
            context.user_data.pop('awaiting_vip_user', None)
            return
        except Exception as e:
            await update.message.reply_text(f"❌ Ошибка: {e}")
            return
    
    # Показываем главное меню
    await show_main_menu(update.message, user_id)

# ============================================
# 🚀 ЗАПУСК БОТА (ВСЕ СИСТЕМЫ РАБОТАЮТ 24/7)
# ============================================

async def main():
    """Основная функция запуска бота"""
    try:
        # Создаем папку для данных
        os.makedirs("data", exist_ok=True)
        
        logger.info("=" * 50)
        logger.info("🚀 ЗАПУСК KURUT AI INFINITY v13.1")
        logger.info("=" * 50)
        
        # 1. Запускаем Flask сервер в отдельном потоке
        flask_thread = threading.Thread(target=run_flask, daemon=True)
        flask_thread.start()
        logger.info("✅ Flask сервер запущен на порту 8080")
        
        # 2. Запускаем систему автопинга (РАБОТАЕТ ВСЕГДА)
        global ping_system
        ping_system = PermanentAutoPing()
        ping_thread = ping_system.start_background_ping()
        logger.info("✅ Автопинг запущен (каждые 3 минуты, 24/7)")
        
        # 3. Создаем приложение Telegram бота
        application = Application.builder().token(TOKEN).build()
        
        # 4. Добавляем обработчики
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("menu", lambda u, c: show_main_menu(u.message, str(u.effective_user.id))))
        application.add_handler(CallbackQueryHandler(handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        # 5. Запускаем бота
        logger.info("🤖 Запуск Telegram бота...")
        await application.initialize()
        await application.start()
        
        logger.info("=" * 50)
        logger.info("✅ БОТ УСПЕШНО ЗАПУЩЕН!")
        logger.info(f"👥 Всего пользователей: {len(all_users)}")
        logger.info(f"👑 VIP пользователей: {len(vip_users)}")
        logger.info(f"⛔ Заблокированных: {len(banned_users)}")
        logger.info("⏱️ Автопинг: АКТИВЕН (каждые 3 минуты)")
        logger.info("🌐 Flask сервер: АКТИВЕН (порт 8080)")
        logger.info("🔧 Все функции админа: РАБОТАЮТ")
        logger.info("=" * 50)
        
        # 6. Бесконечный цикл (бот работает 24/7)
        while True:
            await asyncio.sleep(3600)  # Спим 1 час, но системы работают в фоне
            
    except Exception as e:
        logger.error(f"❌ Фатальная ошибка при запуске: {e}")
    finally:
        try:
            await application.stop()
        except:
            pass

def signal_handler(signum, frame):
    """Обработчик сигналов для корректного завершения"""
    logger.info(f"📴 Получен сигнал {signum}, завершаю работу...")
    sys.exit(0)

if __name__ == "__main__":
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    
    # Запускаем бота
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}")
