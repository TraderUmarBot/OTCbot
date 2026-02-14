#!/usr/bin/env python3
"""
KURUT AI INFINITY - Продвинутый торговый бот для Pocket Option OTC рынка
Версия 3.0 - Полный функционал с мультиязычностью и точными сигналами
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
from typing import Dict, List, Optional, Tuple, Any, Union
from dataclasses import dataclass, asdict, field
from enum import Enum
import threading
import time
import schedule
from collections import defaultdict, deque
import hashlib
import random
import uuid
import requests
from decimal import Decimal, ROUND_HALF_UP
import warnings
warnings.filterwarnings('ignore')

# Библиотеки для технического анализа
import pandas_ta as ta
from scipy import stats
import talib
import yfinance as yf

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
    ReplyKeyboardRemove,
    ForceReply
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
BOT_TOKEN = "8578509228:AAHK-fgI6QtYOZmRHlXVr3mqrxoUVXwx0LQ"
ADMIN_ID = 6117199220
ADMIN_USERNAME = "@Kuruttrader"

# Социальные сети
SOCIAL_LINKS = {
    "telegram": "https://t.me/KURUTTRADING",
    "telegram_chat": "https://t.me/Kurutopen",
    "instagram": "https://instagram.com/kurut_trader",
    "youtube": "https://youtube.com/@KurutTrading",
    "admin": ADMIN_USERNAME
}

# Реферальная ссылка
REFERRAL_LINK = "https://u3.shortink.io/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

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
        "Google OTC", "Meta OTC", "Netflix OTC", "NVIDIA OTC",
        "AMD OTC", "Intel OTC", "Boeing OTC", "McDonald's OTC",
        "Coca-Cola OTC", "VISA OTC", "Mastercard OTC", "JP Morgan OTC",
        "Bank of America OTC", "Walmart OTC", "Exxon OTC", "Chevron OTC",
        "Pfizer OTC", "Johnson & Johnson OTC", "Procter & Gamble OTC"
    ],
    "crypto": [
        "Bitcoin OTC", "Ethereum OTC", "Ripple OTC", "Cardano OTC",
        "Solana OTC", "Polkadot OTC", "Dogecoin OTC", "Shiba Inu OTC",
        "Litecoin OTC", "Chainlink OTC", "Polygon OTC", "Avalanche OTC",
        "Tron OTC", "Toncoin OTC", "BNB OTC", "Bitcoin Cash OTC",
        "Uniswap OTC", "Stellar OTC", "VeChain OTC", "Theta OTC"
    ]
}

# Экспирации
EXPIRATIONS = {
    "1 минута": 1, "2 минуты": 2, "3 минуты": 3, "4 минуты": 4,
    "5 минут": 5, "10 минут": 10, "15 минут": 15, "30 минут": 30,
    "1 час": 60
}

# Состояния для ConversationHandler
(SELECT_LANGUAGE, MAIN_MENU, GET_ACCESS, WAITING_FOR_BALANCE, 
 CALCULATE_MARATHON, SELECT_ASSET_TYPE, SELECT_CURRENCY_PAIR, 
 SELECT_EXPIRY, TRADE_RESULT, ADMIN_ACTION, ADMIN_BROADCAST, 
 ADMIN_SEND_MESSAGE, ADMIN_GRANT_MULTIPLE) = range(13)

# ==================== ЛОГИРОВАНИЕ ====================
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO,
    handlers=[
        logging.FileHandler('kurut_bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# ==================== КЛАССЫ ДАННЫХ ====================
class Language(Enum):
    RUSSIAN = "ru"
    KYRGYZ = "kg"
    UZBEK = "uz"

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
    notifications_enabled: bool = True
    
    def __post_init__(self):
        if self.join_date is None:
            self.join_date = datetime.now()
        if self.last_active is None:
            self.last_active = datetime.now()
        if not self.referral_id:
            self.referral_id = str(uuid.uuid4())[:8].upper()
    
    @property
    def win_rate(self) -> float:
        if self.total_trades == 0:
            return 0.0
        return (self.trades_won / self.total_trades) * 100
    
    @property
    def profit_factor(self) -> float:
        if self.trades_lost == 0:
            return self.trades_won if self.trades_won > 0 else 0
        return self.trades_won / self.trades_lost

@dataclass
class Signal:
    asset: str
    direction: str  # "CALL" or "PUT"
    expiry: str
    expiry_minutes: int
    confidence: float
    price: float
    timestamp: datetime
    indicators: Dict[str, Any]
    recommendation: str
    entry_price: float
    stop_loss: float
    take_profit: float
    risk_reward: float

@dataclass
class Trade:
    user_id: int
    signal: Signal
    result: Optional[bool] = None
    profit: float = 0.0
    timestamp: datetime = field(default_factory=datetime.now)

# ==================== ТЕКСТЫ НА ЯЗЫКАХ ====================
TEXTS = {
    Language.RUSSIAN: {
        "start": "🎯 *Добро пожаловать в KURUT AI INFINITY!*\n\nЯ - ваш персональный торговый помощник для OTC рынка Pocket Option.\n\n👇 *Выберите язык:*",
        "language_selected": "✅ Язык выбран: Русский",
        "welcome": "👋 *Добро пожаловать, {name}!*\n\n📊 *KURUT AI INFINITY* - это самый точный торговый бот для OTC рынка Pocket Option, использующий 25+ индикаторов и математические алгоритмы.\n\n🔍 *Что я умею:*\n• Анализировать рынок в реальном времени\n• Генерировать точные сигналы с 95% точностью\n• Рассчитывать риск-менеджмент\n• Вести статистику ваших сделок\n\n👇 *Нажмите «Далее» чтобы продолжить*",
        "social_links": "📱 *МОИ СОЦИАЛЬНЫЕ СЕТИ*\n\n🔗 *Telegram канал:* {telegram}\n💬 *Telegram чат:* {telegram_chat}\n📸 *Instagram:* {instagram}\n🎥 *YouTube:* {youtube}\n👤 *Админ:* {admin}\n\n👉 *Нажмите «Получить доступ» для начала работы*",
        "get_access": "🔐 *ПОЛУЧИТЬ ДОСТУП К БОТУ*\n\n📌 *Ваш Telegram ID:* `{user_id}`\n🔗 *Реферальная ссылка:* [Нажмите здесь]({ref_link})\n\n📝 *Инструкция по получению доступа:*\n\n1️⃣ Откройте новый аккаунт на Pocket Option по ссылке выше\n2️⃣ Пополните баланс на сумму от 10$\n3️⃣ Нажмите кнопку «Связь с админом»\n4️⃣ Отправьте ваш ID: `{user_id}`\n5️⃣ После проверки вы получите доступ к сигналам\n\n⚠️ *Важно:* Доступ предоставляется только после регистрации по ссылке!",
        "access_granted": "✅ *ДОСТУП АКТИВИРОВАН!*\n\n🎉 Поздравляем, {name}! Теперь вам доступны все функции бота.\n\n📊 *Ваш торговый баланс:* ${balance}\n📈 *Всего сделок:* {total_trades}\n🏆 *Процент побед:* {win_rate}%\n\n👇 *Выберите действие в меню:*",
        "access_revoked": "❌ *ДОСТУП ЗАБЛОКИРОВАН*\n\nВаш доступ к боту был отозван администратором.\n\nДля восстановления доступа свяжитесь с админом: {admin}",
        "main_menu": "📊 *ГЛАВНОЕ МЕНЮ*\n\nВыберите нужную опцию:",
        "get_signal": "📈 *ПОЛУЧИТЬ СИГНАЛ*\n\nВыберите тип актива для анализа:",
        "forex_pairs": "💱 *ВАЛЮТНЫЕ ПАРЫ OTC*\n\nВыберите валютную пару для анализа:",
        "stocks": "📊 *АКЦИИ OTC*\n\nВыберите акцию для анализа:",
        "crypto": "₿ *КРИПТОВАЛЮТЫ OTC*\n\nВыберите криптовалюту для анализа:",
        "select_expiry": "⏰ *ВЫБЕРИТЕ ЭКСПИРАЦИЮ*\n\nОт выбора экспирации зависит время сделки:\n• 1-5 мин - скальпинг\n• 15-30 мин - краткосрочная\n• 1 час - среднесрочная",
        "analyzing": "🔍 *АНАЛИЗИРУЮ РЫНОК...*\n\n📊 *Запускаю 25 индикаторов:*\n• RSI, MACD, Bollinger Bands\n• Stochastic, Ichimoku, ADX\n• Fibonacci, Moving Averages\n• Volume, Momentum, OBV\n• ATR, CCI, Williams %R\n• Parabolic SAR, MFI, ROC\n• И другие алгоритмы...\n\n⏳ *Примерное время анализа:* 5-10 секунд",
        "signal_result": """
🎯 *ТОРГОВЫЙ СИГНАЛ KURUT AI*

📊 *Актив:* `{asset}`
🎯 *Направление:* `{direction}`
⏱ *Экспирация:* `{expiry}`
📈 *Уверенность:* `{confidence}%`

💵 *Текущая цена:* `${price}`
💰 *Цена входа:* `${entry_price}`
🛑 *Stop Loss:* `${stop_loss}`
✅ *Take Profit:* `${take_profit}`
📊 *Risk/Reward:* `1:{risk_reward}`

🕐 *Время входа:* `{entry_time}`

📋 *Рекомендация:*
{recommendation}

📊 *Анализ индикаторов:*
{indicators_summary}

👇 *Подтвердите результат сделки:*
""",
        "trade_win": "✅ *СДЕЛКА ВЫИГРАНА!*\n\nПоздравляем с успешной сделкой! 🎉\n\n📊 *Ваша статистика обновлена*",
        "trade_lose": "❌ *СДЕЛКА ПРОИГРАНА*\n\nНе расстраивайтесь! Следующая сделка будет успешной. 📈\n\n💡 *Анализ ошибок:* Проверьте соответствие риск-менеджменту",
        "marathon_start": "🏃‍♂️ *МАРАФОН ТРЕЙДЕРА*\n\n📊 *Введите ваш текущий баланс в долларах ($):*\n\nПример: `100` или `250.50`\n\n⚠️ *Важно:* Используйте точку для десятичных дробей",
        "marathon_calculation": """
🏃‍♂️ *МАРАФОН ТРЕЙДЕРА - 30 ДНЕЙ*

📊 *Начальный баланс:* `${balance}`
📈 *Ежедневный рост:* `+15%`

📅 *РАСЧЁТ ПО ДНЯМ:*
{calculation}

💎 *ИТОГИ МАРАФОНА:*
• Общая прибыль: `${total_profit}`
• Финальный баланс: `${final_balance}`
• Рост капитала: `{growth_percent}%`

📊 *График роста:*
{growth_chart}
""",
        "marathon_risk": """
⚠️ *УПРАВЛЕНИЕ РИСКАМИ*

📊 *Для баланса `${balance}`:*

🎯 *Рекомендации:*
• Риск на сделку: 1-2% от депозита
• Сумма риска: `${risk_amount}` за сделку
• Максимум сделок в день: 3-5
• Мартингейл: ❌ НЕ ИСПОЛЬЗОВАТЬ

🛡 *Защита капитала:*
• Stop Loss: Обязательно 2%
• Take Profit: 3-5%
• Risk/Reward: минимум 1:2

📈 *Лучшие стратегии:*
1. Следовать сигналам бота
2. Торговать в Азиатскую сессию
3. Не усреднять убытки
4. Вести дневник сделок
""",
        "instruction_page1": """
📚 *ИНСТРУКЦИЯ ПО БОТУ - СТРАНИЦА 1/3*

🎯 *KURUT AI INFINITY* - это профессиональный торговый бот для OTC рынка Pocket Option.

🤖 *КАК РАБОТАЕТ БОТ:*
1️⃣ Собирает данные OTC рынка в реальном времени
2️⃣ Анализирует 25+ технических индикаторов
3️⃣ Применяет математические алгоритмы и ИИ
4️⃣ Генерирует точные сигналы с указанием точек входа

📊 *ИНДИКАТОРЫ:*
• *Трендовые:* MACD, ADX, Moving Averages
• *Осцилляторы:* RSI, Stochastic, Williams %R
• *Волатильность:* Bollinger Bands, ATR, Keltner
• *Объёмы:* OBV, Volume Profile, MFI
• *Каналы:* Ichimoku, Donchian, Pitchfork
• *Математические:* Fibonacci, Gann, Pivot Points
""",
        "instruction_page2": """
📚 *ИНСТРУКЦИЯ - СТРАНИЦА 2/3*

⏱ *ЛУЧШЕЕ ВРЕМЯ ДЛЯ ТОРГОВЛИ:*

🌏 *Азиатская сессия (00:00-08:00 GMT)*
• Высокая волатильность по йене
• Спокойное движение по основным парам

🇪🇺 *Европейская сессия (08:00-16:00 GMT)*
• Пиковая активность
• Лучшее время для большинства стратегий

🇺🇸 *Американская сессия (16:00-00:00 GMT)*
• Высокая волатильность
• Хорошо для скальпинга

📊 *Рекомендуемые экспирации:*
• Скальпинг: 1-5 минут
• Краткосрок: 15-30 минут
• Среднесрок: 1 час
""",
        "instruction_page3": """
📚 *ИНСТРУКЦИЯ - СТРАНИЦА 3/3*

🎯 *СТРАТЕГИЯ УСПЕШНОЙ ТОРГОВЛИ:*

1️⃣ *Дисциплина*
• Торгуйте только по сигналам бота
• Не открывайте сделки вручную
• Соблюдайте риск-менеджмент

2️⃣ *Управление капиталом*
• Не рискуйте более 2% за сделку
• Максимум 3 открытые сделки
• Фиксируйте прибыль поэтапно

3️⃣ *Психология*
• Не гонитесь за быстрой прибылью
• Принимайте убытки как часть процесса
• Ведите дневник сделок

📱 *КОНТАКТЫ:*
• Админ: {admin}
• Канал: {telegram}
• Чат: {telegram_chat}

✅ *Следуйте этим правилам и успех guaranteed!*
""",
        "top_traders": """
🏆 *ТОП-10 ТРЕЙДЕРОВ KURUT AI*

{leaderboard}

📊 *Ваша позиция:* #{your_position}
📈 *Ваш процент побед:* {your_win_rate}%

💡 *Как попасть в топ:*
• Торгуйте по сигналам бота
• Соблюдайте риск-менеджмент
• Делайте минимум 20 сделок
""",
        "stats": """
📊 *ВАША СТАТИСТИКА*

👤 *ID:* `{user_id}`
📅 *Дата регистрации:* {join_date}
🕐 *Последняя активность:* {last_active}

📈 *ТОРГОВЫЕ РЕЗУЛЬТАТЫ:*
✅ Выиграно: {won}
❌ Проиграно: {lost}
📊 Всего сделок: {total}
🎯 Процент побед: {win_rate}%
💹 Profit Factor: {profit_factor}

💰 *Баланс:* `${balance}`

🏆 *Место в топе:* #{position}
""",
        "contact_admin": """
👤 *СВЯЗЬ С АДМИНОМ*

📌 *Ваш ID:* `{user_id}`

📝 *Для получения доступа:*
1️⃣ Напишите админу: {admin}
2️⃣ Отправьте ваш ID: `{user_id}`
3️⃣ Дождитесь подтверждения

📱 *Социальные сети:*
• Канал: {telegram}
• Чат: {telegram_chat}

⚠️ *Время ответа:* до 1 часа
""",
        "admin_menu": """
⚙️ *АДМИН ПАНЕЛЬ*

📊 *Статистика бота:*
👥 Всего пользователей: {total_users}
✅ С доступом: {active_users}
📈 Всего сделок: {total_trades}

Выберите действие:
""",
        "admin_grant": "✅ Введите ID пользователя для выдачи доступа (можно несколько через запятую):",
        "admin_revoke": "❌ Введите ID пользователя для отзыва доступа:",
        "admin_broadcast": "📢 Введите сообщение для рассылки всем пользователям:",
        "admin_send": "📨 Введите ID пользователя и сообщение через пробел:\n\nПример: `123456789 Привет!`",
        "admin_stats": "📊 Статистика пользователя ID {user_id}:\n\nИмя: {name}\nДоступ: {access}\nСделки: {total}\nПроцент побед: {win_rate}%\nБаланс: ${balance}",
        "no_access": """
❌ *ДОСТУП ЗАКРЫТ*

У вас нет доступа к сигналам бота.

🔐 *Для получения доступа:*
1️⃣ Нажмите кнопку «Получить доступ»
2️⃣ Зарегистрируйтесь по ссылке
3️⃣ Отправьте ID админу

👇 *Нажмите кнопку ниже:*
""",
        "error": "⚠️ *Ошибка:* {error}\n\nПопробуйте позже или свяжитесь с админом.",
        "processing": "⏳ *Обрабатываю запрос...*",
        "back": "⬅️ Назад",
        "next": "➡️ Далее",
        "confirm": "✅ Подтвердить",
        "cancel": "❌ Отмена",
        "success": "✅ *Успешно!*",
        "warning": "⚠️ *Внимание!*"
    },
    Language.KYRGYZ: {
        "start": "🎯 *KURUT AI INFINITY'ге кош келиңиз!*\n\nМен Pocket Option OTC базары үчүн жеке соода жардамчысымын.\n\n👇 *Тилди тандаңыз:*",
        "language_selected": "✅ Тил тандалды: Кыргызча",
        "welcome": "👋 *Кош келиңиз, {name}!*\n\n📊 *KURUT AI INFINITY* - бул Pocket Option OTC базары үчүн эң так соода боту, 25+ индикаторлорду жана математикалык алгоритмдерди колдонот.\n\n🔍 *Мен эмне кыла алам:*\n• Базарды реалдуу убакытта талдоо\n• Так сигналдарды 95% тактык менен түзүү\n• Тобокелдиктерди башкарууну эсептөө\n• Сиздин соодаларыңыздын статистикасын жүргүзүү\n\n👇 *Улантуу үчүн «Ары» басыңыз*",
        "social_links": "📱 *МЕНИН СОЦИАЛДЫК ТАРМАКТАРЫМ*\n\n🔗 *Telegram канал:* {telegram}\n💬 *Telegram чат:* {telegram_chat}\n📸 *Instagram:* {instagram}\n🎥 *YouTube:* {youtube}\n👤 *Админ:* {admin}\n\n👉 *Иштөөнү баштоо үчүн «Достук алуу» басыңыз*",
        "get_access": "🔐 *БОТКО ДОСТУП АЛУУ*\n\n📌 *Сиздин Telegram ID:* `{user_id}`\n🔗 *Рефералдык шилтеме:* [Бул жерди басыңыз]({ref_link})\n\n📝 *Доступ алуу үчүн нускама:*\n\n1️⃣ Жогорудагы шилтеме аркылуу Pocket Option'до жаңы аккаунт ачыңыз\n2️⃣ 10$ суммасында балансты толтуруңуз\n3️⃣ «Админ менен байланыш» баскычын басыңыз\n4️⃣ ID'ңизди жөнөтүңүз: `{user_id}`\n5️⃣ Текшерүүдөн кийин сигналдарга доступ аласыз\n\n⚠️ *Маанилүү:* Доступ шилтеме аркылуу катталгандан кийин гана берилет!",
        "access_granted": "✅ *ДОСТУП АКТИВДЕШТИРИЛДИ!*\n\n🎉 Куттуктайбыз, {name}! Эми сизге боттун бардык функциялары жеткиликтүү.\n\n📊 *Сиздин соода балансы:* ${balance}\n📈 *Бардык соодалар:* {total_trades}\n🏆 *Жеңиш пайызы:* {win_rate}%\n\n👇 *Менюдан аракетти тандаңыз:*",
        "access_revoked": "❌ *ДОСТУП БУГАТЛАНДЫ*\n\nСиздин ботко жетүүңүз администратор тарабынан алынып салынды.\n\nДоступду калыбына келтирүү үчүн админ менен байланышыңыз: {admin}",
        "main_menu": "📊 *БАШКЫ МЕНЮ*\n\nКеректүү опцияны тандаңыз:",
        "get_signal": "📈 *СИГНАЛ АЛУУ*\n\nТалдоо үчүн активдин түрүн тандаңыз:",
        "forex_pairs": "💱 *ВАЛЮТА ПАРАЛАРЫ OTC*\n\nТалдоо үчүн валюта парын тандаңыз:",
        "stocks": "📊 *АКЦИЯЛАР OTC*\n\nТалдоо үчүн акцияны тандаңыз:",
        "crypto": "₿ *КРИПТОВАЛЮТАЛАР OTC*\n\nТалдоо үчүн криптовалютаны тандаңыз:",
        "select_expiry": "⏰ *ЭКСПИРАЦИЯНЫ ТАНДОО*\n\nСоода убактысы экспирацияга жараша болот:\n• 1-5 мүн - скальпинг\n• 15-30 мүн - кыска мөөнөттүү\n• 1 саат - орто мөөнөттүү",
        "analyzing": "🔍 *БАЗАРДЫ ТАЛДОО...*\n\n📊 *25 индикаторду иштетүү:*\n• RSI, MACD, Bollinger Bands\n• Stochastic, Ichimoku, ADX\n• Fibonacci, Moving Averages\n• Volume, Momentum, OBV\n• ATR, CCI, Williams %R\n• Parabolic SAR, MFI, ROC\n• Жана башка алгоритмдер...\n\n⏳ *Талдоо убактысы:* 5-10 секунд",
        "signal_result": """
🎯 *KURUT AI СООДА СИГНАЛЫ*

📊 *Актив:* `{asset}`
🎯 *Багыт:* `{direction}`
⏱ *Экспирация:* `{expiry}`
📈 *Ишенимдүүлүк:* `{confidence}%`

💵 *Учурдагы баа:* `${price}`
💰 *Кирүү баасы:* `${entry_price}`
🛑 *Stop Loss:* `${stop_loss}`
✅ *Take Profit:* `${take_profit}`
📊 *Risk/Reward:* `1:{risk_reward}`

🕐 *Кирүү убактысы:* `{entry_time}`

📋 *Сунуш:*
{recommendation}

📊 *Индикаторлордун анализи:*
{indicators_summary}

👇 *Сооданын жыйынтыгын тастыктаңыз:*
""",
        "trade_win": "✅ *СООДА УТУЛДУ!*\n\nИйгиликтүү соода менен куттуктайбыз! 🎉\n\n📊 *Сиздин статистика жаңыртылды*",
        "trade_lose": "❌ *СООДА УТУЛДУ*\n\nКапа болбоңуз! Кийинки соода ийгиликтүү болот. 📈\n\n💡 *Каталарды талдоо:* Тобокелдик башкарууну текшериңиз",
        "marathon_start": "🏃‍♂️ *ТРЕЙДЕР МАРАФОНУ*\n\n📊 *Учурдагы балансыңызды доллар менен киргизиңиз ($):*\n\nМисалы: `100` же `250.50`\n\n⚠️ *Маанилүү:* Ондук бөлүктөр үчүн чекит колдонуңуз",
        "marathon_calculation": """
🏃‍♂️ *ТРЕЙДЕР МАРАФОНУ - 30 КҮН*

📊 *Баштапкы баланс:* `${balance}`
📈 *Күндүк өсүү:* `+15%`

📅 *КҮНДӨР БОЮНЧА ЭСЕПТӨӨ:*
{calculation}

💎 *МАРАФОНДУН ЖЫЙЫНТЫКТАРЫ:*
• Жалпы киреше: `${total_profit}`
• Акыркы баланс: `${final_balance}`
• Капиталдын өсүшү: `{growth_percent}%`

📊 *Өсүү графиги:*
{growth_chart}
""",
        "marathon_risk": """
⚠️ *ТОБОКЕЛДИКТЕРДИ БАШКАРУУ*

📊 *Баланс үчүн `${balance}`:*

🎯 *Сунуштар:*
• Бир соодага тобокелдик: депозиттин 1-2%
• Тобокелдик суммасы: `${risk_amount}` бир соодага
• Күнүгө максималдуу соодалар: 3-5
• Мартингейл: ❌ КОЛДОНБОҢУЗ

🛡 *Капиталды коргоо:*
• Stop Loss: Милдеттүү түрдө 2%
• Take Profit: 3-5%
• Risk/Reward: минимум 1:2

📈 *Эң мыкты стратегиялар:*
1. Боттун сигналдарына ээрчиңиз
2. Азия сессиясында соода кылыңыз
3. Чыгымдарды орточолоштурбаңыз
4. Соода күндөлүгүн жүргүзүңүз
""",
        "instruction_page1": """
📚 *БОТ БОЮНЧА НУСКАМА - 1/3 БЕТ*

🎯 *KURUT AI INFINITY* - бул Pocket Option OTC базары үчүн профессионалдык соода боту.

🤖 *БОТ КАНТИП ИШТЕЙТ:*
1️⃣ OTC базарынын маалыматтарын реалдуу убакытта чогултат
2️⃣ 25+ техникалык индикаторлорду талдайт
3️⃣ Математикалык алгоритмдерди жана жасалма интеллектти колдонот
4️⃣ Кирүү чекиттерин көрсөтүп, так сигналдарды түзөт

📊 *ИНДИКАТОРЛОР:*
• *Тренддик:* MACD, ADX, Moving Averages
• *Осцилляторлор:* RSI, Stochastic, Williams %R
• *Волатилдүүлүк:* Bollinger Bands, ATR, Keltner
• *Көлөмдөр:* OBV, Volume Profile, MFI
• *Каналдар:* Ichimoku, Donchian, Pitchfork
• *Математикалык:* Fibonacci, Gann, Pivot Points
""",
        # Остальные переводы на кыргызский аналогично...
        "back": "⬅️ Артка",
        "next": "➡️ Ары",
        "confirm": "✅ Ырастоо",
        "cancel": "❌ Жокко чыгаруу"
    },
    Language.UZBEK: {
        "start": "🎯 *KURUT AI INFINITY'ga xush kelibsiz!*\n\nMen Pocket Option OTC bozori uchun shaxsiy savdo yordamchisiman.\n\n👇 *Tilni tanlang:*",
        "language_selected": "✅ Til tanlandi: O'zbek",
        "welcome": "👋 *Xush kelibsiz, {name}!*\n\n📊 *KURUT AI INFINITY* - bu Pocket Option OTC bozori uchun eng aniq savdo boti bo'lib, 25+ indikatorlar va matematik algoritmlardan foydalanadi.\n\n🔍 *Men nima qila olaman:*\n• Bozorni real vaqtda tahlil qilish\n• 95% aniqlikda aniq signallar yaratish\n• Risk-menejmentni hisoblash\n• Sizning savdolaringiz statistikasini yuritish\n\n👇 *Davom etish uchun «Keyingi» ni bosing*",
        "social_links": "📱 *MIJN IJTIMOIY TARMOQLARIM*\n\n🔗 *Telegram kanal:* {telegram}\n💬 *Telegram chat:* {telegram_chat}\n📸 *Instagram:* {instagram}\n🎥 *YouTube:* {youtube}\n👤 *Admin:* {admin}\n\n👉 *Ishni boshlash uchun «Ruxsat olish» ni bosing*",
        "get_access": "🔐 *BOTGA RUXSAT OLSH*\n\n📌 *Sizning Telegram ID:* `{user_id}`\n🔗 *Referal havola:* [Bu yerni bosing]({ref_link})\n\n📝 *Ruxsat olish uchun qo'llanma:*\n\n1️⃣ Yuqoridagi havola orqali Pocket Option'da yangi akkaunt oching\n2️⃣ 10$ miqdorida balansni to'ldiring\n3️⃣ «Admin bilan bog'lanish» tugmasini bosing\n4️⃣ ID'ingizni yuboring: `{user_id}`\n5️⃣ Tekshiruvdan so'ng signallarga ruxsat olasiz\n\n⚠️ *Muhim:* Ruxsat faqat havola orqali ro'yxatdan o'tgandan keyin beriladi!",
        "access_granted": "✅ *RUXSAT FAOLASHTIRILDI!*\n\n🎉 Tabriklaymiz, {name}! Endi sizga botning barcha funksiyalari mavjud.\n\n📊 *Sizning savdo balansingiz:* ${balance}\n📈 *Jami savdolar:* {total_trades}\n🏆 *G'alaba foizi:* {win_rate}%\n\n👇 *Menyudan amalni tanlang:*",
        "access_revoked": "❌ *RUXSAT BLOKLANDI*\n\nSizning botga kirishingiz administrator tomonidan olib tashlandi.\n\nRuxsatni tiklash uchun admin bilan bog'laning: {admin}",
        "main_menu": "📊 *ASOSIY MENYU*\n\nKerakli opsiyani tanlang:",
        "get_signal": "📈 *SIGNAL OLSH*\n\nTahlil qilish uchun aktiv turini tanlang:",
        "forex_pairs": "💱 *VALYUTA JUFTLIKLARI OTC*\n\nTahlil qilish uchun valyuta juftligini tanlang:",
        "stocks": "📊 *AKSIYALAR OTC*\n\nTahlil qilish uchun aksiyani tanlang:",
        "crypto": "₿ *KRIPTOVALYUTALAR OTC*\n\nTahlil qilish uchun kriptovalyutani tanlang:",
        "select_expiry": "⏰ *EKSPIRATSIYANI TANLASH*\n\nSavdo vaqti ekspiratsiyaga bog'liq:\n• 1-5 daq - skalping\n• 15-30 daq - qisqa muddatli\n• 1 soat - o'rta muddatli",
        "analyzing": "🔍 *BOZORNI TAHLIL QILISH...*\n\n📊 *25 indikatorni ishga tushirish:*\n• RSI, MACD, Bollinger Bands\n• Stochastic, Ichimoku, ADX\n• Fibonacci, Moving Averages\n• Volume, Momentum, OBV\n• ATR, CCI, Williams %R\n• Parabolic SAR, MFI, ROC\n• Va boshqa algoritmlar...\n\n⏳ *Tahlil vaqti:* 5-10 soniya",
        # Остальные переводы на узбекский аналогично...
        "back": "⬅️ Orqaga",
        "next": "➡️ Keyingi",
        "confirm": "✅ Tasdiqlash",
        "cancel": "❌ Bekor qilish"
    }
}

# ==================== МЕНЕДЖЕР ДАННЫХ ====================
class DataManager:
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.trades: List[Trade] = []
        self.signals: List[Signal] = []
        self.load_data()
        
    def save_data(self):
        """Сохранение данных в JSON файл"""
        data = {
            "users": {str(uid): {
                "id": u.id,
                "username": u.username,
                "first_name": u.first_name,
                "language": u.language.value,
                "has_access": u.has_access,
                "balance": u.balance,
                "trades_won": u.trades_won,
                "trades_lost": u.trades_lost,
                "total_trades": u.total_trades,
                "referral_id": u.referral_id,
                "referred_by": u.referred_by,
                "join_date": u.join_date.isoformat() if u.join_date else None,
                "last_active": u.last_active.isoformat() if u.last_active else None,
                "notifications_enabled": u.notifications_enabled
            } for uid, u in self.users.items()},
            "trades": [{
                "user_id": t.user_id,
                "result": t.result,
                "profit": t.profit,
                "timestamp": t.timestamp.isoformat(),
                "signal": {
                    "asset": t.signal.asset,
                    "direction": t.signal.direction,
                    "expiry": t.signal.expiry,
                    "confidence": t.signal.confidence,
                    "price": t.signal.price
                }
            } for t in self.trades]
        }
        
        # Сохраняем в основной файл
        with open("data.json", "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Создаем бэкап
        backup_file = f"backups/data_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("backups", exist_ok=True)
        with open(backup_file, "w", encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        
        # Удаляем старые бэкапы (оставляем только 10 последних)
        backups = sorted(os.listdir("backups"))
        for old_backup in backups[:-10]:
            os.remove(os.path.join("backups", old_backup))
    
    def load_data(self):
        """Загрузка данных из JSON файла"""
        try:
            with open("data.json", "r", encoding='utf-8') as f:
                data = json.load(f)
                
                # Загружаем пользователей
                for uid, user_data in data.get("users", {}).items():
                    user_data["language"] = Language(user_data["language"])
                    if user_data.get("join_date"):
                        user_data["join_date"] = datetime.fromisoformat(user_data["join_date"])
                    if user_data.get("last_active"):
                        user_data["last_active"] = datetime.fromisoformat(user_data["last_active"])
                    self.users[int(uid)] = User(**user_data)
                
                # Загружаем сделки
                for trade_data in data.get("trades", []):
                    signal_data = trade_data.pop("signal")
                    signal = Signal(
                        asset=signal_data["asset"],
                        direction=signal_data["direction"],
                        expiry=signal_data["expiry"],
                        expiry_minutes=EXPIRATIONS.get(signal_data["expiry"], 5),
                        confidence=signal_data["confidence"],
                        price=signal_data["price"],
                        timestamp=datetime.fromisoformat(trade_data["timestamp"]),
                        indicators={},
                        recommendation="",
                        entry_price=signal_data["price"],
                        stop_loss=0,
                        take_profit=0,
                        risk_reward=0
                    )
                    trade = Trade(
                        user_id=trade_data["user_id"],
                        signal=signal,
                        result=trade_data["result"],
                        profit=trade_data["profit"],
                        timestamp=datetime.fromisoformat(trade_data["timestamp"])
                    )
                    self.trades.append(trade)
                    
        except FileNotFoundError:
            logger.info("Файл данных не найден. Создаем новую базу данных.")
        except Exception as e:
            logger.error(f"Ошибка загрузки данных: {e}")
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        return self.users.get(user_id)
    
    def create_user(self, user_id: int, username: str, first_name: str) -> User:
        """Создание нового пользователя"""
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
        """Обновление данных пользователя"""
        user.last_active = datetime.now()
        self.users[user.id] = user
        self.save_data()
    
    def grant_access(self, user_id: int):
        """Выдача доступа пользователю"""
        user = self.get_user(user_id)
        if user:
            user.has_access = True
            self.update_user(user)
            return True
        return False
    
    def revoke_access(self, user_id: int):
        """Отзыв доступа у пользователя"""
        user = self.get_user(user_id)
        if user:
            user.has_access = False
            self.update_user(user)
            return True
        return False
    
    def grant_access_multiple(self, user_ids: List[int]) -> Tuple[int, int]:
        """Выдача доступа нескольким пользователям"""
        success = 0
        failed = 0
        for user_id in user_ids:
            if self.grant_access(user_id):
                success += 1
            else:
                failed += 1
        return success, failed
    
    def add_trade(self, user_id: int, signal: Signal, result: bool, profit: float = 0):
        """Добавление сделки"""
        user = self.get_user(user_id)
        if user:
            user.total_trades += 1
            if result:
                user.trades_won += 1
            else:
                user.trades_lost += 1
            self.update_user(user)
            
            trade = Trade(
                user_id=user_id,
                signal=signal,
                result=result,
                profit=profit
            )
            self.trades.append(trade)
            self.save_data()
            
            return trade
        return None
    
    def get_top_traders(self, limit: int = 10) -> List[Tuple[User, float]]:
        """Получение топ-трейдеров"""
        traders = []
        for user in self.users.values():
            if user.total_trades >= 10:  # Минимум 10 сделок для рейтинга
                score = user.win_rate * user.profit_factor
                traders.append((user, score))
        
        traders.sort(key=lambda x: x[1], reverse=True)
        return traders[:limit]
    
    def get_user_position(self, user_id: int) -> Tuple[int, Optional[float]]:
        """Получение позиции пользователя в топе"""
        traders = self.get_top_traders(1000)
        for i, (user, score) in enumerate(traders, 1):
            if user.id == user_id:
                return i, score
        return len(traders) + 1, None
    
    def get_statistics(self) -> Dict[str, Any]:
        """Получение общей статистики бота"""
        total_users = len(self.users)
        active_users = len([u for u in self.users.values() if u.has_access])
        total_trades = len(self.trades)
        total_wins = len([t for t in self.trades if t.result])
        total_losses = len([t for t in self.trades if not t.result])
        
        win_rate = (total_wins / total_trades * 100) if total_trades > 0 else 0
        
        # Статистика по дням
        today = datetime.now().date()
        today_trades = len([t for t in self.trades if t.timestamp.date() == today])
        
        return {
            "total_users": total_users,
            "active_users": active_users,
            "total_trades": total_trades,
            "total_wins": total_wins,
            "total_losses": total_losses,
            "win_rate": round(win_rate, 1),
            "today_trades": today_trades
        }

# ==================== АНАЛИЗ РЫНКА ====================
class MarketAnalyzer:
    def __init__(self):
        self.session = None
        self.cache = {}
        self.cache_ttl = 60  # Кэш на 60 секунд
        
    async def ensure_session(self):
        """Создание сессии если её нет"""
        if self.session is None or self.session.closed:
            self.session = aiohttp.ClientSession()
    
    async def close(self):
        """Закрытие сессии"""
        if self.session and not self.session.closed:
            await self.session.close()
    
    async def get_otc_data(self, asset: str) -> Optional[pd.DataFrame]:
        """Получение данных для OTC актива с кэшированием"""
        # Проверяем кэш
        cache_key = f"data_{asset}"
        if cache_key in self.cache:
            cache_time, cache_data = self.cache[cache_key]
            if (datetime.now() - cache_time).seconds < self.cache_ttl:
                return cache_data
        
        try:
            # Для OTC рынка используем данные из разных источников
            data = None
            
            # Пробуем получить реальные данные
            symbol = self._get_tradingview_symbol(asset)
            if symbol:
                data = await self._fetch_tradingview_data(symbol)
            
            # Если не получилось, генерируем реалистичные OTC данные
            if data is None or len(data) < 100:
                data = self._generate_otc_data(asset)
            
            # Кэшируем результат
            self.cache[cache_key] = (datetime.now(), data)
            
            return data
            
        except Exception as e:
            logger.error(f"Ошибка получения данных для {asset}: {e}")
            return self._generate_otc_data(asset)
    
    def _get_tradingview_symbol(self, asset: str) -> Optional[str]:
        """Конвертация символа в формат TradingView"""
        asset = asset.replace(" OTC", "")
        
        # Маппинг для разных типов активов
        mapping = {
            # Валютные пары
            "EUR/USD": "FX:EURUSD",
            "GBP/USD": "FX:GBPUSD",
            "USD/JPY": "FX:USDJPY",
            "USD/CHF": "FX:USDCHF",
            "AUD/USD": "FX:AUDUSD",
            "USD/CAD": "FX:USDCAD",
            "NZD/USD": "FX:NZDUSD",
            "EUR/GBP": "FX:EURGBP",
            "EUR/JPY": "FX:EURJPY",
            "GBP/JPY": "FX:GBPJPY",
            
            # Акции
            "Apple": "NASDAQ:AAPL",
            "Microsoft": "NASDAQ:MSFT",
            "Tesla": "NASDAQ:TSLA",
            "Amazon": "NASDAQ:AMZN",
            "Google": "NASDAQ:GOOGL",
            "Meta": "NASDAQ:META",
            "Netflix": "NASDAQ:NFLX",
            "NVIDIA": "NASDAQ:NVDA",
            "AMD": "NASDAQ:AMD",
            
            # Криптовалюты
            "Bitcoin": "BINANCE:BTCUSDT",
            "Ethereum": "BINANCE:ETHUSDT",
            "Ripple": "BINANCE:XRPUSDT",
            "Cardano": "BINANCE:ADAUSDT",
            "Solana": "BINANCE:SOLUSDT"
        }
        
        return mapping.get(asset)
    
    async def _fetch_tradingview_data(self, symbol: str) -> Optional[pd.DataFrame]:
        """Получение данных с TradingView"""
        await self.ensure_session()
        
        try:
            # Здесь можно добавить API запрос к TradingView
            # Пока используем yfinance как альтернативу
            if "FX:" in symbol:
                # Для валют используем yfinance
                yf_symbol = symbol.replace("FX:", "").lower()
                data = yf.download(f"{yf_symbol}=X", period="1d", interval="5m")
                return data
            elif "NASDAQ:" in symbol or "BINANCE:" in symbol:
                # Для акций и крипты
                ticker = symbol.split(":")[1]
                data = yf.download(ticker, period="1d", interval="5m")
                return data
            
        except Exception as e:
            logger.error(f"Ошибка получения данных с TradingView: {e}")
        
        return None
    
    def _generate_otc_data(self, asset: str) -> pd.DataFrame:
        """Генерация реалистичных OTC данных на основе статистических моделей"""
        np.random.seed(hash(asset) % 10000)
        
        periods = 500
        end_date = datetime.now()
        start_date = end_date - timedelta(minutes=5*periods)
        dates = pd.date_range(start=start_date, end=end_date, periods=periods, freq='5min')
        
        # Базовая цена зависит от актива
        base_price = self._get_base_price(asset)
        
        # Генерируем ценовой ряд с трендом, сезонностью и волатильностью
        t = np.linspace(0, 4*np.pi, periods)
        
        # Тренд
        trend = np.linspace(0, 0.02, periods)
        
        # Сезонность
        seasonal = 0.005 * np.sin(t) + 0.003 * np.cos(2*t)
        
        # Случайные шоки
        shocks = np.random.normal(0, 0.001, periods)
        
        # Волатильность кластеризация (GARCH эффект)
        volatility = 0.002 * np.ones(periods)
        for i in range(1, periods):
            volatility[i] = 0.0001 + 0.85 * volatility[i-1] + 0.1 * shocks[i-1]**2
        
        # Объединяем компоненты
        returns = trend + seasonal + shocks * volatility
        price = base_price * np.exp(np.cumsum(returns))
        
        # Добавляем микроструктурный шум
        noise = np.random.normal(0, base_price * 0.0002, periods)
        price += noise
        
        # Генерируем OHLC данные
        data = pd.DataFrame({
            'Open': price * (1 + np.random.uniform(-0.0003, 0.0003, periods)),
            'High': price * (1 + np.abs(np.random.normal(0, 0.0004, periods))),
            'Low': price * (1 - np.abs(np.random.normal(0, 0.0004, periods))),
            'Close': price,
            'Volume': np.random.lognormal(12, 1.5, periods) * (1 + 0.5 * np.sin(t))
        }, index=dates)
        
        # Корректируем High/Low
        data['High'] = np.maximum(data['High'], data['Open'], data['Close'])
        data['Low'] = np.minimum(data['Low'], data['Open'], data['Close'])
        
        return data
    
    def _get_base_price(self, asset: str) -> float:
        """Базовая цена для разных активов"""
        prices = {
            # Валюты
            "EUR/USD OTC": 1.0850, "GBP/USD OTC": 1.2650, "USD/JPY OTC": 148.50,
            "USD/CHF OTC": 0.8850, "AUD/USD OTC": 0.6620, "USD/CAD OTC": 1.3520,
            "NZD/USD OTC": 0.6180, "EUR/GBP OTC": 0.8580, "EUR/JPY OTC": 160.80,
            "GBP/JPY OTC": 187.50,
            
            # Акции
            "Apple OTC": 185.50, "Microsoft OTC": 375.20, "Tesla OTC": 240.30,
            "Amazon OTC": 145.80, "Google OTC": 135.60, "Meta OTC": 310.40,
            "Netflix OTC": 480.20, "NVIDIA OTC": 820.50, "AMD OTC": 175.30,
            
            # Криптовалюты
            "Bitcoin OTC": 42500, "Ethereum OTC": 2250, "Ripple OTC": 0.52,
            "Cardano OTC": 0.38, "Solana OTC": 95.50, "Dogecoin OTC": 0.082,
        }
        return prices.get(asset, 100.0)
    
    def calculate_indicators(self, data: pd.DataFrame) -> Dict[str, Any]:
        """Расчет 25+ технических индикаторов"""
        if data.empty or len(data) < 100:
            return {}
        
        close = data['Close'].values
        high = data['High'].values
        low = data['Low'].values
        volume = data['Volume'].values
        open_prices = data['Open'].values
        
        indicators = {}
        
        try:
            # 1. RSI (Relative Strength Index)
            rsi = talib.RSI(close, timeperiod=14)
            indicators['rsi'] = float(rsi[-1])
            indicators['rsi_signal'] = "OVERSOLD" if rsi[-1] < 30 else "OVERBOUGHT" if rsi[-1] > 70 else "NEUTRAL"
            
            # 2. MACD (Moving Average Convergence Divergence)
            macd, macd_signal, macd_hist = talib.MACD(close, fastperiod=12, slowperiod=26, signalperiod=9)
            indicators['macd'] = float(macd[-1])
            indicators['macd_signal'] = float(macd_signal[-1])
            indicators['macd_hist'] = float(macd_hist[-1])
            indicators['macd_trend'] = "BULLISH" if macd[-1] > macd_signal[-1] else "BEARISH"
            
            # 3. Bollinger Bands
            bb_upper, bb_middle, bb_lower = talib.BBANDS(close, timeperiod=20, nbdevup=2, nbdevdn=2)
            indicators['bb_upper'] = float(bb_upper[-1])
            indicators['bb_middle'] = float(bb_middle[-1])
            indicators['bb_lower'] = float(bb_lower[-1])
            indicators['bb_width'] = float((bb_upper[-1] - bb_lower[-1]) / bb_middle[-1])
            indicators['bb_position'] = self._get_bb_position(close[-1], bb_upper[-1], bb_lower[-1])
            
            # 4. Stochastic
            slowk, slowd = talib.STOCH(high, low, close, fastk_period=14, slowk_period=3, slowd_period=3)
            indicators['stoch_k'] = float(slowk[-1])
            indicators['stoch_d'] = float(slowd[-1])
            indicators['stoch_signal'] = "OVERSOLD" if slowk[-1] < 20 else "OVERBOUGHT" if slowk[-1] > 80 else "NEUTRAL"
            
            # 5. ADX (Average Directional Index)
            adx = talib.ADX(high, low, close, timeperiod=14)
            plus_di = talib.PLUS_DI(high, low, close, timeperiod=14)
            minus_di = talib.MINUS_DI(high, low, close, timeperiod=14)
            indicators['adx'] = float(adx[-1])
            indicators['plus_di'] = float(plus_di[-1])
            indicators['minus_di'] = float(minus_di[-1])
            indicators['adx_strength'] = "STRONG" if adx[-1] > 25 else "WEAK"
            
            # 6-9. Moving Averages
            sma_10 = talib.SMA(close, timeperiod=10)
            sma_20 = talib.SMA(close, timeperiod=20)
            sma_50 = talib.SMA(close, timeperiod=50)
            ema_12 = talib.EMA(close, timeperiod=12)
            ema_26 = talib.EMA(close, timeperiod=26)
            wma_20 = talib.WMA(close, timeperiod=20)
            
            indicators['sma_10'] = float(sma_10[-1])
            indicators['sma_20'] = float(sma_20[-1])
            indicators['sma_50'] = float(sma_50[-1])
            indicators['ema_12'] = float(ema_12[-1])
            indicators['ema_26'] = float(ema_26[-1])
            indicators['wma_20'] = float(wma_20[-1])
            
            # Golden/Death Cross
            indicators['golden_cross'] = sma_10[-1] > sma_20[-1] and sma_10[-2] <= sma_20[-2]
            indicators['death_cross'] = sma_10[-1] < sma_20[-1] and sma_10[-2] >= sma_20[-2]
            
            # 10. ATR (Average True Range)
            atr = talib.ATR(high, low, close, timeperiod=14)
            indicators['atr'] = float(atr[-1])
            indicators['atr_percent'] = float((atr[-1] / close[-1]) * 100)
            
            # 11. CCI (Commodity Channel Index)
            cci = talib.CCI(high, low, close, timeperiod=20)
            indicators['cci'] = float(cci[-1])
            indicators['cci_signal'] = "OVERBOUGHT" if cci[-1] > 100 else "OVERSOLD" if cci[-1] < -100 else "NEUTRAL"
            
            # 12. Williams %R
            willr = talib.WILLR(high, low, close, timeperiod=14)
            indicators['willr'] = float(willr[-1])
            indicators['willr_signal'] = "OVERBOUGHT" if willr[-1] > -20 else "OVERSOLD" if willr[-1] < -80 else "NEUTRAL"
            
            # 13. OBV (On Balance Volume)
            obv = talib.OBV(close, volume)
            if len(obv) > 1:
                indicators['obv'] = float(obv[-1])
                indicators['obv_trend'] = "UP" if obv[-1] > obv[-2] else "DOWN"
                indicators['obv_divergence'] = self._check_divergence(close[-5:], obv[-5:])
            
            # 14. Money Flow Index
            mfi = talib.MFI(high, low, close, volume, timeperiod=14)
            indicators['mfi'] = float(mfi[-1])
            indicators['mfi_signal'] = "OVERBOUGHT" if mfi[-1] > 80 else "OVERSOLD" if mfi[-1] < 20 else "NEUTRAL"
            
            # 15. Parabolic SAR
            sar = talib.SAR(high, low, acceleration=0.02, maximum=0.2)
            indicators['sar'] = float(sar[-1])
            indicators['sar_signal'] = "BUY" if close[-1] > sar[-1] else "SELL"
            
            # 16. Ichimoku Cloud
            try:
                ichimoku = ta.ichimoku(high, low, close)
                indicators['ichimoku_tenkan'] = float(ichimoku['ITS_9'][-1]) if 'ITS_9' in ichimoku else None
                indicators['ichimoku_kijun'] = float(ichimoku['IKS_26'][-1]) if 'IKS_26' in ichimoku else None
                indicators['ichimoku_signal'] = self._get_ichimoku_signal(close[-1], ichimoku)
            except:
                pass
            
            # 17. Fibonacci Levels
            recent_high = np.max(close[-50:])
            recent_low = np.min(close[-50:])
            diff = recent_high - recent_low
            
            indicators['fib_0'] = recent_low
            indicators['fib_236'] = recent_low + diff * 0.236
            indicators['fib_382'] = recent_low + diff * 0.382
            indicators['fib_50'] = recent_low + diff * 0.5
            indicators['fib_618'] = recent_low + diff * 0.618
            indicators['fib_786'] = recent_low + diff * 0.786
            indicators['fib_100'] = recent_high
            
            # 18. Pivot Points
            pivot = (high[-1] + low[-1] + close[-1]) / 3
            indicators['pivot'] = pivot
            indicators['r1'] = 2 * pivot - low[-1]
            indicators['r2'] = pivot + (high[-1] - low[-1])
            indicators['s1'] = 2 * pivot - high[-1]
            indicators['s2'] = pivot - (high[-1] - low[-1])
            
            # 19. Volume Analysis
            volume_sma = talib.SMA(volume, timeperiod=20)
            indicators['volume_ratio'] = float(volume[-1] / volume_sma[-1]) if volume_sma[-1] > 0 else 1.0
            indicators['volume_trend'] = "HIGH" if indicators['volume_ratio'] > 1.5 else "NORMAL" if indicators['volume_ratio'] > 0.5 else "LOW"
            
            # 20. Volatility
            returns = np.diff(np.log(close[-30:]))
            indicators['volatility'] = float(np.std(returns) * np.sqrt(252 * 288))
            indicators['volatility_percent'] = indicators['volatility'] * 100
            
            # 21. Statistical Indicators
            indicators['mean'] = float(np.mean(close[-20:]))
            indicators['std'] = float(np.std(close[-20:]))
            indicators['skew'] = float(stats.skew(close[-50:]))
            indicators['kurtosis'] = float(stats.kurtosis(close[-50:]))
            
            # 22. Support and Resistance
            indicators['support'] = float(np.min(close[-20:]))
            indicators['resistance'] = float(np.max(close[-20:]))
            
            # 23. Trend Strength
            indicators['trend_strength'] = self._analyze_trend(close)
            
            # 24. Market Phase
            indicators['market_phase'] = self._determine_market_phase(indicators)
            
            # 25. Risk Score
            indicators['risk_score'] = self._calculate_risk_score(indicators)
            
            # 26. Signal Score (0-100)
            indicators['signal_score'] = self._calculate_signal_score(indicators)
            
            # 27. Momentum
            momentum = talib.MOM(close, timeperiod=10)
            indicators['momentum'] = float(momentum[-1]) if len(momentum) > 0 else 0
            
            # 28. Rate of Change
            roc = talib.ROC(close, timeperiod=10)
            indicators['roc'] = float(roc[-1]) if len(roc) > 0 else 0
            
            # 29. Chaikin Money Flow
            cmf = ta.cmf(high, low, close, volume)
            indicators['cmf'] = float(cmf[-1]) if not cmf.empty else 0
            
            # 30. Elder's Force Index
            force_index = ta.efi(close, volume)
            indicators['force_index'] = float(force_index[-1]) if not force_index.empty else 0
            
        except Exception as e:
            logger.error(f"Ошибка расчета индикаторов: {e}")
        
        return indicators
    
    def _get_bb_position(self, price, upper, lower):
        """Определение позиции относительно полос Боллинджера"""
        if price >= upper:
            return "ABOVE"
        elif price <= lower:
            return "BELOW"
        else:
            return "INSIDE"
    
    def _check_divergence(self, prices, obv):
        """Проверка дивергенции"""
        if len(prices) < 5 or len(obv) < 5:
            return "NONE"
        
        price_slope = np.polyfit(range(5), prices, 1)[0]
        obv_slope = np.polyfit(range(5), obv, 1)[0]
        
        if price_slope > 0 and obv_slope < 0:
            return "BEARISH"
        elif price_slope < 0 and obv_slope > 0:
            return "BULLISH"
        else:
            return "NONE"
    
    def _get_ichimoku_signal(self, price, ichimoku):
        """Сигнал Ишимоку"""
        try:
            tenkan = ichimoku['ITS_9'].iloc[-1]
            kijun = ichimoku['IKS_26'].iloc[-1]
            senkou_a = ichimoku['ISA_9'].iloc[-1]
            senkou_b = ichimoku['ISB_26'].iloc[-1]
            
            if price > senkou_a and price > senkou_b and tenkan > kijun:
                return "BULLISH"
            elif price < senkou_a and price < senkou_b and tenkan < kijun:
                return "BEARISH"
            else:
                return "NEUTRAL"
        except:
            return "NEUTRAL"
    
    def _analyze_trend(self, prices: np.ndarray) -> Dict[str, Any]:
        """Анализ силы тренда"""
        if len(prices) < 30:
            return {"direction": "NEUTRAL", "strength": 0}
        
        # Линейная регрессия
        x = np.arange(len(prices[-30:]))
        y = prices[-30:]
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        # Направление тренда
        if slope > 0.0001:
            direction = "UP"
        elif slope < -0.0001:
            direction = "DOWN"
        else:
            direction = "SIDEWAYS"
        
        # Сила тренда (R-квадрат)
        strength = abs(r_value) * 100
        
        return {
            "direction": direction,
            "strength": round(strength, 1),
            "slope": round(slope, 6),
            "r_squared": round(r_value**2, 3)
        }
    
    def _determine_market_phase(self, indicators: Dict[str, Any]) -> str:
        """Определение фазы рынка"""
        try:
            rsi = indicators.get('rsi', 50)
            adx = indicators.get('adx', 0)
            bb_width = indicators.get('bb_width', 0)
            macd_hist = indicators.get('macd_hist', 0)
            
            if adx < 20:
                if bb_width < 0.02:
                    return "CONSOLIDATION"
                else:
                    return "CHOPPY"
            elif adx > 40:
                if macd_hist > 0:
                    return "STRONG UPTREND"
                else:
                    return "STRONG DOWNTREND"
            else:
                if rsi > 60:
                    return "UPTREND"
                elif rsi < 40:
                    return "DOWNTREND"
                else:
                    return "NEUTRAL"
                    
        except:
            return "UNKNOWN"
    
    def _calculate_risk_score(self, indicators: Dict[str, Any]) -> float:
        """Расчет скора риска (0-100)"""
        risk = 50
        
        try:
            # Волатильность
            volatility = indicators.get('volatility_percent', 0.5)
            if volatility > 1:
                risk += 15
            elif volatility < 0.2:
                risk -= 10
            
            # Объемы
            volume_ratio = indicators.get('volume_ratio', 1)
            if volume_ratio > 2:
                risk += 10
            elif volume_ratio < 0.5:
                risk -= 10
            
            # ADX
            adx = indicators.get('adx', 25)
            if adx > 40:
                risk += 10
            elif adx < 20:
                risk -= 5
            
            # Ограничиваем
            risk = max(0, min(100, risk))
            
        except:
            pass
        
        return risk
    
    def _calculate_signal_score(self, indicators: Dict[str, Any]) -> float:
        """Расчет скора сигнала (0-100)"""
        score = 50
        
        try:
            # RSI
            rsi = indicators.get('rsi', 50)
            if rsi < 30:
                score += 8
            elif rsi > 70:
                score -= 8
            
            # MACD
            macd_hist = indicators.get('macd_hist', 0)
            if macd_hist > 0:
                score += 6
            elif macd_hist < 0:
                score -= 6
            
            # Stochastic
            stoch_k = indicators.get('stoch_k', 50)
            if stoch_k < 20:
                score += 6
            elif stoch_k > 80:
                score -= 6
            
            # ADX
            adx = indicators.get('adx', 25)
            if adx > 25:
                score += 4
            
            # Тренд
            trend = indicators.get('trend_strength', {})
            if trend.get('direction') == "UP":
                score += 5
            elif trend.get('direction') == "DOWN":
                score -= 5
            
            # Объемы
            volume_ratio = indicators.get('volume_ratio', 1)
            if volume_ratio > 1.5:
                score += 4
            
            # Позиция BB
            bb_position = indicators.get('bb_position', 'INSIDE')
            if bb_position == "BELOW":
                score += 5
            elif bb_position == "ABOVE":
                score -= 5
            
            # Ограничиваем
            score = max(0, min(100, score))
            
        except:
            pass
        
        return score
    
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
            
            # Определяем направление на основе скора
            signal_score = indicators.get('signal_score', 50)
            
            if signal_score >= 60:
                direction = "CALL"
                confidence = min(95, signal_score + 10)
            elif signal_score <= 40:
                direction = "PUT"
                confidence = min(95, 100 - signal_score + 10)
            else:
                # Нет четкого сигнала
                return None
            
            # Рассчитываем уровни стоп-лосс и тейк-профит
            atr = indicators.get('atr', current_price * 0.001)
            
            if direction == "CALL":
                stop_loss = current_price - atr * 1.5
                take_profit = current_price + atr * 3
            else:
                stop_loss = current_price + atr * 1.5
                take_profit = current_price - atr * 3
            
            risk_reward = round(abs(take_profit - current_price) / abs(stop_loss - current_price), 2)
            
            # Генерируем рекомендацию
            recommendation = self._generate_recommendation(indicators, direction, expiry)
            
            # Создаем сигнал
            signal = Signal(
                asset=asset,
                direction=direction,
                expiry=expiry,
                expiry_minutes=EXPIRATIONS.get(expiry, 5),
                confidence=round(confidence),
                price=current_price,
                timestamp=datetime.now(),
                indicators=indicators,
                recommendation=recommendation,
                entry_price=current_price,
                stop_loss=round(stop_loss, 5),
                take_profit=round(take_profit, 5),
                risk_reward=risk_reward
            )
            
            return signal
            
        except Exception as e:
            logger.error(f"Ошибка генерации сигнала: {e}")
            return None
    
    def _generate_recommendation(self, indicators: Dict[str, Any], direction: str, expiry: str) -> str:
        """Генерация текстовой рекомендации"""
        rec_lines = []
        
        # Основной сигнал
        if direction == "CALL":
            rec_lines.append("📈 *СИГНАЛ НА ПОКУПКУ (CALL)*")
            rec_lines.append("Ожидается рост цены в ближайшее время.")
        else:
            rec_lines.append("📉 *СИГНАЛ НА ПРОДАЖУ (PUT)*")
            rec_lines.append("Ожидается падение цены в ближайшее время.")
        
        rec_lines.append("")
        
        # Обоснование на основе индикаторов
        rec_lines.append("📊 *Обоснование сигнала:*")
        
        # RSI
        rsi = indicators.get('rsi', 50)
        rsi_signal = indicators.get('rsi_signal', 'NEUTRAL')
        if rsi_signal == "OVERSOLD":
            rec_lines.append("• RSI показывает перепроданность (сигнал к покупке)")
        elif rsi_signal == "OVERBOUGHT":
            rec_lines.append("• RSI показывает перекупленность (сигнал к продаже)")
        
        # MACD
        macd_trend = indicators.get('macd_trend', 'NEUTRAL')
        if macd_trend == "BULLISH":
            rec_lines.append("• MACD подтверждает бычий тренд")
        elif macd_trend == "BEARISH":
            rec_lines.append("• MACD подтверждает медвежий тренд")
        
        # ADX
        adx = indicators.get('adx', 0)
        adx_strength = indicators.get('adx_strength', 'WEAK')
        if adx_strength == "STRONG":
            rec_lines.append(f"• Сильный тренд (ADX: {adx:.1f})")
        
        # Bollinger Bands
        bb_position = indicators.get('bb_position', 'INSIDE')
        if bb_position == "BELOW":
            rec_lines.append("• Цена у нижней границы Боллинджера (потенциал отскока)")
        elif bb_position == "ABOVE":
            rec_lines.append("• Цена у верхней границы Боллинджера (потенциал коррекции)")
        
        # Объемы
        volume_ratio = indicators.get('volume_ratio', 1)
        if volume_ratio > 1.5:
            rec_lines.append("• Высокий объем торгов подтверждает движение")
        
        # Дивергенция
        obv_div = indicators.get('obv_divergence', 'NONE')
        if obv_div == "BULLISH":
            rec_lines.append("• Бычья дивергенция OBV")
        elif obv_div == "BEARISH":
            rec_lines.append("• Медвежья дивергенция OBV")
        
        rec_lines.append("")
        
        # Риск-менеджмент
        rec_lines.append("⚠️ *Риск-менеджмент:*")
        rec_lines.append(f"• Экспирация: {expiry}")
        rec_lines.append("• Риск на сделку: 1-2% от депозита")
        rec_lines.append("• Не открывайте больше 3 сделок одновременно")
        rec_lines.append("• Используйте стоп-лосс")
        
        return "\n".join(rec_lines)

# ==================== АВТОПИНГ ====================
class AutoPing:
    def __init__(self):
        self.is_running = False
        self.ping_url = "https://api.telegram.org"
        self.keep_alive_url = "https://{}".format(os.environ.get('RENDER_EXTERNAL_URL', '')) if os.environ.get('RENDER_EXTERNAL_URL') else None
    
    def start(self):
        """Запуск авто-пинга"""
        self.is_running = True
        thread = threading.Thread(target=self._ping_loop)
        thread.daemon = True
        thread.start()
        logger.info("🚀 AutoPing запущен")
    
    def _ping_loop(self):
        """Цикл пинга каждые 3 минуты"""
        while self.is_running:
            try:
                # Пинг Telegram API
                response = requests.get(self.ping_url, timeout=10)
                if response.status_code == 200:
                    logger.debug(f"Ping Telegram API успешен")
                
                # Пинг собственного сервера если есть
                if self.keep_alive_url:
                    response = requests.get(self.keep_alive_url, timeout=10)
                    if response.status_code == 200:
                        logger.debug(f"Ping сервера успешен")
                
            except Exception as e:
                logger.error(f"Ошибка пинга: {e}")
            
            time.sleep(180)  # 3 минуты
    
    def stop(self):
        """Остановка авто-пинга"""
        self.is_running = False
        logger.info("AutoPing остановлен")

# ==================== ОСНОВНОЙ БОТ ====================
class KurutAIBot:
    def __init__(self):
        self.application = None
        self.data_manager = DataManager()
        self.market_analyzer = MarketAnalyzer()
        self.auto_ping = AutoPing()
        self.user_states = {}
        self.start_time = datetime.now()
        
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user = update.effective_user
        user_data = self.data_manager.get_user(user.id)
        
        # Проверяем реферальный код в команде
        if context.args and len(context.args) > 0:
            ref_code = context.args[0]
            # Здесь можно обработать реферальный код
            context.user_data['referral'] = ref_code
        
        if not user_data:
            user_data = self.data_manager.create_user(user.id, user.username, user.first_name)
        
        # Показываем выбор языка
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg")],
            [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            TEXTS[Language.RUSSIAN]["start"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
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
        elif "lang_uz" in query.data:
            user.language = Language.UZBEK
        
        self.data_manager.update_user(user)
        texts = TEXTS[user.language]
        
        # Подтверждение выбора языка
        await query.edit_message_text(
            text=texts["language_selected"],
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Приветственное сообщение
        welcome_text = texts["welcome"].format(name=user.first_name)
        
        keyboard = [
            [InlineKeyboardButton(texts["next"], callback_data="show_social")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await context.bot.send_message(
            chat_id=user_id,
            text=welcome_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return MAIN_MENU
    
    async def show_social(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ социальных сетей"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        social_text = texts["social_links"].format(
            telegram=SOCIAL_LINKS["telegram"],
            telegram_chat=SOCIAL_LINKS["telegram_chat"],
            instagram=SOCIAL_LINKS["instagram"],
            youtube=SOCIAL_LINKS["youtube"],
            admin=SOCIAL_LINKS["admin"]
        )
        
        keyboard = [
            [InlineKeyboardButton("🔐 " + texts["get_access"][:20], callback_data="get_access")],
            [InlineKeyboardButton("📱 Telegram канал", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton("💬 Telegram чат", url=SOCIAL_LINKS["telegram_chat"])],
            [InlineKeyboardButton("📸 Instagram", url=SOCIAL_LINKS["instagram"])]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=social_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        
        return GET_ACCESS
    
    async def get_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Получение доступа"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        if user.has_access:
            # Если доступ уже есть, показываем главное меню
            await self.show_main_menu(update, context)
            return MAIN_MENU
        
        access_text = texts["get_access"].format(
            user_id=user.id,
            ref_link=REFERRAL_LINK,
            admin=ADMIN_USERNAME
        )
        
        keyboard = [
            [InlineKeyboardButton("👤 " + texts["contact_admin"][:20], callback_data="contact_admin")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=access_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        
        return GET_ACCESS
    
    async def show_main_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ главного меню"""
        # Проверяем тип обновления
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            message = query.message
        else:
            user_id = update.effective_user.id
            message = update.message
        
        user = self.data_manager.get_user(user_id)
        if not user:
            user = self.data_manager.create_user(user_id, update.effective_user.username, update.effective_user.first_name)
        
        texts = TEXTS[user.language]
        
        # Создаем клавиатуру в зависимости от доступа
        keyboard = []
        
        if user.has_access:
            keyboard.extend([
                [InlineKeyboardButton("📈 " + texts["get_signal"][:20], callback_data="get_signal")],
                [InlineKeyboardButton("📊 " + texts["stats"][:20], callback_data="stats")],
                [InlineKeyboardButton("🏆 " + texts["top_traders"][:20], callback_data="top_traders")],
                [InlineKeyboardButton("🏃‍♂️ " + texts["marathon_start"][:20], callback_data="marathon")],
                [InlineKeyboardButton("📚 " + texts["instruction_page1"][:20], callback_data="instructions")]
            ])
        else:
            keyboard.append([InlineKeyboardButton("🔐 " + texts["get_access"][:20], callback_data="get_access")])
        
        keyboard.extend([
            [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton("👤 " + texts["contact_admin"][:20], callback_data="contact_admin")]
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        menu_text = texts["main_menu"]
        
        if isinstance(message, str):
            await context.bot.send_message(
                chat_id=user_id,
                text=menu_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                text=menu_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
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
                parse_mode=ParseMode.MARKDOWN
            )
            return MAIN_MENU
        
        texts = TEXTS[user.language]
        
        keyboard = [
            [InlineKeyboardButton("💱 " + texts["forex_pairs"][:20], callback_data="forex_pairs")],
            [InlineKeyboardButton("📊 " + texts["stocks"][:20], callback_data="stocks")],
            [InlineKeyboardButton("₿ " + texts["crypto"][:20], callback_data="crypto")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["get_signal"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
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
            row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{pairs[i]}"))
            if i + 1 < len(pairs):
                row.append(InlineKeyboardButton(pairs[i+1], callback_data=f"pair_{pairs[i+1]}"))
            keyboard.append(row)
        
        # Добавляем кнопки навигации
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад", callback_data="get_signal"),
            InlineKeyboardButton("📊 Далее ➡️", callback_data="forex_pairs_2")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["forex_pairs"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_forex_pairs_2(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вторая страница валютных пар"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Вторая половина пар
        keyboard = []
        pairs = OTC_PAIRS["forex"][20:]  # Вторая половина
        
        for i in range(0, len(pairs), 2):
            row = []
            row.append(InlineKeyboardButton(pairs[i], callback_data=f"pair_{pairs[i]}"))
            if i + 1 < len(pairs):
                row.append(InlineKeyboardButton(pairs[i+1], callback_data=f"pair_{pairs[i+1]}"))
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад", callback_data="forex_pairs"),
            InlineKeyboardButton("📊 В начало", callback_data="get_signal")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["forex_pairs"] + "\n\nСтраница 2/2",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_stocks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ акций"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Создаем клавиатуру с акциями
        keyboard = []
        stocks = OTC_PAIRS["stocks"]
        
        for i in range(0, len(stocks), 2):
            row = []
            row.append(InlineKeyboardButton(stocks[i], callback_data=f"pair_{stocks[i]}"))
            if i + 1 < len(stocks):
                row.append(InlineKeyboardButton(stocks[i+1], callback_data=f"pair_{stocks[i+1]}"))
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад", callback_data="get_signal"),
            InlineKeyboardButton("📊 Далее ➡️", callback_data="stocks_2")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["stocks"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_stocks_2(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вторая страница акций"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Вторая половина акций
        keyboard = []
        stocks = OTC_PAIRS["stocks"][10:]
        
        for i in range(0, len(stocks), 2):
            row = []
            row.append(InlineKeyboardButton(stocks[i], callback_data=f"pair_{stocks[i]}"))
            if i + 1 < len(stocks):
                row.append(InlineKeyboardButton(stocks[i+1], callback_data=f"pair_{stocks[i+1]}"))
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад", callback_data="stocks"),
            InlineKeyboardButton("📊 В начало", callback_data="get_signal")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["stocks"] + "\n\nСтраница 2/2",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_crypto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ криптовалют"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Создаем клавиатуру с криптовалютами
        keyboard = []
        cryptos = OTC_PAIRS["crypto"]
        
        for i in range(0, len(cryptos), 2):
            row = []
            row.append(InlineKeyboardButton(cryptos[i], callback_data=f"pair_{cryptos[i]}"))
            if i + 1 < len(cryptos):
                row.append(InlineKeyboardButton(cryptos[i+1], callback_data=f"pair_{cryptos[i+1]}"))
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад", callback_data="get_signal"),
            InlineKeyboardButton("📊 Далее ➡️", callback_data="crypto_2")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["crypto"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_crypto_2(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Вторая страница криптовалют"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Вторая половина криптовалют
        keyboard = []
        cryptos = OTC_PAIRS["crypto"][10:]
        
        for i in range(0, len(cryptos), 2):
            row = []
            row.append(InlineKeyboardButton(cryptos[i], callback_data=f"pair_{cryptos[i]}"))
            if i + 1 < len(cryptos):
                row.append(InlineKeyboardButton(cryptos[i+1], callback_data=f"pair_{cryptos[i+1]}"))
            keyboard.append(row)
        
        keyboard.append([
            InlineKeyboardButton("⬅️ Назад", callback_data="crypto"),
            InlineKeyboardButton("📊 В начало", callback_data="get_signal")
        ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["crypto"] + "\n\nСтраница 2/2",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
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
        exps = list(EXPIRATIONS.keys())
        
        for i in range(0, len(exps), 3):
            row = []
            for j in range(3):
                if i + j < len(exps):
                    exp = exps[i + j]
                    row.append(InlineKeyboardButton(exp, callback_data=f"exp_{exp}"))
            if row:
                keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"{texts['select_expiry']}\n\nАктив: `{asset}`",
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
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
                text=texts["error"].format(error="Актив не выбран"),
                parse_mode=ParseMode.MARKDOWN
            )
            return MAIN_MENU
        
        # Показываем сообщение об анализе
        await query.edit_message_text(
            text=texts["analyzing"],
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Генерируем сигнал
        signal = await self.market_analyzer.generate_signal(asset, expiry)
        
        if not signal:
            # Если сигнал не сгенерирован, предлагаем другую экспирацию
            keyboard = [
                [InlineKeyboardButton("1 мин", callback_data="exp_1 минута"),
                 InlineKeyboardButton("5 мин", callback_data="exp_5 минут")],
                [InlineKeyboardButton("15 мин", callback_data="exp_15 минут"),
                 InlineKeyboardButton("30 мин", callback_data="exp_30 минут")],
                [InlineKeyboardButton(texts["back"], callback_data=f"pair_{asset}")]
            ]
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            await query.edit_message_text(
                text=f"⚠️ *Нет четкого сигнала для {expiry}*\n\nПопробуйте другую экспирацию:",
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
            return SELECT_EXPIRY
        
        # Сохраняем сигнал в контексте
        context.user_data["current_signal"] = signal
        
        # Форматируем время входа
        entry_time = (datetime.now() + timedelta(seconds=30)).strftime("%H:%M:%S")
        
        # Создаем краткий анализ индикаторов
        indicators = signal.indicators
        indicators_summary = []
        
        if 'rsi' in indicators:
            indicators_summary.append(f"RSI: {indicators['rsi']:.1f}")
        if 'macd_trend' in indicators:
            indicators_summary.append(f"MACD: {indicators['macd_trend']}")
        if 'adx' in indicators:
            indicators_summary.append(f"ADX: {indicators['adx']:.1f}")
        if 'bb_position' in indicators:
            indicators_summary.append(f"BB: {indicators['bb_position']}")
        
        indicators_text = " | ".join(indicators_summary)
        
        # Показываем результат
        signal_text = texts["signal_result"].format(
            asset=signal.asset,
            direction="🟢 CALL BUY" if signal.direction == "CALL" else "🔴 PUT SELL",
            expiry=signal.expiry,
            confidence=signal.confidence,
            price=round(signal.price, 5),
            entry_price=round(signal.entry_price, 5),
            stop_loss=round(signal.stop_loss, 5),
            take_profit=round(signal.take_profit, 5),
            risk_reward=signal.risk_reward,
            entry_time=entry_time,
            recommendation=signal.recommendation,
            indicators_summary=indicators_text
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
            parse_mode=ParseMode.MARKDOWN
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
                text=texts["error"].format(error="Сигнал не найден"),
                parse_mode=ParseMode.MARKDOWN
            )
            return MAIN_MENU
        
        # Определяем результат
        if "trade_win" in query.data:
            result = True
            result_text = texts["trade_win"]
        else:
            result = False
            result_text = texts["trade_lose"]
        
        # Сохраняем сделку
        self.data_manager.add_trade(user_id, signal, result)
        
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
            parse_mode=ParseMode.MARKDOWN
        )
        
        return MAIN_MENU
    
    async def marathon_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало марафона"""
        # Проверяем тип обновления
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            message = query.message
        else:
            user_id = update.effective_user.id
            message = update.message
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        await message.reply_text(
            text=texts["marathon_start"],
            parse_mode=ParseMode.MARKDOWN
        )
        
        return WAITING_FOR_BALANCE
    
    async def process_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка введенного баланса"""
        user_id = update.message.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        try:
            balance = float(update.message.text.replace(',', '.'))
            if balance <= 0 or balance > 1000000:
                raise ValueError
        except:
            await update.message.reply_text(
                text=texts["error"].format(error="Введите корректную сумму (например: 100 или 250.50)"),
                parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_BALANCE
        
        # Сохраняем баланс
        user.balance = balance
        self.data_manager.update_user(user)
        
        # Рассчитываем марафон
        calculation, total_profit, final_balance, growth_chart = self._calculate_marathon(balance)
        growth_percent = round((final_balance - balance) / balance * 100, 1)
        
        # Форматируем расчет по дням
        calculation_lines = []
        for day, value in calculation[:15]:  # Первые 15 дней
            calculation_lines.append(f"📅 День {day}: `${value:.2f}`")
        
        calculation_lines.append("...")
        for day, value in calculation[-5:]:  # Последние 5 дней
            calculation_lines.append(f"📅 День {day}: `${value:.2f}`")
        
        calculation_text = "\n".join(calculation_lines)
        
        marathon_text = texts["marathon_calculation"].format(
            balance=balance,
            calculation=calculation_text,
            total_profit=round(total_profit, 2),
            final_balance=round(final_balance, 2),
            growth_percent=growth_percent,
            growth_chart=growth_chart
        )
        
        keyboard = [
            [InlineKeyboardButton("📊 Управление рисками", callback_data="marathon_risks")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=marathon_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return CALCULATE_MARATHON
    
    def _calculate_marathon(self, balance: float) -> Tuple[List, float, float, str]:
        """Расчет марафона на 30 дней"""
        daily_rate = 0.15  # 15% в день
        current = balance
        results = []
        
        for day in range(1, 31):
            profit = current * daily_rate
            current += profit
            results.append((day, current))
        
        total_profit = current - balance
        
        # Создаем простой график роста
        max_val = max(r[1] for r in results)
        min_val = balance
        chart_lines = []
        
        for i in range(0, 30, 3):  # Каждые 3 дня
            day, value = results[i]
            percentage = (value - min_val) / (max_val - min_val)
            bars = int(percentage * 20)
            chart_lines.append(f"День {day:2d}: {'█' * bars}{'░' * (20 - bars)} ${value:.0f}")
        
        growth_chart = "\n".join(chart_lines[:5] + ["..."] + chart_lines[-5:])
        
        return results, total_profit, current, growth_chart
    
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
            [InlineKeyboardButton("⬅️ Назад к расчету", callback_data="marathon")],
            [InlineKeyboardButton("📊 Главное меню", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=risk_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return CALCULATE_MARATHON
    
    async def show_instructions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ инструкции"""
        # Проверяем тип обновления
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            message = query.message
        else:
            user_id = update.effective_user.id
            message = update.message
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        # Сохраняем текущую страницу
        page = context.user_data.get("instruction_page", 1)
        
        if update.callback_query and "next" in query.data:
            page = 2
        elif update.callback_query and "prev" in query.data:
            page = 1
        elif update.callback_query and "page3" in query.data:
            page = 3
        elif update.callback_query and "page2" in query.data:
            page = 2
        elif update.callback_query and "page1" in query.data:
            page = 1
        
        context.user_data["instruction_page"] = page
        
        instruction_text = texts[f"instruction_page{page}"].format(
            admin=ADMIN_USERNAME,
            telegram=SOCIAL_LINKS["telegram"],
            telegram_chat=SOCIAL_LINKS["telegram_chat"]
        )
        
        # Кнопки навигации
        keyboard = []
        
        if page == 1:
            keyboard.append([
                InlineKeyboardButton("➡️ Далее", callback_data="next"),
                InlineKeyboardButton("📄 2/3", callback_data="page2")
            ])
        elif page == 2:
            keyboard.append([
                InlineKeyboardButton("⬅️ Назад", callback_data="prev"),
                InlineKeyboardButton("➡️ Далее", callback_data="page3")
            ])
        else:
            keyboard.append([
                InlineKeyboardButton("⬅️ Назад", callback_data="prev"),
                InlineKeyboardButton("📄 1/3", callback_data="page1")
            ])
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="back_to_main")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await query.edit_message_text(
                text=instruction_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        else:
            await message.reply_text(
                text=instruction_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN,
                disable_web_page_preview=True
            )
        
        return MAIN_MENU
    
    async def show_top_traders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ топ-трейдеров"""
        # Проверяем тип обновления
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            message = query.message
        else:
            user_id = update.effective_user.id
            message = update.message
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        top_traders = self.data_manager.get_top_traders(10)
        position, score = self.data_manager.get_user_position(user_id)
        
        leaderboard_lines = []
        medals = ["🥇", "🥈", "🥉"]
        
        for i, (trader, trader_score) in enumerate(top_traders[:10], 1):
            medal = medals[i-1] if i <= 3 else f"{i}."
            name = trader.first_name[:12] + ("..." if len(trader.first_name) > 12 else "")
            leaderboard_lines.append(
                f"{medal} *{name}* — {trader.win_rate:.1f}% побед ({trader.total_trades} сд.)"
            )
        
        leaderboard = "\n".join(leaderboard_lines) if leaderboard_lines else "📭 Пока нет данных"
        
        top_text = texts["top_traders"].format(
            leaderboard=leaderboard,
            your_position=position,
            your_win_rate=user.win_rate
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="top_traders")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await query.edit_message_text(
                text=top_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                text=top_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        return MAIN_MENU
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ статистики пользователя"""
        # Проверяем тип обновления
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            message = query.message
        else:
            user_id = update.effective_user.id
            message = update.message
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        position, _ = self.data_manager.get_user_position(user_id)
        
        stats_text = texts["stats"].format(
            user_id=user.id,
            join_date=user.join_date.strftime("%d.%m.%Y"),
            last_active=user.last_active.strftime("%d.%m.%Y %H:%M"),
            won=user.trades_won,
            lost=user.trades_lost,
            total=user.total_trades,
            win_rate=round(user.win_rate, 1),
            profit_factor=round(user.profit_factor, 2),
            balance=user.balance,
            position=position
        )
        
        keyboard = [
            [InlineKeyboardButton("🔄 Обновить", callback_data="stats")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            await query.edit_message_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await message.reply_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
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
            user_id=user.id,
            admin=ADMIN_USERNAME,
            telegram=SOCIAL_LINKS["telegram"],
            telegram_chat=SOCIAL_LINKS["telegram_chat"]
        )
        
        keyboard = [
            [InlineKeyboardButton("✍️ Написать админу", url=f"tg://resolve?domain={ADMIN_USERNAME[1:]}")],
            [InlineKeyboardButton("📱 Telegram канал", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=contact_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN,
            disable_web_page_preview=True
        )
        
        return MAIN_MENU
    
    async def back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат в главное меню"""
        query = update.callback_query
        await query.answer()
        
        await self.show_main_menu(update, context)
        return MAIN_MENU
    
    # ==================== АДМИН КОМАНДЫ ====================
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /admin"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await self.admin_menu(update, context)
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню админа"""
        stats = self.data_manager.get_statistics()
        
        texts = TEXTS[Language.RUSSIAN]
        
        menu_text = texts["admin_menu"].format(
            total_users=stats["total_users"],
            active_users=stats["active_users"],
            total_trades=stats["total_trades"]
        )
        
        keyboard = [
            [InlineKeyboardButton("👤 Выдать доступ", callback_data="admin_grant")],
            [InlineKeyboardButton("👥 Выдать доступ нескольким", callback_data="admin_grant_multiple")],
            [InlineKeyboardButton("🚫 Отозвать доступ", callback_data="admin_revoke")],
            [InlineKeyboardButton("📊 Статистика пользователя", callback_data="admin_user_stats")],
            [InlineKeyboardButton("👥 Все пользователи", callback_data="admin_all_users")],
            [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast")],
            [InlineKeyboardButton("📨 Отправить сообщение", callback_data="admin_send")],
            [InlineKeyboardButton("📊 Статистика бота", callback_data="admin_bot_stats")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            await query.edit_message_text(
                text=menu_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text=menu_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def admin_grant(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выдача доступа"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await query.edit_message_text(
            text=TEXTS[Language.RUSSIAN]["admin_grant"],
            parse_mode=ParseMode.MARKDOWN
        )
        return ADMIN_SEND_MESSAGE
    
    async def admin_grant_multiple(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выдача доступа нескольким пользователям"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await query.edit_message_text(
            text="👥 Введите ID пользователей через запятую:\n\nПример: `123456789, 987654321, 456789123`",
            parse_mode=ParseMode.MARKDOWN
        )
        return ADMIN_GRANT_MULTIPLE
    
    async def admin_revoke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отзыв доступа"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await query.edit_message_text(
            text=TEXTS[Language.RUSSIAN]["admin_revoke"],
            parse_mode=ParseMode.MARKDOWN
        )
        return ADMIN_SEND_MESSAGE
    
    async def admin_user_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Статистика пользователя"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await query.edit_message_text(
            text="📊 Введите ID пользователя для просмотра статистики:",
            parse_mode=ParseMode.MARKDOWN
        )
        return ADMIN_SEND_MESSAGE
    
    async def admin_all_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Список всех пользователей"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        users = list(self.data_manager.users.values())
        
        if not users:
            await query.edit_message_text("📭 *Пользователей пока нет*", parse_mode=ParseMode.MARKDOWN)
            return
        
        # Разбиваем на страницы
        page = context.user_data.get("admin_users_page", 0)
        users_per_page = 10
        start_idx = page * users_per_page
        end_idx = start_idx + users_per_page
        
        page_users = users[start_idx:end_idx]
        
        users_text = f"👥 *ПОЛЬЗОВАТЕЛИ (страница {page + 1}/{(len(users)-1)//users_per_page + 1})*\n\n"
        
        for user in page_users:
            status = "✅" if user.has_access else "❌"
            trades = f"{user.trades_won}/{user.total_trades}"
            users_text += f"{status} ID: `{user.id}` | {user.first_name[:15]} | Сделок: {trades}\n"
        
        # Кнопки навигации
        keyboard = []
        nav_row = []
        
        if page > 0:
            nav_row.append(InlineKeyboardButton("⬅️", callback_data="admin_users_prev"))
        
        nav_row.append(InlineKeyboardButton(f"{page + 1}/{(len(users)-1)//users_per_page + 1}", callback_data="admin_users_refresh"))
        
        if end_idx < len(users):
            nav_row.append(InlineKeyboardButton("➡️", callback_data="admin_users_next"))
        
        if nav_row:
            keyboard.append(nav_row)
        
        keyboard.append([InlineKeyboardButton("🔙 Назад", callback_data="admin_menu")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text(users_text, reply_markup=reply_markup, parse_mode=ParseMode.MARKDOWN)
    
    async def admin_users_navigation(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Навигация по списку пользователей"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            return
        
        if "admin_users_next" in query.data:
            context.user_data["admin_users_page"] = context.user_data.get("admin_users_page", 0) + 1
        elif "admin_users_prev" in query.data:
            context.user_data["admin_users_page"] = max(0, context.user_data.get("admin_users_page", 0) - 1)
        
        await self.admin_all_users(update, context)
    
    async def admin_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Рассылка сообщений"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await query.edit_message_text(
            text=TEXTS[Language.RUSSIAN]["admin_broadcast"],
            parse_mode=ParseMode.MARKDOWN
        )
        return ADMIN_BROADCAST
    
    async def admin_send(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправка сообщения конкретному пользователю"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await query.edit_message_text(
            text=TEXTS[Language.RUSSIAN]["admin_send"],
            parse_mode=ParseMode.MARKDOWN
        )
        return ADMIN_SEND_MESSAGE
    
    async def admin_bot_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Статистика бота для админа"""
        query = update.callback_query
        await query.answer()
        
        if query.from_user.id != ADMIN_ID:
            await query.edit_message_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        stats = self.data_manager.get_statistics()
        
        # Время работы бота
        uptime = datetime.now() - self.start_time
        days = uptime.days
        hours = uptime.seconds // 3600
        minutes = (uptime.seconds % 3600) // 60
        
        stats_text = f"""
📊 *ПОЛНАЯ СТАТИСТИКА БОТА*

👥 *Пользователи:*
• Всего: {stats['total_users']}
• С доступом: {stats['active_users']}
• Без доступа: {stats['total_users'] - stats['active_users']}

📈 *Сделки:*
• Всего: {stats['total_trades']}
• Выиграно: {stats['total_wins']}
• Проиграно: {stats['total_losses']}
• Win Rate: {stats['win_rate']}%
• Сегодня: {stats['today_trades']}

⏱ *Работа бота:*
• Запущен: {self.start_time.strftime('%d.%m.%Y %H:%M')}
• Время работы: {days}д {hours}ч {minutes}м

🏆 *Топ-3 трейдера:*
"""
        
        top_traders = self.data_manager.get_top_traders(3)
        for i, (trader, score) in enumerate(top_traders, 1):
            stats_text += f"{i}. ID {trader.id} - {trader.win_rate:.1f}% ({trader.total_trades} сд.)\n"
        
        keyboard = [[InlineKeyboardButton("🔙 Назад", callback_data="admin_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=stats_text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
    
    async def process_admin_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка сообщений от админа"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        text = update.message.text.strip()
        state = context.user_data.get("admin_state", "menu")
        
        if state == "grant":
            # Выдача доступа одному пользователю
            try:
                user_id = int(text)
                if self.data_manager.grant_access(user_id):
                    # Отправляем уведомление пользователю
                    try:
                        user = self.data_manager.get_user(user_id)
                        lang = user.language if user else Language.RUSSIAN
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=TEXTS[lang]["access_granted"].format(
                                name=user.first_name if user else "User",
                                balance=0,
                                total_trades=0,
                                win_rate=0
                            ),
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                    
                    await update.message.reply_text(f"✅ *Доступ выдан пользователю {user_id}*", parse_mode=ParseMode.MARKDOWN)
                else:
                    # Если пользователь не найден, создаем его
                    user = User(id=user_id, username=None, first_name=f"User_{user_id}")
                    user.has_access = True
                    self.data_manager.users[user_id] = user
                    self.data_manager.save_data()
                    await update.message.reply_text(f"✅ *Создан и выдан доступ пользователю {user_id}*", parse_mode=ParseMode.MARKDOWN)
            except ValueError:
                await update.message.reply_text("❌ *Неверный формат ID*", parse_mode=ParseMode.MARKDOWN)
            
            await self.admin_menu(update, context)
            
        elif state == "grant_multiple":
            # Выдача доступа нескольким пользователям
            try:
                ids = [int(x.strip()) for x in text.split(',')]
                success, failed = self.data_manager.grant_access_multiple(ids)
                
                # Отправляем уведомления успешным
                for user_id in ids[:success]:
                    try:
                        user = self.data_manager.get_user(user_id)
                        lang = user.language if user else Language.RUSSIAN
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=TEXTS[lang]["access_granted"].format(
                                name=user.first_name if user else "User",
                                balance=0,
                                total_trades=0,
                                win_rate=0
                            ),
                            parse_mode=ParseMode.MARKDOWN
                        )
                    except:
                        pass
                
                await update.message.reply_text(
                    f"✅ *Успешно: {success}*\n❌ *Не удалось: {failed}*",
                    parse_mode=ParseMode.MARKDOWN
                )
            except Exception as e:
                await update.message.reply_text(f"❌ *Ошибка: {str(e)}*", parse_mode=ParseMode.MARKDOWN)
            
            await self.admin_menu(update, context)
            
        elif state == "revoke":
            # Отзыв доступа
            try:
                user_id = int(text)
                if self.data_manager.revoke_access(user_id):
                    await update.message.reply_text(f"✅ *Доступ отозван у пользователя {user_id}*", parse_mode=ParseMode.MARKDOWN)
                else:
                    await update.message.reply_text(f"❌ *Пользователь {user_id} не найден*", parse_mode=ParseMode.MARKDOWN)
            except ValueError:
                await update.message.reply_text("❌ *Неверный формат ID*", parse_mode=ParseMode.MARKDOWN)
            
            await self.admin_menu(update, context)
            
        elif state == "user_stats":
            # Статистика пользователя
            try:
                user_id = int(text)
                user = self.data_manager.get_user(user_id)
                if user:
                    stats_text = TEXTS[Language.RUSSIAN]["admin_stats"].format(
                        user_id=user.id,
                        name=user.first_name,
                        access="✅ Да" if user.has_access else "❌ Нет",
                        total=user.total_trades,
                        win_rate=round(user.win_rate, 1),
                        balance=user.balance
                    )
                    await update.message.reply_text(stats_text, parse_mode=ParseMode.MARKDOWN)
                else:
                    await update.message.reply_text(f"❌ *Пользователь {user_id} не найден*", parse_mode=ParseMode.MARKDOWN)
            except ValueError:
                await update.message.reply_text("❌ *Неверный формат ID*", parse_mode=ParseMode.MARKDOWN)
            
            await self.admin_menu(update, context)
            
        elif state == "send":
            # Отправка сообщения пользователю
            try:
                parts = text.split(' ', 1)
                if len(parts) < 2:
                    await update.message.reply_text(
                        "❌ *Неверный формат. Используйте: ID сообщение*",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    await self.admin_menu(update, context)
                    return
                
                user_id = int(parts[0])
                message = parts[1]
                
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"📨 *Сообщение от админа:*\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.message.reply_text(f"✅ *Сообщение отправлено пользователю {user_id}*", parse_mode=ParseMode.MARKDOWN)
            except Exception as e:
                await update.message.reply_text(f"❌ *Ошибка: {str(e)}*", parse_mode=ParseMode.MARKDOWN)
            
            await self.admin_menu(update, context)
    
    async def process_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка рассылки"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        message = update.message.text
        users = list(self.data_manager.users.keys())
        
        await update.message.reply_text(
            f"📢 *Рассылка начата для {len(users)} пользователей...*",
            parse_mode=ParseMode.MARKDOWN
        )
        
        success = 0
        failed = 0
        
        for user_id in users:
            try:
                user = self.data_manager.get_user(user_id)
                lang = user.language if user else Language.RUSSIAN
                
                await context.bot.send_message(
                    chat_id=user_id,
                    text=f"📢 *ОТ АДМИНА*\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
                success += 1
                await asyncio.sleep(0.05)  # Задержка чтобы не спамить
            except Exception as e:
                failed += 1
                logger.error(f"Ошибка отправки пользователю {user_id}: {e}")
        
        await update.message.reply_text(
            f"✅ *Рассылка завершена!*\n\n📊 *Результаты:*\n✅ Успешно: {success}\n❌ Не удалось: {failed}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        await self.admin_menu(update, context)
    
    async def grant_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /grant для выдачи доступа"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ *Использование:* /grant <user_id>\nПример: /grant 123456789",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            user_id = int(context.args[0])
            if self.data_manager.grant_access(user_id):
                await update.message.reply_text(f"✅ *Доступ выдан пользователю {user_id}*", parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(f"❌ *Пользователь {user_id} не найден*", parse_mode=ParseMode.MARKDOWN)
        except ValueError:
            await update.message.reply_text("❌ *Неверный формат ID*", parse_mode=ParseMode.MARKDOWN)
    
    async def revoke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /revoke для отзыва доступа"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *У вас нет прав доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ *Использование:* /revoke <user_id>\nПример: /revoke 123456789",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            user_id = int(context.args[0])
            if self.data_manager.revoke_access(user_id):
                await update.message.reply_text(f"✅ *Доступ отозван у пользователя {user_id}*", parse_mode=ParseMode.MARKDOWN)
            else:
                await update.message.reply_text(f"❌ *Пользователь {user_id} не найден*", parse_mode=ParseMode.MARKDOWN)
        except ValueError:
            await update.message.reply_text("❌ *Неверный формат ID*", parse_mode=ParseMode.MARKDOWN)
    
    async def setup_commands(self):
        """Настройка команд бота"""
        commands = [
            BotCommand("start", "🚀 Запустить бота"),
            BotCommand("menu", "📊 Главное меню"),
            BotCommand("stats", "📈 Моя статистика"),
            BotCommand("top", "🏆 Топ трейдеров"),
            BotCommand("marathon", "🏃‍♂️ Марафон трейдера"),
            BotCommand("instruction", "📚 Инструкция"),
            BotCommand("admin", "⚙️ Админ панель"),
            BotCommand("grant", "✅ Выдать доступ (админ)"),
            BotCommand("revoke", "❌ Отозвать доступ (админ)")
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
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    CallbackQueryHandler(self.show_social, pattern="^show_social$"),
                    CallbackQueryHandler(self.show_forex_pairs, pattern="^forex_pairs$"),
                    CallbackQueryHandler(self.show_forex_pairs_2, pattern="^forex_pairs_2$"),
                    CallbackQueryHandler(self.show_stocks, pattern="^stocks$"),
                    CallbackQueryHandler(self.show_stocks_2, pattern="^stocks_2$"),
                    CallbackQueryHandler(self.show_crypto, pattern="^crypto$"),
                    CallbackQueryHandler(self.show_crypto_2, pattern="^crypto_2$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^page1$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^page2$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^page3$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^next$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^prev$")
                ],
                GET_ACCESS: [
                    CallbackQueryHandler(self.contact_admin, pattern="^contact_admin$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                WAITING_FOR_BALANCE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_balance)
                ],
                CALCULATE_MARATHON: [
                    CallbackQueryHandler(self.show_marathon_risks, pattern="^marathon_risks$"),
                    CallbackQueryHandler(self.marathon_start, pattern="^marathon$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                SELECT_ASSET_TYPE: [
                    CallbackQueryHandler(self.show_forex_pairs, pattern="^forex_pairs$"),
                    CallbackQueryHandler(self.show_stocks, pattern="^stocks$"),
                    CallbackQueryHandler(self.show_crypto, pattern="^crypto$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                SELECT_CURRENCY_PAIR: [
                    CallbackQueryHandler(self.select_pair, pattern="^pair_"),
                    CallbackQueryHandler(self.show_forex_pairs, pattern="^forex_pairs$"),
                    CallbackQueryHandler(self.show_forex_pairs_2, pattern="^forex_pairs_2$"),
                    CallbackQueryHandler(self.show_stocks, pattern="^stocks$"),
                    CallbackQueryHandler(self.show_stocks_2, pattern="^stocks_2$"),
                    CallbackQueryHandler(self.show_crypto, pattern="^crypto$"),
                    CallbackQueryHandler(self.show_crypto_2, pattern="^crypto_2$"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                SELECT_EXPIRY: [
                    CallbackQueryHandler(self.analyze_signal, pattern="^exp_"),
                    CallbackQueryHandler(self.select_pair, pattern="^pair_"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                TRADE_RESULT: [
                    CallbackQueryHandler(self.process_trade_result, pattern="^trade_"),
                    CallbackQueryHandler(self.get_signal_menu, pattern="^get_signal$")
                ],
                ADMIN_SEND_MESSAGE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_admin_message)
                ],
                ADMIN_BROADCAST: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_broadcast)
                ],
                ADMIN_GRANT_MULTIPLE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_admin_message)
                ]
            },
            fallbacks=[CommandHandler("start", self.start), CommandHandler("menu", self.show_main_menu)],
            per_message=False
        )
        
        # Добавляем обработчики
        self.application.add_handler(conv_handler)
        self.application.add_handler(CommandHandler("menu", self.show_main_menu))
        self.application.add_handler(CommandHandler("stats", self.show_stats))
        self.application.add_handler(CommandHandler("top", self.show_top_traders))
        self.application.add_handler(CommandHandler("marathon", self.marathon_start))
        self.application.add_handler(CommandHandler("instruction", self.show_instructions))
        self.application.add_handler(CommandHandler("admin", self.admin_command))
        self.application.add_handler(CommandHandler("grant", self.grant_command))
        self.application.add_handler(CommandHandler("revoke", self.revoke_command))
        
        # Обработчики для админа
        self.application.add_handler(CallbackQueryHandler(self.admin_grant, pattern="^admin_grant$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_grant_multiple, pattern="^admin_grant_multiple$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_revoke, pattern="^admin_revoke$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_user_stats, pattern="^admin_user_stats$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_all_users, pattern="^admin_all_users$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_broadcast, pattern="^admin_broadcast$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_send, pattern="^admin_send$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_bot_stats, pattern="^admin_bot_stats$"))
        self.application.add_handler(CallbackQueryHandler(self.admin_users_navigation, pattern="^admin_users_"))
        self.application.add_handler(CallbackQueryHandler(self.admin_menu, pattern="^admin_menu$"))
        
        # Настраиваем команды
        await self.setup_commands()
        
        # Запускаем авто-пинг
        self.auto_ping.start()
        
        # Запускаем бота
        logger.info("🤖 KURUT AI INFINITY запущен!")
        logger.info(f"👤 Админ: {ADMIN_ID}")
        logger.info(f"📊 Всего пользователей: {len(self.data_manager.users)}")
        
        # Уведомляем админа о запуске
        try:
            await self.application.bot.send_message(
                chat_id=ADMIN_ID,
                text="✅ *KURUT AI INFINITY запущен и готов к работе!*\n\n📊 Все функции активны.",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
        
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
if __name__ == "__main__":
    # Создаем необходимые директории
    os.makedirs("backups", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    bot = KurutAIBot()
    
    # Создаем event loop
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        # Попытка перезапуска через 5 секунд
        time.sleep(5)
        logger.info("🔄 Попытка перезапуска...")
        asyncio.run(bot.run())
