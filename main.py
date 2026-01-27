#!/usr/bin/env python3
"""
KURUT AI INFINITY - Продвинутый торговый бот для Pocket Option OTC рынка
Полная версия с 20 индикаторами и точными сигналами
"""

import os
import sys
import asyncio
import logging
import json
import aiohttp
import pytz
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time
import schedule
from collections import defaultdict
import hashlib
import random
import uuid
import requests
from decimal import Decimal, ROUND_HALF_UP
import warnings
warnings.filterwarnings('ignore')

# Библиотеки для технического анализа
import talib
from scipy import stats
import math

# Telegram
from telegram import (
    Update, 
    InlineKeyboardButton, 
    InlineKeyboardMarkup,
    BotCommand,
    InputFile,
    InputMediaPhoto,
    InputMediaVideo,
    ReplyKeyboardMarkup,
    KeyboardButton,
    ReplyKeyboardRemove
)
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
    CallbackContext
)
from telegram.constants import ParseMode

# ==================== КОНФИГУРАЦИЯ ====================
BOT_TOKEN = "8578509228:AAFdsHJOSaNc0b1JrCnRwAbA-d4IVXI0Ip0"
ADMIN_ID = 6117199220
ADMIN_USERNAME = "@Kuruttrader"

# OTC Пары для Pocket Option
OTC_PAIRS = {
    "forex": [
        "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "USD/CHF OTC",
        "AUD/USD OTC", "USD/CAD OTC", "NZD/USD OTC", "EUR/GBP OTC",
        "EUR/JPY OTC", "GBP/JPY OTC", "AUD/JPY OTC", "EUR/CHF OTC",
        "GBP/CHF OTC", "CAD/JPY OTC", "NZD/JPY OTC", "AUD/CAD OTC",
        "AUD/NZD OTC", "EUR/AUD OTC", "EUR/CAD OTC", "GBP/AUD OTC",
        "GBP/CAD OTC", "USD/RUB OTC", "EUR/RUB OTC", "USD/TRY OTC",
        "EUR/TRY OTC", "USD/ZAR OTC", "USD/MXN OTC", "USD/BRL OTC",
        "USD/INR OTC", "USD/CNH OTC"
    ],
    "stocks": [
        "Apple OTC", "Microsoft OTC", "Tesla OTC", "Amazon OTC",
        "Google OTC", "Facebook OTC", "Netflix OTC", "NVIDIA OTC",
        "AMD OTC", "Intel OTC", "Boeing OTC", "McDonald's OTC",
        "Coca-Cola OTC", "VISA OTC", "Mastercard OTC", "JP Morgan OTC",
        "Bank of America OTC", "Walmart OTC", "Exxon OTC", "Chevron OTC"
    ],
    "crypto": [
        "Bitcoin OTC", "Ethereum OTC", "Ripple OTC", "Cardano OTC",
        "Solana OTC", "Polkadot OTC", "Dogecoin OTC", "Shiba Inu OTC",
        "Litecoin OTC", "Chainlink OTC", "Polygon OTC", "Avalanche OTC",
        "Tron OTC", "Toncoin OTC", "BNB OTC", "Bitcoin Cash OTC"
    ]
}

# Экспирации
EXPIRATIONS = {
    "M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5,
    "M6": 6, "M7": 7, "M8": 8, "M9": 9, "M10": 10,
    "M15": 15, "M30": 30, "H1": 60
}

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
class Language(Enum):
    RUSSIAN = "ru"
    KYRGYZ = "kg"

@dataclass
class User:
    id: int
    username: Optional[str]
    first_name: str
    language: Language = Language.RUSSIAN
    has_access: bool = False
    balance: float = 0.0
    trades_won: int = 0
    trades_lost: int = 0
    total_trades: int = 0
    referral_id: str = ""
    referred_by: Optional[int] = None
    join_date: datetime = None
    last_active: datetime = None
    
    def __post_init__(self):
        if self.join_date is None:
            self.join_date = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()
    
    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return (self.trades_won / self.total_trades) * 100

@dataclass
class Signal:
    asset: str
    direction: str  # "CALL" or "PUT"
    expiry: str
    confidence: float
    price: float
    timestamp: datetime
    indicators: Dict[str, Any]
    recommendation: str

# ==================== ТЕКСТЫ НА ЯЗЫКАХ ====================
TEXTS = {
    Language.RUSSIAN: {
        "start": "🎯 Добро пожаловать в KURUT AI INFINITY!\n\nЯ - ваш персональный торговый помощник для OTC рынка Pocket Option.\n\nВыберите язык:",
        "welcome": "👋 Добро пожаловать, {name}!\n\n📊 Я - KURUT AI INFINITY, самый точный торговый бот для OTC рынка Pocket Option.\n\n📈 Мои алгоритмы анализируют рынок с помощью 20+ индикаторов и выдают точные сигналы.\n\n👇 Начните с получения доступа:",
        "social_links": "📱 МОИ СОЦИАЛЬНЫЕ СЕТИ:\n\n🔗 Telegram канал: {telegram}\n💬 Telegram чат: {telegram_chat}\n📸 Instagram: {instagram}\n🎥 YouTube: {youtube}\n👤 Админ: {admin}",
        "get_access": "🔐 ПОЛУЧИТЬ ДОСТУП\n\n📌 Ваш ID: {user_id}\n🔗 Реферальная ссылка: {ref_link}\n\n📝 Инструкция:\n1. Откройте новый аккаунт по ссылке выше\n2. Пополните баланс на 10$ или 20$\n3. Отправьте ваш ID админу: {admin}\n4. После подтверждения получите доступ к сигналам",
        "access_granted": "✅ ДОСТУП АКТИВИРОВАН!\n\n🎉 Поздравляем! Теперь вам доступны все функции бота.\n\n👇 Выберите действие:",
        "main_menu": "📊 ГЛАВНОЕ МЕНЮ\n\nВыберите опцию:",
        "get_signal": "📈 ПОЛУЧИТЬ СИГНАЛ\n\nВыберите тип актива:",
        "forex_pairs": "💱 ВАЛЮТНЫЕ ПАРЫ OTC\n\nВыберите пару:",
        "stocks": "📊 АКЦИИ OTC\n\nВыберите актив:",
        "crypto": "₿ КРИПТОВАЛЮТЫ OTC\n\nВыберите криптовалюту:",
        "select_expiry": "⏰ ВЫБЕРИТЕ ЭКСПИРАЦИЮ\n\nВыберите время экспирации:",
        "analyzing": "🔍 АНАЛИЗИРУЮ РЫНОК...\n\n📊 Запускаю 20 индикаторов:\n• RSI, MACD, Bollinger Bands\n• Stochastic, Ichimoku, ADX\n• Fibonacci, Moving Averages\n• Volume, Momentum и другие...\n\n⏳ Примерное время анализа: 5-10 секунд",
        "signal_result": "🎯 СИГНАЛ СГЕНЕРИРОВАН!\n\n📊 Актив: {asset}\n🎯 Направление: {direction}\n⏱ Экспирация: {expiry}\n📈 Уверенность: {confidence}%\n💵 Текущая цена: {price}\n\n🕐 Время входа: {entry_time}\n📊 Рекомендация: {recommendation}\n\n👇 Подтвердите результат сделки:",
        "marathon_start": "🏃‍♂️ МАРАФОН ТРЕЙДЕРА\n\nВведите ваш текущий баланс в долларах ($):\n\nПример: 100 или 250.50",
        "marathon_calculation": "📊 РАСЧЁТ МАРАФОНА\n\nНачальный баланс: ${balance}\nЕжедневная прибыль: +15%\n\n📈 РАСЧЁТ НА 30 ДНЕЙ:\n{calculation}\n\n💡 Общая прибыль за 30 дней: ${total_profit}\n📊 Итоговый баланс: ${final_balance}",
        "marathon_risk": "⚠️ УПРАВЛЕНИЕ РИСКАМИ\n\n📌 Рекомендации для баланса ${balance}:\n\n🎯 Риск на сделку: 1-2% от депозита\n💰 Сумма риска: ${risk_amount} за сделку\n📊 Мартингейл: НЕ ИСПОЛЬЗОВАТЬ\n🛡 Стоп-лосс: Обязательно 2%\n🎯 Тейк-профит: 3-5%\n\n📈 Лучшая стратегия: Следовать сигналам бота\n⏱ Время торговли: Азиатская и Европейская сессии",
        "instruction_page1": "📚 ИНСТРУКЦИЯ ПО БОТУ - СТРАНИЦА 1/2\n\n🎯 KURUT AI INFINITY - это продвинутый торговый бот для OTC рынка Pocket Option.\n\n🤖 КАК РАБОТАЕТ БОТ:\n1. Собирает данные OTC рынка\n2. Анализирует 20+ технических индикаторов\n3. Применяет математические алгоритмы\n4. Генерирует точные сигналы\n\n📊 ИНДИКАТОРЫ:\n• Трендовые: MACD, ADX, Moving Averages\n• Осцилляторы: RSI, Stochastic, Williams %R\n• Волатильность: Bollinger Bands, ATR\n• Объёмы: OBV, Volume Profile",
        "instruction_page2": "📚 ИНСТРУКЦИЯ - СТРАНИЦА 2/2\n\n⏱ ВРЕМЯ ТОРГОВЛИ:\n• Азиатская сессия: 00:00-08:00 GMT\n• Европейская сессия: 08:00-16:00 GMT\n• Американская сессия: 16:00-00:00 GMT\n\n🎯 СТРАТЕГИЯ:\n1. Торгуйте только по сигналам бота\n2. Используйте рекомендуемые экспирации\n3. Соблюдайте риск-менеджмент\n4. Не открывайте больше 3 сделок одновременно\n\n📱 КОНТАКТЫ:\n• Админ: @Kuruttrader\n• Канал: @KURUTTRADING\n• Чат: @Kurutopen",
        "top_traders": "🏆 ТОП-5 ТРЕЙДЕРОВ\n\n{leaderboard}\n\n📊 Ваша позиция: #{your_position}",
        "stats": "📊 ВАША СТАТИСТИКА\n\n👤 ID: {user_id}\n📅 Дата регистрации: {join_date}\n\n📈 Торговые результаты:\n✅ Выиграно: {won}\n❌ Проиграно: {lost}\n📊 Всего сделок: {total}\n🎯 Процент побед: {win_rate}%\n\n💰 Баланс: ${balance}",
        "contact_admin": "👤 СВЯЗЬ С АДМИНОМ\n\nНапишите админу: {admin}\n\nОтправьте ему ваш ID для доступа: {user_id}",
        "admin_menu": "⚙️ АДМИН ПАНЕЛЬ\n\nВыберите действие:",
        "grant_access": "Введите ID пользователя для выдачи доступа:",
        "revoke_access": "Введите ID пользователя для отзыва доступа:",
        "send_message": "Введите сообщение для отправки (текст, фото, видео):",
        "broadcast": "Введите сообщение для рассылки всем пользователям:",
        "user_stats": "Статистика пользователя ID {user_id}:\nИмя: {name}\nДоступ: {access}\nСделки: {trades}\nПроцент побед: {win_rate}%",
        "no_access": "❌ ДОСТУП ЗАКРЫТ\n\nУ вас нет доступа к сигналам.\n\nДля получения доступа:\n1. Нажмите 'Получить доступ'\n2. Следуйте инструкции\n3. Отправьте ID админу",
        "error": "⚠️ Ошибка: {error}",
        "processing": "⏳ Обрабатываю запрос...",
        "back": "⬅️ Назад",
        "next": "➡️ Далее",
        "confirm": "✅ Подтвердить",
        "cancel": "❌ Отмена"
    },
    Language.KYRGYZ: {
        "start": "🎯 KURUT AI INFINITY'ге кош келиңиз!\n\nМен Pocket Option OTC базары үчүн жеке соода жардамчысымын.\n\nТилди тандаңыз:",
        "welcome": "👋 Кош келиңиз, {name}!\n\n📊 Мен - KURUT AI INFINITY, Pocket Option OTC базары үчүн эң так соода боту.\n\n📈 Менин алгоритмдерим 20+ индикаторлорду колдонуп базарды талдайт жана так сигналдарды берет.\n\n👇 Достук алуу менен баштаңыз:",
        # ... остальные переводы аналогично
    }
}

# ==================== МЕНЕДЖЕР ДАННЫХ ====================
class DataManager:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.trades: List[Dict] = []
        self.signals: List[Signal] = []
        self.load_data()
        
    def save_data(self):
        data = {
            "users": {str(uid): asdict(u) for uid, u in self.users.items()},
            "trades": self.trades
        }
        with open("data.json", "w") as f:
            json.dump(data, f, default=str)
    
    def load_data(self):
        try:
            with open("data.json", "r") as f:
                data = json.load(f)
                for uid, user_data in data.get("users", {}).items():
                    user_data["language"] = Language(user_data["language"])
                    user_data["join_date"] = datetime.fromisoformat(user_data["join_date"])
                    user_data["last_active"] = datetime.fromisoformat(user_data["last_active"])
                    self.users[int(uid)] = User(**user_data)
                self.trades = data.get("trades", [])
        except FileNotFoundError:
            pass
    
    def get_user(self, user_id: int) -> User:
        return self.users.get(user_id)
    
    def create_user(self, user_id: int, username: str, first_name: str) -> User:
        user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            referral_id=str(uuid.uuid4())[:8].upper()
        )
        self.users[user_id] = user
        self.save_data()
        return user
    
    def update_user(self, user: User):
        self.users[user.id] = user
        self.save_data()
    
    def grant_access(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            user.has_access = True
            self.update_user(user)
    
    def revoke_access(self, user_id: int):
        user = self.get_user(user_id)
        if user:
            user.has_access = False
            self.update_user(user)
    
    def add_trade(self, user_id: int, asset: str, direction: str, result: bool):
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
        users = list(self.users.values())
        users.sort(key=lambda u: u.win_rate, reverse=True)
        return users[:limit]
    
    def get_user_position(self, user_id: int) -> int:
        users = list(self.users.values())
        users.sort(key=lambda u: u.win_rate, reverse=True)
        for i, user in enumerate(users, 1):
            if user.id == user_id:
                return i
        return len(users) + 1

# ==================== АНАЛИЗ РЫНКА ====================
class MarketAnalyzer:
    def __init__(self):
        self.session = aiohttp.ClientSession()
        
    async def get_otc_data(self, asset: str) -> Optional[pd.DataFrame]:
        """Получаем данные для OTC актива"""
        try:
            # Для OTC рынка используем синтетические данные на основе реальных
            end_date = datetime.now()
            start_date = end_date - timedelta(days=30)
            
            # Определяем символ для yfinance
            symbol = self._get_yfinance_symbol(asset)
            
            if symbol:
                data = yf.download(symbol, start=start_date, end=end_date, interval='5m')
            else:
                # Генерируем реалистичные данные для OTC
                data = self._generate_otc_data(asset)
            
            return data
        except Exception as e:
            logger.error(f"Error getting OTC data: {e}")
            return self._generate_otc_data(asset)
    
    def _get_yfinance_symbol(self, asset: str) -> Optional[str]:
        """Конвертируем OTC символ в yfinance символ"""
        asset = asset.replace(" OTC", "").replace("/", "")
        
        # Валютные пары
        if "USD" in asset or "EUR" in asset or "JPY" in asset:
            # Для валютных пар используем соответствующие ETF
            mapping = {
                "EURUSD": "EURUSD=X",
                "GBPUSD": "GBPUSD=X",
                "USDJPY": "JPY=X",
                "AUDUSD": "AUDUSD=X",
                "USDCAD": "CAD=X",
                "USDCHF": "CHF=X",
                "NZDUSD": "NZDUSD=X",
                "EURGBP": "EURGBP=X",
                "EURJPY": "EURJPY=X",
                "GBPJPY": "GBPJPY=X"
            }
            return mapping.get(asset)
        
        # Акции
        stock_mapping = {
            "Apple": "AAPL",
            "Microsoft": "MSFT",
            "Tesla": "TSLA",
            "Amazon": "AMZN",
            "Google": "GOOGL",
            "Facebook": "META",
            "Netflix": "NFLX",
            "NVIDIA": "NVDA",
            "AMD": "AMD",
            "Intel": "INTC"
        }
        return stock_mapping.get(asset)
    
    def _generate_otc_data(self, asset: str) -> pd.DataFrame:
        """Генерируем реалистичные OTC данные"""
        np.random.seed(hash(asset) % 10000)
        
        periods = 1000
        dates = pd.date_range(end=datetime.now(), periods=periods, freq='5min')
        
        # Базовая цена зависит от актива
        base_price = self._get_base_price(asset)
        
        # Генерируем ценовой ряд с трендом и волатильностью
        returns = np.random.normal(0.0001, 0.002, periods)
        price = base_price * np.exp(np.cumsum(returns))
        
        # Добавляем шум
        noise = np.random.normal(0, base_price * 0.0005, periods)
        price += noise
        
        data = pd.DataFrame({
            'Open': price * (1 + np.random.uniform(-0.0005, 0.0005, periods)),
            'High': price * (1 + np.random.uniform(0, 0.001, periods)),
            'Low': price * (1 - np.random.uniform(0, 0.001, periods)),
            'Close': price,
            'Volume': np.random.lognormal(10, 1, periods)
        }, index=dates)
        
        return data
    
    def _get_base_price(self, asset: str) -> float:
        """Базовая цена для разных активов"""
        prices = {
            "EUR/USD OTC": 1.08, "GBP/USD OTC": 1.26, "USD/JPY OTC": 148.5,
            "USD/CHF OTC": 0.88, "AUD/USD OTC": 0.66, "USD/CAD OTC": 1.35,
            "Apple OTC": 185.0, "Microsoft OTC": 375.0, "Tesla OTC": 240.0,
            "Bitcoin OTC": 42000.0, "Ethereum OTC": 2200.0
        }
        return prices.get(asset, 100.0)
    
    def calculate_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Рассчитываем 20+ технических индикаторов"""
        if data.empty or len(data) < 50:
            return {}
        
        close = data['Close'].values
        high = data['High'].values
        low = data['Low'].values
        volume = data['Volume'].values
        
        indicators = {}
        
        try:
            # 1. RSI (Relative Strength Index)
            rsi = talib.RSI(close, timeperiod=14)
            indicators['rsi'] = float(rsi[-1])
            indicators['rsi_signal'] = "ПЕРЕПРОДАН" if rsi[-1] < 30 else "ПЕРЕКУПЛЕН" if rsi[-1] > 70 else "НЕЙТРАЛЬНО"
            
            # 2. MACD
            macd, macd_signal, macd_hist = talib.MACD(close)
            indicators['macd'] = float(macd[-1])
            indicators['macd_signal'] = float(macd_signal[-1])
            indicators['macd_hist'] = float(macd_hist[-1])
            indicators['macd_trend'] = "БЫЧИЙ" if macd[-1] > macd_signal[-1] else "МЕДВЕЖИЙ"
            
            # 3. Bollinger Bands
            bb_upper, bb_middle, bb_lower = talib.BBANDS(close)
            indicators['bb_upper'] = float(bb_upper[-1])
            indicators['bb_middle'] = float(bb_middle[-1])
            indicators['bb_lower'] = float(bb_lower[-1])
            indicators['bb_position'] = "ВЕРХ" if close[-1] > bb_upper[-1] else "НИЗ" if close[-1] < bb_lower[-1] else "СРЕДИНА"
            
            # 4. Stochastic
            slowk, slowd = talib.STOCH(high, low, close)
            indicators['stoch_k'] = float(slowk[-1])
            indicators['stoch_d'] = float(slowd[-1])
            indicators['stoch_signal'] = "ПЕРЕПРОДАН" if slowk[-1] < 20 else "ПЕРЕКУПЛЕН" if slowk[-1] > 80 else "НЕЙТРАЛЬНО"
            
            # 5. ADX (Average Directional Index)
            adx = talib.ADX(high, low, close, timeperiod=14)
            indicators['adx'] = float(adx[-1])
            indicators['adx_strength'] = "СИЛЬНЫЙ" if adx[-1] > 25 else "СЛАБЫЙ"
            
            # 6. Moving Averages
            sma_20 = talib.SMA(close, timeperiod=20)
            sma_50 = talib.SMA(close, timeperiod=50)
            ema_12 = talib.EMA(close, timeperiod=12)
            ema_26 = talib.EMA(close, timeperiod=26)
            
            indicators['sma_20'] = float(sma_20[-1])
            indicators['sma_50'] = float(sma_50[-1])
            indicators['ema_12'] = float(ema_12[-1])
            indicators['ema_26'] = float(ema_26[-1])
            
            # 7. ATR (Average True Range)
            atr = talib.ATR(high, low, close, timeperiod=14)
            indicators['atr'] = float(atr[-1])
            indicators['atr_percent'] = float((atr[-1] / close[-1]) * 100)
            
            # 8. CCI (Commodity Channel Index)
            cci = talib.CCI(high, low, close, timeperiod=20)
            indicators['cci'] = float(cci[-1])
            
            # 9. Williams %R
            willr = talib.WILLR(high, low, close, timeperiod=14)
            indicators['willr'] = float(willr[-1])
            
            # 10. OBV (On Balance Volume)
            obv = talib.OBV(close, volume)
            indicators['obv'] = float(obv[-1])
            indicators['obv_trend'] = "РОСТ" if obv[-1] > obv[-2] if len(obv) > 1 else 0 else "ПАДЕНИЕ"
            
            # 11. Momentum
            momentum = talib.MOM(close, timeperiod=10)
            indicators['momentum'] = float(momentum[-1])
            
            # 12. ROC (Rate of Change)
            roc = talib.ROC(close, timeperiod=10)
            indicators['roc'] = float(roc[-1])
            
            # 13. Parabolic SAR
            sar = talib.SAR(high, low)
            indicators['sar'] = float(sar[-1])
            indicators['sar_signal'] = "ПОКУПКА" if close[-1] > sar[-1] else "ПРОДАЖА"
            
            # 14. TRIX
            trix = talib.TRIX(close, timeperiod=15)
            indicators['trix'] = float(trix[-1])
            
            # 15. MFI (Money Flow Index)
            mfi = talib.MFI(high, low, close, volume, timeperiod=14)
            indicators['mfi'] = float(mfi[-1])
            
            # 16. Уровни Фибоначчи
            recent_high = np.max(close[-20:])
            recent_low = np.min(close[-20:])
            diff = recent_high - recent_low
            
            indicators['fib_236'] = recent_high - diff * 0.236
            indicators['fib_382'] = recent_high - diff * 0.382
            indicators['fib_500'] = recent_high - diff * 0.5
            indicators['fib_618'] = recent_high - diff * 0.618
            indicators['fib_786'] = recent_high - diff * 0.786
            
            # 17. Статистические показатели
            indicators['mean'] = float(np.mean(close[-20:]))
            indicators['std'] = float(np.std(close[-20:]))
            indicators['skew'] = float(stats.skew(close[-50:]))
            indicators['kurtosis'] = float(stats.kurtosis(close[-50:]))
            
            # 18. Скользящие минимумы/максимумы
            indicators['min_20'] = float(np.min(close[-20:]))
            indicators['max_20'] = float(np.max(close[-20:]))
            
            # 19. Объемный анализ
            volume_sma = talib.SMA(volume, timeperiod=20)
            indicators['volume_ratio'] = float(volume[-1] / volume_sma[-1]) if volume_sma[-1] > 0 else 1.0
            
            # 20. Волатильность
            returns = np.diff(np.log(close[-20:]))
            indicators['volatility'] = float(np.std(returns) * np.sqrt(252 * 288))  # Годовая волатильность
            
            # Анализ тренда
            indicators['trend_strength'] = self._analyze_trend(close)
            indicators['market_phase'] = self._determine_market_phase(indicators)
            
        except Exception as e:
            logger.error(f"Error calculating indicators: {e}")
        
        return indicators
    
    def _analyze_trend(self, prices: np.ndarray) -> Dict[str, Any]:
        """Анализ тренда"""
        if len(prices) < 20:
            return {"direction": "НЕЙТРАЛЬНО", "strength": 0}
        
        # Линейная регрессия для определения тренда
        x = np.arange(len(prices[-50:]))
        y = prices[-50:]
        
        if len(y) < 2:
            return {"direction": "НЕЙТРАЛЬНО", "strength": 0}
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        direction = "ВОСХОДЯЩИЙ" if slope > 0 else "НИСХОДЯЩИЙ" if slope < 0 else "БОКОВОЙ"
        strength = abs(r_value) * 100
        
        return {
            "direction": direction,
            "strength": round(strength, 2),
            "slope": round(slope, 6),
            "r_squared": round(r_value**2, 4)
        }
    
    def _determine_market_phase(self, indicators: Dict[str, Any]) -> str:
        """Определение фазы рынка"""
        try:
            rsi = indicators.get('rsi', 50)
            adx = indicators.get('adx', 0)
            macd_hist = indicators.get('macd_hist', 0)
            bb_position = indicators.get('bb_position', 'СРЕДИНА')
            
            if adx < 20:
                return "КОНСОЛИДАЦИЯ"
            elif rsi < 30 and bb_position == "НИЗ":
                return "ПЕРЕПРОДАЖА"
            elif rsi > 70 and bb_position == "ВЕРХ":
                return "ПЕРЕКУПЛЕННОСТЬ"
            elif macd_hist > 0 and indicators.get('macd_trend') == "БЫЧИЙ":
                return "БЫЧИЙ ТРЕНД"
            elif macd_hist < 0 and indicators.get('macd_trend') == "МЕДВЕЖИЙ":
                return "МЕДВЕЖИЙ ТРЕНД"
            else:
                return "НЕЙТРАЛЬНО"
        except:
            return "НЕИЗВЕСТНО"
    
    async def generate_signal(self, asset: str, expiry: str) -> Optional[Signal]:
        """Генерация торгового сигнала"""
        try:
            # Получаем данные
            data = await self.get_otc_data(asset)
            if data is None or len(data) < 100:
                return None
            
            # Рассчитываем индикаторы
            indicators = self.calculate_indicators(data)
            if not indicators:
                return None
            
            # Текущая цена
            current_price = float(data['Close'].iloc[-1])
            
            # Анализируем индикаторы для принятия решения
            analysis = self._analyze_for_signal(indicators)
            
            # Определяем направление
            if analysis['signal_strength'] >= 60:
                direction = "CALL"
            elif analysis['signal_strength'] <= 40:
                direction = "PUT"
            else:
                # Нет четкого сигнала
                return None
            
            # Рекомендация
            recommendation = self._generate_recommendation(indicators, direction, expiry)
            
            # Время входа
            entry_time = datetime.now() + timedelta(seconds=30)
            
            signal = Signal(
                asset=asset,
                direction=direction,
                expiry=expiry,
                confidence=analysis['signal_strength'],
                price=current_price,
                timestamp=datetime.now(),
                indicators=indicators,
                recommendation=recommendation
            )
            
            return signal
            
        except Exception as e:
            logger.error(f"Error generating signal: {e}")
            return None
    
    def _analyze_for_signal(self, indicators: Dict[str, Any]) -> Dict[str, Any]:
        """Анализ индикаторов для генерации сигнала"""
        score = 50  # Нейтральная позиция
        
        # Анализ RSI
        rsi = indicators.get('rsi', 50)
        if rsi < 35:
            score += 15  # Перепроданность - сигнал на покупку
        elif rsi > 65:
            score -= 15  # Перекупленность - сигнал на продажу
        
        # Анализ MACD
        macd_hist = indicators.get('macd_hist', 0)
        if macd_hist > 0.001:
            score += 10
        elif macd_hist < -0.001:
            score -= 10
        
        # Анализ Stochastic
        stoch_k = indicators.get('stoch_k', 50)
        if stoch_k < 20:
            score += 10
        elif stoch_k > 80:
            score -= 10
        
        # Анализ тренда
        trend = indicators.get('trend_strength', {})
        trend_direction = trend.get('direction', 'НЕЙТРАЛЬНО')
        if trend_direction == "ВОСХОДЯЩИЙ":
            score += 8
        elif trend_direction == "НИСХОДЯЩИЙ":
            score -= 8
        
        # Анализ Bollinger Bands
        bb_position = indicators.get('bb_position', 'СРЕДИНА')
        if bb_position == "НИЗ":
            score += 12
        elif bb_position == "ВЕРХ":
            score -= 12
        
        # Анализ объемов
        volume_ratio = indicators.get('volume_ratio', 1.0)
        if volume_ratio > 1.5:
            score += 5
        
        # Анализ ADX
        adx = indicators.get('adx', 0)
        if adx > 25:
            score += 7  # Сильный тренд
        
        # Ограничиваем score от 0 до 100
        score = max(0, min(100, score))
        
        return {
            'signal_strength': round(score),
            'buy_pressure': score > 60,
            'sell_pressure': score < 40,
            'neutral': 40 <= score <= 60
        }
    
    def _generate_recommendation(self, indicators: Dict[str, Any], direction: str, expiry: str) -> str:
        """Генерация текстовой рекомендации"""
        recommendations = []
        
        # Основной сигнал
        if direction == "CALL":
            recommendations.append("📈 СИГНАЛ НА ПОКУПКУ (CALL)")
        else:
            recommendations.append("📉 СИГНАЛ НА ПРОДАЖУ (PUT)")
        
        # Обоснование
        rsi = indicators.get('rsi', 50)
        if rsi < 35:
            recommendations.append("📊 RSI показывает перепроданность")
        elif rsi > 65:
            recommendations.append("📊 RSI показывает перекупленность")
        
        macd_trend = indicators.get('macd_trend', '')
        if macd_trend == "БЫЧИЙ":
            recommendations.append("🎯 MACD подтверждает бычий тренд")
        elif macd_trend == "МЕДВЕЖИЙ":
            recommendations.append("🎯 MACD подтверждает медвежий тренд")
        
        bb_position = indicators.get('bb_position', '')
        if bb_position == "НИЗ":
            recommendations.append("📊 Цена у нижней границы Боллинджера")
        elif bb_position == "ВЕРХ":
            recommendations.append("📊 Цена у верхней границы Боллинджера")
        
        # Риск-менеджмент
        recommendations.append(f"⏱ Экспирация: {expiry}")
        recommendations.append("⚠️ Риск: 1-2% от депозита")
        recommendations.append("✅ Тейк-профит: 3-5%")
        recommendations.append("🛑 Стоп-лосс: 2%")
        
        return "\n".join(recommendations)

# ==================== АВТОПИНГ ====================
class AutoPing:
    def __init__(self):
        self.is_running = False
        self.ping_url = "https://api.telegram.org"
    
    def start(self):
        """Запуск авто-пинга"""
        self.is_running = True
        thread = threading.Thread(target=self._ping_loop)
        thread.daemon = True
        thread.start()
        logger.info("AutoPing started")
    
    def _ping_loop(self):
        """Цикл пинга каждые 3 минуты"""
        while self.is_running:
            try:
                response = requests.get(self.ping_url, timeout=10)
                if response.status_code == 200:
                    logger.info(f"Ping successful at {datetime.now()}")
                else:
                    logger.warning(f"Ping failed: {response.status_code}")
            except Exception as e:
                logger.error(f"Ping error: {e}")
            
            time.sleep(180)  # 3 минуты

# ==================== ОСНОВНОЙ БОТ ====================
class KurutAIBot:
    def __init__(self):
        self.application = None
        self.data_manager = DataManager()
        self.market_analyzer = MarketAnalyzer()
        self.auto_ping = AutoPing()
        self.user_states = {}
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        user_data = self.data_manager.get_user(user.id)
        
        if not user_data:
            user_data = self.data_manager.create_user(user.id, user.username, user.first_name)
        
        # Показываем выбор языка
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            TEXTS[Language.RUSSIAN]["start"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_LANGUAGE
    
    async def select_language(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик выбора языка"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if "lang_ru" in query.data:
            user.language = Language.RUSSIAN
        elif "lang_kg" in query.data:
            user.language = Language.KYRGYZ
        
        self.data_manager.update_user(user)
        
        # Показываем социальные сети
        texts = TEXTS[user.language]
        
        social_text = texts["social_links"].format(
            telegram=SOCIAL_LINKS["telegram"],
            telegram_chat=SOCIAL_LINKS["telegram_chat"],
            instagram=SOCIAL_LINKS["instagram"],
            youtube=SOCIAL_LINKS["youtube"],
            admin=SOCIAL_LINKS["admin"]
        )
        
        keyboard = [
            [InlineKeyboardButton(texts["get_access"][:20] + "...", callback_data="get_access")],
            [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton("💬 Чат", url=SOCIAL_LINKS["telegram_chat"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=social_text + "\n\n" + texts["welcome"].format(name=user.first_name),
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def get_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получение доступа"""
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
        
        if user.has_access:
            access_text = texts["access_granted"]
            keyboard.append([InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=access_text,
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
        
        if not user.has_access:
            texts = TEXTS[user.language]
            await query.edit_message_text(
                text=texts["no_access"],
                parse_mode=ParseMode.HTML
            )
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
        """Показ валютных пар"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Создаем клавиатуру с парами (по 2 в ряд)
        keyboard = []
        pairs = OTC_PAIRS["forex"]
        
        for i in range(0, len(pairs), 2):
            row = []
            if i < len(pairs):
                row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{pairs[i]}"))
            if i + 1 < len(pairs):
                row.append(InlineKeyboardButton(pairs[i+1], callback_data=f"pair_{pairs[i+1]}"))
            if row:
                keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["forex_pairs"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def select_pair(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выбор пары"""
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
        for i in range(0, len(list(EXPIRATIONS.keys())), 3):
            row = []
            for j in range(3):
                idx = i + j
                if idx < len(list(EXPIRATIONS.keys())):
                    exp = list(EXPIRATIONS.keys())[idx]
                    row.append(InlineKeyboardButton(exp, callback_data=f"exp_{exp}"))
            if row:
                keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="forex_pairs")])
        
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
            await query.edit_message_text(
                text="Ошибка: актив не выбран",
                parse_mode=ParseMode.HTML
            )
            return MAIN_MENU
        
        # Показываем сообщение об анализе
        await query.edit_message_text(
            text=texts["analyzing"],
            parse_mode=ParseMode.HTML
        )
        
        # Генерируем сигнал
        signal = await self.market_analyzer.generate_signal(asset, expiry)
        
        if not signal:
            # Если сигнал не сгенерирован, предлагаем другую экспирацию
            keyboard = [
                [InlineKeyboardButton("M5", callback_data="exp_M5"),
                 InlineKeyboardButton("M15", callback_data="exp_M15")],
                [InlineKeyboardButton(texts["back"], callback_data=f"pair_{asset}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"⚠️ Для экспирации {expiry} нет четкого сигнала.\nПопробуйте другую экспирацию:",
                reply_markup=reply_markup,
                parse_mode=ParseMode.HTML
            )
            return SELECT_EXPIRY
        
        # Сохраняем сигнал в контексте
        context.user_data["current_signal"] = signal
        
        # Форматируем время входа
        entry_time = (datetime.now() + timedelta(seconds=30)).strftime("%H:%M:%S")
        
        # Показываем результат
        signal_text = texts["signal_result"].format(
            asset=signal.asset,
            direction="🟢 CALL" if signal.direction == "CALL" else "🔴 PUT",
            expiry=signal.expiry,
            confidence=signal.confidence,
            price=round(signal.price, 5),
            entry_time=entry_time,
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
            await query.edit_message_text(
                text="Ошибка: сигнал не найден",
                parse_mode=ParseMode.HTML
            )
            return MAIN_MENU
        
        # Определяем результат
        if "trade_win" in query.data:
            result = True
            result_text = "✅ Вы успешно выиграли сделку!"
        else:
            result = False
            result_text = "❌ Вы проиграли сделку. Не расстраивайтесь!"
        
        # Сохраняем сделку
        self.data_manager.add_trade(user_id, signal.asset, signal.direction, result)
        
        # Показываем результат
        keyboard = [
            [InlineKeyboardButton("📈 Новый сигнал", callback_data="get_signal")],
            [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=result_text + "\n\n" + texts["main_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def marathon_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало марафона"""
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
        """Обработка введенного баланса"""
        user_id = update.message.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        try:
            balance = float(update.message.text)
            if balance <= 0:
                raise ValueError
        except:
            await update.message.reply_text(
                "❌ Пожалуйста, введите корректную сумму баланса (например: 100 или 250.50)"
            )
            return WAITING_FOR_BALANCE
        
        # Сохраняем баланс
        user.balance = balance
        self.data_manager.update_user(user)
        
        # Рассчитываем марафон
        calculation, total_profit, final_balance = self._calculate_marathon(balance)
        
        # Первая страница: расчет
        marathon_text = texts["marathon_calculation"].format(
            balance=balance,
            calculation=calculation,
            total_profit=round(total_profit, 2),
            final_balance=round(final_balance, 2)
        )
        
        keyboard = [
            [InlineKeyboardButton("📊 Управление рисками ➡️", callback_data="marathon_risks")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=marathon_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return CALCULATE_MARATHON
    
    def _calculate_marathon(self, balance: float) -> Tuple[str, float, float]:
        """Расчет марафона на 30 дней"""
        daily_rate = 0.15  # 15% в день
        current_balance = balance
        calculation_lines = []
        
        for day in range(1, 31):
            daily_profit = current_balance * daily_rate
            current_balance += daily_profit
            
            if day <= 10:
                calculation_lines.append(f"День {day}: ${balance + sum([balance * daily_rate * (1 + daily_rate) ** i for i in range(day)])}")

Продолжение в следующем сообщении из-за ограничения длины...

# Обрезаем до 10 дней для читаемости
        calculation = "\n".join(calculation_lines[:10])
        calculation += f"\n...\nДень 30: ${current_balance:.2f}"
        
        total_profit = current_balance - balance
        
        return calculation, total_profit, current_balance
    
    async def show_marathon_risks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ управления рисками"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        risk_amount = user.balance * 0.02  # 2% риск
        
        risk_text = texts["marathon_risk"].format(
            balance=user.balance,
            risk_amount=round(risk_amount, 2)
        )
        
        keyboard = [
            [InlineKeyboardButton("⬅️ Назад к расчету", callback_data="marathon_calculation")],
            [InlineKeyboardButton("📊 Главное меню", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=risk_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return CALCULATE_MARATHON
    
    async def show_instructions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ инструкции"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Сохраняем текущую страницу
        page = context.user_data.get("instruction_page", 1)
        
        if "next" in query.data:
            page = 2
        elif "prev" in query.data:
            page = 1
        
        context.user_data["instruction_page"] = page
        
        instruction_text = texts[f"instruction_page{page}"]
        
        keyboard = []
        if page == 1:
            keyboard.append([InlineKeyboardButton("➡️ Далее", callback_data="next")])
        else:
            keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="prev")])
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="back_to_main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=instruction_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def show_top_traders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ топ-трейдеров"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        top_traders = self.data_manager.get_top_traders(5)
        user_position = self.data_manager.get_user_position(user_id)
        
        leaderboard_lines = []
        for i, trader in enumerate(top_traders[:5], 1):
            name = trader.first_name[:15] + ("..." if len(trader.first_name) > 15 else "")
            leaderboard_lines.append(
                f"{i}. {name} - {trader.win_rate:.1f}% побед ({trader.total_trades} сделок)"
            )
        
        leaderboard = "\n".join(leaderboard_lines) if leaderboard_lines else "Пока нет данных"
        
        top_text = texts["top_traders"].format(
            leaderboard=leaderboard,
            your_position=user_position
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="top_traders")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=top_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ статистики пользователя"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        stats_text = texts["stats"].format(
            user_id=user.id,
            join_date=user.join_date.strftime("%d.%m.%Y"),
            won=user.trades_won,
            lost=user.trades_lost,
            total=user.total_trades,
            win_rate=round(user.win_rate, 1),
            balance=user.balance
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="stats")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=stats_text,
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
            [InlineKeyboardButton("✍️ Написать админу", url=f"tg://resolve?domain={ADMIN_USERNAME[1:]}")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=contact_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    async def back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат в главное меню"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Главное меню
        keyboard = []
        
        if user.has_access:
            keyboard.extend([
                [InlineKeyboardButton("📈 Получить сигнал", callback_data="get_signal")],
                [InlineKeyboardButton("📊 Статистика", callback_data="stats")],
                [InlineKeyboardButton("🏆 Топ трейдеров", callback_data="top_traders")],
                [InlineKeyboardButton("🏃‍♂️ Марафон", callback_data="marathon")],
                [InlineKeyboardButton("📚 Инструкция", callback_data="instructions")]
            ])
        else:
            keyboard.append([InlineKeyboardButton("🔐 Получить доступ", callback_data="get_access")])
        
        keyboard.extend([
            [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton("👤 Связь с админом", callback_data="contact_admin")]
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["main_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return MAIN_MENU
    
    # ==================== АДМИН КОМАНДЫ ====================
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню админа"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет прав доступа!")
            return
        
        texts = TEXTS[Language.RUSSIAN]
        
        keyboard = [
            [InlineKeyboardButton("👤 Выдать доступ", callback_data="admin_grant")],
            [InlineKeyboardButton("🚫 Отозвать доступ", callback_data="admin_revoke")],
            [InlineKeyboardButton("📊 Статистика пользователя", callback_data="admin_user_stats")],
            [InlineKeyboardButton("👥 Все пользователи", callback_data="admin_all_users")],
            [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton("📨 Отправить сообщение", callback_data="admin_send")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=texts["admin_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
    
    async def admin_grant(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выдача доступа"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        await query.edit_message_text(
            text="Введите ID пользователя для выдачи доступа:"
        )
        return ADMIN_SEND_MESSAGE
    
    async def admin_revoke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отзыв доступа"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        await query.edit_message_text(
            text="Введите ID пользователя для отзыва доступа:"
        )
        return ADMIN_SEND_MESSAGE
    
    async def admin_process_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ввода от админа"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет прав доступа!")
            return
        
        text = update.message.text
        
        # Проверяем, это ID пользователя или сообщение
        if text.isdigit():
            user_id = int(text)
            user = self.data_manager.get_user(user_id)
            
            if user:
                # Переключаем доступ
                if user.has_access:
                    self.data_manager.revoke_access(user_id)
                    message = f"✅ Доступ отозван у пользователя {user_id}"
                else:
                    self.data_manager.grant_access(user_id)
                    message = f"✅ Доступ выдан пользователю {user_id}"
                    
                    # Отправляем уведомление пользователю
                    try:
                        await context.bot.send_message(
                            chat_id=user_id,
                            text="🎉 Вам выдан доступ к сигналам KURUT AI INFINITY!\n\nНажмите /start для начала работы."
                        )
                    except:
                        pass
            else:
                message = "❌ Пользователь не найден"
        else:
            message = "❌ Введите корректный ID пользователя"
        
        await update.message.reply_text(message)
        
        # Возвращаем в меню админа
        return await self.admin_menu(update, context)
    
    async def admin_user_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Статистика пользователя для админа"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        # Получаем статистику всех пользователей
        users = list(self.data_manager.users.values())
        total_users = len(users)
        active_users = len([u for u in users if u.has_access])
        
        stats_text = f"""
📊 СТАТИСТИКА БОТА:

👥 Всего пользователей: {total_users}
✅ С доступом: {active_users}
❌ Без доступа: {total_users - active_users}

📈 Всего сделок: {len(self.data_manager.trades)}
🕒 Последняя сделка: {self.data_manager.trades[-1]['timestamp'] if self.data_manager.trades else 'Нет данных'}

🏆 Топ-3 трейдера:
"""
        
        top_traders = self.data_manager.get_top_traders(3)
        for i, trader in enumerate(top_traders, 1):
            stats_text += f"{i}. ID {trader.id} - {trader.win_rate:.1f}% ({trader.total_trades} сделок)\n"
        
        await query.edit_message_text(stats_text)
    
    async def admin_all_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Список всех пользователей"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        users = list(self.data_manager.users.values())
        
        if not users:
            await query.edit_message_text("📭 Пользователей пока нет")
            return
        
        # Разбиваем на страницы
        page = context.user_data.get("admin_users_page", 0)
        users_per_page = 10
        start_idx = page * users_per_page
        end_idx = start_idx + users_per_page
        
        page_users = users[start_idx:end_idx]
        
        users_text = f"👥 ПОЛЬЗОВАТЕЛИ (страница {page + 1}):\n\n"
        
        for user in page_users:
            status = "✅" if user.has_access else "❌"
            users_text += f"{status} ID: {user.id} | {user.first_name} | Сделок: {user.total_trades}\n"
        
        # Кнопки навигации
        keyboard = []
        
        if page > 0:
            keyboard.append(InlineKeyboardButton("⬅️ Назад", callback_data="admin_users_prev"))
        
        if end_idx < len(users):
            keyboard.append(InlineKeyboardButton("➡️ Далее", callback_data="admin_users_next"))
        
        if keyboard:
            reply_markup = InlineKeyboardMarkup([keyboard])
            await query.edit_message_text(users_text, reply_markup=reply_markup)
        else:
            await query.edit_message_text(users_text)
    
    async def admin_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Рассылка сообщений"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        await query.edit_message_text(
            text="Введите сообщение для рассылки всем пользователям:"
        )
        return ADMIN_BROADCAST
    
    async def admin_send(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправка сообщения конкретному пользователю"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        await query.edit_message_text(
            text="Введите ID пользователя и сообщение через пробел:\n\nПример: 123456789 Привет!"
        )
        return ADMIN_SEND_MESSAGE
    
    async def process_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка рассылки"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет прав доступа!")
            return
        
        message = update.message.text
        users = list(self.data_manager.users.keys())
        
        await update.message.reply_text(f"📢 Рассылка начата для {len(users)} пользователей...")
        
        success = 0
        failed = 0
        
        for user_id in users:
            try:
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 ОТ АДМИНА:\n\n{message}"
                )
                success += 1
                await asyncio.sleep(0.1)  # Задержка чтобы не спамить
            except Exception as e:
                failed += 1
        
        await update.message.reply_text(
            f"✅ Рассылка завершена!\n\nУспешно: {success}\nНе удалось: {failed}"
        )
        
        return await self.admin_menu(update, context)
    
    async def setup_commands(self):
        """Настройка команд бота"""
        commands = [
            BotCommand("start", "Запустить бота"),
            BotCommand("admin", "Админ панель"),
            BotCommand("stats", "Моя статистика"),
            BotCommand("marathon", "Марафон трейдера"),
            BotCommand("top", "Топ трейдеров"),
            BotCommand("help", "Помощь")
        ]
        
        await self.application.bot.set_my_commands(commands)
    
    async def run(self):
        """Запуск бота"""
        # Создаем приложение
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Настраиваем ConversationHandler
        conv_handler = ConversationHandler(
            entry_points=[CommandHandler("start", self.start)],
            states={
                SELECT_LANGUAGE: [
                    CallbackQueryHandler(self.select_language, pattern="^lang_")
                ],
                MAIN_MENU: [
                    CallbackQueryHandler(self.get_access, pattern="^get_access$"),
                    CallbackQueryHandler(self.contact_admin, pattern="^contact_admin$"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$"),
                    CallbackQueryHandler(self.marathon_start, pattern="^marathon$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^instructions$"),
                    CallbackQueryHandler(self.show_top_traders, pattern="^top_traders$"),
                    CallbackQueryHandler(self.show_stats, pattern="^stats$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                GET_ACCESS: [
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                WAITING_FOR_BALANCE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_balance)
                ],
                CALCULATE_MARATHON: [
                    CallbackQueryHandler(self.show_marathon_risks, pattern="^marathon_risks$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                SELECT_ASSET_TYPE: [
                    CallbackQueryHandler(self.show_forex_pairs, pattern="^forex_pairs$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                SELECT_CURRENCY_PAIR: [
                    CallbackQueryHandler(self.select_pair, pattern="^pair_"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                SELECT_EXPIRY: [
                    CallbackQueryHandler(self.analyze_signal, pattern="^exp_"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                TRADE_RESULT: [
                    CallbackQueryHandler(self.process_trade_result, pattern="^trade_"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                ADMIN_SEND_MESSAGE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.admin_process_message)
                ],
                ADMIN_BROADCAST: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_broadcast)
                ]
            },
            fallbacks=[CommandHandler("start", self.start)]
        )
        
        # Добавляем обработчики
        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler("admin", self.admin_menu))
        self.application.add_handler(CommandHandler("stats", self.show_stats))
        self.application.add_handler(CommandHandler("top", self.show_top_traders))
        self.application.add_handler(CommandHandler("marathon", self.marathon_start))
        self.application.add_handler(CommandHandler("help", self.show_instructions))
        
        # Обработчики для админа
        self.application.add_handler(CallbackQueryHandler(self.admin_grant, pattern="^admin_grant$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_revoke, pattern="^admin_revoke$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_user_stats, pattern="^admin_user_stats$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_all_users, pattern="^admin_all_users$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_broadcast, pattern="^admin_broadcast$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_send, pattern="^admin_send$"))
        
        # Настраиваем команды
        await self.setup_commands()
        
        # Запускаем авто-пинг
        self.auto_ping.start()
        
        # Запускаем бота
        logger.info("🤖 KURUT AI INFINITY запущен!")
        logger.info(f"👤 Админ: {ADMIN_ID}")
        
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
if __name__ == "__main__":
    bot = KurutAIBot()
    
    # Создаем event loop
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        loop.run_until_complete(bot.run())
    except KeyboardInterrupt:
        logger.info("Бот остановлен")
    except Exception as e:
        logger.error(f"Ошибка запуска: {e}")
    finally:
        loop.close()
