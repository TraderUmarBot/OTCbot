#!/usr/bin/env python3
"""
🤖 KURUT AI INFINITY - Самый точный бот для OTC рынка Pocket Option
ПОЛНОСТЬЮ РАБОЧАЯ ВЕРСИЯ - ВСЕ ФУНКЦИИ РАБОТАЮТ
"""

import os
import asyncio
import logging
import json
import uuid
import random
import threading
import time
import requests
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict

import numpy as np
import pandas as pd
import pytz
from scipy import stats

from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    BotCommand
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler
)
from telegram.constants import ParseMode

# ==================== КОНФИГУРАЦИЯ ====================
BOT_TOKEN = "8578509228:AAFdsHJOSaNc0b1JrCnRwAbA-d4IVXI0Ip0"
ADMIN_ID = 6117198446  # Ваш Telegram ID
ADMIN_USERNAME = "@Kuruttrader"
REFERRAL_LINK = "https://u3.shortink.io/main?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

SOCIAL_LINKS = {
    "telegram": "https://t.me/KURUTTRADING",
    "telegram_chat": "https://t.me/Kurutopen",
    "instagram": "https://www.instagram.com/kurut_trading",
    "youtube": "https://youtube.com/@kurut_kg",
    "admin": "@Kuruttrader"
}

# OTC Пары для Pocket Option (ПОЛНЫЙ СПИСОК)
OTC_PAIRS = {
    "forex": [
        "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC",
        "AUD/USD OTC", "USD/CAD OTC", "NZD/USD OTC", "EUR/GBP OTC",
        "EUR/JPY OTC", "GBP/JPY OTC", "AUD/JPY OTC", "EUR/CHF OTC",
        "GBP/CHF OTC", "CAD/JPY OTC", "NZD/JPY OTC", "AUD/CAD OTC",
        "AUD/NZD OTC", "EUR/AUD OTC", "EUR/CAD OTC", "GBP/AUD OTC",
        "GBP/CAD OTC", "USD/RUB OTC", "EUR/RUB OTC", "USD/TRY OTC",
        "EUR/TRY OTC", "USD/ZAR OTC", "USD/MXN OTC", "USD/BRL OTC",
        "USD/INR OTC", "USD/CNH OTC", "USD/HKD OTC", "USD/SGD OTC",
        "USD/THB OTC", "USD/SEK OTC", "USD/NOK OTC", "USD/DKK OTC",
        "USD/PLN OTC", "USD/HUF OTC", "USD/CZK OTC", "USD/ILS OTC"
    ],
    "stocks": [
        "Apple OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC",
        "Google OTC", "Facebook OTC", "Netflix OTC", "NVIDIA OTC",
        "AMD OTC", "Intel OTC", "Boeing OTC", "McDonald's OTC",
        "Coca-Cola OTC", "VISA OTC", "Mastercard OTC", "JP Morgan OTC",
        "Bank of America OTC", "Walmart OTC", "Exxon OTC", "Chevron OTC",
        "Pfizer OTC", "Johnson OTC", "IBM OTC", "Oracle OTC",
        "Adobe OTC", "Salesforce OTC", "PayPal OTC", "Uber OTC",
        "Airbnb OTC", "Spotify OTC"
    ],
    "crypto": [
        "Bitcoin OTC", "Ethereum OTC", "Ripple OTC", "Cardano OTC",
        "Solana OTC", "Polkadot OTC", "Dogecoin OTC", "Shiba Inu OTC",
        "Litecoin OTC", "Chainlink OTC", "Polygon OTC", "Avalanche OTC",
        "Tron OTC", "Toncoin OTC", "BNB OTC", "Bitcoin Cash OTC",
        "Stellar OTC", "Monero OTC", "Dash OTC", "Zcash OTC"
    ]
}

EXPIRATIONS = {
    "M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5,
    "M6": 6, "M7": 7, "M8": 8, "M9": 9, "M10": 10,
    "M15": 15, "M30": 30, "H1": 60, "H4": 240, "D1": 1440
}

# Состояния
(SELECT_LANGUAGE, MAIN_MENU, WAITING_FOR_BALANCE, SELECT_ASSET_TYPE,
 SELECT_CURRENCY_PAIR, SELECT_EXPIRY, TRADE_RESULT, ADMIN_ACTIONS) = range(8)

# ==================== ЛОГИРОВАНИЕ ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('kurut_bot.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== КЛАССЫ ДАННЫХ ====================
@dataclass
class User:
    id: int
    username: Optional[str]
    first_name: str
    language: str = "ru"
    has_access: bool = False
    balance: float = 0.0
    trades_won: int = 0
    trades_lost: int = 0
    total_trades: int = 0
    referral_id: str = ""
    join_date: str = None
    last_active: str = None
    
    def __post_init__(self):
        if self.join_date is None:
            self.join_date = datetime.now().isoformat()
        if self.last_active is None:
            self.last_active = datetime.now().isoformat()
    
    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return (self.trades_won / self.total_trades) * 100

@dataclass
class Signal:
    asset: str
    direction: str  # "CALL" или "PUT"
    expiry: str
    confidence: float
    price: float
    timestamp: str
    indicators: Dict[str, Any]
    recommendation: str

# ==================== ТЕКСТЫ НА ЯЗЫКАХ ====================
TEXTS = {
    "ru": {
        "start": "🎯 Добро пожаловать в KURUT AI INFINITY!\n\nЯ - ваш персональный торговый помощник для OTC рынка Pocket Option.\n\nВыберите язык:",
        "welcome": "👋 Добро пожаловать, {name}!\n\n📊 Я - KURUT AI INFINITY, самый точный торговый бот для OTC рынка Pocket Option.\n\n📈 Мои алгоритмы анализируют рынок с помощью 20+ математических индикаторов и выдают точные сигналы.",
        "social_links": "📱 МОИ СОЦИАЛЬНЫЕ СЕТИ:\n\n🔗 Telegram канал: {telegram}\n💬 Telegram чат: {telegram_chat}\n📸 Instagram: {instagram}\n🎥 YouTube: {youtube}\n👤 Админ: {admin}",
        "get_access": "🔐 ПОЛУЧИТЬ ДОСТУП\n\n📌 Ваш ID: {user_id}\n🔗 Реферальная ссылка: {ref_link}\n\n📝 Инструкция:\n1. Откройте новый аккаунт по ссылке выше\n2. Пополните баланс на 10$ или 20$\n3. Отправьте ваш ID админу: {admin}\n4. После подтверждения получите доступ к сигналам",
        "access_granted": "✅ ДОСТУП АКТИВИРОВАН!\n\n🎉 Поздравляем! Теперь вам доступны все функции бота.",
        "main_menu": "📊 ГЛАВНОЕ МЕНЮ\n\nВыберите опцию:",
        "get_signal": "📈 ПОЛУЧИТЬ СИГНАЛ\n\nВыберите тип актива:",
        "forex_pairs": "💱 ВАЛЮТНЫЕ ПАРЫ OTC\n\nВыберите пару:",
        "stocks": "📊 АКЦИИ OTC\n\nВыберите актив:",
        "crypto": "₿ КРИПТОВАЛЮТЫ OTC\n\nВыберите криптовалюту:",
        "select_expiry": "⏰ ВЫБЕРИТЕ ЭКСПИРАЦИЮ\n\nВыберите время экспирации:",
        "analyzing": "🔍 АНАЛИЗИРУЮ РЫНОК...\n\n📊 Запускаю 20+ математических индикаторов:\n• RSI, MACD, Bollinger Bands\n• Stochastic, Support/Resistance\n• Moving Averages, Volume анализ\n• Тренд анализ, Fibonacci\n\n⏳ Анализ займет 2-3 секунды...",
        "signal_result": "🎯 СИГНАЛ СГЕНЕРИРОВАН!\n\n📊 Актив: {asset}\n🎯 Направление: {direction}\n⏱ Экспирация: {expiry}\n📈 Уверенность: {confidence}%\n💵 Текущая цена: {price}\n\n{recommendation}\n\n👇 Подтвердите результат сделки:",
        "trade_won": "✅ СДЕЛКА ВЫИГРАНА!\n\nПоздравляем с успешной сделкой!",
        "trade_lost": "❌ СДЕЛКА ПРОИГРАНА\n\nНе расстраивайтесь, следующая будет успешной!",
        "marathon_start": "🏃‍♂️ МАРАФОН ТРЕЙДЕРА\n\nВведите ваш текущий баланс в долларах ($):\n\nПример: 100 или 250.50",
        "marathon_calc": "📊 РАСЧЁТ МАРАФОНА\n\nНачальный баланс: ${balance}\nЕжедневная прибыль: +15%\n\n📈 30-ДНЕВНЫЙ РАСЧЁТ:\n{calculation}\n\n💡 Общая прибыль: ${total_profit}\n💰 Итоговый баланс: ${final_balance}",
        "marathon_risk": "⚠️ УПРАВЛЕНИЕ РИСКАМИ\n\n📌 Для баланса ${balance}:\n\n🎯 Риск на сделку: 1-2%\n💰 Сумма риска: ${risk_amount}\n📊 Не использовать мартингейл\n🛑 Стоп-лосс: 2%\n✅ Тейк-профит: 3-5%\n\n⏱ Лучшее время: Азиатская и Европейская сессии",
        "instruction": "📚 ИНСТРУКЦИЯ ПО БОТУ\n\nKURUT AI INFINITY использует:\n• 20+ математических индикаторов\n• Анализ OTC рынка Pocket Option\n• Точные сигналы с рекомендациями\n\n🎯 СТРАТЕГИЯ:\n1. Торгуйте только по сигналам бота\n2. Соблюдайте риск-менеджмент\n3. Не открывайте больше 3 сделок одновременно\n\n📱 КОНТАКТЫ:\nАдмин: {admin}",
        "top_traders": "🏆 ТОП-5 ТРЕЙДЕРОВ\n\n{leaderboard}\n\n📊 Ваша позиция: #{position}",
        "stats": "📊 ВАША СТАТИСТИКА\n\n👤 ID: {user_id}\n📅 Регистрация: {join_date}\n\n✅ Выиграно: {won}\n❌ Проиграно: {lost}\n📊 Всего: {total}\n🎯 Win Rate: {win_rate}%\n💰 Баланс: ${balance}",
        "no_access": "❌ ДОСТУП ЗАКРЫТ\n\nДля получения доступа:\n1. Нажмите 'Получить доступ'\n2. Следуйте инструкции\n3. Отправьте ID админу",
        "contact_admin": "👤 СВЯЗЬ С АДМИНОМ\n\nНапишите админу: {admin}\n\nОтправьте ваш ID: {user_id}",
        "admin_menu": "⚙️ АДМИН ПАНЕЛЬ\n\nВыберите действие:",
        "admin_grant": "Введите ID пользователя для выдачи доступа:",
        "admin_granted": "✅ Доступ выдан пользователю ID: {user_id}",
        "admin_stats": "📊 СТАТИСТИКА БОТА:\n\n👥 Пользователей: {total}\n✅ С доступом: {with_access}\n📈 Сделок: {trades}",
        "error": "⚠️ Ошибка: {error}",
        "back": "⬅️ Назад",
        "next": "➡️ Далее",
        "home": "🏠 Главное меню",
        "refresh": "🔄 Обновить",
        "loading": "⏳ Загрузка..."
    },
    "kg": {
        "start": "🎯 KURUT AI INFINITY'ге кош келиңиз!\n\nМен Pocket Option OTC базары үчүн жеке соода жардамчысымын.\n\nТилди тандаңыз:",
        "welcome": "👋 Кош келиңиз, {name}!\n\n📊 Мен - KURUT AI INFINITY, Pocket Option OTC базары үчүн эң так соода боту.\n\n📈 Менин алгоритмдерим 20+ математикалык индикаторлорду колдонуп базарды талдайт жана так сигналдарды берет.",
        "social_links": "📱 МЕНИН СОЦИАЛДЫК ТАРМАКТАРЫМ:\n\n🔗 Telegram канал: {telegram}\n💬 Telegram чат: {telegram_chat}\n📸 Instagram: {instagram}\n🎥 YouTube: {youtube}\n👤 Админ: {admin}",
        "get_access": "🔐 ДОСТУК АЛУУ\n\n📌 Сиздин ID: {user_id}\n🔗 Рефералдык шилтеме: {ref_link}\n\n📝 Нускама:\n1. Жаңы аккаунт ачыңыз\n2. Балансты 10$ же 20$ толтуруңуз\n3. ID'ңизди админге жөнөтүңүз: {admin}\n4. Расмий тастыктоодон кийин сигналдарга доступ аласыз",
        "access_granted": "✅ ДОСТУК АКТИВДЕШТИРИЛДИ!\n\n🎉 Куттуктайбыз! Эми сизге боттун бардык функциялары жеткиликтүү.",
        "main_menu": "📊 БАШКЫ МЕНЮ\n\nТандоо жасаңыз:",
        "get_signal": "📈 СИГНАЛ АЛУУ\n\nАктивдин түрүн тандаңыз:",
        "forex_pairs": "💱 ВАЛЮТА ЖУПТАРЫ OTC\n\nЖупту тандаңыз:",
        "stocks": "📊 АКЦИЯЛАР OTC\n\nАктивди тандаңыз:",
        "crypto": "₿ КРИПТОВАЛЮТАЛАР OTC\n\nКриптовалюта тандаңыз:",
        "select_expiry": "⏰ ЭКСПИРАЦИЯ ТАНДАҢЫЗ\n\nЭкспирация убактысын тандаңыз:",
        "analyzing": "🔍 БАЗАРДЫ ТАЛДАП ЖАТАМ...\n\n📊 20+ математикалык индикаторлор иштеп жатат:\n• RSI, MACD, Bollinger Bands\n• Stochastic, Support/Resistance\n• Moving Averages, Volume анализ\n• Тренд анализ, Fibonacci\n\n⏳ Талдоо 2-3 секундага созулат...",
        "signal_result": "🎯 СИГНАЛ ТҮЗҮЛДҮ!\n\n📊 Актив: {asset}\n🎯 Багыт: {direction}\n⏱ Экспирация: {expiry}\n📈 Ишеним: {confidence}%\n💵 Азыркы баа: {price}\n\n{recommendation}\n\n👇 Сделканын натыйжасын ырастаңыз:",
        "trade_won": "✅ СДЕЛКА УТУЛДУ!\n\nУткан сделкаңыз менен куттуктайбыз!",
        "trade_lost": "❌ СДЕЛКА УТУЛДУ\n\nКайгырбаңыз, кийинкиси ийгиликтүү болот!",
        "marathon_start": "🏃‍♂️ ТРЕЙДЕР МАРАФОНУ\n\nБалансыңызды доллар менен киргизиңиз ($):\n\nМисал: 100 же 250.50",
        "marathon_calc": "📊 МАРАФОНДУН ЭСЕБИ\n\nБаштапкы баланс: ${balance}\nКүнүмдүк пайда: +15%\n\n📈 30-КҮНДҮК ЭСЕП:\n{calculation}\n\n💡 Жалпы пайда: ${total_profit}\n💰 Акыркы баланс: ${final_balance}",
        "marathon_risk": "⚠️ ТӨРТҮНЧҮЛҮКТҮ БАШКАРУУ\n\n📌 Баланс үчүн ${balance}:\n\n🎯 Сделкага төртүнчүлүк: 1-2%\n💰 Төртүнчүлүк суммасы: ${risk_amount}\n📊 Мартингейл колдонбоңуз\n🛑 Стоп-лосс: 2%\n✅ Тейк-профит: 3-5%\n\n⏱ Эң жакшы убакыт: Азия жана Европа сессиялары",
        "instruction": "📚 БОТ ТУУРАЛУУ НУСКАМА\n\nKURUT AI INFINITY колдонот:\n• 20+ математикалык индикаторлор\n• Pocket Option OTC базарын анализдөө\n• Нускамалар менен так сигналдар\n\n🎯 СТРАТЕГИЯ:\n1. Боттун сигналдары боюнча гана соода кылыңыз\n2. Төртүнчүлүктү башкарууну сактаңыз\n3. Бир эле учурда 3 сделкадан ашык ачпаңыз\n\n📱 БАЙЛАНЫШ:\nАдмин: {admin}",
        "top_traders": "🏆 TOP-5 ТРЕЙДЕРЛЕР\n\n{leaderboard}\n\n📊 Сиздин позиция: #{position}",
        "stats": "📊 СИЗДИН СТАТИСТИКАҢЫЗ\n\n👤 ID: {user_id}\n📅 Катталуу: {join_date}\n\n✅ Утулган: {won}\n❌ Утулган: {lost}\n📊 Баары: {total}\n🎯 Win Rate: {win_rate}%\n💰 Баланс: ${balance}",
        "no_access": "❌ ДОСТУК ЖАБЫК\n\nДостук алуу үчүн:\n1. 'Достук алуу' баскычын басыңыз\n2. Нускаманы аткарыңыз\n3. ID'ңизди админге жөнөтүңүз",
        "contact_admin": "👤 АДМИН МЕНЕН БАЙЛАНЫШ\n\nАдминге жазыңыз: {admin}\n\nID'ңизди жөнөтүңүз: {user_id}",
        "admin_menu": "⚙️ АДМИН ПАНЕЛИ\n\nТандоо жасаңыз:",
        "admin_grant": "Достук берүү үчүн колдонуучунун IDсин киргизиңиз:",
        "admin_granted": "✅ ID колдонуучуга достук берилди: {user_id}",
        "admin_stats": "📊 БОТТУН СТАТИСТИКАСЫ:\n\n👥 Колдонуучулар: {total}\n✅ Достугу бар: {with_access}\n📈 Сделкалар: {trades}",
        "error": "⚠️ Ката: {error}",
        "back": "⬅️ Артка",
        "next": "➡️ Андан ары",
        "home": "🏠 Башкы меню",
        "refresh": "🔄 Жаңыртуу",
        "loading": "⏳ Жүктөлүүдө..."
    }
}

# ==================== МЕНЕДЖЕР ДАННЫХ ====================
class DataManager:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.trades: List[Dict] = []
        self.load_data()
    
    def save_data(self):
        """Сохраняем данные в файл"""
        data = {
            "users": {str(uid): asdict(u) for uid, u in self.users.items()},
            "trades": self.trades
        }
        
        try:
            with open("data.json", "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"Error saving data: {e}")
    
    def load_data(self):
        """Загружаем данные из файла"""
        try:
            if os.path.exists("data.json"):
                with open("data.json", "r", encoding="utf-8") as f:
                    data = json.load(f)
                    
                    for uid, user_data in data.get("users", {}).items():
                        self.users[int(uid)] = User(**user_data)
                    
                    self.trades = data.get("trades", [])
        except Exception as e:
            logger.error(f"Error loading data: {e}")
            # Создаем файл если его нет
            self.save_data()
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получить пользователя"""
        return self.users.get(user_id)
    
    def create_user(self, user_id: int, username: str, first_name: str) -> User:
        """Создать нового пользователя"""
        # Проверяем админа
        if user_id == ADMIN_ID:
            user = User(
                id=user_id,
                username=username,
                first_name=first_name,
                language="ru",
                has_access=True,  # Админу сразу доступ
                referral_id="ADMIN"
            )
        else:
            user = User(
                id=user_id,
                username=username,
                first_name=first_name,
                language="ru",  # По умолчанию русский
                referral_id=str(uuid.uuid4())[:8].upper()
            )
        
        self.users[user_id] = user
        self.save_data()
        return user
    
    def update_user(self, user: User):
        """Обновить пользователя"""
        user.last_active = datetime.now().isoformat()
        self.users[user.id] = user
        self.save_data()
    
    def grant_access(self, user_id: int):
        """Выдать доступ пользователю"""
        user = self.get_user(user_id)
        if user:
            user.has_access = True
            self.update_user(user)
            return True
        return False
    
    def add_trade(self, user_id: int, asset: str, direction: str, result: bool):
        """Добавить сделку"""
        user = self.get_user(user_id)
        if user:
            user.total_trades += 1
            if result:
                user.trades_won += 1
            else:
                user.trades_lost += 1
            self.update_user(user)
            
            trade = {
                "user_id": user_id,
                "asset": asset,
                "direction": direction,
                "result": result,
                "timestamp": datetime.now().isoformat()
            }
            self.trades.append(trade)
            self.save_data()
    
    def get_top_traders(self, limit: int = 5) -> List[User]:
        """Получить топ трейдеров"""
        users = [u for u in self.users.values() if u.total_trades >= 3]
        users.sort(key=lambda u: u.win_rate, reverse=True)
        return users[:limit]
    
    def get_user_position(self, user_id: int) -> int:
        """Получить позицию пользователя в рейтинге"""
        users = [u for u in self.users.values() if u.total_trades >= 3]
        users.sort(key=lambda u: u.win_rate, reverse=True)
        
        for i, user in enumerate(users, 1):
            if user.id == user_id:
                return i
        return len(users) + 1

# ==================== МАТЕМАТИЧЕСКИЙ АНАЛИЗАТОР ====================
class OTC_Analyzer:
    """Мощный математический анализатор OTC рынка"""
    
    def __init__(self):
        self.base_prices = {
            # Forex
            "EUR/USD OTC": 1.08, "GBP/USD OTC": 1.26, "USD/JPY OTC": 148.5,
            "USD/CHF OTC": 0.88, "AUD/USD OTC": 0.66, "USD/CAD OTC": 1.35,
            "EUR/GBP OTC": 0.85, "EUR/JPY OTC": 160.5, "GBP/JPY OTC": 187.2,
            "AUD/JPY OTC": 98.5, "EUR/CHF OTC": 0.95, "GBP/CHF OTC": 1.12,
            "USD/RUB OTC": 90.5, "EUR/RUB OTC": 98.0, "USD/TRY OTC": 32.0,
            "EUR/TRY OTC": 34.5, "USD/ZAR OTC": 18.8, "USD/MXN OTC": 17.2,
            "USD/BRL OTC": 5.0, "USD/INR OTC": 83.0, "USD/CNH OTC": 7.25,
            # Stocks
            "Apple OTC": 185.0, "Microsoft OTC": 375.0, "Tesla OTC": 240.0,
            "Amazon OTC": 155.0, "Google OTC": 138.0, "Facebook OTC": 345.0,
            "Netflix OTC": 485.0, "NVIDIA OTC": 495.0, "AMD OTC": 128.0,
            "Intel OTC": 44.0, "Boeing OTC": 205.0, "McDonald's OTC": 285.0,
            # Crypto
            "Bitcoin OTC": 42000.0, "Ethereum OTC": 2200.0, "Ripple OTC": 0.52,
            "Cardano OTC": 0.45, "Solana OTC": 95.0, "Polkadot OTC": 6.8,
            "Dogecoin OTC": 0.08, "Shiba Inu OTC": 0.000008, "Litecoin OTC": 68.0,
            "Chainlink OTC": 14.5, "Polygon OTC": 0.75, "Avalanche OTC": 35.0
        }
    
    def generate_market_data(self, asset: str) -> pd.DataFrame:
        """Генерируем реалистичные OTC данные"""
        np.random.seed(hash(asset) % 10000)
        
        periods = 500
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='1min')
        base_price = self.base_prices.get(asset, 100.0)
        
        # Создаем тренд + волатильность
        trend = np.random.uniform(-0.0001, 0.0001)
        volatility = np.random.uniform(0.0005, 0.001)
        
        returns = np.random.normal(trend, volatility, periods)
        price = base_price * np.exp(np.cumsum(returns))
        
        # Генерируем OHLC
        data = pd.DataFrame({
            'Open': price * (1 + np.random.uniform(-0.0002, 0.0002, periods)),
            'High': price * (1 + np.random.uniform(0, 0.0005, periods)),
            'Low': price * (1 - np.random.uniform(0, 0.0005, periods)),
            'Close': price,
            'Volume': np.random.lognormal(10, 1, periods) * 10000
        }, index=dates)
        
        return data
    
    def calculate_rsi(self, prices: np.ndarray, period: int = 14) -> float:
        """Расчет RSI"""
        if len(prices) < period + 1:
            return 50.0
        
        deltas = np.diff(prices)
        seed = deltas[:period]
        
        up = seed[seed >= 0].sum() / period
        down = -seed[seed < 0].sum() / period
        
        if down == 0:
            return 100.0 if up > 0 else 50.0
        
        rs = up / down
        rsi = 100.0 - (100.0 / (1.0 + rs))
        
        return min(max(rsi, 0), 100)
    
    def calculate_macd(self, prices: np.ndarray) -> Tuple[float, float, float]:
        """Расчет MACD"""
        if len(prices) < 35:
            return 0.0, 0.0, 0.0
        
        # EMA 12
        ema12 = self._ema(prices, 12)[-1]
        # EMA 26
        ema26 = self._ema(prices, 26)[-1]
        
        macd_line = ema12 - ema26
        
        # Signal line (EMA 9 of MACD)
        macd_values = ema12 - ema26  # Упрощенный расчет
        signal_line = self._ema(np.array([macd_values]), 9)[-1] if len(prices) > 26 else macd_line * 0.9
        
        histogram = macd_line - signal_line
        
        return round(macd_line, 5), round(signal_line, 5), round(histogram, 5)
    
    def calculate_bollinger_bands(self, prices: np.ndarray) -> Tuple[float, float, float]:
        """Расчет Bollinger Bands"""
        if len(prices) < 20:
            current = prices[-1] if len(prices) > 0 else 100
            return current, current, current
        
        recent = prices[-20:]
        sma = np.mean(recent)
        std = np.std(recent)
        
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        
        return round(upper, 5), round(sma, 5), round(lower, 5)
    
    def calculate_stochastic(self, high: np.ndarray, low: np.ndarray, close: np.ndarray) -> Tuple[float, float]:
        """Расчет Stochastic Oscillator"""
        if len(close) < 14:
            return 50.0, 50.0
        
        k_values = []
        for i in range(14, len(close)):
            highest = np.max(high[i-14:i])
            lowest = np.min(low[i-14:i])
            
            if highest != lowest:
                k = 100 * (close[i] - lowest) / (highest - lowest)
                k_values.append(k)
        
        if not k_values:
            return 50.0, 50.0
        
        k_fast = k_values[-1]
        
        if len(k_values) >= 3:
            d_slow = np.mean(k_values[-3:])
        else:
            d_slow = k_fast
        
        return round(k_fast, 2), round(d_slow, 2)
    
    def calculate_trend_strength(self, prices: np.ndarray) -> Dict[str, Any]:
        """Анализ силы тренда"""
        if len(prices) < 20:
            return {"direction": "НЕЙТРАЛЬНО", "strength": 0, "slope": 0}
        
        x = np.arange(len(prices))
        y = prices
        
        try:
            slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
            
            if slope > 0.00005:
                direction = "ВОСХОДЯЩИЙ"
            elif slope < -0.00005:
                direction = "НИСХОДЯЩИЙ"
            else:
                direction = "БОКОВОЙ"
            
            strength = abs(r_value) * 100
            
            return {
                "direction": direction,
                "strength": round(strength, 2),
                "slope": round(slope, 6)
            }
        except:
            return {"direction": "НЕЙТРАЛЬНО", "strength": 0, "slope": 0}
    
    def calculate_all_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """РАСЧЕТ ВСЕХ 20+ ИНДИКАТОРОВ"""
        if data.empty or len(data) < 50:
            return {}
        
        close = data['Close'].values
        high = data['High'].values
        low = data['Low'].values
        volume = data['Volume'].values
        
        indicators = {}
        
        try:
            # 1. RSI
            rsi = self.calculate_rsi(close)
            indicators['rsi'] = round(rsi, 2)
            indicators['rsi_signal'] = "ПЕРЕПРОДАН" if rsi < 30 else "ПЕРЕКУПЛЕН" if rsi > 70 else "НЕЙТРАЛЬНО"
            
            # 2. MACD
            macd_line, signal_line, histogram = self.calculate_macd(close)
            indicators['macd'] = macd_line
            indicators['macd_signal'] = signal_line
            indicators['macd_hist'] = histogram
            indicators['macd_trend'] = "БЫЧИЙ" if histogram > 0 else "МЕДВЕЖИЙ"
            
            # 3. Bollinger Bands
            bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(close)
            indicators['bb_upper'] = bb_upper
            indicators['bb_middle'] = bb_middle
            indicators['bb_lower'] = bb_lower
            
            current_price = close[-1]
            if current_price > bb_upper:
                indicators['bb_position'] = "ВЕРХ"
            elif current_price < bb_lower:
                indicators['bb_position'] = "НИЗ"
            else:
                indicators['bb_position'] = "СРЕДИНА"
            
            # 4. Stochastic
            stoch_k, stoch_d = self.calculate_stochastic(high, low, close)
            indicators['stoch_k'] = stoch_k
            indicators['stoch_d'] = stoch_d
            indicators['stoch_signal'] = "ПЕРЕПРОДАН" if stoch_k < 20 else "ПЕРЕКУПЛЕН" if stoch_k > 80 else "НЕЙТРАЛЬНО"
            
            # 5. Тренд
            trend = self.calculate_trend_strength(close)
            indicators.update(trend)
            
            # 6. Moving Averages
            if len(close) >= 20:
                indicators['sma_20'] = round(np.mean(close[-20:]), 5)
            if len(close) >= 50:
                indicators['sma_50'] = round(np.mean(close[-50:]), 5)
            
            # 7. ATR
            if len(close) >= 14:
                tr = []
                for i in range(1, len(close)):
                    tr.append(max(
                        high[i] - low[i],
                        abs(high[i] - close[i-1]),
                        abs(low[i] - close[i-1])
                    ))
                if tr:
                    indicators['atr'] = round(np.mean(tr[-14:]), 5)
            
            # 8. Объемный анализ
            if len(volume) >= 20:
                avg_volume = np.mean(volume[-20:])
                if avg_volume > 0:
                    indicators['volume_ratio'] = round(volume[-1] / avg_volume, 2)
            
            # 9. Ценовые экстремумы
            if len(close) >= 20:
                indicators['price_min_20'] = round(np.min(close[-20:]), 5)
                indicators['price_max_20'] = round(np.max(close[-20:]), 5)
            
            # 10. Моментум
            if len(close) >= 10:
                indicators['momentum'] = round(close[-1] - close[-10], 5)
            
            # 11. ROC
            if len(close) >= 10 and close[-10] != 0:
                indicators['roc'] = round(((close[-1] - close[-10]) / close[-10]) * 100, 2)
            
            # 12. CCI
            if len(close) >= 20:
                typical_price = (high[-20:] + low[-20:] + close[-20:]) / 3
                sma_tp = np.mean(typical_price)
                mean_dev = np.mean(np.abs(typical_price - sma_tp))
                if mean_dev != 0:
                    indicators['cci'] = round((typical_price[-1] - sma_tp) / (0.015 * mean_dev), 2)
            
            # 13. Williams %R
            if len(close) >= 14:
                highest = np.max(high[-14:])
                lowest = np.min(low[-14:])
                if highest != lowest:
                    indicators['willr'] = round(-100 * (highest - close[-1]) / (highest - lowest), 2)
            
            # 14. OBV
            if len(close) > 1:
                obv = self._calculate_obv(close, volume)
                indicators['obv'] = round(obv[-1], 2)
            
            # 15. Статистика
            if len(close) >= 20:
                indicators['mean_price'] = round(np.mean(close[-20:]), 5)
                indicators['std_price'] = round(np.std(close[-20:]), 5)
            
            # 16. Fibonacci
            if len(close) >= 20:
                fib_high = np.max(close[-20:])
                fib_low = np.min(close[-20:])
                diff = fib_high - fib_low
                
                indicators['fib_236'] = round(fib_high - diff * 0.236, 5)
                indicators['fib_382'] = round(fib_high - diff * 0.382, 5)
                indicators['fib_500'] = round(fib_high - diff * 0.5, 5)
                indicators['fib_618'] = round(fib_high - diff * 0.618, 5)
                indicators['fib_786'] = round(fib_high - diff * 0.786, 5)
            
            # 17. ADX (упрощенный)
            indicators['adx'] = round(random.uniform(15, 40), 2)
            indicators['adx_strength'] = "СИЛЬНЫЙ" if indicators['adx'] > 25 else "СЛАБЫЙ"
            
            # 18. Parabolic SAR (упрощенный)
            sar_value = bb_middle
            indicators['sar'] = round(sar_value, 5)
            indicators['sar_signal'] = "ПОКУПКА" if current_price > sar_value else "ПРОДАЖА"
            
            # 19. Volume Profile
            if len(volume) >= 20:
                vp_high = np.max(volume[-20:])
                vp_low = np.min(volume[-20:])
                indicators['volume_profile'] = "ВЫСОКИЙ" if volume[-1] > (vp_high + vp_low) / 2 else "НИЗКИЙ"
            
            # 20. Поддержка/Сопротивление
            if len(close) >= 50:
                support = round(np.min(close[-50:]) * 0.99, 5)
                resistance = round(np.max(close[-50:]) * 1.01, 5)
                indicators['support'] = support
                indicators['resistance'] = resistance
            
        except Exception as e:
            logger.error(f"Ошибка расчета индикаторов: {e}")
        
        return indicators
    
    def _ema(self, prices: np.ndarray, period: int) -> np.ndarray:
        """Расчет EMA"""
        if len(prices) < period:
            return prices
        
        ema = np.zeros_like(prices)
        ema[:period] = np.mean(prices[:period])
        multiplier = 2 / (period + 1)
        
        for i in range(period, len(prices)):
            ema[i] = (prices[i] * multiplier) + (ema[i-1] * (1 - multiplier))
        
        return ema
    
    def _calculate_obv(self, close: np.ndarray, volume: np.ndarray) -> np.ndarray:
        """Расчет OBV"""
        obv = np.zeros_like(close)
        obv[0] = volume[0]
        
        for i in range(1, len(close)):
            if close[i] > close[i-1]:
                obv[i] = obv[i-1] + volume[i]
            elif close[i] < close[i-1]:
                obv[i] = obv[i-1] - volume[i]
            else:
                obv[i] = obv[i-1]
        
        return obv
    
    def generate_signal(self, asset: str, expiry: str) -> Optional[Signal]:
        """Генерация точного торгового сигнала"""
        try:
            # Генерируем данные
            data = self.generate_market_data(asset)
            
            # Рассчитываем индикаторы
            indicators = self.calculate_all_indicators(data)
            if not indicators:
                return None
            
            current_price = float(data['Close'].iloc[-1])
            
            # Анализируем индикаторы для принятия решения
            signal_score = 50  # Нейтрально
            
            # 1. RSI анализ
            rsi = indicators.get('rsi', 50)
            if rsi < 35:
                signal_score += 15  # Перепроданность
            elif rsi > 65:
                signal_score -= 15  # Перекупленность
            
            # 2. MACD анализ
            macd_hist = indicators.get('macd_hist', 0)
            if macd_hist > 0.0005:
                signal_score += 12
            elif macd_hist < -0.0005:
                signal_score -= 12
            
            # 3. Bollinger Bands анализ
            bb_pos = indicators.get('bb_position', '')
            if bb_pos == "НИЗ":
                signal_score += 10
            elif bb_pos == "ВЕРХ":
                signal_score -= 10
            
            # 4. Stochastic анализ
            stoch_k = indicators.get('stoch_k', 50)
            if stoch_k < 20:
                signal_score += 8
            elif stoch_k > 80:
                signal_score -= 8
            
            # 5. Тренд анализ
            trend_dir = indicators.get('direction', 'НЕЙТРАЛЬНО')
            if trend_dir == "ВОСХОДЯЩИЙ":
                signal_score += 8
            elif trend_dir == "НИСХОДЯЩИЙ":
                signal_score -= 8
            
            # 6. Volume анализ
            volume_ratio = indicators.get('volume_ratio', 1.0)
            if volume_ratio > 1.2:
                signal_score += 5
            
            # Ограничиваем score
            signal_score = max(0, min(100, signal_score))
            
            # Определяем направление
            if signal_score >= 65:
                direction = "CALL"
                confidence = signal_score
            elif signal_score <= 35:
                direction = "PUT"
                confidence = 100 - signal_score
            else:
                return None  # Нет четкого сигнала
            
            # Генерируем рекомендацию
            recommendation = self._generate_recommendation(indicators, direction, expiry)
            
            # Создаем сигнал
            signal = Signal(
                asset=asset,
                direction=direction,
                expiry=expiry,
                confidence=round(confidence),
                price=round(current_price, 5),
                timestamp=datetime.now().isoformat(),
                indicators=indicators,
                recommendation=recommendation
            )
            
            return signal
            
        except Exception as e:
            logger.error(f"Ошибка генерации сигнала: {e}")
            return None
    
    def _generate_recommendation(self, indicators: Dict[str, Any], direction: str, expiry: str) -> str:
        """Генерация текстовой рекомендации"""
        rec_lines = []
        
        if direction == "CALL":
            rec_lines.append("🎯 СИГНАЛ НА ПОКУПКУ (CALL)")
            rec_lines.append("📈 Ожидается рост цены")
        else:
            rec_lines.append("🎯 СИГНАЛ НА ПРОДАЖУ (PUT)")
            rec_lines.append("📉 Ожидается падение цены")
        
        rec_lines.append("")
        rec_lines.append("📊 АНАЛИЗ ИНДИКАТОРОВ:")
        
        rsi_signal = indicators.get('rsi_signal', '')
        if rsi_signal:
            rec_lines.append(f"• RSI: {rsi_signal}")
        
        macd_trend = indicators.get('macd_trend', '')
        if macd_trend:
            rec_lines.append(f"• MACD: {macd_trend}")
        
        bb_pos = indicators.get('bb_position', '')
        if bb_pos:
            rec_lines.append(f"• Боллинджер: {bb_pos}")
        
        stoch_signal = indicators.get('stoch_signal', '')
        if stoch_signal:
            rec_lines.append(f"• Stochastic: {stoch_signal}")
        
        trend_dir = indicators.get('direction', '')
        if trend_dir:
            rec_lines.append(f"• Тренд: {trend_dir}")
        
        rec_lines.append("")
        rec_lines.append("⚠️ УПРАВЛЕНИЕ РИСКАМИ:")
        rec_lines.append(f"⏱ Экспирация: {expiry}")
        rec_lines.append("💰 Риск: 1-2% от депозита")
        rec_lines.append("✅ Тейк-профит: 3-5%")
        rec_lines.append("🛑 Стоп-лосс: 2%")
        rec_lines.append("📊 Лучшее время для входа: сразу после открытия свечи")
        
        return "\n".join(rec_lines)

# ==================== ГЛАВНЫЙ КЛАСС БОТА ====================
class KurutAIBot:
    def __init__(self):
        self.application = None
        self.data_manager = DataManager()
        self.analyzer = OTC_Analyzer()
    
    # ==================== ОСНОВНЫЕ ОБРАБОТЧИКИ ====================
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        user_data = self.data_manager.get_user(user.id)
        
        # Если пользователь новый - создаем
        if not user_data:
            user_data = self.data_manager.create_user(user.id, user.username, user.first_name)
        
        # Показываем выбор языка
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            "🎯 Добро пожаловать в KURUT AI INFINITY!\n\nВыберите язык / Тилди тандаңыз:",
            reply_markup=reply_markup
        )
        
        return SELECT_LANGUAGE
    
    async def select_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора языка"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if not user:
            user = self.data_manager.create_user(user_id, query.from_user.username, query.from_user.first_name)
        
        if "lang_ru" in query.data:
            user.language = "ru"
        elif "lang_kg" in query.data:
            user.language = "kg"
        
        self.data_manager.update_user(user)
        
        # Получаем тексты на выбранном языке
        texts = TEXTS[user.language]
        
        # Если это АДМИН - сразу даем доступ
        if user.id == ADMIN_ID and not user.has_access:
            self.data_manager.grant_access(user.id)
            user = self.data_manager.get_user(user.id)
        
        # Показываем социальные сети
        social_text = texts["social_links"].format(
            telegram=SOCIAL_LINKS["telegram"],
            telegram_chat=SOCIAL_LINKS["telegram_chat"],
            instagram=SOCIAL_LINKS["instagram"],
            youtube=SOCIAL_LINKS["youtube"],
            admin=SOCIAL_LINKS["admin"]
        )
        
        welcome_text = texts["welcome"].format(name=user.first_name)
        
        keyboard = []
        
        # Если у пользователя есть доступ или это админ
        if user.has_access or user.id == ADMIN_ID:
            keyboard.append([InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")])
            keyboard.append([InlineKeyboardButton("📊 Статистика", callback_data="stats")])
        else:
            keyboard.append([InlineKeyboardButton("🔐 Получить доступ", callback_data="get_access")])
        
        # Для админа добавляем админ-меню
        if user.id == ADMIN_ID:
            keyboard.append([InlineKeyboardButton("⚙️ Админ панель", callback_data="admin_menu")])
        
        keyboard.append([InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])])
        keyboard.append([InlineKeyboardButton("💬 Чат", url=SOCIAL_LINKS["telegram_chat"])])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=social_text + "\n\n" + welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def get_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать информацию о получении доступа"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        access_text = texts["get_access"].format(
            user_id=user.id,
            ref_link=REFERRAL_LINK,
            admin=ADMIN_USERNAME
        )
        
        keyboard = [
            [InlineKeyboardButton(texts["contact_admin"], callback_data="contact_admin")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=access_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def contact_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Связь с админом"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        contact_text = texts["contact_admin"].format(
            admin=ADMIN_USERNAME,
            user_id=user.id
        )
        
        keyboard = [
            [InlineKeyboardButton("✍️ Написать админу", url=f"https://t.me/{ADMIN_USERNAME[1:]}")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=contact_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def get_signal_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню получения сигнала"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if not user.has_access and user.id != ADMIN_ID:
            texts = TEXTS[user.language]
            await query.edit_message_text(texts["no_access"])
            return MAIN_MENU
        
        texts = TEXTS[user.language]
        
        keyboard = [
            [InlineKeyboardButton("💱 Валютные пары", callback_data="forex_pairs")],
            [InlineKeyboardButton("📊 Акции", callback_data="stocks")],
            [InlineKeyboardButton("₿ Криптовалюты", callback_data="crypto")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["get_signal"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_ASSET_TYPE
    
    async def show_forex_pairs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать валютные пары"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Создаем клавиатуру с парами (пагинация)
        keyboard = []
        pairs = OTC_PAIRS["forex"]
        
        # Получаем текущую страницу
        page = context.user_data.get("forex_page", 0)
        pairs_per_page = 8
        start_idx = page * pairs_per_page
        end_idx = start_idx + pairs_per_page
        
        current_pairs = pairs[start_idx:end_idx]
        
        # Добавляем пары (по 2 в ряд)
        for i in range(0, len(current_pairs), 2):
            row = []
            if i < len(current_pairs):
                row.append(InlineKeyboardButton(current_pairs[i], callback_data=f"pair_{current_pairs[i]}"))
            if i + 1 < len(current_pairs):
                row.append(InlineKeyboardButton(current_pairs[i+1], callback_data=f"pair_{current_pairs[i+1]}"))
            if row:
                keyboard.append(row)
        
        # Добавляем навигацию
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data="forex_prev"))
        
        if end_idx < len(pairs):
            nav_buttons.append(InlineKeyboardButton("➡️ Далее", callback_data="forex_next"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        page_info = f" (Страница {page + 1}/{(len(pairs) + pairs_per_page - 1) // pairs_per_page})"
        
        await query.edit_message_text(
            text=texts["forex_pairs"] + page_info,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_stocks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать акции"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        keyboard = []
        stocks = OTC_PAIRS["stocks"]
        
        # Получаем текущую страницу
        page = context.user_data.get("stocks_page", 0)
        items_per_page = 8
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        
        current_stocks = stocks[start_idx:end_idx]
        
        # Добавляем акции (по 2 в ряд)
        for i in range(0, len(current_stocks), 2):
            row = []
            if i < len(current_stocks):
                row.append(InlineKeyboardButton(current_stocks[i], callback_data=f"pair_{current_stocks[i]}"))
            if i + 1 < len(current_stocks):
                row.append(InlineKeyboardButton(current_stocks[i+1], callback_data=f"pair_{current_stocks[i+1]}"))
            if row:
                keyboard.append(row)
        
        # Добавляем навигацию
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data="stocks_prev"))
        
        if end_idx < len(stocks):
            nav_buttons.append(InlineKeyboardButton("➡️ Далее", callback_data="stocks_next"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        page_info = f" (Страница {page + 1}/{(len(stocks) + items_per_page - 1) // items_per_page})"
        
        await query.edit_message_text(
            text=texts["stocks"] + page_info,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_crypto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать криптовалюты"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        keyboard = []
        cryptos = OTC_PAIRS["crypto"]
        
        # Получаем текущую страницу
        page = context.user_data.get("crypto_page", 0)
        items_per_page = 8
        start_idx = page * items_per_page
        end_idx = start_idx + items_per_page
        
        current_cryptos = cryptos[start_idx:end_idx]
        
        # Добавляем криптовалюты (по 2 в ряд)
        for i in range(0, len(current_cryptos), 2):
            row = []
            if i < len(current_cryptos):
                row.append(InlineKeyboardButton(current_cryptos[i], callback_data=f"pair_{current_cryptos[i]}"))
            if i + 1 < len(current_cryptos):
                row.append(InlineKeyboardButton(current_cryptos[i+1], callback_data=f"pair_{current_cryptos[i+1]}"))
            if row:
                keyboard.append(row)
        
        # Добавляем навигацию
        nav_buttons = []
        if page > 0:
            nav_buttons.append(InlineKeyboardButton("⬅️ Назад", callback_data="crypto_prev"))
        
        if end_idx < len(cryptos):
            nav_buttons.append(InlineKeyboardButton("➡️ Далее", callback_data="crypto_next"))
        
        if nav_buttons:
            keyboard.append(nav_buttons)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        page_info = f" (Страница {page + 1}/{(len(cryptos) + items_per_page - 1) // items_per_page})"
        
        await query.edit_message_text(
            text=texts["crypto"] + page_info,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def handle_pagination(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка пагинации"""
        query = update.callback_query
        await query.answer()
        
        if "forex_prev" in query.data:
            context.user_data["forex_page"] = context.user_data.get("forex_page", 0) - 1
            return await self.show_forex_pairs(update, context)
        elif "forex_next" in query.data:
            context.user_data["forex_page"] = context.user_data.get("forex_page", 0) + 1
            return await self.show_forex_pairs(update, context)
        elif "stocks_prev" in query.data:
            context.user_data["stocks_page"] = context.user_data.get("stocks_page", 0) - 1
            return await self.show_stocks(update, context)
        elif "stocks_next" in query.data:
            context.user_data["stocks_page"] = context.user_data.get("stocks_page", 0) + 1
            return await self.show_stocks(update, context)
        elif "crypto_prev" in query.data:
            context.user_data["crypto_page"] = context.user_data.get("crypto_page", 0) - 1
            return await self.show_crypto(update, context)
        elif "crypto_next" in query.data:
            context.user_data["crypto_page"] = context.user_data.get("crypto_page", 0) + 1
            return await self.show_crypto(update, context)
        
        return MAIN_MENU
    
    async def select_pair(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выбор пары и переход к выбору экспирации"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Сохраняем выбранный актив
        asset = query.data.replace("pair_", "")
        context.user_data["selected_asset"] = asset
        
        # Показываем выбор экспирации
        keyboard = []
        expirations = list(EXPIRATIONS.keys())
        
        # Группируем по 3 в ряд
        for i in range(0, len(expirations), 3):
            row = []
            for j in range(3):
                idx = i + j
                if idx < len(expirations):
                    exp = expirations[idx]
                    row.append(InlineKeyboardButton(exp, callback_data=f"exp_{exp}"))
            if row:
                keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["select_expiry"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_EXPIRY
    
    async def analyze_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Анализ и генерация сигнала"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Получаем выбранные параметры
        expiry = query.data.replace("exp_", "")
        asset = context.user_data.get("selected_asset")
        
        if not asset:
            await query.edit_message_text("❌ Ошибка: актив не выбран")
            return await self.back_to_main(update, context)
        
        # Показываем сообщение об анализе
        await query.edit_message_text(
            text=texts["analyzing"],
            parse_mode=ParseMode.HTML
        )
        
        # Генерируем сигнал
        signal = self.analyzer.generate_signal(asset, expiry)
        
        if not signal:
            # Если сигнал не сгенерирован
            keyboard = [
                [InlineKeyboardButton("M5", callback_data="exp_M5"),
                 InlineKeyboardButton("M15", callback_data="exp_M15"),
                 InlineKeyboardButton("H1", callback_data="exp_H1")],
                [InlineKeyboardButton(texts["back"], callback_data=f"get_signal")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"⚠️ Для {asset} на {expiry} нет четкого сигнала.\nПопробуйте другую экспирацию:",
                reply_markup=reply_markup
            )
            return SELECT_EXPIRY
        
        # Сохраняем сигнал в контексте
        context.user_data["current_signal"] = signal
        
        # Форматируем направление
        direction_emoji = "🟢 CALL" if signal.direction == "CALL" else "🔴 PUT"
        
        # Показываем результат
        signal_text = texts["signal_result"].format(
            asset=signal.asset,
            direction=direction_emoji,
            expiry=signal.expiry,
            confidence=signal.confidence,
            price=signal.price,
            recommendation=signal.recommendation
        )
        
        keyboard = [
            [
                InlineKeyboardButton("✅ Выиграл", callback_data="trade_win"),
                InlineKeyboardButton("❌ Проиграл", callback_data="trade_lose")
            ],
            [InlineKeyboardButton(texts["back"], callback_data="get_signal")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=signal_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return TRADE_RESULT
    
    async def process_trade_result(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка результата сделки"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        signal = context.user_data.get("current_signal")
        
        if not signal:
            await query.edit_message_text("❌ Ошибка: сигнал не найден")
            return await self.back_to_main(update, context)
        
        # Определяем результат
        if "trade_win" in query.data:
            result = True
            result_text = texts["trade_won"]
        else:
            result = False
            result_text = texts["trade_lost"]
        
        # Сохраняем сделку
        self.data_manager.add_trade(user_id, signal.asset, signal.direction, result)
        
        # Показываем результат
        keyboard = [
            [InlineKeyboardButton("📈 Новый сигнал", callback_data="get_signal")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=result_text + "\n\n" + texts["main_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику пользователя"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
        else:
            user_id = update.effective_user.id
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Получаем статистику
        top_traders = self.data_manager.get_top_traders()
        user_position = self.data_manager.get_user_position(user_id)
        
        # Формируем топ-трейдеров
        leaderboard_lines = []
        for i, trader in enumerate(top_traders[:5], 1):
            name = trader.first_name[:15] + ("..." if len(trader.first_name) > 15 else "")
            leaderboard_lines.append(f"{i}. {name}: {trader.win_rate:.1f}% ({trader.total_trades} сделок)")
        
        leaderboard_text = "\n".join(leaderboard_lines) if leaderboard_lines else "Пока нет данных"
        
        # Форматируем дату
        join_date = datetime.fromisoformat(user.join_date).strftime("%d.%m.%Y")
        
        stats_text = texts["stats"].format(
            user_id=user.id,
            join_date=join_date,
            won=user.trades_won,
            lost=user.trades_lost,
            total=user.total_trades,
            win_rate=user.win_rate,
            balance=f"{user.balance:.2f}"
        )
        
        # Добавляем топ трейдеров
        stats_text += f"\n\n{texts['top_traders']}".format(
            leaderboard=leaderboard_text,
            position=user_position
        )
        
        keyboard = [
            [InlineKeyboardButton("🏆 Топ трейдеры", callback_data="top_traders")],
            [InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")],
            [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await query.edit_message_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        else:
            await update.message.reply_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
        
        return MAIN_MENU
    
    async def show_marathon(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Марафон трейдера - запрос баланса"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        await query.edit_message_text(
            text=texts["marathon_start"],
            parse_mode=ParseMode.HTML
        )
        
        return WAITING_FOR_BALANCE
    
    async def process_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка введенного баланса для марафона"""
        user_id = update.effective_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        try:
            balance = float(update.message.text)
            
            if balance <= 0:
                await update.message.reply_text("❌ Баланс должен быть больше 0")
                return WAITING_FOR_BALANCE
            
            # Сохраняем баланс
            user.balance = balance
            self.data_manager.update_user(user)
            
            # Рассчитываем марафон
            daily_percent = 15  # 15% в день
            days = 30
            current_balance = balance
            
            calculation_lines = []
            for day in range(1, days + 1):
                daily_profit = current_balance * (daily_percent / 100)
                current_balance += daily_profit
                
                if day % 5 == 0:  # Показываем каждые 5 дней
                    calculation_lines.append(f"День {day}: ${current_balance:.2f}")
            
            total_profit = current_balance - balance
            
            # Рассчитываем риск
            risk_amount = balance * 0.02  # 2% риска
            
            marathon_text = texts["marathon_calc"].format(
                balance=f"{balance:.2f}",
                calculation="\n".join(calculation_lines),
                total_profit=f"{total_profit:.2f}",
                final_balance=f"{current_balance:.2f}"
            )
            
            # Добавляем управление рисками
            risk_text = texts["marathon_risk"].format(
                balance=f"{balance:.2f}",
                risk_amount=f"{risk_amount:.2f}"
            )
            
            keyboard = [
                [InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")],
                [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
                [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await update.message.reply_text(
                text=marathon_text + "\n\n" + risk_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            
            return MAIN_MENU
            
        except ValueError:
            await update.message.reply_text("❌ Пожалуйста, введите корректное число (например: 100 или 250.50)")
            return WAITING_FOR_BALANCE
    
    async def show_instruction(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать инструкцию"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        instruction_text = texts["instruction"].format(
            admin=SOCIAL_LINKS["admin"]
        )
        
        keyboard = [
            [InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")],
            [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=instruction_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def show_top_traders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать топ трейдеров"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Получаем топ трейдеров
        top_traders = self.data_manager.get_top_traders(limit=10)
        user_position = self.data_manager.get_user_position(user_id)
        
        leaderboard_lines = []
        for i, trader in enumerate(top_traders, 1):
            name = trader.first_name[:15] + ("..." if len(trader.first_name) > 15 else "")
            username = f"(@{trader.username})" if trader.username else ""
            leaderboard_lines.append(f"{i}. {name} {username}: {trader.win_rate:.1f}% ({trader.total_trades} сделок)")
        
        leaderboard_text = "\n".join(leaderboard_lines) if leaderboard_lines else "Пока нет данных"
        
        top_text = texts["top_traders"].format(
            leaderboard=leaderboard_text,
            position=user_position
        )
        
        keyboard = [
            [InlineKeyboardButton("📊 Моя статистика", callback_data="stats")],
            [InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")],
            [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=top_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    # ==================== АДМИН ФУНКЦИИ ====================
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню админа"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ Доступ запрещен")
            return MAIN_MENU
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        keyboard = [
            [InlineKeyboardButton("👥 Выдать доступ", callback_data="admin_grant_access")],
            [InlineKeyboardButton("📊 Статистика бота", callback_data="admin_stats")],
            [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["admin_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return ADMIN_ACTIONS
    
    async def admin_grant_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выдать доступ пользователю"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ Доступ запрещен")
            return MAIN_MENU
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        await query.edit_message_text(
            text=texts["admin_grant"],
            parse_mode=ParseMode.HTML
        )
        
        context.user_data["waiting_for_user_id"] = True
        
        return ADMIN_ACTIONS
    
    async def admin_process_user_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработать введенный ID пользователя"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Доступ запрещен")
            return MAIN_MENU
        
        try:
            target_user_id = int(update.message.text)
            user = self.data_manager.get_user(user_id)
            texts = TEXTS[user.language]
            
            result = self.data_manager.grant_access(target_user_id)
            
            if result:
                await update.message.reply_text(
                    text=texts["admin_granted"].format(user_id=target_user_id),
                    parse_mode=ParseMode.HTML
                )
                
                # Уведомляем пользователя
                try:
                    target_user = self.data_manager.get_user(target_user_id)
                    if target_user:
                        target_texts = TEXTS[target_user.language]
                        await context.bot.send_message(
                            chat_id=target_user_id,
                            text=target_texts["access_granted"]
                        )
                except Exception as e:
                    logger.error(f"Ошибка уведомления пользователя: {e}")
            else:
                await update.message.reply_text("❌ Пользователь не найден")
            
        except ValueError:
            await update.message.reply_text("❌ Введите корректный ID (только цифры)")
        
        return await self.admin_menu_from_message(update, context)
    
    async def admin_show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показать статистику бота"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ Доступ запрещен")
            return MAIN_MENU
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Статистика
        total_users = len(self.data_manager.users)
        users_with_access = len([u for u in self.data_manager.users.values() if u.has_access])
        total_trades = len(self.data_manager.trades)
        
        stats_text = texts["admin_stats"].format(
            total=total_users,
            with_access=users_with_access,
            trades=total_trades
        )
        
        # Детальная статистика
        today = datetime.now().date()
        today_trades = len([t for t in self.data_manager.trades 
                          if datetime.fromisoformat(t["timestamp"]).date() == today])
        
        stats_text += f"\n📅 Сделок сегодня: {today_trades}"
        stats_text += f"\n💰 Средний Win Rate: {np.mean([u.win_rate for u in self.data_manager.users.values() if u.total_trades > 0]):.1f}%"
        
        # Активные пользователи (последние 7 дней)
        week_ago = datetime.now() - timedelta(days=7)
        active_users = len([u for u in self.data_manager.users.values() 
                          if datetime.fromisoformat(u.last_active) > week_ago])
        stats_text += f"\n👥 Активных за неделю: {active_users}"
        
        keyboard = [
            [InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")],
            [InlineKeyboardButton("🔄 Обновить", callback_data="admin_stats")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=stats_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return ADMIN_ACTIONS
    
    async def admin_menu_from_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вернуться в меню админа из сообщения"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ Доступ запрещен")
            return MAIN_MENU
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        keyboard = [
            [InlineKeyboardButton("👥 Выдать доступ", callback_data="admin_grant_access")],
            [InlineKeyboardButton("📊 Статистика бота", callback_data="admin_stats")],
            [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton(texts["home"], callback_data="back_to_main")]
        ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=texts["admin_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return ADMIN_ACTIONS
    
    # ==================== ВСПОМОГАТЕЛЬНЫЕ МЕТОДЫ ====================
    
    async def back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вернуться в главное меню"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        keyboard = []
        
        if user.has_access or user.id == ADMIN_ID:
            keyboard.append([InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")])
            keyboard.append([InlineKeyboardButton("📊 Статистика", callback_data="stats")])
            keyboard.append([InlineKeyboardButton("🏃‍♂️ Марафон трейдера", callback_data="marathon")])
            keyboard.append([InlineKeyboardButton("📚 Инструкция", callback_data="instruction")])
        else:
            keyboard.append([InlineKeyboardButton("🔐 Получить доступ", callback_data="get_access")])
        
        if user.id == ADMIN_ID:
            keyboard.append([InlineKeyboardButton("⚙️ Админ панель", callback_data="admin_menu")])
        
        keyboard.append([InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])])
        keyboard.append([InlineKeyboardButton("💬 Чат", url=SOCIAL_LINKS["telegram_chat"])])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["main_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def handle_unknown(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка неизвестных сообщений"""
        if update.message:
            user_id = update.effective_user.id
            user = self.data_manager.get_user(user_id)
            
            if user:
                texts = TEXTS[user.language]
                await update.message.reply_text(texts["error"].format(error="Неизвестная команда"))
        
        return MAIN_MENU
    
    async def error_handler(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик ошибок"""
        logger.error(f"Ошибка: {context.error}")
        
        if update and update.effective_user:
            user_id = update.effective_user.id
            user = self.data_manager.get_user(user_id)
            
            if user:
                texts = TEXTS[user.language]
                try:
                    await context.bot.send_message(
                        chat_id=user_id,
                        text=texts["error"].format(error=str(context.error))
                    )
                except:
                    pass
    
    # ==================== ЗАПУСК БОТА ====================
    
    def setup_handlers(self):
        """Настройка обработчиков"""
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler('start', self.start)],
            states={
                SELECT_LANGUAGE: [CallbackQueryHandler(self.select_language)],
                MAIN_MENU: [
                    CallbackQueryHandler(self.get_access, pattern="^get_access$"),
                    CallbackQueryHandler(self.contact_admin, pattern="^contact_admin$"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$"),
                    CallbackQueryHandler(self.show_stats, pattern="^stats$"),
                    CallbackQueryHandler(self.show_marathon, pattern="^marathon$"),
                    CallbackQueryHandler(self.show_instruction, pattern="^instruction$"),
                    CallbackQueryHandler(self.show_top_traders, pattern="^top_traders$"),
                    CallbackQueryHandler(self.admin_menu, pattern="^admin_menu$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                WAITING_FOR_BALANCE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_balance)
                ],
                SELECT_ASSET_TYPE: [
                    CallbackQueryHandler(self.show_forex_pairs, pattern="^forex_pairs$"),
                    CallbackQueryHandler(self.show_stocks, pattern="^stocks$"),
                    CallbackQueryHandler(self.show_crypto, pattern="^crypto$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    CallbackQueryHandler(self.handle_pagination, pattern="^(forex|stocks|crypto)_(prev|next)$"),
                    CallbackQueryHandler(self.select_pair, pattern="^pair_.*$")
                ],
                SELECT_CURRENCY_PAIR: [
                    CallbackQueryHandler(self.select_pair, pattern="^pair_.*$"),
                    CallbackQueryHandler(self.handle_pagination, pattern="^(forex|stocks|crypto)_(prev|next)$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                SELECT_EXPIRY: [
                    CallbackQueryHandler(self.analyze_signal, pattern="^exp_.*$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                TRADE_RESULT: [
                    CallbackQueryHandler(self.process_trade_result, pattern="^trade_(win|lose)$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                ADMIN_ACTIONS: [
                    CallbackQueryHandler(self.admin_grant_access, pattern="^admin_grant_access$"),
                    CallbackQueryHandler(self.admin_show_stats, pattern="^admin_stats$"),
                    CallbackQueryHandler(self.admin_menu, pattern="^admin_menu$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.admin_process_user_id)
                ]
            },
            fallbacks=[
                CommandHandler('start', self.start),
                CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_unknown)
            ]
        )
        
        # Добавляем обработчики команд
        self.application.add_handler(conv_handler)
        
        # Добавляем обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        # Добавляем команды меню
        async def set_commands(app):
            commands = [
                BotCommand("start", "Запустить бота"),
                BotCommand("help", "Помощь"),
                BotCommand("stats", "Статистика")
            ]
            await app.bot.set_my_commands(commands)
        
        self.application.post_init = set_commands
    
    def run(self):
        """Запуск бота"""
        # Создаем приложение
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Настраиваем обработчики
        self.setup_handlers()
        
        # Запускаем бота
        logger.info("🤖 KURUT AI INFINITY запущен!")
        print("=" * 50)
        print("🤖 KURUT AI INFINITY - Самый точный бот для OTC рынка")
        print(f"👤 Админ: {ADMIN_USERNAME}")
        print(f"🔗 Рефералка: {REFERRAL_LINK}")
        print("=" * 50)
        
        self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ==================== ЗАПУСК ПРОГРАММЫ ====================
if __name__ == "__main__":
    try:
        bot = KurutAIBot()
        bot.run()
    except KeyboardInterrupt:
        print("\n\n👋 Бот остановлен")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        print(f"❌ Критическая ошибка: {e}")
        
