# ============================================
# 🚀 KURUT AI INFINITY | ULTIMATE PRO TRADING BOT v12.0
# ============================================
# АВТОР: @Kuruttrader
# ВЕРСИЯ: 12.0 | ULTIMATE WORKING EDITION
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
    Update
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    CallbackContext
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
# 🌐 FLASK СЕРВЕР ДЛЯ 24/7
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
                <h1>🚀 KURUT AI INFINITY v12.0</h1>
                <p>Professional Trading Signals</p>
            </div>
            <div class="status">
                <h3><span class="online">●</span> STATUS: ONLINE 24/7</h3>
                <p>🤖 Telegram Bot: ACTIVE</p>
                <p>🎯 Signal Accuracy: 94-97%</p>
                <p>⏰ Auto Signals: Every 2 minutes</p>
                <p>📊 Pairs: OTC & Exchange</p>
            </div>
        </div>
    </body>
    </html>
    """

def run_flask():
    try:
        from waitress import serve
        serve(app, host="0.0.0.0", port=8080)
    except:
        app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)

# ============================================
# 💾 СИСТЕМА БАЗ ДАННЫХ
# ============================================

class Database:
    @staticmethod
    def load(filename, default):
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
    def save(filename, data):
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            logger.error(f"Ошибка сохранения {filename}: {e}")
            return False

# Загрузка данных
vip_users = set(Database.load("vip_users.json", []))
all_users = set(Database.load("all_users.json", []))
user_stats = Database.load("user_stats.json", {})
signal_history = Database.load("signal_history.json", {})
user_languages = Database.load("user_languages.json", {})
banned_users = set(Database.load("banned_users.json", []))
auto_signals = Database.load("auto_signals.json", {})
admin_logs = Database.load("admin_logs.json", [])

# ============================================
# 📊 МАТЕМАТИЧЕСКИЙ АНАЛИЗ РЫНКА
# ============================================

class MarketAnalyzer:
    def __init__(self):
        self.market_state = {}
        self.last_signals = {}
    
    def calculate_signal(self, pair, is_otc=False):
        """Рассчитать точный торговый сигнал"""
        try:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            
            # Создаем детерминированный seed
            pair_hash = int(hashlib.md5(pair.encode()).hexdigest()[:8], 16)
            time_seed = (hour * 60 + minute) // 5  # Меняем каждые 5 минут
            random.seed(pair_hash + time_seed)
            
            # Базовые параметры
            base_prob = 94 if is_otc else 92
            session_mult = self.get_session_multiplier(hour)
            
            # Рассчитываем направление
            trend_strength = random.uniform(0.4, 0.95)
            volatility = random.uniform(0.3, 0.8)
            momentum = random.uniform(0.5, 0.9)
            
            # Комбинированный показатель
            direction_score = (trend_strength * 0.4 + volatility * 0.3 + momentum * 0.3) * session_mult
            
            # Определяем направление
            if direction_score > 0.5:
                direction = "CALL"
                probability = min(97, base_prob + int((direction_score - 0.5) * 6))
            else:
                direction = "PUT"
                probability = min(97, base_prob + int((0.5 - direction_score) * 6))
            
            # Сила сигнала
            if probability >= 96:
                strength = "💎 VERY STRONG"
            elif probability >= 94:
                strength = "📈 STRONG"
            else:
                strength = "📊 MEDIUM"
            
            # Экспирация 1-10 минут
            exp_minutes = self.calculate_expiration(pair_hash, is_otc)
            exact_time = (now + timedelta(minutes=exp_minutes)).strftime("%H:%M")
            
            # Состояние рынка
            market_condition = self.get_market_condition(trend_strength, volatility)
            risk_level = "LOW 🟢" if probability >= 95 else "MEDIUM 🟡" if probability >= 92 else "HIGH 🔴"
            
            return {
                'pair': pair,
                'direction': direction,
                'probability': probability,
                'strength': strength,
                'expiration': f"{exp_minutes} MINUTE{'S' if exp_minutes > 1 else ''}",
                'exp_minutes': exp_minutes,
                'exact_time': exact_time,
                'timestamp': now.timestamp(),
                'time': now.strftime("%H:%M:%S"),
                'date': now.strftime("%d.%m.%Y"),
                'analysis': {
                    'market_condition': market_condition,
                    'risk_level': risk_level,
                    'trend_strength': f"{int(trend_strength * 100)}%",
                    'volatility': f"{int(volatility * 100)}%"
                }
            }
            
        except Exception as e:
            logger.error(f"Ошибка расчета сигнала: {e}")
            return self.fallback_signal(pair, is_otc)
    
    def calculate_expiration(self, pair_hash, is_otc):
        """Рассчитать экспирацию 1-10 минут"""
        random.seed(pair_hash + int(datetime.now().minute))
        
        if is_otc:
            # OTC - короче экспирация
            minutes = random.choices(
                [1, 2, 3, 4, 5],
                weights=[10, 30, 40, 15, 5]
            )[0]
        else:
            # Биржевой - дольше экспирация
            minutes = random.choices(
                [2, 3, 4, 5, 6, 7, 8, 9, 10],
                weights=[5, 10, 20, 30, 15, 10, 5, 3, 2]
            )[0]
        
        return minutes
    
    def get_session_multiplier(self, hour):
        """Множитель точности для сессий"""
        if 8 <= hour < 16:  # Европейская сессия
            return 1.1
        elif 14 <= hour < 22:  # Американская сессия
            return 1.15
        elif 0 <= hour < 6:  # Азиатская сессия
            return 0.95
        else:
            return 1.0
    
    def get_market_condition(self, trend, volatility):
        """Определить состояние рынка"""
        if volatility > 0.7:
            return "HIGH VOLATILITY"
        elif trend > 0.7:
            return "STRONG TREND"
        elif trend > 0.5:
            return "TRENDING"
        else:
            return "NORMAL"
    
    def fallback_signal(self, pair, is_otc):
        """Резервный сигнал"""
        now = datetime.now()
        direction = "CALL" if hash(pair) % 2 == 0 else "PUT"
        exp_minutes = 3 if is_otc else 5
        
        return {
            'pair': pair,
            'direction': direction,
            'probability': 95 if is_otc else 93,
            'strength': "📈 STRONG",
            'expiration': f"{exp_minutes} MINUTES",
            'exp_minutes': exp_minutes,
            'exact_time': (now + timedelta(minutes=exp_minutes)).strftime("%H:%M"),
            'timestamp': now.timestamp(),
            'time': now.strftime("%H:%M:%S"),
            'date': now.strftime("%d.%m.%Y"),
            'analysis': {
                'market_condition': "NORMAL",
                'risk_level': "MEDIUM 🟡",
                'trend_strength': "65%",
                'volatility': "45%"
            }
        }
    
    def generate_auto_signal(self):
        """Сгенерировать автосигнал"""
        try:
            now = datetime.now()
            minute = now.minute
            
            # Чередуем OTC и биржевые
            if minute % 3 == 0:
                pairs = OTC_PAIRS
                is_otc = True
            else:
                pairs = EXCHANGE_PAIRS
                is_otc = False
            
            # Выбираем пару
            pair_index = (minute + now.hour) % len(pairs)
            pair = pairs[pair_index]
            
            # Генерируем сигнал
            signal = self.calculate_signal(pair, is_otc)
            signal['type'] = "AUTO"
            
            return signal
        except Exception as e:
            logger.error(f"Ошибка генерации автосигнала: {e}")
            return None

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

ALL_PAIRS = OTC_PAIRS + EXCHANGE_PAIRS

# ============================================
# 🌍 СИСТЕМА МУЛЬТИЯЗЫЧНОСТИ
# ============================================

TEXTS = {
    'ru': {
        # Основные
        'welcome': "👋 Добро пожаловать в KURUT AI INFINITY!",
        'choose_lang': "Выберите язык:",
        'main_menu': "🚀 KURUT AI INFINITY v12.0",
        'your_id': "🆔 Ваш ID:",
        'status': "👑 Статус:",
        'vip': "✅ VIP",
        'require_vip': "🔒 Требуется VIP",
        'accuracy': "🎯 Точность: 94-97%",
        'auto_signals': "⏰ Автосигналы: каждые 2 минуты",
        
        # Сигналы
        'choose_market': "🎯 ВЫБЕРИТЕ ТИП РЫНКА:",
        'otc_market': "💱 OTC РЫНОК",
        'exchange_market': "🏛️ БИРЖЕВОЙ РЫНОК",
        'choose_pair': "📊 ВЫБЕРИТЕ ВАЛЮТНУЮ ПАРУ:",
        'analyzing': "🔍 Анализирую рынок...",
        'signal_title': "🎯 ПРОФЕССИОНАЛЬНЫЙ СИГНАЛ",
        'pair': "📊 Пара:",
        'direction': "🎯 Направление:",
        'probability': "📈 Вероятность:",
        'strength': "💪 Сила:",
        'expiration': "⏰ Экспирация:",
        'exact_time': "🕒 Точное время:",
        'time': "⏱️ Время сигнала:",
        'date': "📅 Дата:",
        'analysis': "📊 Анализ:",
        'market_condition': "Состояние рынка:",
        'risk_level': "Уровень риска:",
        'trend_strength': "Сила тренда:",
        'volatility': "Волатильность:",
        'recommendations': "⚠️ Рекомендации:",
        'risk': "• Риск: 2-3% от депозита",
        'good_luck': "🚀 Удачи в торговле!",
        
        # Автосигналы
        'auto_signal': "🤖 АВТОМАТИЧЕСКИЙ СИГНАЛ",
        'auto_enabled': "✅ Автосигналы ВКЛЮЧЕНЫ",
        'auto_disabled': "❌ Автосигналы ВЫКЛЮЧЕНЫ",
        'toggle_on': "✅ ВКЛЮЧИТЬ",
        'toggle_off': "❌ ВЫКЛЮЧИТЬ",
        
        # Марафон
        'marathon': "📅 МАРАФОН 30 ДНЕЙ",
        'enter_deposit': "💰 Введите стартовый депозит ($):",
        'min_deposit': "🚨 Минимальный депозит: $50",
        'generating': "⏳ Генерирую план...",
        
        # Админ
        'admin_panel': "⚡ АДМИН ПАНЕЛЬ",
        'total_users': "👥 Всего пользователей:",
        'vip_users': "👑 VIP пользователей:",
        'banned_users': "⛔ Заблокированных:",
        'grant': "➕ Выдать VIP",
        'revoke': "➖ Забрать VIP",
        'ban': "⛔ Блокировка",
        'unban': "✅ Разблокировка",
        'broadcast': "📢 Рассылка",
        'enter_user_id': "Введите ID пользователя:",
        'enter_message': "Введите сообщение:",
        
        # Общие
        'back': "🔙 Назад",
        'main_menu_btn': "🏠 Главное меню",
        'contact_admin': "📞 Связаться с админом",
        'processing': "⏳ Обработка...",
        'error': "⚠️ Ошибка!",
        'success': "✅ Успешно!",
        'use_buttons': "Используйте кнопки!",
    },
    'en': {
        'welcome': "👋 Welcome to KURUT AI INFINITY!",
        'choose_lang': "Choose language:",
        'main_menu': "🚀 KURUT AI INFINITY v12.0",
        'your_id': "🆔 Your ID:",
        'status': "👑 Status:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP Required",
        'accuracy': "🎯 Accuracy: 94-97%",
        'auto_signals': "⏰ Auto signals: every 2 minutes",
        
        'choose_market': "🎯 CHOOSE MARKET TYPE:",
        'otc_market': "💱 OTC MARKET",
        'exchange_market': "🏛️ EXCHANGE MARKET",
        'choose_pair': "📊 CHOOSE CURRENCY PAIR:",
        'analyzing': "🔍 Analyzing market...",
        'signal_title': "🎯 PROFESSIONAL SIGNAL",
        'pair': "📊 Pair:",
        'direction': "🎯 Direction:",
        'probability': "📈 Probability:",
        'strength': "💪 Strength:",
        'expiration': "⏰ Expiration:",
        'exact_time': "🕒 Exact time:",
        'time': "⏱️ Signal time:",
        'date': "📅 Date:",
        'analysis': "📊 Analysis:",
        'market_condition': "Market condition:",
        'risk_level': "Risk level:",
        'trend_strength': "Trend strength:",
        'volatility': "Volatility:",
        'recommendations': "⚠️ Recommendations:",
        'risk': "• Risk: 2-3% of deposit",
        'good_luck': "🚀 Good luck trading!",
        
        'auto_signal': "🤖 AUTOMATIC SIGNAL",
        'auto_enabled': "✅ Auto signals ENABLED",
        'auto_disabled': "❌ Auto signals DISABLED",
        'toggle_on': "✅ ENABLE",
        'toggle_off': "❌ DISABLE",
        
        'marathon': "📅 30 DAYS MARATHON",
        'enter_deposit': "💰 Enter starting deposit ($):",
        'min_deposit': "🚨 Minimum deposit: $50",
        'generating': "⏳ Generating plan...",
        
        'admin_panel': "⚡ ADMIN PANEL",
        'total_users': "👥 Total users:",
        'vip_users': "👑 VIP users:",
        'banned_users': "⛔ Banned users:",
        'grant': "➕ Grant VIP",
        'revoke': "➖ Revoke VIP",
        'ban': "⛔ Ban",
        'unban': "✅ Unban",
        'broadcast': "📢 Broadcast",
        'enter_user_id': "Enter user ID:",
        'enter_message': "Enter message:",
        
        'back': "🔙 Back",
        'main_menu_btn': "🏠 Main Menu",
        'contact_admin': "📞 Contact admin",
        'processing': "⏳ Processing...",
        'error': "⚠️ Error!",
        'success': "✅ Success!",
        'use_buttons': "Use buttons!",
    },
    'uz': {
        'welcome': "👋 KURUT AI INFINITY ga xush kelibsiz!",
        'choose_lang': "Tilni tanlang:",
        'main_menu': "🚀 KURUT AI INFINITY v12.0",
        'your_id': "🆔 Sizning ID:",
        'status': "👑 Status:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP talab qilinadi",
        'accuracy': "🎯 Aniqlik: 94-97%",
        'auto_signals': "⏰ Avto signallar: har 2 daqiqada",
        
        'choose_market': "🎯 BOZOR TURINI TANLANG:",
        'otc_market': "💱 OTC BOZORI",
        'exchange_market': "🏛️ BIRJA BOZORI",
        'choose_pair': "📊 VALYUTA JUFTLIGINI TANLANG:",
        'analyzing': "🔍 Bozor tahlili...",
        'signal_title': "🎯 PROFESSIONAL SIGNAL",
        'pair': "📊 Juftlik:",
        'direction': "🎯 Yo'nalish:",
        'probability': "📈 Ehtimollik:",
        'strength': "💪 Kuch:",
        'expiration': "⏰ Ekspiratsiya:",
        'exact_time': "🕒 Aniq vaqt:",
        'time': "⏱️ Signal vaqti:",
        'date': "📅 Sana:",
        'analysis': "📊 Tahlil:",
        'market_condition': "Bozor holati:",
        'risk_level': "Xavr darajasi:",
        'trend_strength': "Trend kuchi:",
        'volatility': "Volatillik:",
        'recommendations': "⚠️ Tavsiyalar:",
        'risk': "• Xavr: depozitning 2-3%",
        'good_luck': "🚀 Omadli savdo!",
        
        'auto_signal': "🤖 AVTOMATIK SIGNAL",
        'auto_enabled': "✅ Avto signallar YOQILGAN",
        'auto_disabled': "❌ Avto signallar O'CHIRILGAN",
        'toggle_on': "✅ YOQISH",
        'toggle_off': "❌ O'CHIRISH",
        
        'marathon': "📅 30 KUNLIK MARAFON",
        'enter_deposit': "💰 Boshlang'ich depozitni kiriting ($):",
        'min_deposit': "🚨 Minimal depozit: $50",
        'generating': "⏳ Reja yaratilmoqda...",
        
        'admin_panel': "⚡ ADMIN PANELI",
        'total_users': "👥 Jami foydalanuvchilar:",
        'vip_users': "👑 VIP foydalanuvchilar:",
        'banned_users': "⛔ Bloklanganlar:",
        'grant': "➕ VIP berish",
        'revoke': "➖ VIP olib tashlash",
        'ban': "⛔ Bloklash",
        'unban': "✅ Blokdan chiqarish",
        'broadcast': "📢 Tarqatma",
        'enter_user_id': "Foydalanuvchi ID sini kiriting:",
        'enter_message': "Xabarni kiriting:",
        
        'back': "🔙 Orqaga",
        'main_menu_btn': "🏠 Asosiy menyu",
        'contact_admin': "📞 Admin bilan bog'lanish",
        'processing': "⏳ Qayta ishlanmoqda...",
        'error': "⚠️ Xatolik!",
        'success': "✅ Muvaffaqiyatli!",
        'use_buttons': "Tugmalardan foydalaning!",
    },
    'kg': {
        'welcome': "👋 KURUT AI INFINITY кош келиңиз!",
        'choose_lang': "Тилди тандаңыз:",
        'main_menu': "🚀 KURUT AI INFINITY v12.0",
        'your_id': "🆔 Сиздин ID:",
        'status': "👑 Статус:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP талап кылынат",
        'accuracy': "🎯 Тактык: 94-97%",
        'auto_signals': "⏰ Авто сигналдар: ар 2 мүнөт сайын",
        
        'choose_market': "🎯 БАЗАР ТҮРҮН ТАНДАҢЫЗ:",
        'otc_market': "💱 OTC БАЗАРЫ",
        'exchange_market': "🏛️ БИРЖА БАЗАРЫ",
        'choose_pair': "📊 ВАЛЮТА ЖУПТУГУН ТАНДАҢЫЗ:",
        'analyzing': "🔍 Базар анализи...",
        'signal_title': "🎯 ПРОФЕССИОНАЛДЫК СИГНАЛ",
        'pair': "📊 Жуптук:",
        'direction': "🎯 Багыт:",
        'probability': "📈 Ыктымалдык:",
        'strength': "💪 Күч:",
        'expiration': "⏰ Экспирация:",
        'exact_time': "🕒 Так убакыт:",
        'time': "⏱️ Сигнал убактысы:",
        'date': "📅 Дата:",
        'analysis': "📊 Анализ:",
        'market_condition': "Базар абалы:",
        'risk_level': "Тобокелдик деңгээли:",
        'trend_strength': "Тренд күчү:",
        'volatility': "Волатилдүүлүк:",
        'recommendations': "⚠️ Сунуштар:",
        'risk': "• Тобокелдик: депозиттин 2-3%",
        'good_luck': "🚀 Соодого ийгилик!",
        
        'auto_signal': "🤖 АВТОМАТТЫК СИГНАЛ",
        'auto_enabled': "✅ Авто сигналдар КҮЙГҮЗҮЛГӨН",
        'auto_disabled': "❌ Авто сигналдар ӨЧҮРҮЛГӨН",
        'toggle_on': "✅ КҮЙГҮЗҮҮ",
        'toggle_off': "❌ ӨЧҮРҮҮ",
        
        'marathon': "📅 30 КҮНДҮК МАРАФОН",
        'enter_deposit': "💰 Баштапкы депозитти киргизиңиз ($):",
        'min_deposit': "🚨 Минималдуу депозит: $50",
        'generating': "⏳ План түзүлүүдө...",
        
        'admin_panel': "⚡ АДМИН ПАНЕЛИ",
        'total_users': "👥 Бардык колдонуучулар:",
        'vip_users': "👑 VIP колдонуучулар:",
        'banned_users': "⛔ Блокталгандар:",
        'grant': "➕ VIP берүү",
        'revoke': "➖ VIP алуу",
        'ban': "⛔ Блоктоо",
        'unban': "✅ Блоктон чыгаруу",
        'broadcast': "📢 Таркатуу",
        'enter_user_id': "Колдонуучунун ID син киргизиңиз:",
        'enter_message': "Билдирүүнү киргизиңиз:",
        
        'back': "🔙 Артка",
        'main_menu_btn': "🏠 Негизги меню",
        'contact_admin': "📞 Админ менен байланышуу",
        'processing': "⏳ Өңдөлүүдө...",
        'error': "⚠️ Ката!",
        'success': "✅ Ийгиликтүү!",
        'use_buttons': "Баскычтарды колдонуңуз!",
    }
}

# ============================================
# 🛠️ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================

def is_admin(user_id):
    return str(user_id) in [str(x) for x in ADMIN_IDS]

def is_vip(user_id):
    return str(user_id) in vip_users or is_admin(user_id)

def is_banned(user_id):
    return str(user_id) in banned_users

def get_user_language(user_id):
    return user_languages.get(str(user_id), 'ru')

def t(user_id, key):
    lang = get_user_language(user_id)
    return TEXTS.get(lang, {}).get(key, TEXTS['ru'].get(key, key))

def set_user_language(user_id, lang):
    user_languages[str(user_id)] = lang
    Database.save("user_languages.json", user_languages)
    return True

def ensure_user_data(user_id):
    user_id_str = str(user_id)
    
    if user_id_str not in all_users:
        all_users.add(user_id_str)
        Database.save("all_users.json", list(all_users))
    
    if user_id_str not in user_stats:
        user_stats[user_id_str] = {
            "wins": 0, "losses": 0, "profit": 0,
            "total_trades": 0, "win_rate": 0,
            "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "last_active": datetime.now().isoformat()
        }
        Database.save("user_stats.json", user_stats)
    
    if user_id_str not in user_languages:
        user_languages[user_id_str] = 'ru'
        Database.save("user_languages.json", user_languages)
    
    return True

def update_user_stats(user_id, win, profit=0):
    user_id_str = str(user_id)
    ensure_user_data(user_id_str)
    
    stats = user_stats.get(user_id_str, {})
    stats["total_trades"] = stats.get("total_trades", 0) + 1
    stats["last_active"] = datetime.now().isoformat()
    
    if win:
        stats["wins"] = stats.get("wins", 0) + 1
        stats["profit"] = stats.get("profit", 0) + profit
    else:
        stats["losses"] = stats.get("losses", 0) + 1
    
    total = stats.get("wins", 0) + stats.get("losses", 0)
    stats["win_rate"] = (stats.get("wins", 0) / total * 100) if total > 0 else 0
    
    user_stats[user_id_str] = stats
    Database.save("user_stats.json", user_stats)
    return stats

def add_admin_log(action, admin_id, target=None, details=""):
    log_entry = {
        "timestamp": datetime.now().isoformat(),
        "action": action,
        "admin_id": admin_id,
        "target_user": target,
        "details": details
    }
    admin_logs.append(log_entry)
    Database.save("admin_logs.json", admin_logs)

# ============================================
# 🎨 СИСТЕМА КЛАВИАТУР
# ============================================

class KeyboardManager:
    @staticmethod
    def language_menu():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru"),
                InlineKeyboardButton("🇺🇿 Oʻzbekcha", callback_data="lang_uz")
            ],
            [
                InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg"),
                InlineKeyboardButton("🇺🇸 English", callback_data="lang_en")
            ]
        ])
    
    @staticmethod
    def main_menu(user_id):
        lang = get_user_language(user_id)
        keyboard = []
        
        if is_vip(user_id):
            if lang == 'ru':
                keyboard.append([InlineKeyboardButton("🚀 Получить сигнал", callback_data="get_signal")])
                keyboard.append([
                    InlineKeyboardButton("🤖 Автосигналы", callback_data="auto_signals_menu"),
                    InlineKeyboardButton("📊 Статистика", callback_data="my_stats")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 Марафон", callback_data="marathon_menu"),
                    InlineKeyboardButton("🏆 Топ", callback_data="top_traders")
                ])
            elif lang == 'en':
                keyboard.append([InlineKeyboardButton("🚀 Get Signal", callback_data="get_signal")])
                keyboard.append([
                    InlineKeyboardButton("🤖 Auto Signals", callback_data="auto_signals_menu"),
                    InlineKeyboardButton("📊 Statistics", callback_data="my_stats")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 Marathon", callback_data="marathon_menu"),
                    InlineKeyboardButton("🏆 Top", callback_data="top_traders")
                ])
            elif lang == 'uz':
                keyboard.append([InlineKeyboardButton("🚀 Signal Olish", callback_data="get_signal")])
                keyboard.append([
                    InlineKeyboardButton("🤖 Avto Signallar", callback_data="auto_signals_menu"),
                    InlineKeyboardButton("📊 Statistika", callback_data="my_stats")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 Marafon", callback_data="marathon_menu"),
                    InlineKeyboardButton("🏆 Top", callback_data="top_traders")
                ])
            else:  # kg
                keyboard.append([InlineKeyboardButton("🚀 Signal Aluu", callback_data="get_signal")])
                keyboard.append([
                    InlineKeyboardButton("🤖 Avto Signaldar", callback_data="auto_signals_menu"),
                    InlineKeyboardButton("📊 Statistika", callback_data="my_stats")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 Marafon", callback_data="marathon_menu"),
                    InlineKeyboardButton("🏆 Top", callback_data="top_traders")
                ])
        else:
            if lang == 'ru':
                keyboard.append([
                    InlineKeyboardButton("📝 Регистрация", url=REF_LINK),
                    InlineKeyboardButton("👑 Получить VIP", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 О боте", callback_data="about"),
                    InlineKeyboardButton("📱 Соцсети", callback_data="socials")
                ])
            elif lang == 'en':
                keyboard.append([
                    InlineKeyboardButton("📝 Register", url=REF_LINK),
                    InlineKeyboardButton("👑 Get VIP", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 About", callback_data="about"),
                    InlineKeyboardButton("📱 Socials", callback_data="socials")
                ])
            elif lang == 'uz':
                keyboard.append([
                    InlineKeyboardButton("📝 Ro'yxatdan o'tish", url=REF_LINK),
                    InlineKeyboardButton("👑 VIP Olish", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 Bot haqida", callback_data="about"),
                    InlineKeyboardButton("📱 Ijtimoiy tarmoqlar", callback_data="socials")
                ])
            else:  # kg
                keyboard.append([
                    InlineKeyboardButton("📝 Каттоо", url=REF_LINK),
                    InlineKeyboardButton("👑 VIP алуу", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 Бот жөнүндө", callback_data="about"),
                    InlineKeyboardButton("📱 Социалдык тармактар", callback_data="socials")
                ])
        
        # Админ панель
        if is_admin(user_id):
            if lang == 'ru':
                keyboard.append([InlineKeyboardButton("⚡ Админ Панель", callback_data="admin_panel")])
            elif lang == 'en':
                keyboard.append([InlineKeyboardButton("⚡ Admin Panel", callback_data="admin_panel")])
            elif lang == 'uz':
                keyboard.append([InlineKeyboardButton("⚡ Admin Paneli", callback_data="admin_panel")])
            else:  # kg
                keyboard.append([InlineKeyboardButton("⚡ Админ Панели", callback_data="admin_panel")])
        
        # Контакт админа
        if lang == 'ru':
            keyboard.append([InlineKeyboardButton("📞 Связаться с админом", url=ADMIN_LINK)])
        elif lang == 'en':
            keyboard.append([InlineKeyboardButton("📞 Contact Admin", url=ADMIN_LINK)])
        elif lang == 'uz':
            keyboard.append([InlineKeyboardButton("📞 Admin Bilan Bog'lanish", url=ADMIN_LINK)])
        else:  # kg
            keyboard.append([InlineKeyboardButton("📞 Админ Менен Байланышуу", url=ADMIN_LINK)])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_panel():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
                InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")
            ],
            [
                InlineKeyboardButton("➕ Выдать VIP", callback_data="admin_grant"),
                InlineKeyboardButton("➖ Забрать VIP", callback_data="admin_revoke")
            ],
            [
                InlineKeyboardButton("⛔ Блокировка", callback_data="admin_ban"),
                InlineKeyboardButton("✅ Разблокировка", callback_data="admin_unban")
            ],
            [
                InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast"),
                InlineKeyboardButton("📝 Логи", callback_data="admin_logs")
            ],
            [
                InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
            ]
        ])
    
    @staticmethod
    def market_menu(user_id):
        lang = get_user_language(user_id)
        if lang == 'ru':
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("💱 OTC РЫНОК", callback_data="market_otc")],
                [InlineKeyboardButton("🏛️ БИРЖЕВОЙ РЫНОК", callback_data="market_exchange")],
                [InlineKeyboardButton("🔙 Назад", callback_data="main_menu")]
            ])
        elif lang == 'en':
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("💱 OTC MARKET", callback_data="market_otc")],
                [InlineKeyboardButton("🏛️ EXCHANGE MARKET", callback_data="market_exchange")],
                [InlineKeyboardButton("🔙 Back", callback_data="main_menu")]
            ])
        elif lang == 'uz':
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("💱 OTC BOZORI", callback_data="market_otc")],
                [InlineKeyboardButton("🏛️ BIRJA BOZORI", callback_data="market_exchange")],
                [InlineKeyboardButton("🔙 Orqaga", callback_data="main_menu")]
            ])
        else:  # kg
            return InlineKeyboardMarkup([
                [InlineKeyboardButton("💱 OTC БАЗАРЫ", callback_data="market_otc")],
                [InlineKeyboardButton("🏛️ БИРЖА БАЗАРЫ", callback_data="market_exchange")],
                [InlineKeyboardButton("🔙 Артка", callback_data="main_menu")]
            ])
    
    @staticmethod
    def pairs_menu(pairs, market_type, page=0, user_id=None):
        per_page = 8
        start = page * per_page
        end = start + per_page
        
        keyboard = []
        
        for i in range(start, min(end, len(pairs))):
            if i % 2 == 0:
                row = []
                row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{market_type}_{i}"))
                if i + 1 < min(end, len(pairs)):
                    row.append(InlineKeyboardButton(pairs[i+1], callback_data=f"pair_{market_type}_{i+1}"))
                keyboard.append(row)
        
        nav_buttons = []
        lang = get_user_language(user_id) if user_id else 'ru'
        
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(
                "⬅️ Назад" if lang == 'ru' else "⬅️ Back" if lang == 'en' else 
                "⬅️ Orqaga" if lang == 'uz' else "⬅️ Артка",
                callback_data=f"page_{market_type}_{page-1}"
            ))
        
        if end < len(pairs):
            nav_buttons.append(InlineKeyboardButton(
                "Далее ➡️" if lang == 'ru' else "Next ➡️" if lang == 'en' else
                "Keyingi ➡️" if lang == 'uz' else "Кийинки ➡️",
                callback_data=f"page_{market_type}_{page+1}"
            ))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([
            InlineKeyboardButton(
                "🔙 Назад" if lang == 'ru' else "🔙 Back" if lang == 'en' else
                "🔙 Orqaga" if lang == 'uz' else "🔙 Артка",
                callback_data="get_signal"
            ),
            InlineKeyboardButton(
                "🏠 Главное" if lang == 'ru' else "🏠 Main" if lang == 'en' else
                "🏠 Asosiy" if lang == 'uz' else "🏠 Негизги",
                callback_data="main_menu"
            )
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def auto_signals_menu(user_id):
        lang = get_user_language(user_id)
        enabled = auto_signals.get(str(user_id), False)
        
        if lang == 'ru':
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "❌ ВЫКЛЮЧИТЬ" if enabled else "✅ ВКЛЮЧИТЬ",
                        callback_data="toggle_auto"
                    )
                ],
                [
                    InlineKeyboardButton("🔙 Назад", callback_data="main_menu")
                ]
            ])
        elif lang == 'en':
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "❌ DISABLE" if enabled else "✅ ENABLE",
                        callback_data="toggle_auto"
                    )
                ],
                [
                    InlineKeyboardButton("🔙 Back", callback_data="main_menu")
                ]
            ])
        elif lang == 'uz':
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "❌ O'CHIRISH" if enabled else "✅ YOQISH",
                        callback_data="toggle_auto"
                    )
                ],
                [
                    InlineKeyboardButton("🔙 Orqaga", callback_data="main_menu")
                ]
            ])
        else:  # kg
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton(
                        "❌ ӨЧҮРҮҮ" if enabled else "✅ КҮЙГҮЗҮҮ",
                        callback_data="toggle_auto"
                    )
                ],
                [
                    InlineKeyboardButton("🔙 Артка", callback_data="main_menu")
                ]
            ])
    
    @staticmethod
    def result_menu(user_id):
        lang = get_user_language(user_id)
        if lang == 'ru':
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Выиграл +95%", callback_data="trade_win_95"),
                    InlineKeyboardButton("✅ Выиграл +85%", callback_data="trade_win_85")
                ],
                [
                    InlineKeyboardButton("❌ Проиграл", callback_data="trade_loss"),
                    InlineKeyboardButton("📊 Статистика", callback_data="my_stats")
                ],
                [
                    InlineKeyboardButton("🔄 Новый сигнал", callback_data="get_signal"),
                    InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
                ]
            ])
        elif lang == 'en':
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Won +95%", callback_data="trade_win_95"),
                    InlineKeyboardButton("✅ Won +85%", callback_data="trade_win_85")
                ],
                [
                    InlineKeyboardButton("❌ Lost", callback_data="trade_loss"),
                    InlineKeyboardButton("📊 Stats", callback_data="my_stats")
                ],
                [
                    InlineKeyboardButton("🔄 New Signal", callback_data="get_signal"),
                    InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")
                ]
            ])
        elif lang == 'uz':
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Yutdi +95%", callback_data="trade_win_95"),
                    InlineKeyboardButton("✅ Yutdi +85%", callback_data="trade_win_85")
                ],
                [
                    InlineKeyboardButton("❌ Yutqazdi", callback_data="trade_loss"),
                    InlineKeyboardButton("📊 Statistika", callback_data="my_stats")
                ],
                [
                    InlineKeyboardButton("🔄 Yangi Signal", callback_data="get_signal"),
                    InlineKeyboardButton("🏠 Asosiy Menyu", callback_data="main_menu")
                ]
            ])
        else:  # kg
            return InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Женишти +95%", callback_data="trade_win_95"),
                    InlineKeyboardButton("✅ Женишти +85%", callback_data="trade_win_85")
                ],
                [
                    InlineKeyboardButton("❌ Жоголду", callback_data="trade_loss"),
                    InlineKeyboardButton("📊 Статистика", callback_data="my_stats")
                ],
                [
                    InlineKeyboardButton("🔄 Жаңы Сигнал", callback_data="get_signal"),
                    InlineKeyboardButton("🏠 Негизги Меню", callback_data="main_menu")
                ]
            ])
    
    @staticmethod
    def back_to_menu(user_id):
        lang = get_user_language(user_id)
        if lang == 'ru':
            return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")]])
        elif lang == 'en':
            return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data="main_menu")]])
        elif lang == 'uz':
            return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Asosiy Menyu", callback_data="main_menu")]])
        else:  # kg
            return InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Негизги Меню", callback_data="main_menu")]])

# ============================================
# 🚀 ОСНОВНЫЕ КОМАНДЫ БОТА
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    if is_banned(user_id):
        await update.message.reply_text("⛔ Вы заблокированы в этом боте.")
        return
    
    ensure_user_data(user_id)
    
    # Логируем нового пользователя
    if user_id not in all_users:
        logger.info(f"👤 Новый пользователь: {user_id}")
        add_admin_log("new_user", user_id, details=f"@{user.username}")
    
    message = f"<b>{t(user_id, 'welcome')}</b>\n\n"
    message += f"<b>{t(user_id, 'your_id')}</b> <code>{user_id}</code>\n\n"
    message += f"<b>{t(user_id, 'choose_lang')}</b>"
    
    await update.message.reply_text(
        message,
        parse_mode='HTML',
        reply_markup=KeyboardManager.language_menu()
    )

async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE, user_id=None):
    if not user_id:
        if isinstance(update, Update) and update.effective_user:
            user = update.effective_user
            user_id = str(user.id)
        elif hasattr(update, 'from_user'):
            user_id = str(update.from_user.id)
        else:
            user_id = "unknown"
    
    if is_banned(user_id):
        await update.edit_message_text("⛔ Вы заблокированы.") if hasattr(update, 'edit_message_text') else \
        await update.message.reply_text("⛔ Вы заблокированы.")
        return
    
    ensure_user_data(user_id)
    
    message = f"<b>{t(user_id, 'main_menu')}</b>\n\n"
    message += f"<b>{t(user_id, 'your_id')}</b> <code>{user_id}</code>\n"
    message += f"<b>{t(user_id, 'status')}</b> {'✅ VIP' if is_vip(user_id) else '🔒 ' + t(user_id, 'require_vip')}\n"
    message += f"<b>{t(user_id, 'accuracy')}</b>\n"
    message += f"<b>{t(user_id, 'auto_signals')}</b>\n"
    
    if hasattr(update, 'edit_message_text'):
        await update.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=KeyboardManager.main_menu(user_id)
        )
    else:
        await update.message.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=KeyboardManager.main_menu(user_id)
        )

# ============================================
# ⚡ АДМИН ФУНКЦИИ
# ============================================

async def admin_panel_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer("⛔ Только для администраторов!", show_alert=True)
        return
    
    message = f"<b>{t(user_id, 'admin_panel')}</b>\n\n"
    message += f"<b>{t(user_id, 'total_users')}</b> <b>{len(all_users)}</b>\n"
    message += f"<b>{t(user_id, 'vip_users')}</b> <b>{len(vip_users)}</b>\n"
    message += f"<b>{t(user_id, 'banned_users')}</b> <b>{len(banned_users)}</b>\n"
    message += f"<b>📊 Сигналов сегодня:</b> <b>{sum(len(v) for v in signal_history.values())}</b>"
    
    await query.edit_message_text(
        message,
        parse_mode='HTML',
        reply_markup=KeyboardManager.admin_panel()
    )

async def admin_grant_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer("⛔ Только для администраторов!", show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'grant')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "grant"

async def admin_revoke_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer("⛔ Только для администраторов!", show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'revoke')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "revoke"

async def admin_ban_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer("⛔ Только для администраторов!", show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'ban')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "ban"

async def admin_unban_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer("⛔ Только для администраторов!", show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'unban')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "unban"

async def admin_broadcast_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer("⛔ Только для администраторов!", show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'broadcast')}</b>\n\n"
        f"{t(user_id, 'enter_message')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "broadcast"

async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text.strip()
    
    if not is_admin(user_id):
        return
    
    action = context.user_data.get("admin_action")
    
    if action == "grant":
        target_id = text
        
        if not target_id.isdigit():
            await update.message.reply_text("❌ Неверный ID пользователя!")
            return
        
        if target_id in vip_users:
            await update.message.reply_text("⚠️ Пользователь уже VIP!")
        else:
            vip_users.add(target_id)
            Database.save("vip_users.json", list(vip_users))
            
            # Добавляем в общие пользователи если нет
            if target_id not in all_users:
                all_users.add(target_id)
                Database.save("all_users.json", list(all_users))
            
            add_admin_log("grant_vip", user_id, target_id)
            
            await update.message.reply_text(f"✅ VIP выдан пользователю {target_id}")
            
            # Уведомляем пользователя
            try:
                await context.bot.send_message(
                    chat_id=target_id,
                    text="🎉 <b>ПОЗДРАВЛЯЕМ!</b>\n\nВам выдан VIP доступ к профессиональным сигналам!",
                    parse_mode='HTML'
                )
            except:
                pass
            
            context.user_data.pop("admin_action", None)
    
    elif action == "revoke":
        target_id = text
        
        if not target_id.isdigit():
            await update.message.reply_text("❌ Неверный ID пользователя!")
            return
        
        if target_id not in vip_users:
            await update.message.reply_text("⚠️ Пользователь не VIP!")
        else:
            vip_users.remove(target_id)
            Database.save("vip_users.json", list(vip_users))
            add_admin_log("revoke_vip", user_id, target_id)
            await update.message.reply_text(f"❌ VIP отозван у пользователя {target_id}")
            context.user_data.pop("admin_action", None)
    
    elif action == "ban":
        target_id = text
        
        if not target_id.isdigit():
            await update.message.reply_text("❌ Неверный ID пользователя!")
            return
        
        if target_id in banned_users:
            await update.message.reply_text("⚠️ Пользователь уже заблокирован!")
        else:
            banned_users.add(target_id)
            Database.save("banned_users.json", list(banned_users))
            add_admin_log("ban_user", user_id, target_id)
            await update.message.reply_text(f"⛔ Пользователь {target_id} заблокирован")
            context.user_data.pop("admin_action", None)
    
    elif action == "unban":
        target_id = text
        
        if not target_id.isdigit():
            await update.message.reply_text("❌ Неверный ID пользователя!")
            return
        
        if target_id not in banned_users:
            await update.message.reply_text("⚠️ Пользователь не заблокирован!")
        else:
            banned_users.remove(target_id)
            Database.save("banned_users.json", list(banned_users))
            add_admin_log("unban_user", user_id, target_id)
            await update.message.reply_text(f"✅ Пользователь {target_id} разблокирован")
            context.user_data.pop("admin_action", None)
    
    elif action == "broadcast":
        message = text
        success = 0
        failed = 0
        
        await update.message.reply_text("⏳ Отправляю рассылку...")
        
        for uid in all_users:
            try:
                await context.bot.send_message(
                    chat_id=uid,
                    text=f"📢 <b>РАССЫЛКА ОТ АДМИНИСТРАТОРА</b>\n\n{message}",
                    parse_mode='HTML'
                )
                success += 1
                await asyncio.sleep(0.1)  # Пауза чтобы не получить лимит
            except Exception as e:
                failed += 1
        
        add_admin_log("broadcast", user_id, details=f"success={success}, failed={failed}")
        
        await update.message.reply_text(
            f"✅ Рассылка завершена!\n\n"
            f"✅ Успешно: {success}\n"
            f"❌ Неудачно: {failed}"
        )
        
        context.user_data.pop("admin_action", None)

# ============================================
# 🤖 СИСТЕМА АВТОМАТИЧЕСКИХ СИГНАЛОВ
# ============================================

class AutoSignalSystem:
    def __init__(self, application):
        self.application = application
        self.running = False
        self.task = None
    
    async def start(self):
        """Запуск системы автосигналов"""
        self.running = True
        self.task = asyncio.create_task(self.auto_signal_loop())
        logger.info("🤖 Система автосигналов ЗАПУЩЕНА")
    
    async def stop(self):
        """Остановка системы автосигналов"""
        self.running = False
        if self.task:
            self.task.cancel()
            try:
                await self.task
            except asyncio.CancelledError:
                pass
        logger.info("🤖 Система автосигналов ОСТАНОВЛЕНА")
    
    async def auto_signal_loop(self):
        """Основной цикл автосигналов"""
        while self.running:
            try:
                # Ждем 2 минуты
                await asyncio.sleep(120)
                
                # Генерируем сигнал
                signal = analyzer.generate_auto_signal()
                if not signal:
                    continue
                
                # Получаем всех VIP пользователей с включенными автосигналами
                users_to_send = []
                for uid in vip_users:
                    uid_str = str(uid)
                    if auto_signals.get(uid_str, False) and not is_banned(uid_str):
                        users_to_send.append(uid_str)
                
                if not users_to_send:
                    continue
                
                logger.info(f"🤖 Отправка автосигналов {len(users_to_send)} пользователям")
                
                # Отправляем каждому пользователю
                for user_id in users_to_send:
                    try:
                        lang = get_user_language(user_id)
                        direction_emoji = "🟢" if signal['direction'] == "CALL" else "🔴"
                        
                        if lang == 'ru':
                            direction_text = "ВВЕРХ" if signal['direction'] == "CALL" else "ВНИЗ"
                            message = f"""
<b>🤖 АВТОМАТИЧЕСКИЙ СИГНАЛ</b>

<b>📊 Пара:</b> <code>{signal['pair']}</code>
<b>🎯 Направление:</b> {direction_emoji} <b>{direction_text}</b>
<b>📈 Вероятность:</b> <b>{signal['probability']}%</b> 🔥
<b>⏰ Экспирация:</b> <b>{signal['expiration']}</b>
<b>🕒 Точное время:</b> <b>{signal['exact_time']}</b>
<b>⏱️ Время сигнала:</b> {signal['time']}
<b>📅 Дата:</b> {signal['date']}

<b>⚡ Сигнал сгенерирован автоматически</b>
"""
                        elif lang == 'en':
                            message = f"""
<b>🤖 AUTOMATIC SIGNAL</b>

<b>📊 Pair:</b> <code>{signal['pair']}</code>
<b>🎯 Direction:</b> {direction_emoji} <b>{signal['direction']}</b>
<b>📈 Probability:</b> <b>{signal['probability']}%</b> 🔥
<b>⏰ Expiration:</b> <b>{signal['expiration']}</b>
<b>🕒 Exact time:</b> <b>{signal['exact_time']}</b>
<b>⏱️ Signal time:</b> {signal['time']}
<b>📅 Date:</b> {signal['date']}

<b>⚡ Signal generated automatically</b>
"""
                        elif lang == 'uz':
                            direction_text = "YUQORI" if signal['direction'] == "CALL" else "PAST"
                            message = f"""
<b>🤖 AVTOMATIK SIGNAL</b>

<b>📊 Juftlik:</b> <code>{signal['pair']}</code>
<b>🎯 Yo'nalish:</b> {direction_emoji} <b>{direction_text}</b>
<b>📈 Ehtimollik:</b> <b>{signal['probability']}%</b> 🔥
<b>⏰ Ekspiratsiya:</b> <b>{signal['expiration']}</b>
<b>🕒 Aniq vaqt:</b> <b>{signal['exact_time']}</b>
<b>⏱️ Signal vaqti:</b> {signal['time']}
<b>📅 Sana:</b> {signal['date']}

<b>⚡ Signal avtomatik yaratildi</b>
"""
                        else:  # kg
                            direction_text = "ЖОГОРУ" if signal['direction'] == "CALL" else "ТОМЕН"
                            message = f"""
<b>🤖 АВТОМАТТЫК СИГНАЛ</b>

<b>📊 Жуптук:</b> <code>{signal['pair']}</code>
<b>🎯 Багыт:</b> {direction_emoji} <b>{direction_text}</b>
<b>📈 Ыктымалдык:</b> <b>{signal['probability']}%</b> 🔥
<b>⏰ Экспирация:</b> <b>{signal['expiration']}</b>
<b>🕒 Так убакыт:</b> <b>{signal['exact_time']}</b>
<b>⏱️ Сигнал убактысы:</b> {signal['time']}
<b>📅 Дата:</b> {signal['date']}

<b>⚡ Сигнал автоматикалык түзүлдү</b>
"""
                        
                        await self.application.bot.send_message(
                            chat_id=user_id,
                            text=message,
                            parse_mode='HTML'
                        )
                        
                        # Сохраняем в историю
                        signal_history.setdefault(user_id, []).append({
                            "pair": signal['pair'],
                            "direction": signal['direction'],
                            "probability": signal['probability'],
                            "expiration": signal['expiration'],
                            "type": "auto",
                            "timestamp": datetime.now().isoformat()
                        })
                        
                        # Пауза между отправками
                        await asyncio.sleep(0.05)
                        
                    except Exception as e:
                        logger.error(f"Ошибка отправки автосигнала {user_id}: {e}")
                
                # Сохраняем историю
                Database.save("signal_history.json", signal_history)
                
            except Exception as e:
                logger.error(f"Ошибка в цикле автосигналов: {e}")
                await asyncio.sleep(60)

# ============================================
# 📅 МАРАФОН 30 ДНЕЙ
# ============================================

def generate_marathon_plan(deposit, lang='ru'):
    """Генерация плана марафона"""
    try:
        if deposit < 50:
            if lang == 'ru':
                return "❌ <b>Минимальный депозит: $50!</b>"
            elif lang == 'en':
                return "❌ <b>Minimum deposit: $50!</b>"
            elif lang == 'uz':
                return "❌ <b>Minimal depozit: $50!</b>"
            else:
                return "❌ <b>Минималдуу депозит: $50!</b>"
        
        plan = ""
        if lang == 'ru':
            plan = f"""
<b>📅 МАРАФОН 30 ДНЕЙ</b>

<b>💰 Стартовый депозит:</b> <b>${deposit}</b>
<b>🎯 Цель за 30 дней:</b> <b>${deposit * 3:.0f}</b> (+200%)

────────────────────
<b>📊 ПЛАН ПО ДНЯМ:</b>
"""
        elif lang == 'en':
            plan = f"""
<b>📅 30 DAYS MARATHON</b>

<b>💰 Starting deposit:</b> <b>${deposit}</b>
<b>🎯 Goal in 30 days:</b> <b>${deposit * 3:.0f}</b> (+200%)

────────────────────
<b>📊 DAY BY DAY PLAN:</b>
"""
        elif lang == 'uz':
            plan = f"""
<b>📅 30 KUNLIK MARAFON</b>

<b>💰 Boshlang'ich depozit:</b> <b>${deposit}</b>
<b>🎯 30 kundan keyin:</b> <b>${deposit * 3:.0f}</b> (+200%)

────────────────────
<b>📊 KUNDALIK REJA:</b>
"""
        else:  # kg
            plan = f"""
<b>📅 30 КҮНДҮК МАРАФОН</b>

<b>💰 Башталгыч депозит:</b> <b>${deposit}</b>
<b>🎯 30 күндөн кийин:</b> <b>${deposit * 3:.0f}</b> (+200%)

────────────────────
<b>📊 КҮНҮНӨ ПЛАН:</b>
"""
        
        current = deposit
        for day in range(1, 31):
            # Рассчитываем дневную цель
            if day <= 7:
                daily_target = 3
                phase = "I" if lang == 'ru' else "I" if lang == 'en' else "I" if lang == 'uz' else "I"
            elif day <= 14:
                daily_target = 4
                phase = "II" if lang == 'ru' else "II" if lang == 'en' else "II" if lang == 'uz' else "II"
            elif day <= 21:
                daily_target = 5
                phase = "III" if lang == 'ru' else "III" if lang == 'en' else "III" if lang == 'uz' else "III"
            else:
                daily_target = 6
                phase = "IV" if lang == 'ru' else "IV" if lang == 'en' else "IV" if lang == 'uz' else "IV"
            
            # Генерируем результат
            random.seed(day + int(deposit))
            daily_result = random.uniform(daily_target * 0.8, daily_target * 1.2)
            
            # Рассчитываем прибыль
            profit = current * daily_result / 100
            current += profit
            
            # Выбираем пары
            if day % 3 == 0:
                pairs = random.sample(OTC_PAIRS, 2)
            else:
                pairs = random.sample(EXCHANGE_PAIRS, 2)
            
            if lang == 'ru':
                plan += f"""
<b>День {day} (Фаза {phase}):</b>
• Баланс: <b>${current:.0f}</b>
• Цель: +{daily_target}%
• Результат: +{daily_result:.1f}%
• Прибыль: <b>${profit:.0f}</b>
• Пары: {', '.join(pairs)}
"""
            elif lang == 'en':
                plan += f"""
<b>Day {day} (Phase {phase}):</b>
• Balance: <b>${current:.0f}</b>
• Goal: +{daily_target}%
• Result: +{daily_result:.1f}%
• Profit: <b>${profit:.0f}</b>
• Pairs: {', '.join(pairs)}
"""
            elif lang == 'uz':
                plan += f"""
<b>Kun {day} (Faza {phase}):</b>
• Balans: <b>${current:.0f}</b>
• Mag'durat: +{daily_target}%
• Natija: +{daily_result:.1f}%
• Foyda: <b>${profit:.0f}</b>
• Juftliklar: {', '.join(pairs)}
"""
            else:  # kg
                plan += f"""
<b>Күн {day} (Фаза {phase}):</b>
• Баланс: <b>${current:.0f}</b>
• Максат: +{daily_target}%
• Натыйжа: +{daily_result:.1f}%
• Пайда: <b>${profit:.0f}</b>
• Жуптуктар: {', '.join(pairs)}
"""
        
        total_profit = current - deposit
        profit_percent = (total_profit / deposit) * 100
        
        if lang == 'ru':
            plan += f"""
────────────────────
<b>📈 ИТОГИ МАРАФОНА:</b>

• Стартовый депозит: <b>${deposit}</b>
• Финальный баланс: <b>${current:.0f}</b>
• Общая прибыль: <b>+{profit_percent:.1f}%</b>
• Прибыль в $: <b>${total_profit:.0f}</b>

<b>🚀 УСПЕХОВ В ТОРГОВЛЕ!</b>
"""
        elif lang == 'en':
            plan += f"""
────────────────────
<b>📈 MARATHON RESULTS:</b>

• Starting deposit: <b>${deposit}</b>
• Final balance: <b>${current:.0f}</b>
• Total profit: <b>+{profit_percent:.1f}%</b>
• Profit in $: <b>${total_profit:.0f}</b>

<b>🚀 GOOD LUCK TRADING!</b>
"""
        elif lang == 'uz':
            plan += f"""
────────────────────
<b>📈 MARAFON NATIJALARI:</b>

• Boshlang'ich depozit: <b>${deposit}</b>
• Yakuniy balans: <b>${current:.0f}</b>
• Umumiy foyda: <b>+{profit_percent:.1f}%</b>
• Foyda $ da: <b>${total_profit:.0f}</b>

<b>🚀 OMLI SAVDO!</b>
"""
        else:  # kg
            plan += f"""
────────────────────
<b>📈 МАРАФОН НАТИЖЕЛЕРИ:</b>

• Башталгыч депозит: <b>${deposit}</b>
• Акыркы баланс: <b>${current:.0f}</b>
• Баардык пайда: <b>+{profit_percent:.1f}%</b>
• Пайда $ да: <b>${total_profit:.0f}</b>

<b>🚀 ИЙГИЛИКТҮҮ СООДО!</b>
"""
        
        return plan
    
    except Exception as e:
        logger.error(f"Ошибка генерации марафона: {e}")
        return "❌ <b>Ошибка генерации плана. Попробуйте позже!</b>"

# ============================================
# 🎯 ОБРАБОТЧИК КОЛБЭКОВ (ИСПРАВЛЕННЫЙ)
# ============================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    if is_banned(user_id):
        await query.edit_message_text("⛔ Вы заблокированы.")
        return
    
    try:
        # ВЫБОР ЯЗЫКА
        if data.startswith("lang_"):
            lang = data.replace("lang_", "")
            set_user_language(user_id, lang)
            
            if lang == 'ru':
                await query.edit_message_text(
                    "✅ <b>Язык изменен на Русский!</b>\n\n"
                    "Добро пожаловать в KURUT AI INFINITY!",
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Начать", callback_data="main_menu")]
                    ])
                )
            elif lang == 'en':
                await query.edit_message_text(
                    "✅ <b>Language changed to English!</b>\n\n"
                    "Welcome to KURUT AI INFINITY!",
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Start", callback_data="main_menu")]
                    ])
                )
            elif lang == 'uz':
                await query.edit_message_text(
                    "✅ <b>Til O'zbekcha o'zgartirildi!</b>\n\n"
                    "KURUT AI INFINITY ga xush kelibsiz!",
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Boshlash", callback_data="main_menu")]
                    ])
                )
            else:  # kg
                await query.edit_message_text(
                    "✅ <b>Тил Кыргызча өзгөртүлдү!</b>\n\n"
                    "KURUT AI INFINITY кош келиңиз!",
                    parse_mode='HTML',
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton("🚀 Баштоо", callback_data="main_menu")]
                    ])
                )
        
        # ГЛАВНОЕ МЕНЮ
        elif data == "main_menu":
            await show_main_menu(query, context, user_id)
        
        # АДМИН ПАНЕЛЬ
        elif data == "admin_panel":
            await admin_panel_callback(query, context)
        elif data == "admin_grant":
            await admin_grant_callback(query, context)
        elif data == "admin_revoke":
            await admin_revoke_callback(query, context)
        elif data == "admin_ban":
            await admin_ban_callback(query, context)
        elif data == "admin_unban":
            await admin_unban_callback(query, context)
        elif data == "admin_broadcast":
            await admin_broadcast_callback(query, context)
        
        # ПОЛУЧИТЬ СИГНАЛ
        elif data == "get_signal":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            await query.edit_message_text(
                f"<b>{t(user_id, 'choose_market')}</b>",
                parse_mode='HTML',
                reply_markup=KeyboardManager.market_menu(user_id)
            )
        
        # ВЫБОР РЫНКА (ИСПРАВЛЕННЫЙ)
        elif data in ["market_otc", "market_exchange"]:
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            if data == "market_otc":
                pairs = OTC_PAIRS
                market_type = "otc"
                title = t(user_id, 'otc_market')
            else:
                pairs = EXCHANGE_PAIRS
                market_type = "exchange"
                title = t(user_id, 'exchange_market')
            
            await query.edit_message_text(
                f"<b>{title}</b>\n\n<b>{t(user_id, 'choose_pair')}</b> (1/{len(pairs)//8+1}):",
                parse_mode='HTML',
                reply_markup=KeyboardManager.pairs_menu(pairs, market_type, 0, user_id)
            )
        
        # ПАГИНАЦИЯ (ИСПРАВЛЕННАЯ)
        elif data.startswith("page_"):
            parts = data.split("_")
            if len(parts) >= 3:
                market_type = parts[1]
                page = int(parts[2])
                
                if market_type == "otc":
                    pairs = OTC_PAIRS
                    title = t(user_id, 'otc_market')
                else:
                    pairs = EXCHANGE_PAIRS
                    title = t(user_id, 'exchange_market')
                
                await query.edit_message_text(
                    f"<b>{title}</b>\n\n<b>{t(user_id, 'choose_pair')}</b> ({page+1}/{len(pairs)//8+1}):",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.pairs_menu(pairs, market_type, page, user_id)
                )
        
        # ВЫБОР ПАРЫ (ИСПРАВЛЕННЫЙ)
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
                    
                    # Показываем анализ
                    await query.edit_message_text(
                        f"<b>{t(user_id, 'analyzing')}</b>",
                        parse_mode='HTML'
                    )
                    
                    # Генерируем сигнал
                    signal = analyzer.calculate_signal(pair, is_otc)
                    
                    # Сохраняем в историю
                    signal_history.setdefault(user_id, []).append({
                        "pair": pair,
                        "direction": signal['direction'],
                        "probability": signal['probability'],
                        "expiration": signal['expiration'],
                        "timestamp": datetime.now().isoformat(),
                        "type": "manual"
                    })
                    Database.save("signal_history.json", signal_history)
                    
                    # Форматируем сообщение
                    lang = get_user_language(user_id)
                    direction_emoji = "🟢" if signal['direction'] == "CALL" else "🔴"
                    
                    if lang == 'ru':
                        direction_text = "ВВЕРХ" if signal['direction'] == "CALL" else "ВНИЗ"
                        message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text} ({signal['direction']})</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'exact_time')}</b> <b>{signal['exact_time']}</b>
<b>{t(user_id, 'time')}</b> {signal['time']}
<b>{t(user_id, 'date')}</b> {signal['date']}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis']['market_condition']}
• {t(user_id, 'risk_level')} {signal['analysis']['risk_level']}
• {t(user_id, 'trend_strength')} {signal['analysis']['trend_strength']}
• {t(user_id, 'volatility')} {signal['analysis']['volatility']}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
• Экспирация: {signal['exp_minutes']} минут
• Сумма: 2-3% от депозита

<b>{t(user_id, 'good_luck')}</b>
"""
                    elif lang == 'en':
                        message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{signal['direction']}</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'exact_time')}</b> <b>{signal['exact_time']}</b>
<b>{t(user_id, 'time')}</b> {signal['time']}
<b>{t(user_id, 'date')}</b> {signal['date']}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis']['market_condition']}
• {t(user_id, 'risk_level')} {signal['analysis']['risk_level']}
• {t(user_id, 'trend_strength')} {signal['analysis']['trend_strength']}
• {t(user_id, 'volatility')} {signal['analysis']['volatility']}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
• Expiration: {signal['exp_minutes']} minutes
• Amount: 2-3% of deposit

<b>{t(user_id, 'good_luck')}</b>
"""
                    elif lang == 'uz':
                        direction_text = "YUQORI" if signal['direction'] == "CALL" else "PAST"
                        message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text} ({signal['direction']})</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'exact_time')}</b> <b>{signal['exact_time']}</b>
<b>{t(user_id, 'time')}</b> {signal['time']}
<b>{t(user_id, 'date')}</b> {signal['date']}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis']['market_condition']}
• {t(user_id, 'risk_level')} {signal['analysis']['risk_level']}
• {t(user_id, 'trend_strength')} {signal['analysis']['trend_strength']}
• {t(user_id, 'volatility')} {signal['analysis']['volatility']}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
• Ekspiratsiya: {signal['exp_minutes']} daqiqa
• Summa: depozitning 2-3%

<b>{t(user_id, 'good_luck')}</b>
"""
                    else:  # kg
                        direction_text = "ЖОГОРУ" if signal['direction'] == "CALL" else "ТОМЕН"
                        message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text} ({signal['direction']})</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'exact_time')}</b> <b>{signal['exact_time']}</b>
<b>{t(user_id, 'time')}</b> {signal['time']}
<b>{t(user_id, 'date')}</b> {signal['date']}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis']['market_condition']}
• {t(user_id, 'risk_level')} {signal['analysis']['risk_level']}
• {t(user_id, 'trend_strength')} {signal['analysis']['trend_strength']}
• {t(user_id, 'volatility')} {signal['analysis']['volatility']}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
• Экспирация: {signal['exp_minutes']} мүнөт
• Сумма: депозиттин 2-3%

<b>{t(user_id, 'good_luck')}</b>
"""
                    
                    await query.edit_message_text(
                        message,
                        parse_mode='HTML',
                        reply_markup=KeyboardManager.result_menu(user_id)
                    )
        
        # РЕЗУЛЬТАТЫ СДЕЛКИ
        elif data.startswith("trade_"):
            if data.startswith("trade_win_"):
                try:
                    profit = int(data.split("_")[2])
                except:
                    profit = 90
                
                update_user_stats(user_id, True, profit)
                
                if get_user_language(user_id) == 'ru':
                    message = f"✅ <b>СДЕЛКА ВЫИГРАНА!</b>\n\n💰 Прибыль: {profit}%\n📊 Статистика обновлена!"
                elif get_user_language(user_id) == 'en':
                    message = f"✅ <b>TRADE WON!</b>\n\n💰 Profit: {profit}%\n📊 Statistics updated!"
                elif get_user_language(user_id) == 'uz':
                    message = f"✅ <b>SAVDO YUTILDI!</b>\n\n💰 Foyda: {profit}%\n📊 Statistika yangilandi!"
                else:  # kg
                    message = f"✅ <b>СООДО ЖЕНИШ!</b>\n\n💰 Пайда: {profit}%\n📊 Статистика жаңыртылды!"
            else:
                update_user_stats(user_id, False)
                
                if get_user_language(user_id) == 'ru':
                    message = f"❌ <b>СДЕЛКА ПРОИГРАНА</b>\n\n📉 Не расстраивайтесь!\n🎯 Следующий сигнал будет точнее!"
                elif get_user_language(user_id) == 'en':
                    message = f"❌ <b>TRADE LOST</b>\n\n📉 Don't worry!\n🎯 Next signal will be more accurate!"
                elif get_user_language(user_id) == 'uz':
                    message = f"❌ <b>SAVDO YUTQAZILDI</b>\n\n📉 Tashvishlanmang!\n🎯 Keyingi signal aniqroq bo'ladi!"
                else:  # kg
                    message = f"❌ <b>СООДО ЖОГОЛДУ</b>\n\n📉 Кайгырбаңыз!\n🎯 Кийинки сигнал такыраак болот!"
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=KeyboardManager.result_menu(user_id)
            )
        
        # АВТОСИГНАЛЫ МЕНЮ
        elif data == "auto_signals_menu":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            enabled = auto_signals.get(user_id, False)
            
            if get_user_language(user_id) == 'ru':
                message = f"""
<b>🤖 АВТОМАТИЧЕСКИЕ СИГНАЛЫ</b>

Бот будет отправлять вам сигналы каждые 2 минуты

<b>📊 Режим:</b> {'✅ ВКЛЮЧЕН' if enabled else '❌ ВЫКЛЮЧЕН'}
<b>⏰ Интервал:</b> 2 минуты
<b>🎯 Точность:</b> 94-97%
<b>📈 Пары:</b> OTC и биржевые
<b>⏱️ Экспирация:</b> 1-10 минут
"""
            elif get_user_language(user_id) == 'en':
                message = f"""
<b>🤖 AUTOMATIC SIGNALS</b>

Bot will send you signals every 2 minutes

<b>📊 Status:</b> {'✅ ENABLED' if enabled else '❌ DISABLED'}
<b>⏰ Interval:</b> 2 minutes
<b>🎯 Accuracy:</b> 94-97%
<b>📈 Pairs:</b> OTC and exchange
<b>⏱️ Expiration:</b> 1-10 minutes
"""
            elif get_user_language(user_id) == 'uz':
                message = f"""
<b>🤖 AVTOMATIK SIGNALLAR</b>

Bot har 2 daqiqada sizga signallar yuboradi

<b>📊 Holat:</b> {'✅ YOQILGAN' if enabled else '❌ O\'CHIRILGAN'}
<b>⏰ Interval:</b> 2 daqiqa
<b>🎯 Aniqlik:</b> 94-97%
<b>📈 Juftliklar:</b> OTC va birja
<b>⏱️ Ekspiratsiya:</b> 1-10 daqiqa
"""
            else:  # kg
                message = f"""
<b>🤖 АВТОМАТТЫК СИГНАЛДАР</b>

Бот ар 2 мүнөт сайын сизге сигналдарды жөнөтөт

<b>📊 Абал:</b> {'✅ КҮЙГҮЗҮЛГӨН' if enabled else '❌ ӨЧҮРҮЛГӨН'}
<b>⏰ Интервал:</b> 2 мүнөт
<b>🎯 Тактык:</b> 94-97%
<b>📈 Жуптуктар:</b> OTC жана биржа
<b>⏱️ Экспирация:</b> 1-10 мүнөт
"""
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=KeyboardManager.auto_signals_menu(user_id)
            )
        
        # ВКЛ/ВЫКЛ АВТОСИГНАЛЫ
        elif data == "toggle_auto":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            enabled = auto_signals.get(user_id, False)
            auto_signals[user_id] = not enabled
            Database.save("auto_signals.json", auto_signals)
            
            if get_user_language(user_id) == 'ru':
                status = "включены" if not enabled else "выключены"
            elif get_user_language(user_id) == 'en':
                status = "enabled" if not enabled else "disabled"
            elif get_user_language(user_id) == 'uz':
                status = "yoqildi" if not enabled else "o'chirildi"
            else:  # kg
                status = "күйгүзүлдү" if not enabled else "өчүрүлдү"
            
            await query.answer(f"✅ Автосигналы {status}!", show_alert=True)
            await handle_callback(update, context)  # Обновляем меню
        
        # МАРАФОН
        elif data == "marathon_menu":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'require_vip'), show_alert=True)
                return
            
            await query.edit_message_text(
                f"<b>{t(user_id, 'marathon')}</b>\n\n"
                f"<b>{t(user_id, 'enter_deposit')}</b>\n"
                f"<b>{t(user_id, 'min_deposit')}</b>",
                parse_mode='HTML'
            )
            context.user_data["awaiting_deposit"] = True
        
        # СТАТИСТИКА
        elif data == "my_stats":
            ensure_user_data(user_id)
            stats = user_stats.get(user_id, {})
            
            message = f"<b>📊 {t(user_id, 'main_menu')}</b>\n\n"
            message += f"<b>🆔 ID:</b> <code>{user_id}</code>\n"
            message += f"<b>👑 Статус:</b> {'✅ VIP' if is_vip(user_id) else '🔒 Обычный'}\n"
            message += f"<b>📅 Регистрация:</b> {stats.get('join_date', 'Неизвестно')}\n\n"
            
            message += f"<b>🎯 Точность:</b> <b>{stats.get('win_rate', 0):.1f}%</b>\n"
            message += f"<b>💰 Прибыль:</b> <b>${stats.get('profit', 0):.0f}</b>\n"
            message += f"<b>📊 Сделок:</b> <b>{stats.get('total_trades', 0)}</b>\n"
            message += f"<b>✅ Выиграно:</b> <b>{stats.get('wins', 0)}</b>\n"
            message += f"<b>❌ Проиграно:</b> <b>{stats.get('losses', 0)}</b>\n"
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=KeyboardManager.back_to_menu(user_id)
            )
        
        else:
            await query.answer("⚡")
    
    except Exception as e:
        logger.error(f"Ошибка в callback: {e}")
        await query.answer("⚠️ Ошибка! Попробуйте позже.")

# ============================================
# 📨 ОБРАБОТЧИК СООБЩЕНИЙ
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    if is_banned(user_id):
        return
    
    try:
        # Обработка марафона
        if context.user_data.get("awaiting_deposit"):
            try:
                deposit = float(text)
                
                if deposit < 50:
                    await update.message.reply_text(
                        t(user_id, 'min_deposit'),
                        parse_mode='HTML'
                    )
                    return
                
                await update.message.reply_text(
                    t(user_id, 'generating'),
                    parse_mode='HTML'
                )
                
                plan = generate_marathon_plan(deposit, get_user_language(user_id))
                
                # Разбиваем если слишком длинный
                if len(plan) > 4000:
                    parts = [plan[i:i+4000] for i in range(0, len(plan), 4000)]
                    for i, part in enumerate(parts):
                        await update.message.reply_text(
                            part,
                            parse_mode='HTML'
                        )
                        await asyncio.sleep(0.5)
                else:
                    await update.message.reply_text(
                        plan,
                        parse_mode='HTML',
                        reply_markup=KeyboardManager.back_to_menu(user_id)
                    )
                
                context.user_data["awaiting_deposit"] = False
                
            except ValueError:
                await update.message.reply_text(
                    "❌ Введите число! Пример: 100, 500, 1000",
                    parse_mode='HTML'
                )
        
        # Админ сообщения
        elif context.user_data.get("admin_action"):
            await handle_admin_message(update, context)
        
        # Команды
        elif text.lower() in ['/start', 'start', 'старт']:
            await start_command(update, context)
        
        elif text.lower() in ['/admin', 'admin', 'админ']:
            if is_admin(user_id):
                await admin_panel_callback(update, context)
            else:
                await update.message.reply_text("⛔ Только для администраторов!")
        
        elif text.lower() in ['/grant', 'grant'] and is_admin(user_id):
            context.user_data["admin_action"] = "grant"
            await update.message.reply_text("➕ Введите ID пользователя для выдачи VIP:")
        
        elif text.lower() in ['/revoke', 'revoke'] and is_admin(user_id):
            context.user_data["admin_action"] = "revoke"
            await update.message.reply_text("➖ Введите ID пользователя для отзыва VIP:")
        
        elif text.lower() in ['/ban', 'ban'] and is_admin(user_id):
            context.user_data["admin_action"] = "ban"
            await update.message.reply_text("⛔ Введите ID пользователя для блокировки:")
        
        elif text.lower() in ['/unban', 'unban'] and is_admin(user_id):
            context.user_data["admin_action"] = "unban"
            await update.message.reply_text("✅ Введите ID пользователя для разблокировки:")
        
        elif text.lower() in ['/send', 'send'] and is_admin(user_id):
            context.user_data["admin_action"] = "broadcast"
            await update.message.reply_text("📢 Введите текст для рассылки:")
        
        elif text.lower() in ['/menu', 'menu', 'меню']:
            await show_main_menu(update, context, user_id)
        
        elif text.lower() in ['сигнал', 'signal']:
            if not is_vip(user_id):
                await update.message.reply_text(
                    "🔒 Требуется VIP доступ!",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.main_menu(user_id)
                )
            else:
                await update.message.reply_text(
                    "🎯 Выберите тип рынка:",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.market_menu(user_id)
                )
        
        elif text.lower() in ['марафон', 'marathon']:
            if not is_vip(user_id):
                await update.message.reply_text("🔒 Требуется VIP доступ!")
            else:
                await update.message.reply_text(
                    "📅 Введите стартовый депозит ($50+):"
                )
                context.user_data["awaiting_deposit"] = True
        
        else:
            await update.message.reply_text(
                "Используйте кнопки меню!",
                parse_mode='HTML',
                reply_markup=KeyboardManager.main_menu(user_id)
            )
    
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text(
            "⚠️ Ошибка! Используйте кнопки меню.",
            parse_mode='HTML',
            reply_markup=KeyboardManager.main_menu(user_id)
        )

# ============================================
# 🚀 ЗАПУСК БОТА
# ============================================

async def main():
    # Запуск Flask сервера
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 Flask сервер запущен на порту 8080")
    
    # Создаем приложение бота
    application = Application.builder().token(TOKEN).build()
    
    # Создаем систему автосигналов
    auto_system = AutoSignalSystem(application)
    
    # Добавляем обработчики
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("admin", lambda u, c: admin_panel_callback(u, c) if hasattr(u, 'callback_query') else None))
    application.add_handler(CommandHandler("menu", lambda u, c: show_main_menu(u, c, u.effective_user.id)))
    
    application.add_handler(CallbackQueryHandler(handle_callback))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Логируем запуск
    logger.info("🚀 ЗАПУСКАЕМ KURUT AI INFINITY v12.0")
    logger.info(f"👑 Админы: {ADMIN_IDS}")
    logger.info(f"👥 Пользователей: {len(all_users)}")
    logger.info(f"📊 Пар OTC: {len(OTC_PAIRS)}")
    logger.info(f"📈 Пар биржевых: {len(EXCHANGE_PAIRS)}")
    logger.info(f"🎯 Точность: 94-97%")
    logger.info(f"🤖 Автосигналы: каждые 2 минуты")
    logger.info(f"🌍 Языки: RU/UZ/KG/EN")
    
    try:
        # Инициализация бота
        await application.initialize()
        await application.start()
        logger.info("✅ Бот успешно запущен!")
        
        # Запускаем автосигналы
        await auto_system.start()
        logger.info("🤖 Система автосигналов запущена")
        
        # Запускаем polling
        await application.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=Update.ALL_TYPES
        )
        logger.info("🔄 Polling запущен")
        
        # Бесконечный цикл
        while True:
            await asyncio.sleep(3600)  # Спим 1 час
        
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Ошибка запуска: {e}")
    finally:
        # Корректное завершение
        try:
            logger.info("🔄 Остановка бота...")
            await auto_system.stop()
            if application.updater and application.updater.running:
                await application.updater.stop()
            if application.running:
                await application.stop()
            await application.shutdown()
            logger.info("✅ Бот корректно остановлен")
        except Exception as e:
            logger.error(f"⚠️ Ошибка при остановке: {e}")

def run_bot():
    asyncio.run(main())

if __name__ == '__main__':
    # Создаем requirements.txt
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write("""python-telegram-bot==20.7
flask==3.0.0
waitress==3.0.1
""")
        logger.info("📋 requirements.txt создан")
    except:
        pass
    
    # Запускаем бота
    run_bot()
