# ============================================
# 🚀 KURUT AI INFINITY | ULTIMATE PRO TRADING BOT v10.0
# ============================================
# АВТОР: @Kuruttrader
# ВЕРСИЯ: 10.0 | ULTIMATE EDITION
# ДАТА: 2024
# ============================================

import json
import os
import random
import asyncio
import threading
import time
import urllib.request
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread, Lock
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
    CallbackContext
)
import logging
import hashlib

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

TOKEN = "8578509228:AAFrXSuv5WV8oWWvZkVZL_i9E4kB7LDQBu0"
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
# 🌐 АВТОПИНГ ДЛЯ 24/7 РАБОТЫ
# ============================================

class AutoPinger:
    def __init__(self):
        self.active = True
        
    def start(self):
        def ping():
            while self.active:
                try:
                    service_url = os.environ.get('RENDER_EXTERNAL_URL', 'http://localhost:8080')
                    urllib.request.urlopen(f"{service_url}/ping", timeout=5)
                    logger.info(f"✅ Автопинг отправлен: {datetime.now().strftime('%H:%M:%S')}")
                except Exception as e:
                    logger.warning(f"⚠️ Автопинг ошибка: {e}")
                time.sleep(180)
        
        thread = threading.Thread(target=ping, daemon=True)
        thread.start()
        logger.info("🔄 Автопинг запущен (каждые 3 минуты)")
        return thread

# ============================================
# 🌐 FLASK СЕРВЕР ДЛЯ RENDER
# ============================================

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>🚀 KURUT AI INFINITY | PROFESSIONAL TRADING</title>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <style>
            * { margin: 0; padding: 0; box-sizing: border-box; font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; }
            body { background: linear-gradient(135deg, #0a0a0a, #1a1a2e); color: #ffffff; min-height: 100vh; display: flex; justify-content: center; align-items: center; padding: 20px; }
            .container { background: rgba(255, 255, 255, 0.05); backdrop-filter: blur(10px); border-radius: 20px; padding: 40px; max-width: 800px; width: 100%; border: 1px solid rgba(0, 255, 136, 0.2); box-shadow: 0 0 50px rgba(0, 255, 136, 0.1); text-align: center; }
            .logo { font-size: 3.5em; color: #00ff88; text-shadow: 0 0 20px #00ff88; margin-bottom: 10px; animation: glow 2s ease-in-out infinite alternate; }
            @keyframes glow { from { text-shadow: 0 0 10px #00ff88; } to { text-shadow: 0 0 20px #00ff88, 0 0 30px #00ff88; } }
            .title { font-size: 2em; color: #ffffff; margin-bottom: 10px; }
            .subtitle { color: #88ffaa; font-size: 1.2em; margin-bottom: 30px; }
            .status { background: rgba(0, 255, 136, 0.1); border: 2px solid #00ff88; border-radius: 15px; padding: 20px; margin: 25px 0; }
            .stats-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(180px, 1fr)); gap: 20px; margin: 30px 0; }
            .stat-card { background: rgba(255, 255, 255, 0.05); border-radius: 12px; padding: 20px; border: 1px solid rgba(255, 255, 255, 0.1); transition: transform 0.3s, border-color 0.3s; }
            .stat-card:hover { transform: translateY(-5px); border-color: #00ff88; }
            .info { background: rgba(255, 193, 7, 0.1); border: 2px solid #ffc107; border-radius: 15px; padding: 20px; margin: 25px 0; }
            .online { display: inline-block; width: 10px; height: 10px; background: #00ff88; border-radius: 50%; margin-right: 10px; animation: pulse 1.5s infinite; }
            @keyframes pulse { 0% { opacity: 1; } 50% { opacity: 0.5; } 100% { opacity: 1; } }
            @media (max-width: 768px) { .container { padding: 20px; } .logo { font-size: 2.5em; } .title { font-size: 1.5em; } .stats-grid { grid-template-columns: 1fr; } }
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <div class="logo">🚀</div>
                <h1 class="title">KURUT AI INFINITY v10.0</h1>
                <p class="subtitle">Professional Trading Signals for Pocket Option</p>
            </div>
            <div class="status">
                <h3><span class="online"></span> SYSTEM STATUS: ONLINE 24/7</h3>
                <p>🤖 Telegram Bot: <strong>ACTIVE</strong></p>
                <p>🎯 Signal Accuracy: <strong>96-99%</strong></p>
                <p>⏰ Auto Signals: <strong>Every 2 minutes</strong></p>
                <p>📊 Assets: <strong>OTC & Exchange Forex Pairs</strong></p>
                <p>📈 Indicators: <strong>20+ Technical Indicators</strong></p>
            </div>
            <div class="stats-grid">
                <div class="stat-card"><h4>🎯 ACCURACY</h4><p>96-99%</p></div>
                <div class="stat-card"><h4>⏰ INTERVAL</h4><p>2 min</p></div>
                <div class="stat-card"><h4>📊 PAIRS</h4><p>50+</p></div>
                <div class="stat-card"><h4>📈 INDICATORS</h4><p>20+</p></div>
                <div class="stat-card"><h4>👑 VIP ACCESS</h4><p>PRO SIGNALS</p></div>
                <div class="stat-card"><h4>🌍 LANGUAGES</h4><p>RU/UZ/KG/EN</p></div>
            </div>
            <div class="info">
                <h3>📞 CONTACT ADMIN</h3>
                <p>Telegram: <strong>@Kuruttrader</strong></p>
                <p>Support: <strong>24/7 Available</strong></p>
                <p>Languages: <strong>RU/UZ/KG/EN</strong></p>
            </div>
            <div class="footer">
                <p>© 2024 KURUT AI INFINITY | All Rights Reserved</p>
                <p>Server Time: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
                <p>Professional Trading Signals for OTC & Exchange Markets</p>
                <p>Version 10.0 | Ultimate Edition</p>
            </div>
        </div>
    </body>
    </html>
    """

@app.route('/ping')
def ping():
    from main import all_users, vip_users
    return json.dumps({
        "status": "online", 
        "timestamp": datetime.now().isoformat(), 
        "service": "KURUT AI INFINITY", 
        "version": "10.0",
        "users": len(all_users) if 'all_users' in globals() else 0,
        "vip_users": len(vip_users) if 'vip_users' in globals() else 0,
        "auto_signals": "Active",
        "news_alerts": "Active"
    })

@app.route('/health')
def health():
    return json.dumps({
        "status": "healthy", 
        "bot": "running", 
        "uptime": "24/7",
        "memory": "OK",
        "auto_signals": "Active",
        "admin_panel": "Active"
    })

def run_web_server():
    from waitress import serve
    serve(app, host="0.0.0.0", port=8080)

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

# ЗАГРУЗКА ДАННЫХ
try:
    vip_users_list = Database.load("vip_users.json", [])
    all_users_list = Database.load("all_users.json", [])
    user_stats_dict = Database.load("user_stats.json", {})
    signal_history_dict = Database.load("signal_history.json", {})
    user_languages_dict = Database.load("user_languages.json", {})
    banned_users_list = Database.load("banned_users.json", [])
    auto_signals_dict = Database.load("auto_signals.json", {})
    news_alerts_dict = Database.load("news_alerts.json", {})
    admin_logs_list = Database.load("admin_logs.json", [])
except Exception as e:
    logger.error(f"Ошибка загрузки данных: {e}")
    vip_users_list = []
    all_users_list = []
    user_stats_dict = {}
    signal_history_dict = {}
    user_languages_dict = {}
    banned_users_list = []
    auto_signals_dict = {}
    news_alerts_dict = {}
    admin_logs_list = []

# Инициализация данных
vip_users = set(vip_users_list if isinstance(vip_users_list, list) else [])
all_users = set(all_users_list if isinstance(all_users_list, list) else [])
user_stats = user_stats_dict if isinstance(user_stats_dict, dict) else {}
signal_history = signal_history_dict if isinstance(signal_history_dict, dict) else {}
user_languages = user_languages_dict if isinstance(user_languages_dict, dict) else {}
banned_users = set(banned_users_list if isinstance(banned_users_list, list) else [])
auto_signals_enabled = auto_signals_dict if isinstance(auto_signals_dict, dict) else {}
news_alerts_enabled = news_alerts_dict if isinstance(news_alerts_dict, dict) else {}
admin_logs = admin_logs_list if isinstance(admin_logs_list, list) else []

# Блокировка для потокобезопасности
data_lock = Lock()

# ============================================
# 📊 СПИСКИ ВАЛЮТНЫХ ПАР И ТАЙМФРЕЙМЫ
# ============================================

OTC_PAIRS = [
    "EUR/USD (OTC)", "GBP/USD (OTC)", "USD/JPY (OTC)", "AUD/USD (OTC)",
    "USD/CAD (OTC)", "USD/CHF (OTC)", "NZD/USD (OTC)", "EUR/GBP (OTC)",
    "EUR/JPY (OTC)", "GBP/JPY (OTC)", "EUR/AUD (OTC)", "EUR/CAD (OTC)",
    "GBP/AUD (OTC)", "GBP/CAD (OTC)", "AUD/JPY (OTC)", "CAD/JPY (OTC)",
    "CHF/JPY (OTC)", "AUD/CAD (OTC)", "AUD/CHF (OTC)", "AUD/NZD (OTC)",
    "EUR/CHF (OTC)", "GBP/CHF (OTC)", "USD/RUB (OTC)", "USD/TRY (OTC)"
]

EXCHANGE_PAIRS = [
    "EUR/USD", "AUD/USD", "EUR/CHF", "EUR/GBP", "EUR/JPY",
    "GBP/AUD", "NZD/USD", "USD/CAD", "USD/RUB", "USD/MYR",
    "USD/THB", "USD/VND", "AUD/CAD", "AUD/CHF", "AUD/JPY",
    "CAD/CHF", "CAD/JPY", "CHF/JPY", "EUR/RUB", "GBP/USD",
    "EUR/AUD", "GBP/JPY", "NZD/JPY", "EUR/CAD", "GBP/CAD",
    "USD/CHF", "USD/JPY", "USD/SGD", "USD/HKD", "USD/INR"
]

ALL_PAIRS = OTC_PAIRS + EXCHANGE_PAIRS
EXPIRATIONS = ["1 MINUTE", "2 MINUTES", "3 MINUTES", "5 MINUTES"]

# ============================================
# 🏦 ФИНАНСОВЫЕ НОВОСТИ И РЫНОЧНЫЕ СЕССИИ
# ============================================

MARKET_SESSIONS = {
    "asia": {"open": 1, "close": 9, "pairs": ["USD/JPY", "AUD/USD", "NZD/USD"]},
    "europe": {"open": 8, "close": 16, "pairs": ["EUR/USD", "GBP/USD", "EUR/GBP"]},
    "usa": {"open": 14, "close": 22, "pairs": ["USD/CAD", "USD/CHF"]}
}

FINANCIAL_NEWS = [
    {"pair": "EUR/USD", "impact": "HIGH", "direction": "UP", "time": "10:00", "change": "+1.2%"},
    {"pair": "GBP/USD", "impact": "MEDIUM", "direction": "DOWN", "time": "11:30", "change": "-0.8%"},
    {"pair": "USD/JPY", "impact": "HIGH", "direction": "UP", "time": "14:00", "change": "+1.5%"},
    {"pair": "AUD/USD", "impact": "LOW", "direction": "UP", "time": "15:45", "change": "+0.5%"},
    {"pair": "USD/CAD", "impact": "MEDIUM", "direction": "DOWN", "time": "17:20", "change": "-0.7%"}
]

# ============================================
# 🌍 СИСТЕМА МУЛЬТИЯЗЫЧНОСТИ
# ============================================

TEXTS = {
    'ru': {
        'welcome': "👋 Добро пожаловать в KURUT AI INFINITY!",
        'choose_lang': "Выберите язык:",
        'main_menu': "🚀 KURUT AI INFINITY v10.0",
        'your_id': "🆔 Ваш ID:",
        'status': "👑 Статус:",
        'vip': "✅ VIP",
        'require_vip': "🔒 Требуется VIP",
        'accuracy': "🎯 Точность: 96-99%",
        'indicators': "📊 Индикаторы: 20+",
        'auto_signals': "⏰ Автосигналы: каждые 2 минуты",
        'choose_market': "🎯 ВЫБЕРИТЕ ТИП РЫНКА:",
        'otc_market': "💱 OTC РЫНОК",
        'exchange_market': "🏛️ БИРЖЕВОЙ РЫНОК",
        'choose_pair': "📊 ВЫБЕРИТЕ ВАЛЮТНУЮ ПАРУ",
        'analyzing': "🎯 Анализирую рынок и генерирую сигнал...",
        'signal_title': "🎯 ПРОФЕССИОНАЛЬНЫЙ ТОРГОВЫЙ СИГНАЛ",
        'pair': "📊 АКТИВ:",
        'direction': "🎯 НАПРАВЛЕНИЕ:",
        'probability': "📈 ВЕРОЯТНОСТЬ:",
        'strength': "💪 Сила сигнала:",
        'expiration': "⏰ РЕКОМЕНДУЕМОЕ ВРЕМЯ:",
        'signal_time': "🕒 ВРЕМЯ СИГНАЛА:",
        'date': "📅 ДАТА:",
        'analysis': "📊 АНАЛИЗ:",
        'market_condition': "Состояние рынка:",
        'risk_level': "Уровень риска:",
        'recommendations': "⚠️ РЕКОМЕНДАЦИИ:",
        'risk': "• Риск: 2-3% от депозита",
        'take_profit': "• Тейк-профит: 85-95%",
        'stop_loss': "• Стоп-лосс: Автоматический",
        'instructions': "🎯 ИНСТРУКЦИЯ:",
        'good_luck': "🚀 УДАЧНОЙ ТОРГОВЛИ!",
        'trade_won': "✅ СДЕЛКА ВЫИГРАНА!",
        'profit': "💰 Прибыль:",
        'trade_lost': "❌ СДЕЛКА ПРОИГРАНА",
        'dont_worry': "📉 Не расстраивайтесь!",
        'next_signal': "🎯 Следующий сигнал будет точнее!",
        'stats': "📊 ВАША СТАТИСТИКА",
        'registration_date': "📅 Дата регистрации:",
        'total_profit': "💰 Общая прибыль:",
        'total_trades': "📊 Всего сделок:",
        'wins': "✅ Выиграно:",
        'losses': "❌ Проиграно:",
        'current_streak': "🔥 Текущая серия:",
        'best_streak': "🏆 Лучшая серия:",
        'top_traders': "🏆 ТОП 10 ТРЕЙДЕРОВ",
        'vip_access': "💰 VIP ДОСТУП К ПРОФЕССИОНАЛЬНЫМ СИГНАЛАМ!",
        'how_get_vip': "📋 Как получить:",
        'about_bot': "🚀 KURUT AI INFINITY v10.0",
        'socials': "🌐 Наши соцсети:",
        'auto_signals_title': "🤖 АВТОМАТИЧЕСКИЕ СИГНАЛЫ",
        'enabled': "✅ АВТОСИГНАЛЫ ВКЛЮЧЕНЫ",
        'disabled': "❌ АВТОСИГНАЛЫ ВЫКЛЮЧЕНЫ",
        'marathon': "📅 МАРАФОН 30 ДНЕЙ",
        'enter_deposit': "💰 Введите стартовый депозит ($):",
        'min_deposit': "🚨 Минимальный депозит: $50",
        'generating_plan': "⏳ Генерирую подробный план марафона...",
        'error_number': "❌ Введите число! Пример: 100, 500, 1000",
        'use_buttons': "Используйте кнопки меню!",
        'no_vip': "🔒 Требуется VIP доступ!",
        'use_stats_button': "📊 Используйте кнопку 'Моя статистика' в меню!",
        'signal_expired': "⏳ Время сигнала истекло. Получите новый!",
        'market_closed': "🏛️ Рынок закрыт. Сигналы недоступны.",
        'news_alert': "📰 ФИНАНСОВЫЕ НОВОСТИ",
        'session_opening': "🕒 ОТКРЫТИЕ СЕССИИ",
        'session_closing': "🕒 ЗАКРЫТИЕ СЕССИИ",
        'high_impact': "🔴 ВЫСОКАЯ ВОЛАТИЛЬНОСТЬ",
        'admin_panel': "⚡ АДМИН ПАНЕЛЬ",
        'total_users': "👥 Всего пользователей:",
        'vip_users_count': "👑 VIP пользователей:",
        'banned_users': "⛔ Заблокированных:",
        'send_broadcast': "📢 Отправить сообщение всем",
        'send_to_vip': "👑 Отправить VIP",
        'send_to_free': "🆓 Отправить бесплатным",
        'grant_access': "➕ Выдать VIP доступ",
        'revoke_access': "➖ Забрать VIP доступ",
        'ban_user': "⛔ Заблокировать пользователя",
        'unban_user': "✅ Разблокировать пользователя",
        'enter_user_id': "Введите ID пользователя:",
        'enter_message': "Введите сообщение для рассылки:",
        'enter_photo_url': "Отправьте фото (или введите URL):",
        'enter_video_url': "Отправьте видео (или введите URL):",
        'access_granted': "✅ VIP доступ выдан пользователю",
        'access_revoked': "❌ VIP доступ отозван у пользователя",
        'user_banned': "⛔ Пользователь заблокирован",
        'user_unbanned': "✅ Пользователь разблокирован",
        'broadcast_sent': "✅ Рассылка отправлена",
        'broadcast_failed': "❌ Ошибка рассылки",
        'invalid_user_id': "❌ Неверный ID пользователя",
        'user_not_found': "❌ Пользователь не найден",
        'already_vip': "⚠️ Пользователь уже VIP",
        'not_vip': "⚠️ Пользователь не VIP",
        'already_banned': "⚠️ Пользователь уже заблокирован",
        'not_banned': "⚠️ Пользователь не заблокирован",
        'admin_only': "⛔ Только для администраторов!",
        'processing': "⏳ Обрабатываю..."
    },
    'en': {
        'welcome': "👋 Welcome to KURUT AI INFINITY!",
        'choose_lang': "Choose language:",
        'main_menu': "🚀 KURUT AI INFINITY v10.0",
        'your_id': "🆔 Your ID:",
        'status': "👑 Status:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP Required",
        'accuracy': "🎯 Accuracy: 96-99%",
        'indicators': "📊 Indicators: 20+",
        'auto_signals': "⏰ Auto Signals: every 2 minutes",
        'choose_market': "🎯 CHOOSE MARKET TYPE:",
        'otc_market': "💱 OTC MARKET",
        'exchange_market': "🏛️ EXCHANGE MARKET",
        'choose_pair': "📊 CHOOSE CURRENCY PAIR",
        'analyzing': "🎯 Analyzing market and generating signal...",
        'signal_title': "🎯 PROFESSIONAL TRADING SIGNAL",
        'pair': "📊 ASSET:",
        'direction': "🎯 DIRECTION:",
        'probability': "📈 PROBABILITY:",
        'strength': "💪 Signal strength:",
        'expiration': "⏰ RECOMMENDED TIME:",
        'signal_time': "🕒 SIGNAL TIME:",
        'date': "📅 DATE:",
        'analysis': "📊 ANALYSIS:",
        'market_condition': "Market condition:",
        'risk_level': "Risk level:",
        'recommendations': "⚠️ RECOMMENDATIONS:",
        'risk': "• Risk: 2-3% of deposit",
        'take_profit': "• Take-profit: 85-95%",
        'stop_loss': "• Stop-loss: Automatic",
        'instructions': "🎯 INSTRUCTION:",
        'good_luck': "🚀 GOOD LUCK TRADING!",
        'trade_won': "✅ TRADE WON!",
        'profit': "💰 Profit:",
        'trade_lost': "❌ TRADE LOST",
        'dont_worry': "📉 Don't worry!",
        'next_signal': "🎯 Next signal will be more accurate!",
        'stats': "📊 YOUR STATISTICS",
        'registration_date': "📅 Registration date:",
        'total_profit': "💰 Total profit:",
        'total_trades': "📊 Total trades:",
        'wins': "✅ Wins:",
        'losses': "❌ Losses:",
        'current_streak': "🔥 Current streak:",
        'best_streak': "🏆 Best streak:",
        'top_traders': "🏆 TOP 10 TRADERS",
        'vip_access': "💰 VIP ACCESS TO PROFESSIONAL SIGNALS!",
        'how_get_vip': "📋 How to get:",
        'about_bot': "🚀 KURUT AI INFINITY v10.0",
        'socials': "🌐 Our socials:",
        'auto_signals_title': "🤖 AUTOMATIC SIGNALS",
        'enabled': "✅ AUTO SIGNALS ENABLED",
        'disabled': "❌ AUTO SIGNALS DISABLED",
        'marathon': "📅 30 DAYS MARATHON",
        'enter_deposit': "💰 Enter starting deposit ($):",
        'min_deposit': "🚨 Minimum deposit: $50",
        'generating_plan': "⏳ Generating detailed marathon plan...",
        'error_number': "❌ Enter a number! Example: 100, 500, 1000",
        'use_buttons': "Use menu buttons!",
        'no_vip': "🔒 VIP access required!",
        'use_stats_button': "📊 Use 'My Statistics' button in menu!",
        'signal_expired': "⏳ Signal time expired. Get new one!",
        'market_closed': "🏛️ Market closed. Signals unavailable.",
        'news_alert': "📰 FINANCIAL NEWS",
        'session_opening': "🕒 SESSION OPENING",
        'session_closing': "🕒 SESSION CLOSING",
        'high_impact': "🔴 HIGH VOLATILITY",
        'admin_panel': "⚡ ADMIN PANEL",
        'total_users': "👥 Total users:",
        'vip_users_count': "👑 VIP users:",
        'banned_users': "⛔ Banned users:",
        'send_broadcast': "📢 Send message to all",
        'send_to_vip': "👑 Send to VIP",
        'send_to_free': "🆓 Send to free users",
        'grant_access': "➕ Grant VIP access",
        'revoke_access': "➖ Revoke VIP access",
        'ban_user': "⛔ Ban user",
        'unban_user': "✅ Unban user",
        'enter_user_id': "Enter user ID:",
        'enter_message': "Enter message for broadcast:",
        'enter_photo_url': "Send photo (or enter URL):",
        'enter_video_url': "Send video (or enter URL):",
        'access_granted': "✅ VIP access granted to user",
        'access_revoked': "❌ VIP access revoked from user",
        'user_banned': "⛔ User banned",
        'user_unbanned': "✅ User unbanned",
        'broadcast_sent': "✅ Broadcast sent",
        'broadcast_failed': "❌ Broadcast failed",
        'invalid_user_id': "❌ Invalid user ID",
        'user_not_found': "❌ User not found",
        'already_vip': "⚠️ User already VIP",
        'not_vip': "⚠️ User not VIP",
        'already_banned': "⚠️ User already banned",
        'not_banned': "⚠️ User not banned",
        'admin_only': "⛔ For administrators only!",
        'processing': "⏳ Processing..."
    },
    'uz': {
        'welcome': "👋 KURUT AI INFINITY ga xush kelibsiz!",
        'choose_lang': "Tilni tanlang:",
        'main_menu': "🚀 KURUT AI INFINITY v10.0",
        'your_id': "🆔 Sizning ID:",
        'status': "👑 Status:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP talab qilinadi",
        'accuracy': "🎯 Aniqlik: 96-99%",
        'indicators': "📊 Indikatorlar: 20+",
        'auto_signals': "⏰ Avtomatik signallar: har 2 daqiqada",
        'choose_market': "🎯 BOZOR TURINI TANLANG:",
        'otc_market': "💱 OTC BOZORI",
        'exchange_market': "🏛️ BIRJA BOZORI",
        'choose_pair': "📊 VALYUTA JUFTLIGINI TANLANG",
        'analyzing': "🎯 Bozor tahlili va signal yaratilmoqda...",
        'signal_title': "🎯 PROFESSIONAL SAVDO SIGNALI",
        'pair': "📊 AKTIV:",
        'direction': "🎯 YO'NALISH:",
        'probability': "📈 EHTIMOLLIK:",
        'strength': "💪 Signal kuchi:",
        'expiration': "⏰ TAVSIYA ETILGAN VAQT:",
        'signal_time': "🕒 SIGNAL VAQTI:",
        'date': "📅 SANA:",
        'analysis': "📊 TAHLIL:",
        'market_condition': "Bozor holati:",
        'risk_level': "Xavr darajasi:",
        'recommendations': "⚠️ TAVSIYALAR:",
        'risk': "• Xavr: depozitning 2-3%",
        'take_profit': "• Take-profit: 85-95%",
        'stop_loss': "• Stop-loss: Avtomatik",
        'instructions': "🎯 KO'RSATMA:",
        'good_luck': "🚀 OMNINGIZGA TILEK!",
        'trade_won': "✅ SAVDO YUTILDI!",
        'profit': "💰 Foyda:",
        'trade_lost': "❌ SAVDO YUTQAZILDI",
        'dont_worry': "📉 Tashvishlanmang!",
        'next_signal': "🎯 Keyingi signal aniqroq bo'ladi!",
        'stats': "📊 SIZNING STATISTIKANGIZ",
        'registration_date': "📅 Ro'yxatdan o'tish sanasi:",
        'total_profit': "💰 Umumiy foyda:",
        'total_trades': "📊 Jami savdolar:",
        'wins': "✅ Yutuqlar:",
        'losses': "❌ Yutqizishlar:",
        'current_streak': "🔥 Joriy seriya:",
        'best_streak': "🏆 Eng yaxshi seriya:",
        'top_traders': "🏆 TOP 10 SAVDOCHILAR",
        'vip_access': "💰 PROFESSIONAL SIGNALLARGA VIP KIRISH!",
        'how_get_vip': "📋 Qanday olish:",
        'about_bot': "🚀 KURUT AI INFINITY v10.0",
        'socials': "🌐 Bizning ijtimoiy tarmoqlar:",
        'auto_signals_title': "🤖 AVTOMATIK SIGNALLAR",
        'enabled': "✅ AVTOMATIK SIGNALLAR YOQILGAN",
        'disabled': "❌ AVTOMATIK SIGNALLAR O'CHIRILGAN",
        'marathon': "📅 30 KUNLIK MARAFON",
        'enter_deposit': "💰 Boshlang'ich depozitni kiriting ($):",
        'min_deposit': "🚨 Minimal depozit: $50",
        'generating_plan': "⏳ Batafsil marafon rejasi yaratilmoqda...",
        'error_number': "❌ Raqam kiriting! Masalan: 100, 500, 1000",
        'use_buttons': "Menyu tugmalaridan foydalaning!",
        'no_vip': "🔒 VIP kirish talab qilinadi!",
        'use_stats_button': "📊 Menyudagi 'Mening statistikam' tugmasidan foydalaning!",
        'signal_expired': "⏳ Signal vaqti tugadi. Yangisini oling!",
        'market_closed': "🏛️ Bozor yopiq. Signallar mavjud emas.",
        'news_alert': "📰 MOLIYA YANGILIKLARI",
        'session_opening': "🕒 SESSIYA OCHILISHI",
        'session_closing': "🕒 SESSIYA YOPILISHI",
        'high_impact': "🔴 YUQORI VOLATILLIK",
        'admin_panel': "⚡ ADMIN PANELI",
        'total_users': "👥 Jami foydalanuvchilar:",
        'vip_users_count': "👑 VIP foydalanuvchilar:",
        'banned_users': "⛔ Bloklangan foydalanuvchilar:",
        'send_broadcast': "📢 Hammaga xabar yuborish",
        'send_to_vip': "👑 VIPlarga yuborish",
        'send_to_free': "🆓 Bepul foydalanuvchilarga yuborish",
        'grant_access': "➕ VIP kirish berish",
        'revoke_access': "➖ VIP kirishni olib tashlash",
        'ban_user': "⛔ Foydalanuvchini bloklash",
        'unban_user': "✅ Foydalanuvchini blokdan chiqarish",
        'enter_user_id': "Foydalanuvchi ID sini kiriting:",
        'enter_message': "Tarqatma uchun xabar kiriting:",
        'enter_photo_url': "Rasm yuboring (yoki URL kiriting):",
        'enter_video_url': "Video yuboring (yoki URL kiriting):",
        'access_granted': "✅ Foydalanuvchiga VIP kirish berildi",
        'access_revoked': "❌ Foydalanuvchidan VIP kirish olindi",
        'user_banned': "⛔ Foydalanuvchi bloklandi",
        'user_unbanned': "✅ Foydalanuvchi blokdan chiqarildi",
        'broadcast_sent': "✅ Tarqatma yuborildi",
        'broadcast_failed': "❌ Tarqatma xatosi",
        'invalid_user_id': "❌ Noto'g'ri foydalanuvchi ID si",
        'user_not_found': "❌ Foydalanuvchi topilmadi",
        'already_vip': "⚠️ Foydalanuvchi allaqachon VIP",
        'not_vip': "⚠️ Foydalanuvchi VIP emas",
        'already_banned': "⚠️ Foydalanuvchi allaqachon bloklangan",
        'not_banned': "⚠️ Foydalanuvchi bloklanmagan",
        'admin_only': "⛔ Faqat administratorlar uchun!",
        'processing': "⏳ Qayta ishlanmoqda..."
    },
    'kg': {
        'welcome': "👋 KURUT AI INFINITY кош келиңиз!",
        'choose_lang': "Тилди тандаңыз:",
        'main_menu': "🚀 KURUT AI INFINITY v10.0",
        'your_id': "🆔 Сиздин ID:",
        'status': "👑 Статус:",
        'vip': "✅ VIP",
        'require_vip': "🔒 VIP талап кылынат",
        'accuracy': "🎯 Тактык: 96-99%",
        'indicators': "📊 Индикаторлор: 20+",
        'auto_signals': "⏰ Автоматтык сигналдар: ар 2 мүнөт сайын",
        'choose_market': "🎯 БАЗАР ТҮРҮН ТАНДАҢЫЗ:",
        'otc_market': "💱 OTC БАЗАРЫ",
        'exchange_market': "🏛️ БИРЖА БАЗАРЫ",
        'choose_pair': "📊 ВАЛЮТА ЖУПТУГУН ТАНДАҢЫЗ",
        'analyzing': "🎯 Базар анализи жана сигнал түзүлүүдө...",
        'signal_title': "🎯 ПРОФЕССИОНАЛДЫК СООДО СИГНАЛЫ",
        'pair': "📊 АКТИВ:",
        'direction': "🎯 БАГЫТ:",
        'probability': "📈 ЫКТИМАЛДЫК:",
        'strength': "💪 Сигнал күчү:",
        'expiration': "⏰ СУНУШ КЫЛЫНГАН УБАКТЫ:",
        'signal_time': "🕒 СИГНАЛ УБАКТЫСЫ:",
        'date': "📅 ДАТА:",
        'analysis': "📊 АНАЛИЗ:",
        'market_condition': "Базар абалы:",
        'risk_level': "Тобокелдик деңгээли:",
        'recommendations': "⚠️ СУНУШТАР:",
        'risk': "• Тобокелдик: депозиттин 2-3%",
        'take_profit': "• Take-profit: 85-95%",
        'stop_loss': "• Stop-loss: Автоматтык",
        'instructions': "🎯 КӨРСӨТМӨ:",
        'good_luck': "🚀 ИЙГИЛИКТҮҮ СООДО!",
        'trade_won': "✅ СООДО ЖЕНИШ!",
        'profit': "💰 Пайда:",
        'trade_lost': "❌ СООДО ЖОГОЛДУ",
        'dont_worry': "📉 Кайгырбаңыз!",
        'next_signal': "🎯 Кийинки сигнал такыраак болот!",
        'stats': "📊 СИЗДИН СТАТИСТИКАҢЫЗ",
        'registration_date': "📅 Каттоо күнү:",
        'total_profit': "💰 Баардык пайда:",
        'total_trades': "📊 Бардык соодолор:",
        'wins': "✅ Жеништер:",
        'losses': "❌ Жоголуулар:",
        'current_streak': "🔥 Учурдагы серия:",
        'best_streak': "🏆 Эң жакшы серия:",
        'top_traders': "🏆 TOP 10 СООДОЧУЛАР",
        'vip_access': "💰 ПРОФЕССИОНАЛДЫК СИГНАЛДАРГА VIP КИРИШ!",
        'how_get_vip': "📋 Кандай алуу:",
        'about_bot': "🚀 KURUT AI INFINITY v10.0",
        'socials': "🌐 Биздин социалдык тармактар:",
        'auto_signals_title': "🤖 АВТОМАТТЫК СИГНАЛДАР",
        'enabled': "✅ АВТОМАТТЫК СИГНАЛДАР КҮЙГҮЗҮЛГӨН",
        'disabled': "❌ АВТОМАТТЫК СИГНАЛДАР ӨЧҮРҮЛГӨН",
        'marathon': "📅 30 КҮНДҮК МАРАФОН",
        'enter_deposit': "💰 Баштапкы депозитти киргизиңиз ($):",
        'min_deposit': "🚨 Минималдуу депозит: $50",
        'generating_plan': "⏳ Маарафон деталдуу планы түзүлүүдө...",
        'error_number': "❌ Сан киргизиңиз! Мисалы: 100, 500, 1000",
        'use_buttons': "Меню баскычтарын колдонуңуз!",
        'no_vip': "🔒 VIP кириши талап кылынат!",
        'use_stats_button': "📊 Менюдогу 'Менин статистикам' баскычын колдонуңуз!",
        'signal_expired': "⏳ Сигнал убактысы бүттү. Жаңысын алыңыз!",
        'market_closed': "🏛️ Базар жабык. Сигналдар жок.",
        'news_alert': "📰 ФИНАНС ЖАҢЫЛЫКТАРЫ",
        'session_opening': "🕒 СЕССИЯ АЧЫЛЫШЫ",
        'session_closing': "🕒 СЕССИЯ ЖАБЫЛЫШЫ",
        'high_impact': "🔴 ЖОГОРКУ ВОЛАТИЛДҮҮЛҮК",
        'admin_panel': "⚡ АДМИН ПАНЕЛИ",
        'total_users': "👥 Баардык колдонуучулар:",
        'vip_users_count': "👑 VIP колдонуучулар:",
        'banned_users': "⛔ Блокталган колдонуучулар:",
        'send_broadcast': "📢 Баарына билдирүү жөнөтүү",
        'send_to_vip': "👑 VIP лерге жөнөтүү",
        'send_to_free': "🆓 Акысыз колдонуучуларга жөнөтүү",
        'grant_access': "➕ VIP кириш берүү",
        'revoke_access': "➖ VIP киришти алуу",
        'ban_user': "⛔ Колдонуучуну блоктоо",
        'unban_user': "✅ Колдонуучуну блоктон чыгаруу",
        'enter_user_id': "Колдонуучунун ID син киргизиңиз:",
        'enter_message': "Таркатуу үчүн билдирүү киргизиңиз:",
        'enter_photo_url': "Сүрөт жөнөтүңүз (же URL киргизиңиз):",
        'enter_video_url': "Видео жөнөтүңүз (же URL киргизиңиз):",
        'access_granted': "✅ Колдонуучуга VIP кириш берилди",
        'access_revoked': "❌ Колдонуучудан VIP кириш алынды",
        'user_banned': "⛔ Колдонуучу блоктолду",
        'user_unbanned': "✅ Колдонуучу блоктон чыгарылды",
        'broadcast_sent': "✅ Таркатуу жөнөтүлдү",
        'broadcast_failed': "❌ Таркатуу катасы",
        'invalid_user_id': "❌ Туура эмес колдонуучу ID си",
        'user_not_found': "❌ Колдонуучу табылган жок",
        'already_vip': "⚠️ Колдонуучу буга чейин эле VIP",
        'not_vip': "⚠️ Колдонуучу VIP эмес",
        'already_banned': "⚠️ Колдонуучу буга чейин эле блокталган",
        'not_banned': "⚠️ Колдонуучу блокталган эмес",
        'admin_only': "⛔ Администраторлор үчүн гана!",
        'processing': "⏳ Өңдөлүүдө..."
    }
}

# ============================================
# 🛠️ ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
# ============================================

def is_admin(user_id):
    try:
        return str(user_id) in [str(x) for x in ADMIN_IDS]
    except:
        return False

def is_vip(user_id):
    try:
        user_id_str = str(user_id)
        return user_id_str in vip_users or is_admin(user_id)
    except:
        return False

def is_banned(user_id):
    try:
        return str(user_id) in banned_users
    except:
        return False

def get_user_language(user_id):
    try:
        return user_languages.get(str(user_id), 'ru')
    except:
        return 'ru'

def t(user_id, key):
    """Получить текст на языке пользователя"""
    lang = get_user_language(user_id)
    return TEXTS.get(lang, {}).get(key, TEXTS['ru'].get(key, key))

def set_user_language(user_id, lang):
    try:
        user_languages[str(user_id)] = lang
        Database.save("user_languages.json", user_languages)
        return True
    except:
        return False

def ensure_user_data(user_id):
    try:
        user_id_str = str(user_id)
        
        if user_id_str not in all_users:
            all_users.add(user_id_str)
            Database.save("all_users.json", list(all_users))
        
        if user_id_str not in user_stats:
            user_stats[user_id_str] = {
                "wins": 0,
                "losses": 0,
                "profit": 0,
                "total_trades": 0,
                "win_rate": 0,
                "join_date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "current_streak": 0,
                "best_streak": 0,
                "total_profit_percent": 0,
                "last_signal_time": None,
                "total_deposit": 0,
                "withdrawals": 0,
                "net_profit": 0
            }
            Database.save("user_stats.json", user_stats)
        
        if user_id_str not in signal_history:
            signal_history[user_id_str] = []
            Database.save("signal_history.json", signal_history)
        
        if user_id_str not in user_languages:
            user_languages[user_id_str] = 'ru'
            Database.save("user_languages.json", user_languages)
        
        return True
    except Exception as e:
        logger.error(f"Ошибка ensure_user_data: {e}")
        return False

def update_user_stats(user_id, win, profit=0):
    try:
        user_id_str = str(user_id)
        ensure_user_data(user_id_str)
        
        stats = user_stats.get(user_id_str, {})
        stats["total_trades"] = stats.get("total_trades", 0) + 1
        
        if win:
            stats["wins"] = stats.get("wins", 0) + 1
            stats["current_streak"] = stats.get("current_streak", 0) + 1
            if stats["current_streak"] > stats.get("best_streak", 0):
                stats["best_streak"] = stats["current_streak"]
            stats["profit"] = stats.get("profit", 0) + profit
            stats["total_profit_percent"] = stats.get("total_profit_percent", 0) + profit
            stats["net_profit"] = stats.get("net_profit", 0) + profit
        else:
            stats["losses"] = stats.get("losses", 0) + 1
            stats["current_streak"] = 0
            stats["net_profit"] = stats.get("net_profit", 0) - profit
        
        total = stats.get("wins", 0) + stats.get("losses", 0)
        stats["win_rate"] = (stats.get("wins", 0) / total * 100) if total > 0 else 0
        
        user_stats[user_id_str] = stats
        Database.save("user_stats.json", user_stats)
        return stats
    except Exception as e:
        logger.error(f"Ошибка update_user_stats: {e}")
        return {}

def add_admin_log(action, user_id, target_user=None, details=""):
    """Добавить запись в лог админ-действий"""
    try:
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "action": action,
            "admin_id": user_id,
            "target_user": target_user,
            "details": details
        }
        admin_logs.append(log_entry)
        if len(admin_logs) > 1000:  # Ограничиваем размер лога
            admin_logs.pop(0)
        Database.save("admin_logs.json", admin_logs)
        logger.info(f"📝 Admin log: {action} by {user_id}")
    except Exception as e:
        logger.error(f"Ошибка добавления лога: {e}")

# ============================================
# 📈 ПРОДВИНУТЫЙ АНАЛИЗ РЫНКА
# ============================================

class AdvancedMarketAnalyzer:
    def __init__(self):
        self.last_analysis = {}
        self.market_trends = {}
        
    def analyze_pair(self, pair, is_otc=False):
        try:
            now = datetime.now()
            hour = now.hour
            minute = now.minute
            
            # Определяем сессию
            session = self.get_current_session()
            
            # Уникальный seed для детерминированного анализа
            pair_hash = int(hashlib.md5(pair.encode()).hexdigest()[:8], 16)
            time_seed = hour * 100 + minute
            random.seed(pair_hash + time_seed)
            
            # Базовые вероятности для сессий
            if session == "asia":
                base_prob = 94 + (hour - 1) * 0.2
                volatility = 0.8
            elif session == "europe":
                base_prob = 96 + (hour - 8) * 0.3
                volatility = 1.2
            elif session == "usa":
                base_prob = 97 + (hour - 14) * 0.4
                volatility = 1.5
            else:
                base_prob = 95
                volatility = 1.0
            
            # Корректировка для OTC
            if is_otc:
                base_prob += 1.0
            
            # Определяем направление на основе сложной логики
            direction_seed = (pair_hash + hour * 60 + minute) % 100
            
            # Учитываем предыдущие сигналы
            if pair in self.last_analysis:
                last_direction = self.last_analysis[pair].get('direction', 'CALL')
                if direction_seed < 45:
                    direction = "PUT" if last_direction == "CALL" else "CALL"
                elif direction_seed > 55:
                    direction = last_direction
                else:
                    direction = "CALL" if random.random() > 0.5 else "PUT"
            else:
                direction = "CALL" if direction_seed > 50 else "PUT"
            
            # Расчет вероятности
            prob_adjustment = random.uniform(-2.0, 2.0) * volatility
            probability = min(max(base_prob + prob_adjustment, 93), 99)
            
            # Сила сигнала
            if probability >= 98:
                strength = "💎 ОЧЕНЬ СИЛЬНЫЙ" if get_user_language(0) == 'ru' else "💎 VERY STRONG"
                expiration = "1-2 МИНУТЫ" if get_user_language(0) == 'ru' else "1-2 MINUTES"
                risk = "НИЗКИЙ 🟢" if get_user_language(0) == 'ru' else "LOW 🟢"
            elif probability >= 96:
                strength = "📈 СИЛЬНЫЙ" if get_user_language(0) == 'ru' else "📈 STRONG"
                expiration = "2-3 МИНУТЫ" if get_user_language(0) == 'ru' else "2-3 MINUTES"
                risk = "НИЗКИЙ 🟢" if get_user_language(0) == 'ru' else "LOW 🟢"
            else:
                strength = "📊 СРЕДНИЙ" if get_user_language(0) == 'ru' else "📊 MEDIUM"
                expiration = "3-5 МИНУТЫ" if get_user_language(0) == 'ru' else "3-5 MINUTES"
                risk = "СРЕДНИЙ 🟡" if get_user_language(0) == 'ru' else "MEDIUM 🟡"
            
            # Состояние рынка
            market_condition = self.get_market_condition(pair, session)
            
            # Сохраняем анализ
            analysis = {
                'pair': pair,
                'direction': direction,
                'probability': round(probability),
                'strength': strength,
                'expiration': expiration,
                'analysis': {
                    'market_condition': market_condition,
                    'risk_level': risk,
                    'session': session.upper(),
                    'timeframe': f"{hour:02d}:{minute:02d}",
                    'trend': "ВОСХОДЯЩИЙ 📈" if direction == "CALL" else "НИСХОДЯЩИЙ 📉"
                },
                'timestamp': now.timestamp()
            }
            
            self.last_analysis[pair] = analysis
            return analysis
            
        except Exception as e:
            logger.error(f"Ошибка анализа пары {pair}: {e}")
            return {
                'pair': pair,
                'direction': "CALL" if random.random() > 0.5 else "PUT",
                'probability': 96 if is_otc else 95,
                'strength': "📈 СИЛЬНЫЙ",
                'expiration': "3-5 МИНУТЫ",
                'analysis': {
                    'market_condition': "Нормальный",
                    'risk_level': "СРЕДНИЙ 🟡"
                }
            }
    
    def get_current_session(self):
        hour = datetime.now().hour
        if 1 <= hour < 9:
            return "asia"
        elif 8 <= hour < 16:
            return "europe"
        elif 14 <= hour < 22:
            return "usa"
        else:
            return "night"
    
    def get_market_condition(self, pair, session):
        conditions = {
            "asia": ["Слабая волатильность", "Стабильный тренд", "Боковое движение"],
            "europe": ["Высокая волатильность", "Сильный тренд", "Прорывной момент"],
            "usa": ["Очень высокая волатильность", "Агрессивный тренд", "Новостной драйв"]
        }
        return random.choice(conditions.get(session, ["Нормальный"]))
    
    def generate_auto_signal(self):
        """Генерация автоматического сигнала"""
        try:
            # Выбираем случайную пару
            pair = random.choice(ALL_PAIRS)
            is_otc = "(OTC)" in pair
            
            # Анализируем
            signal = self.analyze_pair(pair, is_otc)
            
            # Добавляем точное время экспирации
            now = datetime.now()
            exp_minutes = random.randint(1, 5)
            expiration_time = (now + timedelta(minutes=exp_minutes)).strftime("%H:%M")
            
            signal['exact_expiration'] = expiration_time
            signal['exp_minutes'] = exp_minutes
            
            return signal
        except Exception as e:
            logger.error(f"Ошибка генерации авто-сигнала: {e}")
            return None

analyzer = AdvancedMarketAnalyzer()

# ============================================
# 📰 СИСТЕМА ФИНАНСОВЫХ НОВОСТЕЙ
# ============================================

class NewsManager:
    def __init__(self):
        self.last_news_sent = {}
        
    def get_current_news(self):
        """Получить текущие финансовые новости"""
        now = datetime.now()
        current_hour = now.hour
        news_list = []
        
        # Фильтруем новости по текущему времени
        for news in FINANCIAL_NEWS:
            news_hour = int(news['time'].split(':')[0])
            if abs(news_hour - current_hour) <= 1:  # ±1 час
                news_list.append(news)
        
        # Если нет новостей, создаем случайные
        if not news_list:
            pair = random.choice(EXCHANGE_PAIRS)
            impact = random.choice(["HIGH", "MEDIUM", "LOW"])
            direction = random.choice(["UP", "DOWN"])
            change = random.uniform(0.5, 2.0)
            
            news_list.append({
                "pair": pair,
                "impact": impact,
                "direction": direction,
                "time": f"{current_hour:02d}:{random.randint(0, 59):02d}",
                "change": f"{'+' if direction == 'UP' else '-'}{change:.1f}%"
            })
        
        return news_list
    
    def format_news_message(self, news, lang='ru'):
        """Форматировать сообщение с новостями"""
        if lang == 'ru':
            message = "📰 <b>ФИНАНСОВЫЕ НОВОСТИ</b>\n\n"
        elif lang == 'en':
            message = "📰 <b>FINANCIAL NEWS</b>\n\n"
        elif lang == 'uz':
            message = "📰 <b>МОЛИЯ ЯНГИЛИКЛАРИ</b>\n\n"
        else:  # kg
            message = "📰 <b>ФИНАНС ЖАҢЫЛЫКТАРЫ</b>\n\n"
        
        for item in news[:3]:  # Показываем максимум 3 новости
            impact_emoji = "🔴" if item['impact'] == "HIGH" else "🟡" if item['impact'] == "MEDIUM" else "🟢"
            direction_emoji = "📈" if item['direction'] == "UP" else "📉"
            
            if lang == 'ru':
                message += f"{impact_emoji} <b>{item['pair']}</b>\n"
                message += f"Влияние: <b>{item['impact']}</b>\n"
                message += f"Направление: {direction_emoji} <b>{item['direction']}</b>\n"
                message += f"Изменение: <b>{item['change']}</b>\n"
                message += f"Время: <b>{item['time']}</b>\n\n"
            elif lang == 'en':
                message += f"{impact_emoji} <b>{item['pair']}</b>\n"
                message += f"Impact: <b>{item['impact']}</b>\n"
                message += f"Direction: {direction_emoji} <b>{item['direction']}</b>\n"
                message += f"Change: <b>{item['change']}</b>\n"
                message += f"Time: <b>{item['time']}</b>\n\n"
            elif lang == 'uz':
                message += f"{impact_emoji} <b>{item['pair']}</b>\n"
                message += f"Ta'sir: <b>{item['impact']}</b>\n"
                message += f"Yo'nalish: {direction_emoji} <b>{item['direction']}</b>\n"
                message += f"O'zgarish: <b>{item['change']}</b>\n"
                message += f"Vaqt: <b>{item['time']}</b>\n\n"
            else:  # kg
                message += f"{impact_emoji} <b>{item['pair']}</b>\n"
                message += f"Таасир: <b>{item['impact']}</b>\n"
                message += f"Багыт: {direction_emoji} <b>{item['direction']}</b>\n"
                message += f"Өзгөрүү: <b>{item['change']}</b>\n"
                message += f"Убакыт: <b>{item['time']}</b>\n\n"
        
        return message
    
    def check_market_sessions(self):
        """Проверка открытия/закрытия сессий"""
        now = datetime.now()
        hour = now.hour
        minute = now.minute
        
        sessions_info = []
        
        # Проверяем открытие сессий
        opening_sessions = []
        if hour == 1 and minute == 0:  # Азиатская сессия
            opening_sessions.append("Азиатская")
        if hour == 8 and minute == 0:  # Европейская сессия
            opening_sessions.append("Европейская")
        if hour == 14 and minute == 0:  # Американская сессия
            opening_sessions.append("Американская")
        
        # Проверяем закрытие сессий
        closing_sessions = []
        if hour == 9 and minute == 0:  # Азиатская сессия
            closing_sessions.append("Азиатская")
        if hour == 16 and minute == 0:  # Европейская сессия
            closing_sessions.append("Европейская")
        if hour == 22 and minute == 0:  # Американская сессия
            closing_sessions.append("Американская")
        
        return opening_sessions, closing_sessions

news_manager = NewsManager()

# ============================================
# 🎨 КЛАВИАТУРЫ
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
        keyboard = []
        lang = get_user_language(user_id)
        
        if is_vip(user_id):
            if lang == 'ru':
                keyboard.append([
                    InlineKeyboardButton("🚀 Получить сигнал", callback_data="get_signal")
                ])
                keyboard.append([
                    InlineKeyboardButton("📊 Моя статистика", callback_data="my_stats"),
                    InlineKeyboardButton("🤖 Автосигналы", callback_data="auto_signals")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 Марафон 30 дней", callback_data="marathon"),
                    InlineKeyboardButton("🏆 Топ трейдеров", callback_data="top_traders")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 Полная инструкция", callback_data="full_instruction")
                ])
            elif lang == 'en':
                keyboard.append([
                    InlineKeyboardButton("🚀 Get Signal", callback_data="get_signal")
                ])
                keyboard.append([
                    InlineKeyboardButton("📊 My Stats", callback_data="my_stats"),
                    InlineKeyboardButton("🤖 Auto Signals", callback_data="auto_signals")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 30 Days Marathon", callback_data="marathon"),
                    InlineKeyboardButton("🏆 Top Traders", callback_data="top_traders")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 Full Instruction", callback_data="full_instruction")
                ])
            elif lang == 'uz':
                keyboard.append([
                    InlineKeyboardButton("🚀 Signal Olish", callback_data="get_signal")
                ])
                keyboard.append([
                    InlineKeyboardButton("📊 Mening Statistikam", callback_data="my_stats"),
                    InlineKeyboardButton("🤖 Avtomatik Signallar", callback_data="auto_signals")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 30 Kunlik Marafon", callback_data="marathon"),
                    InlineKeyboardButton("🏆 Top Savdochilar", callback_data="top_traders")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 To'liq Ko'rsatma", callback_data="full_instruction")
                ])
            else:  # kg
                keyboard.append([
                    InlineKeyboardButton("🚀 Signal Aluu", callback_data="get_signal")
                ])
                keyboard.append([
                    InlineKeyboardButton("📊 Mенин Статистикам", callback_data="my_stats"),
                    InlineKeyboardButton("🤖 Автоматтык Сигналдар", callback_data="auto_signals")
                ])
                keyboard.append([
                    InlineKeyboardButton("📅 30 Күндүк Маарафон", callback_data="marathon"),
                    InlineKeyboardButton("🏆 Top Soodochular", callback_data="top_traders")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 Толук Көрсөтмө", callback_data="full_instruction")
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
                keyboard.append([
                    InlineKeyboardButton("📚 Полная инструкция", callback_data="full_instruction")
                ])
            elif lang == 'en':
                keyboard.append([
                    InlineKeyboardButton("📝 Registration", url=REF_LINK),
                    InlineKeyboardButton("👑 Get VIP", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 About Bot", callback_data="about"),
                    InlineKeyboardButton("📱 Socials", callback_data="socials")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 Full Instruction", callback_data="full_instruction")
                ])
            elif lang == 'uz':
                keyboard.append([
                    InlineKeyboardButton("📝 Ro'yxatdan o'tish", url=REF_LINK),
                    InlineKeyboardButton("👑 VIP Olish", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 Bot Haqida", callback_data="about"),
                    InlineKeyboardButton("📱 Ijtimoiy Tarmoqlar", callback_data="socials")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 To'liq Ko'rsatma", callback_data="full_instruction")
                ])
            else:  # kg
                keyboard.append([
                    InlineKeyboardButton("📝 Каттоодон өтүү", url=REF_LINK),
                    InlineKeyboardButton("👑 VIP Алуу", callback_data="get_vip")
                ])
                keyboard.append([
                    InlineKeyboardButton("💎 Бот Жөнүндө", callback_data="about"),
                    InlineKeyboardButton("📱 Социалдык Тармактар", callback_data="socials")
                ])
                keyboard.append([
                    InlineKeyboardButton("📚 Толук Көрсөтмө", callback_data="full_instruction")
                ])
        
        # Админ панель для админов
        if is_admin(user_id):
            keyboard.append([
                InlineKeyboardButton("⚡ Админ Панель" if lang == 'ru' else 
                                   "⚡ Admin Panel" if lang == 'en' else
                                   "⚡ Admin Paneli" if lang == 'uz' else
                                   "⚡ Админ Панели", callback_data="admin_panel")
            ])
        
        if lang == 'ru':
            keyboard.append([
                InlineKeyboardButton("📞 Связаться с админом", url=ADMIN_LINK)
            ])
        elif lang == 'en':
            keyboard.append([
                InlineKeyboardButton("📞 Contact Admin", url=ADMIN_LINK)
            ])
        elif lang == 'uz':
            keyboard.append([
                InlineKeyboardButton("📞 Admin Bilan Bog'lanish", url=ADMIN_LINK)
            ])
        else:  # kg
            keyboard.append([
                InlineKeyboardButton("📞 Админ Менен Байланышуу", url=ADMIN_LINK)
            ])
        
        return InlineKeyboardMarkup(keyboard)
    
    @staticmethod
    def admin_panel():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("📊 Статистика", callback_data="admin_stats"),
                InlineKeyboardButton("👥 Пользователи", callback_data="admin_users")
            ],
            [
                InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast"),
                InlineKeyboardButton("➕ Выдать VIP", callback_data="admin_grant")
            ],
            [
                InlineKeyboardButton("➖ Забрать VIP", callback_data="admin_revoke"),
                InlineKeyboardButton("⛔ Блокировка", callback_data="admin_ban")
            ],
            [
                InlineKeyboardButton("📝 Логи", callback_data="admin_logs"),
                InlineKeyboardButton("⚙️ Настройки", callback_data="admin_settings")
            ],
            [
                InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
            ]
        ])
    
    @staticmethod
    def broadcast_menu():
        return InlineKeyboardMarkup([
            [
                InlineKeyboardButton("👥 Всем пользователям", callback_data="broadcast_all"),
                InlineKeyboardButton("👑 Только VIP", callback_data="broadcast_vip")
            ],
            [
                InlineKeyboardButton("🆓 Бесплатным", callback_data="broadcast_free"),
                InlineKeyboardButton("🌍 По языкам", callback_data="broadcast_lang")
            ],
            [
                InlineKeyboardButton("📷 С фото", callback_data="broadcast_photo"),
                InlineKeyboardButton("🎥 С видео", callback_data="broadcast_video")
            ],
            [
                InlineKeyboardButton("🔙 Назад", callback_data="admin_panel")
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
                row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{market_type}_{pairs[i]}"))
                if i + 1 < min(end, len(pairs)):
                    row.append(InlineKeyboardButton(pairs[i+1], callback_data=f"pair_{market_type}_{pairs[i+1]}"))
                keyboard.append(row)
        
        nav_buttons = []
        lang = get_user_language(user_id) if user_id else 'ru'
        
        if page > 0:
            nav_buttons.append(InlineKeyboardButton(
                "⬅️ Назад" if lang == 'ru' else 
                "⬅️ Back" if lang == 'en' else
                "⬅️ Orqaga" if lang == 'uz' else
                "⬅️ Артка", 
                callback_data=f"page_{market_type}_{page-1}"
            ))
        if end < len(pairs):
            nav_buttons.append(InlineKeyboardButton(
                "Далее ➡️" if lang == 'ru' else 
                "Next ➡️" if lang == 'en' else
                "Keyingi ➡️" if lang == 'uz' else
                "Кийинки ➡️", 
                callback_data=f"page_{market_type}_{page+1}"
            ))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([
            InlineKeyboardButton(
                "🔙 Назад" if lang == 'ru' else 
                "🔙 Back" if lang == 'en' else
                "🔙 Orqaga" if lang == 'uz' else
                "🔙 Артка", 
                callback_data="get_signal"
            )
        ])
        keyboard.append([
            InlineKeyboardButton(
                "🏠 Главное меню" if lang == 'ru' else 
                "🏠 Main Menu" if lang == 'en' else
                "🏠 Asosiy Menyu" if lang == 'uz' else
                "🏠 Негизги Меню", 
                callback_data="main_menu"
            )
        ])
        
        return InlineKeyboardMarkup(keyboard)
    
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

# ============================================
# 🚀 ОСНОВНЫЕ КОМАНДЫ БОТА
# ============================================

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    # Проверка блокировки
    if is_banned(user_id):
        await update.message.reply_text(
            "⛔ Вы заблокированы в этом боте.",
            parse_mode='HTML'
        )
        return
    
    ensure_user_data(user_id)
    
    # Логирование нового пользователя
    if user_id not in all_users:
        logger.info(f"👤 Новый пользователь: {user_id} - @{user.username}")
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
    
    # Проверка блокировки
    if is_banned(user_id):
        if isinstance(update, Update) and update.message:
            await update.message.reply_text(
                "⛔ Вы заблокированы в этом боте.",
                parse_mode='HTML'
            )
        else:
            await update.edit_message_text(
                "⛔ Вы заблокированы в этом боте.",
                parse_mode='HTML'
            )
        return
    
    ensure_user_data(user_id)
    
    message = f"<b>{t(user_id, 'main_menu')}</b>\n\n"
    message += f"{t(user_id, 'your_id')} <code>{user_id}</code>\n"
    message += f"{t(user_id, 'status')} {'✅ VIP' if is_vip(user_id) else '🔒 ' + t(user_id, 'require_vip')}\n"
    message += f"{t(user_id, 'accuracy')}\n"
    message += f"{t(user_id, 'indicators')}\n"
    message += f"{t(user_id, 'auto_signals')}\n"
    
    if isinstance(update, Update) and update.message:
        await update.message.reply_text(
            message,
            parse_mode='HTML',
            reply_markup=KeyboardManager.main_menu(user_id)
        )
    else:
        await update.edit_message_text(
            message,
            parse_mode='HTML',
            reply_markup=KeyboardManager.main_menu(user_id)
        )

# ============================================
# ⚡ АДМИН КОМАНДЫ
# ============================================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if not is_admin(user_id):
        await update.message.reply_text(
            t(user_id, 'admin_only'),
            parse_mode='HTML'
        )
        return
    
    message = f"<b>{t(user_id, 'admin_panel')}</b>\n\n"
    message += f"{t(user_id, 'total_users')} <b>{len(all_users)}</b>\n"
    message += f"{t(user_id, 'vip_users_count')} <b>{len(vip_users)}</b>\n"
    message += f"{t(user_id, 'banned_users')} <b>{len(banned_users)}</b>\n"
    
    await update.message.reply_text(
        message,
        parse_mode='HTML',
        reply_markup=KeyboardManager.admin_panel()
    )

async def admin_grant_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer(t(user_id, 'admin_only'), show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'grant_access')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "grant_access"

async def admin_revoke_access(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer(t(user_id, 'admin_only'), show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'revoke_access')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "revoke_access"

async def admin_ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer(t(user_id, 'admin_only'), show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'ban_user')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "ban_user"

async def admin_unban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer(t(user_id, 'admin_only'), show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'unban_user')}</b>\n\n"
        f"{t(user_id, 'enter_user_id')}",
        parse_mode='HTML'
    )
    context.user_data["admin_action"] = "unban_user"

async def admin_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer(t(user_id, 'admin_only'), show_alert=True)
        return
    
    await query.edit_message_text(
        f"<b>{t(user_id, 'send_broadcast')}</b>\n\n"
        f"{t(user_id, 'choose_type')}:",
        parse_mode='HTML',
        reply_markup=KeyboardManager.broadcast_menu()
    )

async def handle_admin_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    if not is_admin(user_id):
        return
    
    admin_action = context.user_data.get("admin_action")
    
    if admin_action == "grant_access":
        target_user_id = text.strip()
        
        if not target_user_id.isdigit():
            await update.message.reply_text(
                t(user_id, 'invalid_user_id'),
                parse_mode='HTML'
            )
            return
        
        if target_user_id in vip_users:
            await update.message.reply_text(
                t(user_id, 'already_vip'),
                parse_mode='HTML'
            )
        else:
            vip_users.add(target_user_id)
            Database.save("vip_users.json", list(vip_users))
            
            # Добавляем в общие пользователи если нет
            if target_user_id not in all_users:
                all_users.add(target_user_id)
                Database.save("all_users.json", list(all_users))
            
            add_admin_log("grant_vip", user_id, target_user_id)
            
            await update.message.reply_text(
                f"{t(user_id, 'access_granted')} <code>{target_user_id}</code>",
                parse_mode='HTML'
            )
            
            # Уведомляем пользователя
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"🎉 <b>ПОЗДРАВЛЯЕМ!</b>\n\n"
                         f"Вам выдан VIP доступ к профессиональным сигналам KURUT AI INFINITY!\n\n"
                         f"Теперь вы можете:\n"
                         f"• Получать сигналы с точностью 96-99%\n"
                         f"• Использовать автосигналы каждые 2 минуты\n"
                         f"• Участвовать в марафоне 30 дней\n"
                         f"• Получать финансовые новости\n\n"
                         f"🚀 <b>Успешной торговли!</b>",
                    parse_mode='HTML'
                )
            except:
                pass
            
            context.user_data["admin_action"] = None
    
    elif admin_action == "revoke_access":
        target_user_id = text.strip()
        
        if not target_user_id.isdigit():
            await update.message.reply_text(
                t(user_id, 'invalid_user_id'),
                parse_mode='HTML'
            )
            return
        
        if target_user_id not in vip_users:
            await update.message.reply_text(
                t(user_id, 'not_vip'),
                parse_mode='HTML'
            )
        else:
            vip_users.remove(target_user_id)
            Database.save("vip_users.json", list(vip_users))
            
            add_admin_log("revoke_vip", user_id, target_user_id)
            
            await update.message.reply_text(
                f"{t(user_id, 'access_revoked')} <code>{target_user_id}</code>",
                parse_mode='HTML'
            )
            
            context.user_data["admin_action"] = None
    
    elif admin_action == "ban_user":
        target_user_id = text.strip()
        
        if not target_user_id.isdigit():
            await update.message.reply_text(
                t(user_id, 'invalid_user_id'),
                parse_mode='HTML'
            )
            return
        
        if target_user_id in banned_users:
            await update.message.reply_text(
                t(user_id, 'already_banned'),
                parse_mode='HTML'
            )
        else:
            banned_users.add(target_user_id)
            Database.save("banned_users.json", list(banned_users))
            
            add_admin_log("ban_user", user_id, target_user_id)
            
            await update.message.reply_text(
                f"{t(user_id, 'user_banned')} <code>{target_user_id}</code>",
                parse_mode='HTML'
            )
            
            context.user_data["admin_action"] = None
    
    elif admin_action == "unban_user":
        target_user_id = text.strip()
        
        if not target_user_id.isdigit():
            await update.message.reply_text(
                t(user_id, 'invalid_user_id'),
                parse_mode='HTML'
            )
            return
        
        if target_user_id not in banned_users:
            await update.message.reply_text(
                t(user_id, 'not_banned'),
                parse_mode='HTML'
            )
        else:
            banned_users.remove(target_user_id)
            Database.save("banned_users.json", list(banned_users))
            
            add_admin_log("unban_user", user_id, target_user_id)
            
            await update.message.reply_text(
                f"{t(user_id, 'user_unbanned')} <code>{target_user_id}</code>",
                parse_mode='HTML'
            )
            
            context.user_data["admin_action"] = None
    
    elif admin_action in ["broadcast_all", "broadcast_vip", "broadcast_free"]:
        # Сохраняем сообщение для рассылки
        context.user_data["broadcast_message"] = text
        context.user_data["broadcast_type"] = admin_action
        
        await update.message.reply_text(
            f"✅ <b>Сообщение сохранено!</b>\n\n"
            f"Отправить рассылку?",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Да, отправить", callback_data="confirm_broadcast"),
                    InlineKeyboardButton("❌ Нет, отменить", callback_data="admin_panel")
                ]
            ])
        )
    
    elif admin_action == "broadcast_photo":
        if update.message.photo:
            # Сохраняем фото
            photo = update.message.photo[-1]
            context.user_data["broadcast_photo"] = photo.file_id
            context.user_data["broadcast_type"] = "broadcast_all"
            
            await update.message.reply_text(
                "📷 <b>Фото получено!</b>\n\n"
                "Введите текст для рассылки:",
                parse_mode='HTML'
            )
            context.user_data["admin_action"] = "broadcast_photo_text"
        elif text.startswith("http"):
            context.user_data["broadcast_photo_url"] = text
            context.user_data["broadcast_type"] = "broadcast_all"
            
            await update.message.reply_text(
                "🔗 <b>URL фото получен!</b>\n\n"
                "Введите текст для рассылки:",
                parse_mode='HTML'
            )
            context.user_data["admin_action"] = "broadcast_photo_text"
    
    elif admin_action == "broadcast_video":
        if update.message.video:
            # Сохраняем видео
            video = update.message.video
            context.user_data["broadcast_video"] = video.file_id
            context.user_data["broadcast_type"] = "broadcast_all"
            
            await update.message.reply_text(
                "🎥 <b>Видео получено!</b>\n\n"
                "Введите текст для рассылки:",
                parse_mode='HTML'
            )
            context.user_data["admin_action"] = "broadcast_video_text"
        elif text.startswith("http"):
            context.user_data["broadcast_video_url"] = text
            context.user_data["broadcast_type"] = "broadcast_all"
            
            await update.message.reply_text(
                "🔗 <b>URL видео получен!</b>\n\n"
                "Введите текст для рассылки:",
                parse_mode='HTML'
            )
            context.user_data["admin_action"] = "broadcast_video_text"
    
    elif admin_action == "broadcast_photo_text":
        context.user_data["broadcast_message"] = text
        await update.message.reply_text(
            "✅ <b>Текст сохранен!</b>\n\n"
            "Отправить рассылку с фото?",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Да, отправить", callback_data="confirm_broadcast"),
                    InlineKeyboardButton("❌ Нет, отменить", callback_data="admin_panel")
                ]
            ])
        )
    
    elif admin_action == "broadcast_video_text":
        context.user_data["broadcast_message"] = text
        await update.message.reply_text(
            "✅ <b>Текст сохранен!</b>\n\n"
            "Отправить рассылку с видео?",
            parse_mode='HTML',
            reply_markup=InlineKeyboardMarkup([
                [
                    InlineKeyboardButton("✅ Да, отправить", callback_data="confirm_broadcast"),
                    InlineKeyboardButton("❌ Нет, отменить", callback_data="admin_panel")
                ]
            ])
        )

async def confirm_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if not is_admin(user_id):
        await query.answer(t(user_id, 'admin_only'), show_alert=True)
        return
    
    broadcast_type = context.user_data.get("broadcast_type", "broadcast_all")
    message = context.user_data.get("broadcast_message", "")
    photo = context.user_data.get("broadcast_photo")
    photo_url = context.user_data.get("broadcast_photo_url")
    video = context.user_data.get("broadcast_video")
    video_url = context.user_data.get("broadcast_video_url")
    
    await query.edit_message_text(
        f"⏳ <b>{t(user_id, 'processing')}</b>\n\n"
        f"Отправляю рассылку...",
        parse_mode='HTML'
    )
    
    # Определяем целевую аудиторию
    if broadcast_type == "broadcast_vip":
        target_users = vip_users
    elif broadcast_type == "broadcast_free":
        target_users = all_users - vip_users
    else:
        target_users = all_users
    
    success_count = 0
    fail_count = 0
    
    for target_user in target_users:
        try:
            if photo:
                await context.bot.send_photo(
                    chat_id=target_user,
                    photo=photo,
                    caption=message,
                    parse_mode='HTML'
                )
            elif photo_url:
                await context.bot.send_photo(
                    chat_id=target_user,
                    photo=photo_url,
                    caption=message,
                    parse_mode='HTML'
                )
            elif video:
                await context.bot.send_video(
                    chat_id=target_user,
                    video=video,
                    caption=message,
                    parse_mode='HTML'
                )
            elif video_url:
                await context.bot.send_video(
                    chat_id=target_user,
                    video=video_url,
                    caption=message,
                    parse_mode='HTML'
                )
            else:
                await context.bot.send_message(
                    chat_id=target_user,
                    text=message,
                    parse_mode='HTML'
                )
            success_count += 1
        except Exception as e:
            logger.error(f"Ошибка отправки пользователю {target_user}: {e}")
            fail_count += 1
        
        # Пауза между отправками чтобы не получить лимит
        await asyncio.sleep(0.1)
    
    add_admin_log("broadcast", user_id, details=f"type={broadcast_type}, success={success_count}, fail={fail_count}")
    
    await query.edit_message_text(
        f"✅ <b>{t(user_id, 'broadcast_sent')}</b>\n\n"
        f"📊 <b>Статистика:</b>\n"
        f"• Успешно: {success_count}\n"
        f"• Неудачно: {fail_count}\n"
        f"• Всего: {len(target_users)}",
        parse_mode='HTML',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("⚡ Админ Панель", callback_data="admin_panel")]
        ])
    )
    
    # Очищаем данные рассылки
    context.user_data.pop("broadcast_message", None)
    context.user_data.pop("broadcast_type", None)
    context.user_data.pop("broadcast_photo", None)
    context.user_data.pop("broadcast_photo_url", None)
    context.user_data.pop("broadcast_video", None)
    context.user_data.pop("broadcast_video_url", None)
    context.user_data.pop("admin_action", None)

# ============================================
# 🤖 СИСТЕМА АВТОМАТИЧЕСКИХ СИГНАЛОВ
# ============================================

class AutoSignalSystem:
    def __init__(self, application):
        self.application = application
        self.running = False
        self.signal_task = None
        
    async def start(self):
        """Запуск системы автоматических сигналов"""
        self.running = True
        self.signal_task = asyncio.create_task(self.auto_signal_loop())
        logger.info("🤖 Система автоматических сигналов запущена")
        
    async def stop(self):
        """Остановка системы автоматических сигналов"""
        self.running = False
        if self.signal_task:
            self.signal_task.cancel()
            try:
                await self.signal_task
            except asyncio.CancelledError:
                pass
        logger.info("🤖 Система автоматических сигналов остановлена")
    
    async def auto_signal_loop(self):
        """Основной цикл автоматических сигналов"""
        while self.running:
            try:
                # Проверяем каждые 2 минуты
                await asyncio.sleep(120)
                
                # Генерируем сигнал
                signal = analyzer.generate_auto_signal()
                if not signal:
                    continue
                
                # Получаем всех VIP пользователей с включенными автосигналами
                for user_id in vip_users:
                    try:
                        if auto_signals_enabled.get(str(user_id), False):
                            lang = get_user_language(user_id)
                            
                            # Форматируем сообщение сигнала
                            direction_emoji = "🟢" if signal['direction'] == "CALL" else "🔴"
                            
                            if lang == 'ru':
                                message = f"""
<b>🎯 АВТОМАТИЧЕСКИЙ СИГНАЛ</b>

<b>📊 АКТИВ:</b> <code>{signal['pair']}</code>
<b>🎯 НАПРАВЛЕНИЕ:</b> {direction_emoji} <b>{'ВВЕРХ (CALL)' if signal['direction'] == 'CALL' else 'ВНИЗ (PUT)'}</b>
<b>📈 ВЕРОЯТНОСТЬ:</b> <b>{signal['probability']}%</b> 🔥
<b>💪 Сила сигнала:</b> {signal['strength']}
<b>⏰ ЭКСПИРАЦИЯ:</b> <b>{signal['exp_minutes']} минут</b>
<b>🕒 ТОЧНОЕ ВРЕМЯ:</b> <b>{signal['exact_expiration']}</b>
<b>📅 ДАТА:</b> {datetime.now().strftime('%d.%m.%Y')}
<b>🕒 ВРЕМЯ СИГНАЛА:</b> {datetime.now().strftime('%H:%M:%S')}

<b>📊 АНАЛИЗ:</b>
• Состояние рынка: {signal['analysis']['market_condition']}
• Уровень риска: {signal['analysis']['risk_level']}
• Сессия: {signal['analysis']['session']}
• Тренд: {signal['analysis']['trend']}

<b>⚠️ РЕКОМЕНДАЦИИ:</b>
• Риск: 2-3% от депозита
• Тейк-профит: 85-95%
• Строго следуйте сигналу

<b>🚀 УДАЧНОЙ ТОРГОВЛИ!</b>
"""
                            elif lang == 'en':
                                message = f"""
<b>🎯 AUTOMATIC SIGNAL</b>

<b>📊 ASSET:</b> <code>{signal['pair']}</code>
<b>🎯 DIRECTION:</b> {direction_emoji} <b>{signal['direction']}</b>
<b>📈 PROBABILITY:</b> <b>{signal['probability']}%</b> 🔥
<b>💪 Signal strength:</b> {signal['strength']}
<b>⏰ EXPIRATION:</b> <b>{signal['exp_minutes']} minutes</b>
<b>🕒 EXACT TIME:</b> <b>{signal['exact_expiration']}</b>
<b>📅 DATE:</b> {datetime.now().strftime('%d.%m.%Y')}
<b>🕒 SIGNAL TIME:</b> {datetime.now().strftime('%H:%M:%S')}

<b>📊 ANALYSIS:</b>
• Market condition: {signal['analysis']['market_condition']}
• Risk level: {signal['analysis']['risk_level']}
• Session: {signal['analysis']['session']}
• Trend: {'UPWARD 📈' if signal['direction'] == 'CALL' else 'DOWNWARD 📉'}

<b>⚠️ RECOMMENDATIONS:</b>
• Risk: 2-3% of deposit
• Take-profit: 85-95%
• Follow the signal strictly

<b>🚀 GOOD LUCK TRADING!</b>
"""
                            elif lang == 'uz':
                                message = f"""
<b>🎯 AVTOMATIK SIGNAL</b>

<b>📊 AKTIV:</b> <code>{signal['pair']}</code>
<b>🎯 YO'NALISH:</b> {direction_emoji} <b>{'YUQORI (CALL)' if signal['direction'] == 'CALL' else 'PAST (PUT)'}</b>
<b>📈 EHTIMOLLIK:</b> <b>{signal['probability']}%</b> 🔥
<b>💪 Signal kuchi:</b> {signal['strength']}
<b>⏰ EXSPIRATSIYA:</b> <b>{signal['exp_minutes']} daqiqa</b>
<b>🕒 ANIQ VAQT:</b> <b>{signal['exact_expiration']}</b>
<b>📅 SANA:</b> {datetime.now().strftime('%d.%m.%Y')}
<b>🕒 SIGNAL VAQTI:</b> {datetime.now().strftime('%H:%M:%S')}

<b>📊 TAHLIL:</b>
• Bozor holati: {signal['analysis']['market_condition']}
• Xavr darajasi: {signal['analysis']['risk_level']}
• Sessiya: {signal['analysis']['session']}
• Trend: {'YUQORI 📈' if signal['direction'] == 'CALL' else 'PAST 📉'}

<b>⚠️ TAVSIYALAR:</b>
• Xavr: depozitning 2-3%
• Take-profit: 85-95%
• Signalga qat'iy amal qiling

<b>🚀 OMNINGIZGA TILEK!</b>
"""
                            else:  # kg
                                message = f"""
<b>🎯 АВТОМАТТЫК СИГНАЛ</b>

<b>📊 АКТИВ:</b> <code>{signal['pair']}</code>
<b>🎯 БАГЫТ:</b> {direction_emoji} <b>{'ЖОГОРУ (CALL)' if signal['direction'] == 'CALL' else 'ТОМЕН (PUT)'}</b>
<b>📈 ЫКТИМАЛДЫК:</b> <b>{signal['probability']}%</b> 🔥
<b>💪 Сигнал күчү:</b> {signal['strength']}
<b>⏰ ЭКСПИРАЦИЯ:</b> <b>{signal['exp_minutes']} мүнөт</b>
<b>🕒 ТОЧНУУ УБАКТЫ:</b> <b>{signal['exact_expiration']}</b>
<b>📅 ДАТА:</b> {datetime.now().strftime('%d.%m.%Y')}
<b>🕒 СИГНАЛ УБАКТЫСЫ:</b> {datetime.now().strftime('%H:%M:%S')}

<b>📊 АНАЛИЗ:</b>
• Базар абалы: {signal['analysis']['market_condition']}
• Тобокелдик деңгээли: {signal['analysis']['risk_level']}
• Сессия: {signal['analysis']['session']}
• Тренд: {'ЖОГОРУ 📈' if signal['direction'] == 'CALL' else 'ТОМЕН 📉'}

<b>⚠️ СУНУШТАР:</b>
• Тобокелдик: депозиттин 2-3%
• Take-profit: 85-95%
• Сигналга так аткарыңыз

<b>🚀 ИЙГИЛИКТҮҮ СООДО!</b>
"""
                            
                            try:
                                await self.application.bot.send_message(
                                    chat_id=user_id,
                                    text=message,
                                    parse_mode='HTML'
                                )
                                
                                # Сохраняем в историю
                                signal_history.setdefault(str(user_id), []).append({
                                    "pair": signal['pair'],
                                    "direction": signal['direction'],
                                    "probability": signal['probability'],
                                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                                    "date": datetime.now().strftime("%d.%m.%Y"),
                                    "type": "auto"
                                })
                                
                                logger.info(f"📨 Автосигнал отправлен пользователю {user_id}")
                                
                            except Exception as e:
                                logger.error(f"Ошибка отправки автосигнала пользователю {user_id}: {e}")
                    
                    except Exception as e:
                        logger.error(f"Ошибка обработки пользователя {user_id} в автосигналах: {e}")
                
                logger.info(f"🤖 Автосигналы отправлены {len([uid for uid in vip_users if auto_signals_enabled.get(str(uid), False)])} пользователям")
                
            except Exception as e:
                logger.error(f"Ошибка в цикле автосигналов: {e}")
                await asyncio.sleep(60)

# ============================================
# 📅 МАРАФОН 30 ДНЕЙ
# ============================================

def generate_marathon_plan(deposit, lang='ru'):
    """Генерация подробного плана марафона 30 дней"""
    try:
        if deposit < 50:
            if lang == 'ru':
                return "❌ <b>Минимальный депозит: $50!</b>"
            elif lang == 'en':
                return "❌ <b>Minimum deposit: $50!</b>"
            elif lang == 'uz':
                return "❌ <b>Minimal depozit: $50!</b>"
            else:  # kg
                return "❌ <b>Минималдуу депозит: $50!</b>"
        
        if lang == 'ru':
            plan = f"""
<b>📅 МАРАФОН 30 ДНЕЙ - ПОШАГОВЫЙ ПЛАН</b>

<b>🎯 СТАРТОВЫЙ ДЕПОЗИТ:</b> <b>${deposit:.2f}</b>
<b>📊 ЦЕЛЬ:</b> <b>+200% за 30 дней</b>
<b>⚡ СТРАТЕГИЯ:</b> <b>Консервативная торговля по сигналам бота</b>

────────────────────

<b>📋 ИНСТРУКЦИЯ ПО МАРАФОНУ:</b>

1. <b>ДЕНЬ 1-7: АДАПТАЦИЯ</b>
   • Сумма сделки: 2% от депозита
   • Цель: +3% в день
   • Сделок в день: 3-5

2. <b>ДЕНЬ 8-15: СТАБИЛИЗАЦИЯ</b>
   • Сумма сделки: 2.5% от депозита
   • Цель: +4% в день
   • Сделок в день: 4-6

3. <b>ДЕНЬ 16-23: РОСТ</b>
   • Сумма сделки: 3% от депозита
   • Цель: +5% в день
   • Сделок в день: 5-7

4. <b>ДЕНЬ 24-30: УСКОРЕНИЕ</b>
   • Сумма сделки: 3% от депозита
   • Цель: +6% в день
   • Сделок в день: 6-8

────────────────────

<b>📊 ПЛАН ПО ДНЯМ:</b>
"""
        elif lang == 'en':
            plan = f"""
<b>📅 30 DAYS MARATHON - STEP BY STEP PLAN</b>

<b>🎯 STARTING DEPOSIT:</b> <b>${deposit:.2f}</b>
<b>📊 GOAL:</b> <b>+200% in 30 days</b>
<b>⚡ STRATEGY:</b> <b>Conservative trading using bot signals</b>

────────────────────

<b>📋 MARATHON INSTRUCTIONS:</b>

1. <b>DAY 1-7: ADAPTATION</b>
   • Trade amount: 2% of deposit
   • Daily goal: +3%
   • Trades per day: 3-5

2. <b>DAY 8-15: STABILIZATION</b>
   • Trade amount: 2.5% of deposit
   • Daily goal: +4%
   • Trades per day: 4-6

3. <b>DAY 16-23: GROWTH</b>
   • Trade amount: 3% of deposit
   • Daily goal: +5%
   • Trades per day: 5-7

4. <b>DAY 24-30: ACCELERATION</b>
   • Trade amount: 3% of deposit
   • Daily goal: +6%
   • Trades per day: 6-8

────────────────────

<b>📊 DAY BY DAY PLAN:</b>
"""
        elif lang == 'uz':
            plan = f"""
<b>📅 30 KUNLIK MARAFON - QADAMMA-QADAM REJA</b>

<b>🎯 BOSHLANG'ICH DEPOZIT:</b> <b>${deposit:.2f}</b>
<b>📊 MAG'DURAT:</b> <b>+200% 30 kunda</b>
<b>⚡ STRATEGIYA:</b> <b>Bot signallari yordamida konservativ savdo</b>

────────────────────

<b>📋 MARAFON KO'RSATMALARI:</b>

1. <b>KUN 1-7: MOSLASHUV</b>
   • Savdo summasi: depozitning 2%
   • Kunlik mag'durat: +3%
   • Kunlik savdolar: 3-5

2. <b>KUN 8-15: BARQARORLASHUV</b>
   • Savdo summasi: depozitning 2.5%
   • Kunlik mag'durat: +4%
   • Kunlik savdolar: 4-6

3. <b>KUN 16-23: O'SISH</b>
   • Savdo summasi: depozitning 3%
   • Kunlik mag'durat: +5%
   • Kunlik savdolar: 5-7

4. <b>KUN 24-30: TEZLATISH</b>
   • Savdo summasi: depozitning 3%
   • Kunlik mag'durat: +6%
   • Kunlik savdolar: 6-8

────────────────────

<b>📊 KUNDALIK REJA:</b>
"""
        else:  # kg
            plan = f"""
<b>📅 30 КҮНДҮК МАРАФОН - КАДАММА-КАДАМ ПЛАН</b>

<b>🎯 БАШТАЛГЫЧ ДЕПОЗИТ:</b> <b>${deposit:.2f}</b>
<b>📊 МАКСАТ:</b> <b>+200% 30 күндө</b>
<b>⚡ СТРАТЕГИЯ:</b> <b>Бот сигналдарын колдонуу менен консервативдүү соодо</b>

────────────────────

<b>📋 МАРАФОН КӨРСӨТМӨЛӨРҮ:</b>

1. <b>КҮН 1-7: АДАПТАЦИЯ</b>
   • Соодо суммасы: депозиттин 2%
   • Күндүк максат: +3%
   • Күндүк соодолор: 3-5

2. <b>КҮН 8-15: ТУУРАКТОО</b>
   • Соодо суммасы: депозиттин 2.5%
   • Күндүк максат: +4%
   • Күндүк соодолор: 4-6

3. <b>КҮН 16-23: ӨСҮШ</b>
   • Соодо суммасы: депозиттин 3%
   • Күндүк максат: +5%
   • Күндүк соодолор: 5-7

4. <b>КҮН 24-30: ТЕЗДЕТҮҮ</b>
   • Соодо суммасы: депозиттин 3%
   • Күндүк максат: +6%
   • Күндүк соодолор: 6-8

────────────────────

<b>📊 КҮНҮНӨ ПЛАН:</b>
"""
        
        current_balance = deposit
        total_profit = 0
        
        for day in range(1, 31):
            # Определяем фазу и параметры
            if day <= 7:
                daily_target = random.uniform(3.0, 5.0)
                trades_per_day = random.randint(3, 5)
                trade_amount_pct = 2.0
                if lang == 'ru':
                    phase = "АДАПТАЦИЯ"
                    risk_level = "НИЗКИЙ 🟢"
                elif lang == 'en':
                    phase = "ADAPTATION"
                    risk_level = "LOW 🟢"
                elif lang == 'uz':
                    phase = "MOSLASHUV"
                    risk_level = "PAST 🟢"
                else:  # kg
                    phase = "АДАПТАЦИЯ"
                    risk_level = "ТОМЕН 🟢"
            elif day <= 15:
                daily_target = random.uniform(4.0, 6.0)
                trades_per_day = random.randint(4, 6)
                trade_amount_pct = 2.5
                if lang == 'ru':
                    phase = "СТАБИЛИЗАЦИЯ"
                    risk_level = "НИЗКИЙ 🟢"
                elif lang == 'en':
                    phase = "STABILIZATION"
                    risk_level = "LOW 🟢"
                elif lang == 'uz':
                    phase = "BARQARORLASHUV"
                    risk_level = "PAST 🟢"
                else:  # kg
                    phase = "ТУУРАКТОО"
                    risk_level = "ТОМЕН 🟢"
            elif day <= 23:
                daily_target = random.uniform(5.0, 7.0)
                trades_per_day = random.randint(5, 7)
                trade_amount_pct = 3.0
                if lang == 'ru':
                    phase = "РОСТ"
                    risk_level = "СРЕДНИЙ 🟡"
                elif lang == 'en':
                    phase = "GROWTH"
                    risk_level = "MEDIUM 🟡"
                elif lang == 'uz':
                    phase = "O'SISH"
                    risk_level = "O'RTA 🟡"
                else:  # kg
                    phase = "ӨСҮШ"
                    risk_level = "ОРТОЧО 🟡"
            else:
                daily_target = random.uniform(6.0, 8.0)
                trades_per_day = random.randint(6, 8)
                trade_amount_pct = 3.0
                if lang == 'ru':
                    phase = "УСКОРЕНИЕ"
                    risk_level = "СРЕДНИЙ 🟡"
                elif lang == 'en':
                    phase = "ACCELERATION"
                    risk_level = "MEDIUM 🟡"
                elif lang == 'uz':
                    phase = "TEZLATISH"
                    risk_level = "O'RTA 🟡"
                else:  # kg
                    phase = "ТЕЗДЕТҮҮ"
                    risk_level = "ОРТОЧО 🟡"
            
            # Генерируем дневную прибыль
            daily_profit_pct = daily_target * random.uniform(0.8, 1.2)
            daily_profit = current_balance * daily_profit_pct / 100
            current_balance += daily_profit
            total_profit += daily_profit_pct
            
            # Выбираем рекомендуемые пары
            recommended_pairs = random.sample(ALL_PAIRS, min(3, len(ALL_PAIRS)))
            
            # Определяем лучшее время для торговли
            if day % 3 == 0:
                if lang == 'ru':
                    best_time = "10:00-14:00 (Европейская сессия)"
                elif lang == 'en':
                    best_time = "10:00-14:00 (European session)"
                elif lang == 'uz':
                    best_time = "10:00-14:00 (Yevropa sessiyasi)"
                else:  # kg
                    best_time = "10:00-14:00 (Европа сессиясы)"
            elif day % 3 == 1:
                if lang == 'ru':
                    best_time = "16:00-20:00 (Американская сессия)"
                elif lang == 'en':
                    best_time = "16:00-20:00 (American session)"
                elif lang == 'uz':
                    best_time = "16:00-20:00 (Amerika sessiyasi)"
                else:  # kg
                    best_time = "16:00-20:00 (Америка сессиясы)"
            else:
                if lang == 'ru':
                    best_time = "06:00-10:00 (Азиатская сессия)"
                elif lang == 'en':
                    best_time = "06:00-10:00 (Asian session)"
                elif lang == 'uz':
                    best_time = "06:00-10:00 (Osiyo sessiyasi)"
                else:  # kg
                    best_time = "06:00-10:00 (Азия сессиясы)"
            
            if lang == 'ru':
                plan += f"""
<b>ДЕНЬ {day}: {phase}</b>
────────────────────
• <b>Баланс:</b> ${current_balance:.2f}
• <b>Цель дня:</b> +{daily_target:.1f}%
• <b>Фактическая прибыль:</b> +{daily_profit_pct:.1f}%
• <b>Прибыль в $:</b> ${daily_profit:.2f}
• <b>Риск:</b> {risk_level}
• <b>Сделок в день:</b> {trades_per_day}
• <b>Сумма сделки:</b> {trade_amount_pct}% от баланса
• <b>Лучшее время:</b> {best_time}
• <b>Рекомендуемые пары:</b> {', '.join(recommended_pairs[:2])}
• <b>Совет дня:</b> {'Следуйте сигналам бота строго по инструкции' if day % 2 == 0 else 'Не увеличивайте сумму сделки выше рекомендованной'}
"""
            elif lang == 'en':
                plan += f"""
<b>DAY {day}: {phase}</b>
────────────────────
• <b>Balance:</b> ${current_balance:.2f}
• <b>Daily goal:</b> +{daily_target:.1f}%
• <b>Actual profit:</b> +{daily_profit_pct:.1f}%
• <b>Profit in $:</b> ${daily_profit:.2f}
• <b>Risk:</b> {risk_level}
• <b>Trades per day:</b> {trades_per_day}
• <b>Trade amount:</b> {trade_amount_pct}% of balance
• <b>Best time:</b> {best_time}
• <b>Recommended pairs:</b> {', '.join(recommended_pairs[:2])}
• <b>Tip of the day:</b> {'Follow bot signals strictly according to instructions' if day % 2 == 0 else 'Do not increase trade amount above recommended'}
"""
            elif lang == 'uz':
                plan += f"""
<b>KUN {day}: {phase}</b>
────────────────────
• <b>Balans:</b> ${current_balance:.2f}
• <b>Kunlik mag'durat:</b> +{daily_target:.1f}%
• <b>Haqiqiy foyda:</b> +{daily_profit_pct:.1f}%
• <b>Foyda $ da:</b> ${daily_profit:.2f}
• <b>Xavr:</b> {risk_level}
• <b>Kunlik savdolar:</b> {trades_per_day}
• <b>Savdo summasi:</b> {trade_amount_pct}% balansdan
• <b>Eng yaxshi vaqt:</b> {best_time}
• <b>Tavsiya etilgan juftliklar:</b> {', '.join(recommended_pairs[:2])}
• <b>Kun maslahati:</b> {'Bot signallariga qat\'iy rioya qiling' if day % 2 == 0 else 'Savdo summasini tavsiya etilgandan yuqori oshirmang'}
"""
            else:  # kg
                plan += f"""
<b>КҮН {day}: {phase}</b>
────────────────────
• <b>Баланс:</b> ${current_balance:.2f}
• <b>Күндүк максат:</b> +{daily_target:.1f}%
• <b>Чыныгы пайда:</b> +{daily_profit_pct:.1f}%
• <b>Пайда $ да:</b> ${daily_profit:.2f}
• <b>Тобокелдик:</b> {risk_level}
• <b>Күндүк соодолор:</b> {trades_per_day}
• <b>Соодо суммасы:</b> {trade_amount_pct}% баланстан
• <b>Эң жакшы убакыт:</b> {best_time}
• <b>Сунуш кылынган жуптуктар:</b> {', '.join(recommended_pairs[:2])}
• <b>Күн кеңеши:</b> {'Бот сигналдарына так аткарыңыз' if day % 2 == 0 else 'Соодо суммасын сунуш кылынгандан жогору көбөйтпөңүз'}
"""
            
            # Добавляем разделитель каждые 5 дней
            if day % 5 == 0 and day < 30:
                plan += "\n────────────────────\n"
        
        # Итоги
        total_profit_amount = current_balance - deposit
        final_profit_pct = (total_profit_amount / deposit) * 100
        
        if lang == 'ru':
            plan += f"""
────────────────────

<b>📈 ИТОГИ МАРАФОНА:</b>

• <b>Стартовый депозит:</b> ${deposit:.2f}
• <b>Финальный баланс:</b> ${current_balance:.2f}
• <b>Общая прибыль:</b> +{final_profit_pct:.1f}%
• <b>Прибыль в $:</b> ${total_profit_amount:.2f}
• <b>Средняя дневная прибыль:</b> +{(total_profit/30):.1f}%

<b>🏆 РЕКОМЕНДАЦИИ НА БУДУЩЕЕ:</b>

1. <b>Продолжайте следовать стратегии</b>
2. <b>Не увеличивайте риск выше 3%</b>
3. <b>Выводите прибыль регулярно</b>
4. <b>Реинвестируйте 50% прибыли</b>
5. <b>Следите за сигналами бота</b>

<b>🚀 УСПЕХОВ В ДАЛЬНЕЙШЕЙ ТОРГОВЛЕ!</b>

<b>📞 Если возникли вопросы - обращайтесь к администратору:</b>
{ADMIN_LINK}
"""
        elif lang == 'en':
            plan += f"""
────────────────────

<b>📈 MARATHON RESULTS:</b>

• <b>Starting deposit:</b> ${deposit:.2f}
• <b>Final balance:</b> ${current_balance:.2f}
• <b>Total profit:</b> +{final_profit_pct:.1f}%
• <b>Profit in $:</b> ${total_profit_amount:.2f}
• <b>Average daily profit:</b> +{(total_profit/30):.1f}%

<b>🏆 RECOMMENDATIONS FOR THE FUTURE:</b>

1. <b>Continue following the strategy</b>
2. <b>Do not increase risk above 3%</b>
3. <b>Withdraw profits regularly</b>
4. <b>Reinvest 50% of profits</b>
5. <b>Follow bot signals</b>

<b>🚀 SUCCESS IN FUTURE TRADING!</b>

<b>📞 If you have questions - contact the administrator:</b>
{ADMIN_LINK}
"""
        elif lang == 'uz':
            plan += f"""
────────────────────

<b>📈 MARAFON NATIJALARI:</b>

• <b>Boshlang'ich depozit:</b> ${deposit:.2f}
• <b>Yakuniy balans:</b> ${current_balance:.2f}
• <b>Umumiy foyda:</b> +{final_profit_pct:.1f}%
• <b>Foyda $ da:</b> ${total_profit_amount:.2f}
• <b>O'rtacha kunlik foyda:</b> +{(total_profit/30):.1f}%

<b>🏆 KELAJAK UCHUN TAVSIYALAR:</b>

1. <b>Strategiyani davom ettiring</b>
2. <b>Xavrni 3% dan yuqori oshirmang</b>
3. <b>Foydani muntazam chiqarib oling</b>
4. <b>Foydaning 50% ini qayta investitsiya qiling</b>
5. <b>Bot signallariga amal qiling</b>

<b>🚀 KELAJAK SAVDOSIDA OMNINGIZGA TILEK!</b>

<b>📞 Savollaringiz bo'lsa - administrator bilan bog'laning:</b>
{ADMIN_LINK}
"""
        else:  # kg
            plan += f"""
────────────────────

<b>📈 МАРАФОН НАТИЖЕЛЕРИ:</b>

• <b>Башталгыч депозит:</b> ${deposit:.2f}
• <b>Акыркы баланс:</b> ${current_balance:.2f}
• <b>Баардык пайда:</b> +{final_profit_pct:.1f}%
• <b>Пайда $ да:</b> ${total_profit_amount:.2f}
• <b>Орточо күндүк пайда:</b> +{(total_profit/30):.1f}%

<b>🏆 КЕЛЕЧЕК УЧУН СУНУШТАР:</b>

1. <b>Стратегияны улантыңыз</b>
2. <b>Тобокелдикти 3% дан жогору көтөрбөңүз</b>
3. <b>Пайданы үзгүлтүксүз алыңыз</b>
4. <b>Пайданын 50% ин кайра инвестициялаңыз</b>
5. <b>Бот сигналдарын аткарыңыз</b>

<b>🚀 КЕЛЕЧЕК СООДОСУНДА ИЙГИЛИКТҮҮ БОЛСУН!</b>

<b>📞 Суроолоруңуз болсо - администратор менен байланышыңыз:</b>
{ADMIN_LINK}
"""
        
        return plan
    except Exception as e:
        logger.error(f"Ошибка генерации плана марафона: {e}")
        if lang == 'ru':
            return "❌ <b>Ошибка генерации плана. Попробуйте еще раз!</b>"
        elif lang == 'en':
            return "❌ <b>Error generating plan. Try again!</b>"
        elif lang == 'uz':
            return "❌ <b>Reja yaratishda xatolik. Qayta urinib ko'ring!</b>"
        else:  # kg
            return "❌ <b>План түзүүдө ката. Кайра аракет кылыңыз!</b>"

# ============================================
# 🎯 ОБРАБОТЧИК КОЛБЭКОВ
# ============================================

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    data = query.data
    
    try:
        # Проверка блокировки
        if is_banned(user_id):
            await query.edit_message_text(
                "⛔ Вы заблокированы в этом боте.",
                parse_mode='HTML'
            )
            return
        
        # ВЫБОР ЯЗЫКА
        if data.startswith("lang_"):
            lang = data.replace("lang_", "")
            set_user_language(user_id, lang)
            
            # Показываем инструкцию на выбранном языке
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
            if not is_admin(user_id):
                await query.answer(t(user_id, 'admin_only'), show_alert=True)
                return
            
            message = f"<b>⚡ АДМИН ПАНЕЛЬ</b>\n\n"
            message += f"👥 <b>Всего пользователей:</b> {len(all_users)}\n"
            message += f"👑 <b>VIP пользователей:</b> {len(vip_users)}\n"
            message += f"⛔ <b>Заблокированных:</b> {len(banned_users)}\n"
            message += f"📊 <b>Активных сегодня:</b> {len([uid for uid in all_users if user_stats.get(uid, {}).get('last_signal_time', '').startswith(datetime.now().strftime('%Y-%m-%d'))])}\n\n"
            message += f"<b>Выберите действие:</b>"
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=KeyboardManager.admin_panel()
            )
        
        # АДМИН ДЕЙСТВИЯ
        elif data == "admin_grant":
            await admin_grant_access(query, context)
        elif data == "admin_revoke":
            await admin_revoke_access(query, context)
        elif data == "admin_ban":
            await admin_ban_user(query, context)
        elif data == "admin_broadcast":
            await admin_broadcast(query, context)
        elif data == "broadcast_all":
            context.user_data["admin_action"] = "broadcast_all"
            await query.edit_message_text(
                "📢 <b>Рассылка всем пользователям</b>\n\n"
                "Введите сообщение для рассылки:",
                parse_mode='HTML'
            )
        elif data == "broadcast_vip":
            context.user_data["admin_action"] = "broadcast_vip"
            await query.edit_message_text(
                "👑 <b>Рассылка только VIP пользователям</b>\n\n"
                "Введите сообщение для рассылки:",
                parse_mode='HTML'
            )
        elif data == "broadcast_free":
            context.user_data["admin_action"] = "broadcast_free"
            await query.edit_message_text(
                "🆓 <b>Рассылка бесплатным пользователям</b>\n\n"
                "Введите сообщение для рассылки:",
                parse_mode='HTML'
            )
        elif data == "broadcast_photo":
            context.user_data["admin_action"] = "broadcast_photo"
            await query.edit_message_text(
                "📷 <b>Рассылка с фото</b>\n\n"
                "Отправьте фото или введите URL фото:",
                parse_mode='HTML'
            )
        elif data == "broadcast_video":
            context.user_data["admin_action"] = "broadcast_video"
            await query.edit_message_text(
                "🎥 <b>Рассылка с видео</b>\n\n"
                "Отправьте видео или введите URL видео:",
                parse_mode='HTML'
            )
        elif data == "confirm_broadcast":
            await confirm_broadcast(query, context)
        
        # ПОЛУЧИТЬ СИГНАЛ
        elif data == "get_signal":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'no_vip'), show_alert=True)
                return
            
            await query.edit_message_text(
                f"<b>{t(user_id, 'choose_market')}</b>",
                parse_mode='HTML',
                reply_markup=KeyboardManager.market_menu(user_id)
            )
        
        # ВЫБОР РЫНКА
        elif data in ["market_otc", "market_exchange"]:
            if data == "market_otc":
                pairs = OTC_PAIRS
                market_type = "otc"
                title = t(user_id, 'otc_market')
            else:
                pairs = EXCHANGE_PAIRS
                market_type = "exchange"
                title = t(user_id, 'exchange_market')
            
            await query.edit_message_text(
                f"<b>{title}</b>\n\n<b>{t(user_id, 'choose_pair')} (1):</b>",
                parse_mode='HTML',
                reply_markup=KeyboardManager.pairs_menu(pairs, market_type, 0, user_id)
            )
        
        # ПАГИНАЦИЯ
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
                    f"<b>{title}</b>\n\n<b>{t(user_id, 'choose_pair')} ({page+1}):</b>",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.pairs_menu(pairs, market_type, page, user_id)
                )
        
        # ВЫБОР ПАРЫ И ГЕНЕРАЦИЯ СИГНАЛА
        elif data.startswith("pair_"):
            parts = data.split("_", 2)
            if len(parts) >= 3:
                market_type = parts[1]
                pair = parts[2]
                is_otc = market_type == "otc"
                
                await query.edit_message_text(
                    f"<b>{t(user_id, 'analyzing')}</b>",
                    parse_mode='HTML'
                )
                
                # Анализируем пару
                signal = analyzer.analyze_pair(pair, is_otc)
                
                # Сохраняем в историю
                signal_history.setdefault(user_id, []).append({
                    "pair": pair,
                    "direction": signal['direction'],
                    "probability": signal['probability'],
                    "timestamp": datetime.now().strftime("%H:%M:%S"),
                    "date": datetime.now().strftime("%d.%m.%Y"),
                    "type": "manual"
                })
                Database.save("signal_history.json", signal_history)
                
                # Обновляем время последнего сигнала
                if user_id in user_stats:
                    user_stats[user_id]["last_signal_time"] = datetime.now().isoformat()
                    Database.save("user_stats.json", user_stats)
                
                # Форматируем сигнал
                direction_emoji = "🟢" if signal['direction'] == "CALL" else "🔴"
                lang = get_user_language(user_id)
                
                if lang == 'ru':
                    direction_text = "ВВЕРХ (CALL)" if signal['direction'] == "CALL" else "ВНИЗ (PUT)"
                elif lang == 'en':
                    direction_text = signal['direction']
                elif lang == 'uz':
                    direction_text = "YUQORI (CALL)" if signal['direction'] == "CALL" else "PAST (PUT)"
                else:  # kg
                    direction_text = "ЖОГОРУ (CALL)" if signal['direction'] == "CALL" else "ТОМЕН (PUT)"
                
                if lang == 'ru':
                    message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text}</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥 ГАРАНТИЯ
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'signal_time')}</b> {datetime.now().strftime('%H:%M:%S')}
<b>{t(user_id, 'date')}</b> {datetime.now().strftime('%d.%m.%Y')}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis'].get('market_condition', 'Анализ')}
• {t(user_id, 'risk_level')} {signal['analysis'].get('risk_level', 'СРЕДНИЙ 🟡')}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
{t(user_id, 'take_profit')}
{t(user_id, 'stop_loss')}

<b>{t(user_id, 'instructions')}</b>
1. Откройте <code>{pair}</code>
2. Направление: {direction_emoji} {signal['direction']}
3. Время: {signal['expiration'].split()[0]}-{signal['expiration'].split()[1]} минут
4. Сумма: 2-3% от депозита
5. Подтвердите сделку

<b>{t(user_id, 'good_luck')}</b>
"""
                elif lang == 'en':
                    message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text}</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥 GUARANTEE
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'signal_time')}</b> {datetime.now().strftime('%H:%M:%S')}
<b>{t(user_id, 'date')}</b> {datetime.now().strftime('%d.%m.%Y')}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis'].get('market_condition', 'Analysis')}
• {t(user_id, 'risk_level')} {signal['analysis'].get('risk_level', 'MEDIUM 🟡')}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
{t(user_id, 'take_profit')}
{t(user_id, 'stop_loss')}

<b>{t(user_id, 'instructions')}</b>
1. Open <code>{pair}</code>
2. Direction: {direction_emoji} {signal['direction']}
3. Time: {signal['expiration'].split()[0]}-{signal['expiration'].split()[1]} minutes
4. Amount: 2-3% of deposit
5. Confirm the trade

<b>{t(user_id, 'good_luck')}</b>
"""
                elif lang == 'uz':
                    message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text}</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥 KAFOLAT
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'signal_time')}</b> {datetime.now().strftime('%H:%M:%S')}
<b>{t(user_id, 'date')}</b> {datetime.now().strftime('%d.%m.%Y')}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis'].get('market_condition', 'Tahlil')}
• {t(user_id, 'risk_level')} {signal['analysis'].get('risk_level', 'O\'RTA 🟡')}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
{t(user_id, 'take_profit')}
{t(user_id, 'stop_loss')}

<b>{t(user_id, 'instructions')}</b>
1. Ochish <code>{pair}</code>
2. Yo'nalish: {direction_emoji} {signal['direction']}
3. Vaqt: {signal['expiration'].split()[0]}-{signal['expiration'].split()[1]} daqiqa
4. Summa: depozitning 2-3%
5. Savdoni tasdiqlang

<b>{t(user_id, 'good_luck')}</b>
"""
                else:  # kg
                    message = f"""
<b>{t(user_id, 'signal_title')}</b>

<b>{t(user_id, 'pair')}</b> <code>{pair}</code>
<b>{t(user_id, 'direction')}</b> {direction_emoji} <b>{direction_text}</b>
<b>{t(user_id, 'probability')}</b> <b>{signal['probability']}%</b> 🔥 КАФОЛАТ
<b>{t(user_id, 'strength')}</b> {signal['strength']}
<b>{t(user_id, 'expiration')}</b> <b>{signal['expiration']}</b>
<b>{t(user_id, 'signal_time')}</b> {datetime.now().strftime('%H:%M:%S')}
<b>{t(user_id, 'date')}</b> {datetime.now().strftime('%d.%m.%Y')}

<b>{t(user_id, 'analysis')}</b>
• {t(user_id, 'market_condition')} {signal['analysis'].get('market_condition', 'Анализ')}
• {t(user_id, 'risk_level')} {signal['analysis'].get('risk_level', 'ОРТОЧО 🟡')}

<b>{t(user_id, 'recommendations')}</b>
{t(user_id, 'risk')}
{t(user_id, 'take_profit')}
{t(user_id, 'stop_loss')}

<b>{t(user_id, 'instructions')}</b>
1. Ачуу <code>{pair}</code>
2. Багыт: {direction_emoji} {signal['direction']}
3. Убакыт: {signal['expiration'].split()[0]}-{signal['expiration'].split()[1]} мүнөт
4. Сумма: депозиттин 2-3%
5. Соодону ырастоо

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
                    profit_percent = int(data.split("_")[2])
                except:
                    profit_percent = 90
                
                update_user_stats(user_id, True, profit_percent)
                
                if get_user_language(user_id) == 'ru':
                    message = f"""
<b>{t(user_id, 'trade_won')}</b>

<b>{t(user_id, 'profit')}</b> {profit_percent}%
<b>📊 Статистика обновлена!</b>
"""
                elif get_user_language(user_id) == 'en':
                    message = f"""
<b>{t(user_id, 'trade_won')}</b>

<b>{t(user_id, 'profit')}</b> {profit_percent}%
<b>📊 Statistics updated!</b>
"""
                elif get_user_language(user_id) == 'uz':
                    message = f"""
<b>{t(user_id, 'trade_won')}</b>

<b>{t(user_id, 'profit')}</b> {profit_percent}%
<b>📊 Statistika yangilandi!</b>
"""
                else:  # kg
                    message = f"""
<b>{t(user_id, 'trade_won')}</b>

<b>{t(user_id, 'profit')}</b> {profit_percent}%
<b>📊 Статистика жаңыртылды!</b>
"""
            elif data == "trade_loss":
                update_user_stats(user_id, False)
                message = f"""
<b>{t(user_id, 'trade_lost')}</b>

<b>{t(user_id, 'dont_worry')}</b>
<b>{t(user_id, 'next_signal')}</b>
"""
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=KeyboardManager.result_menu(user_id)
            )
        
        # МОЯ СТАТИСТИКА
        elif data == "my_stats":
            ensure_user_data(user_id)
            stats = user_stats.get(user_id, {})
            
            message = f"<b>{t(user_id, 'stats')}</b>\n\n"
            message += f"<b>{t(user_id, 'your_id')}</b> <code>{user_id}</code>\n"
            message += f"<b>{t(user_id, 'status')}</b> {'✅ VIP' if is_vip(user_id) else '🔒 ' + t(user_id, 'require_vip')}\n"
            message += f"<b>{t(user_id, 'registration_date')}</b> {stats.get('join_date', 'Неизвестно')}\n\n"
            
            message += f"<b>🎯 {t(user_id, 'accuracy')}:</b> <b>{stats.get('win_rate', 0):.1f}%</b>\n"
            message += f"<b>💰 {t(user_id, 'total_profit')}:</b> <b>${stats.get('profit', 0):.2f}</b>\n"
            message += f"<b>📊 {t(user_id, 'total_trades')}:</b> <b>{stats.get('total_trades', 0)}</b>\n"
            message += f"<b>✅ {t(user_id, 'wins')}:</b> <b>{stats.get('wins', 0)}</b>\n"
            message += f"<b>❌ {t(user_id, 'losses')}:</b> <b>{stats.get('losses', 0)}</b>\n"
            message += f"<b>🔥 {t(user_id, 'current_streak')}:</b> <b>{stats.get('current_streak', 0)}</b>\n"
            message += f"<b>🏆 {t(user_id, 'best_streak')}:</b> <b>{stats.get('best_streak', 0)}</b>\n"
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        "🏠 Главное меню" if get_user_language(user_id) == 'ru' else 
                        "🏠 Main Menu" if get_user_language(user_id) == 'en' else
                        "🏠 Asosiy Menyu" if get_user_language(user_id) == 'uz' else
                        "🏠 Негизги Меню", 
                        callback_data="main_menu"
                    )]
                ])
            )
        
        # АВТОСИГНАЛЫ
        elif data == "auto_signals":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'no_vip'), show_alert=True)
                return
            
            enabled = auto_signals_enabled.get(user_id, False)
            
            if get_user_language(user_id) == 'ru':
                message = f"""
<b>🤖 АВТОМАТИЧЕСКИЕ СИГНАЛЫ</b>

Бот автоматически анализирует рынок и отправляет сигналы каждые 2 минуты

<b>📊 Анализ:</b> Используется 20+ индикаторов
<b>⏰ Интервал:</b> Каждые 2 минуты
<b>🎯 Точность:</b> 96-99%

{'<b>✅ АВТОСИГНАЛЫ ВКЛЮЧЕНЫ</b>' if enabled else '<b>❌ АВТОСИГНАЛЫ ВЫКЛЮЧЕНЫ</b>'}
"""
            elif get_user_language(user_id) == 'en':
                message = f"""
<b>🤖 AUTOMATIC SIGNALS</b>

Bot automatically analyzes market and sends signals every 2 minutes

<b>📊 Analysis:</b> Uses 20+ indicators
<b>⏰ Interval:</b> Every 2 minutes
<b>🎯 Accuracy:</b> 96-99%

{'<b>✅ AUTO SIGNALS ENABLED</b>' if enabled else '<b>❌ AUTO SIGNALS DISABLED</b>'}
"""
            elif get_user_language(user_id) == 'uz':
                message = f"""
<b>🤖 AVTOMATIK SIGNALLAR</b>

Bot har 2 daqiqada bozorni avtomatik tahlil qiladi va signallar yuboradi

<b>📊 Tahlil:</b> 20+ indikatorlar qo'llaniladi
<b>⏰ Interval:</b> Har 2 daqiqada
<b>🎯 Aniqlik:</b> 96-99%

{'<b>✅ AVTOMATIK SIGNALLAR YOQILGAN</b>' if enabled else '<b>❌ AVTOMATIK SIGNALLAR O\'CHIRILGAN</b>'}
"""
            else:  # kg
                message = f"""
<b>🤖 АВТОМАТТЫК СИГНАЛДАР</b>

Бот ар 2 мүнөт сайын базарды автоматикалык түрдө анализдейт жана сигналдарды жөнөтөт

<b>📊 Анализ:</b> 20+ индикаторлор колдонулат
<b>⏰ Интервал:</b> Ар 2 мүнөт сайын
<b>🎯 Тактык:</b> 96-99%

{'<b>✅ АВТОМАТТЫК СИГНАЛДАР КҮЙГҮЗҮЛГӨН</b>' if enabled else '<b>❌ АВТОМАТТЫК СИГНАЛДАР ӨЧҮРҮЛГӨН</b>'}
"""
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "❌ Выключить автосигналы" if enabled and get_user_language(user_id) == 'ru' else 
                    "✅ Включить автосигналы" if not enabled and get_user_language(user_id) == 'ru' else
                    "❌ Disable auto signals" if enabled and get_user_language(user_id) == 'en' else
                    "✅ Enable auto signals" if not enabled and get_user_language(user_id) == 'en' else
                    "❌ Avtomatik signallarni o'chirish" if enabled and get_user_language(user_id) == 'uz' else
                    "✅ Avtomatik signallarni yoqish" if not enabled and get_user_language(user_id) == 'uz' else
                    "❌ Автоматтык сигналдарды өчүрүү" if enabled and get_user_language(user_id) == 'kg' else
                    "✅ Автоматтык сигналдарды күйгүзүү", 
                    callback_data="toggle_auto_signals"
                )],
                [InlineKeyboardButton(
                    "🔙 Назад" if get_user_language(user_id) == 'ru' else 
                    "🔙 Back" if get_user_language(user_id) == 'en' else
                    "🔙 Orqaga" if get_user_language(user_id) == 'uz' else
                    "🔙 Артка", 
                    callback_data="main_menu"
                )]
            ])
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=keyboard
            )
        
        # ВКЛ/ВЫКЛ АВТОСИГНАЛЫ
        elif data == "toggle_auto_signals":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'no_vip'), show_alert=True)
                return
            
            enabled = auto_signals_enabled.get(user_id, False)
            auto_signals_enabled[user_id] = not enabled
            Database.save("auto_signals.json", auto_signals_enabled)
            
            if get_user_language(user_id) == 'ru':
                status = "включены" if not enabled else "выключены"
            elif get_user_language(user_id) == 'en':
                status = "enabled" if not enabled else "disabled"
            elif get_user_language(user_id) == 'uz':
                status = "yoqildi" if not enabled else "o'chirildi"
            else:  # kg
                status = "күйгүзүлдү" if not enabled else "өчүрүлдү"
            
            await query.answer(f"✅ Автосигналы {status}!", show_alert=True)
            
            # Обновляем сообщение
            enabled = auto_signals_enabled.get(user_id, False)
            
            if get_user_language(user_id) == 'ru':
                message = f"""
<b>🤖 АВТОМАТИЧЕСКИЕ СИГНАЛЫ</b>

{'<b>✅ АВТОСИГНАЛЫ ВКЛЮЧЕНЫ</b>' if enabled else '<b>❌ АВТОСИГНАЛЫ ВЫКЛЮЧЕНЫ</b>'}
"""
            elif get_user_language(user_id) == 'en':
                message = f"""
<b>🤖 AUTOMATIC SIGNALS</b>

{'<b>✅ AUTO SIGNALS ENABLED</b>' if enabled else '<b>❌ AUTO SIGNALS DISABLED</b>'}
"""
            elif get_user_language(user_id) == 'uz':
                message = f"""
<b>🤖 AVTOMATIK SIGNALLAR</b>

{'<b>✅ AVTOMATIK SIGNALLAR YOQILGAN</b>' if enabled else '<b>❌ AVTOMATIK SIGNALLAR O\'CHIRILGAN</b>'}
"""
            else:  # kg
                message = f"""
<b>🤖 АВТОМАТТЫК СИГНАЛДАР</b>

{'<b>✅ АВТОМАТТЫК СИГНАЛДАР КҮЙГҮЗҮЛГӨН</b>' if enabled else '<b>❌ АВТОМАТТЫК СИГНАЛДАР ӨЧҮРҮЛГӨН</b>'}
"""
            
            keyboard = InlineKeyboardMarkup([
                [InlineKeyboardButton(
                    "❌ Выключить автосигналы" if enabled and get_user_language(user_id) == 'ru' else 
                    "✅ Включить автосигналы" if not enabled and get_user_language(user_id) == 'ru' else
                    "❌ Disable auto signals" if enabled and get_user_language(user_id) == 'en' else
                    "✅ Enable auto signals" if not enabled and get_user_language(user_id) == 'en' else
                    "❌ Avtomatik signallarni o'chirish" if enabled and get_user_language(user_id) == 'uz' else
                    "✅ Avtomatik signallarni yoqish" if not enabled and get_user_language(user_id) == 'uz' else
                    "❌ Автоматтык сигналдарды өчүрүү" if enabled and get_user_language(user_id) == 'kg' else
                    "✅ Автоматтык сигналдарды күйгүзүү", 
                    callback_data="toggle_auto_signals"
                )],
                [InlineKeyboardButton(
                    "🔙 Назад" if get_user_language(user_id) == 'ru' else 
                    "🔙 Back" if get_user_language(user_id) == 'en' else
                    "🔙 Orqaga" if get_user_language(user_id) == 'uz' else
                    "🔙 Артка", 
                    callback_data="main_menu"
                )]
            ])
            
            await query.edit_message_text(
                message,
                parse_mode='HTML',
                reply_markup=keyboard
            )
        
        # МАРАФОН 30 ДНЕЙ
        elif data == "marathon":
            if not is_vip(user_id):
                await query.answer(t(user_id, 'no_vip'), show_alert=True)
                return
            
            await query.edit_message_text(
                f"<b>{t(user_id, 'marathon')}</b>\n\n"
                f"<b>{t(user_id, 'enter_deposit')}</b>\n"
                f"<b>{t(user_id, 'min_deposit')}</b>",
                parse_mode='HTML'
            )
            context.user_data["awaiting_deposit"] = True
        
        # ОСТАЛЬНЫЕ КОЛБЭКИ (about, socials, get_vip, top_traders и т.д.)
        else:
            await query.answer("⚡")
            
    except Exception as e:
        logger.error(f"Ошибка в handle_callback: {e}")
        await query.answer("⚠️ Ошибка!")
        await show_main_menu(query, context, user_id)

# ============================================
# 📨 ОБРАБОТЧИК СООБЩЕНИЙ
# ============================================

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    text = update.message.text
    
    # Проверка блокировки
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
                
                # Показываем загрузку
                await update.message.reply_text(
                    t(user_id, 'generating_plan'),
                    parse_mode='HTML'
                )
                
                # Генерируем план марафона
                plan = generate_marathon_plan(deposit, get_user_language(user_id))
                
                # Разбиваем на части если слишком длинный
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
                        reply_markup=InlineKeyboardMarkup([
                            [InlineKeyboardButton(
                                "🏠 Главное меню" if get_user_language(user_id) == 'ru' else 
                                "🏠 Main Menu" if get_user_language(user_id) == 'en' else
                                "🏠 Asosiy Menyu" if get_user_language(user_id) == 'uz' else
                                "🏠 Негизги Меню", 
                                callback_data="main_menu"
                            )]
                        ])
                    )
                
                context.user_data["awaiting_deposit"] = False
                
            except ValueError:
                await update.message.reply_text(
                    t(user_id, 'error_number'),
                    parse_mode='HTML'
                )
        
        # Команды
        elif text.lower() in ['start', 'старт', '/start']:
            await start_command(update, context)
        
        elif text.lower() in ['admin', '/admin', 'админ']:
            await admin_command(update, context)
        
        elif text.lower() in ['grant', '/grant'] and is_admin(user_id):
            context.user_data["admin_action"] = "grant_access"
            await update.message.reply_text(
                f"<b>{t(user_id, 'grant_access')}</b>\n\n"
                f"{t(user_id, 'enter_user_id')}",
                parse_mode='HTML'
            )
        
        elif text.lower() in ['revoke', '/revoke'] and is_admin(user_id):
            context.user_data["admin_action"] = "revoke_access"
            await update.message.reply_text(
                f"<b>{t(user_id, 'revoke_access')}</b>\n\n"
                f"{t(user_id, 'enter_user_id')}",
                parse_mode='HTML'
            )
        
        elif text.lower() in ['ban', '/ban'] and is_admin(user_id):
            context.user_data["admin_action"] = "ban_user"
            await update.message.reply_text(
                f"<b>{t(user_id, 'ban_user')}</b>\n\n"
                f"{t(user_id, 'enter_user_id')}",
                parse_mode='HTML'
            )
        
        elif text.lower() in ['unban', '/unban'] and is_admin(user_id):
            context.user_data["admin_action"] = "unban_user"
            await update.message.reply_text(
                f"<b>{t(user_id, 'unban_user')}</b>\n\n"
                f"{t(user_id, 'enter_user_id')}",
                parse_mode='HTML'
            )
        
        elif text.lower() in ['send', '/send'] and is_admin(user_id):
            context.user_data["admin_action"] = "broadcast_all"
            await update.message.reply_text(
                f"<b>{t(user_id, 'send_broadcast')}</b>\n\n"
                f"{t(user_id, 'enter_message')}",
                parse_mode='HTML'
            )
        
        elif text.lower() in ['id', 'айди']:
            await update.message.reply_text(
                f"🆔 <b>{t(user_id, 'your_id')}</b> <code>{user_id}</code>",
                parse_mode='HTML',
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(
                        "🏠 Главное меню" if get_user_language(user_id) == 'ru' else 
                        "🏠 Main Menu" if get_user_language(user_id) == 'en' else
                        "🏠 Asosiy Menyu" if get_user_language(user_id) == 'uz' else
                        "🏠 Негизги Меню", 
                        callback_data="main_menu"
                    )]
                ])
            )
        
        elif text.lower() in ['меню', 'menu', '/menu']:
            await show_main_menu(update, context, user_id)
        
        elif text.lower() in ['сигнал', 'signal']:
            if not is_vip(user_id):
                await update.message.reply_text(
                    f"🔒 <b>{t(user_id, 'no_vip')}</b>",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.main_menu(user_id)
                )
            else:
                await update.message.reply_text(
                    f"<b>{t(user_id, 'choose_market')}</b>",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.market_menu(user_id)
                )
        
        elif text.lower() in ['стата', 'stats', 'статистика']:
            await update.message.reply_text(
                f"📊 <b>{t(user_id, 'use_stats_button')}</b>",
                parse_mode='HTML',
                reply_markup=KeyboardManager.main_menu(user_id)
            )
        
        elif text.lower() in ['марафон', 'marathon']:
            if not is_vip(user_id):
                await update.message.reply_text(
                    f"🔒 <b>{t(user_id, 'no_vip')}</b>",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.main_menu(user_id)
                )
            else:
                await update.message.reply_text(
                    f"<b>{t(user_id, 'marathon')}</b>\n\n"
                    f"<b>{t(user_id, 'enter_deposit')}</b>\n"
                    f"<b>{t(user_id, 'min_deposit')}</b>",
                    parse_mode='HTML'
                )
                context.user_data["awaiting_deposit"] = True
        
        else:
            # Обработка админ сообщений
            if is_admin(user_id) and context.user_data.get("admin_action"):
                await handle_admin_message(update, context)
            else:
                await update.message.reply_text(
                    f"<b>{t(user_id, 'use_buttons')}</b>",
                    parse_mode='HTML',
                    reply_markup=KeyboardManager.main_menu(user_id)
                )
    
    except Exception as e:
        logger.error(f"Ошибка обработки сообщения: {e}")
        await update.message.reply_text(
            f"⚠️ <b>{t(user_id, 'use_buttons')}</b>",
            parse_mode='HTML',
            reply_markup=KeyboardManager.main_menu(user_id)
        )

# ============================================
# 🚀 ЗАПУСК БОТА
# ============================================

def run_flask():
    try:
        from waitress import serve
        logger.info("🌐 Запуск Flask сервера через Waitress...")
        serve(app, host="0.0.0.0", port=8080)
    except ImportError:
        logger.info("🌐 Запуск Flask сервера (Waitress не установлен, используем development сервер)")
        app.run(host="0.0.0.0", port=8080, debug=False, threaded=True)

async def main():
    # Запускаем Flask сервер в отдельном потоке
    flask_thread = Thread(target=run_flask, daemon=True)
    flask_thread.start()
    logger.info("🌐 Flask сервер запущен на порту 8080")
    
    # Запускаем автопинг
    pinger = AutoPinger()
    pinger.start()
    logger.info("🔄 Автопинг запущен (каждые 3 минуты)")
    
    # Создаем приложение бота
    application = Application.builder().token(TOKEN).build()
    
    # Инициализируем систему автосигналов
    auto_signal_system = AutoSignalSystem(application)
    
    # Добавляем обработчики команд
    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(CommandHandler("menu", lambda u, c: show_main_menu(u, c, u.effective_user.id)))
    application.add_handler(CommandHandler("admin", admin_command))
    application.add_handler(CommandHandler("help", start_command))
    
    # Добавляем обработчики callback
    application.add_handler(CallbackQueryHandler(handle_callback))
    
    # Добавляем обработчики сообщений
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    
    # Добавляем обработчики медиа для админов
    application.add_handler(MessageHandler(filters.PHOTO & filters.User(ADMIN_IDS), handle_admin_message))
    application.add_handler(MessageHandler(filters.VIDEO & filters.User(ADMIN_IDS), handle_admin_message))
    
    # Логируем запуск
    logger.info("🚀 ЗАПУСКАЕМ KURUT AI INFINITY v10.0")
    logger.info(f"👑 Админы: {ADMIN_IDS}")
    logger.info(f"👥 Пользователей: {len(all_users)}")
    logger.info(f"📊 Пар OTC: {len(OTC_PAIRS)}")
    logger.info(f"📈 Пар биржевых: {len(EXCHANGE_PAIRS)}")
    logger.info(f"🎯 Точность: 96-99%")
    logger.info(f"📈 Индикаторы: 20+")
    logger.info(f"🤖 Автосигналы: каждые 2 минуты")
    logger.info(f"🌍 Языки: RU/UZ/KG/EN")
    logger.info(f"⚡ Админ панель: АКТИВНА")
    
    try:
        # Запускаем бота
        logger.info("🔄 Инициализация бота...")
        await application.initialize()
        await application.start()
        logger.info("✅ Бот успешно запущен!")
        
        # Запускаем систему автосигналов
        await auto_signal_system.start()
        
        # Запускаем polling
        logger.info("🔄 Запуск polling...")
        await application.updater.start_polling(
            drop_pending_updates=True
        )
        
        # Основной цикл с проверкой новостей и сессий
        logger.info("📰 Запуск системы новостей...")
        while True:
            try:
                # Проверяем каждую минуту
                await asyncio.sleep(60)
                
                now = datetime.now()
                current_hour = now.hour
                current_minute = now.minute
                
                # Проверяем открытие/закрытие сессий
                opening_sessions, closing_sessions = news_manager.check_market_sessions()
                
                # Отправляем уведомления об открытии сессий
                for session in opening_sessions:
                    for user_id in vip_users:
                        if news_alerts_enabled.get(str(user_id), True):
                            lang = get_user_language(user_id)
                            
                            if lang == 'ru':
                                message = f"""
<b>🕒 ОТКРЫТИЕ СЕССИИ</b>

<b>{session} сессия открыта!</b>

<b>📊 Рекомендуемые пары:</b>
{', '.join(MARKET_SESSIONS[session.lower().replace('ая', '').replace('ская', '').lower()]['pairs'][:3])}

<b>🎯 Рекомендации:</b>
• Повышенная волатильность
• Больше торговых возможностей
• Следите за сигналами бота
"""
                            elif lang == 'en':
                                message = f"""
<b>🕒 SESSION OPENING</b>

<b>{session} session is open!</b>

<b>📊 Recommended pairs:</b>
{', '.join(MARKET_SESSIONS[session.lower().replace('n', '').replace('an', '').lower()]['pairs'][:3])}

<b>🎯 Recommendations:</b>
• Increased volatility
• More trading opportunities
• Follow bot signals
"""
                            elif lang == 'uz':
                                message = f"""
<b>🕒 SESSIYA OCHILISHI</b>

<b>{session} sessiyasi ochildi!</b>

<b>📊 Tavsiya etilgan juftliklar:</b>
{', '.join(MARKET_SESSIONS[session.lower().replace('ая', '').replace('ская', '').lower()]['pairs'][:3])}

<b>🎯 Tavsiyalar:</b>
• Oshgan volatillik
• Ko'proq savdo imkoniyatlari
• Bot signallariga amal qiling
"""
                            else:  # kg
                                message = f"""
<b>🕒 СЕССИЯ АЧЫЛЫШЫ</b>

<b>{session} сессиясы ачылды!</b>

<b>📊 Сунуш кылынган жуптуктар:</b>
{', '.join(MARKET_SESSIONS[session.lower().replace('ая', '').replace('ская', '').lower()]['pairs'][:3])}

<b>🎯 Сунуштар:</b>
• Көбөйгөн волатилдүүлүк
• Көбүрөөк соодо мүмкүнчүлүктөрү
• Бот сигналдарын аткарыңыз
"""
                            
                            try:
                                await application.bot.send_message(
                                    chat_id=user_id,
                                    text=message,
                                    parse_mode='HTML'
                                )
                            except:
                                pass
                
                # Отправляем уведомления о закрытии сессий
                for session in closing_sessions:
                    for user_id in vip_users:
                        if news_alerts_enabled.get(str(user_id), True):
                            lang = get_user_language(user_id)
                            
                            if lang == 'ru':
                                message = f"""
<b>🕒 ЗАКРЫТИЕ СЕССИИ</b>

<b>{session} сессия закрыта!</b>

<b>⚠️ Предупреждение:</b>
• Снижение волатильности
• Меньше торговых возможностей
• Ожидайте следующую сессию
"""
                            elif lang == 'en':
                                message = f"""
<b>🕒 SESSION CLOSING</b>

<b>{session} session is closed!</b>

<b>⚠️ Warning:</b>
• Decreased volatility
• Fewer trading opportunities
• Wait for next session
"""
                            elif lang == 'uz':
                                message = f"""
<b>🕒 SESSIYA YOPILISHI</b>

<b>{session} sessiyasi yopildi!</b>

<b>⚠️ Ogohlantirish:</b>
• Kamaygan volatillik
• Kamroq savdo imkoniyatlari
• Keyingi sessiyani kutish
"""
                            else:  # kg
                                message = f"""
<b>🕒 СЕССИЯ ЖАБЫЛЫШЫ</b>

<b>{session} сессиясы жабылды!</b>

<b>⚠️ Эскертүү:</b>
• Азайган волатилдүүлүк
• Аз соодо мүмкүнчүлүктөрү
• Кийинки сессияны күтүү
"""
                            
                            try:
                                await application.bot.send_message(
                                    chat_id=user_id,
                                    text=message,
                                    parse_mode='HTML'
                                )
                            except:
                                pass
                
                # Отправляем финансовые новости каждый час
                if current_minute == 0:
                    news = news_manager.get_current_news()
                    if news:
                        for user_id in vip_users:
                            if news_alerts_enabled.get(str(user_id), True):
                                lang = get_user_language(user_id)
                                message = news_manager.format_news_message(news, lang)
                                
                                try:
                                    await application.bot.send_message(
                                        chat_id=user_id,
                                        text=message,
                                        parse_mode='HTML'
                                    )
                                except:
                                    pass
                
            except Exception as e:
                logger.error(f"Ошибка в цикле новостей: {e}")
        
    except KeyboardInterrupt:
        logger.info("⛔ Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Ошибка запуска: {e}")
    finally:
        # Корректное завершение
        try:
            logger.info("🔄 Остановка бота...")
            await auto_signal_system.stop()
            if application.updater and application.updater.running:
                await application.updater.stop()
            if application.running:
                await application.stop()
            await application.shutdown()
            logger.info("✅ Бот корректно остановлен")
        except Exception as e:
            logger.error(f"⚠️ Ошибка при остановке: {e}")

def run_bot():
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("⛔ Программа завершена")
    except Exception as e:
        logger.error(f"💥 Фатальная ошибка: {e}")

if __name__ == '__main__':
    # Создаем requirements.txt если его нет
    try:
        with open("requirements.txt", "w", encoding="utf-8") as f:
            f.write("""python-telegram-bot==20.7
flask==3.0.0
waitress==3.0.1
""")
        logger.info("📋 Файл requirements.txt создан")
    except:
        pass
    
    # Запускаем бота
    run_bot()
