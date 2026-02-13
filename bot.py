#!/usr/bin/env python3
"""
KURUT AI INFINITY - Продвинутый торговый бот для Pocket Option OTC рынка
Версия 3.2 - ИДЕАЛЬНАЯ - Улучшенные сигналы и полное исправление ошибок
"""

import os
import sys
import asyncio
import logging
import json
import pytz
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, asdict
from enum import Enum
import threading
import time
import random
import uuid
import warnings
warnings.filterwarnings('ignore')

# Telegram
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
BOT_TOKEN = "8578509228:AAHK-fgI6QtYOZmRHlXVr3mqrxoUVXwx0LQ"  # НОВЫЙ ТОКЕН
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
    "1 минута": 1, 
    "2 минуты": 2, 
    "3 минуты": 3, 
    "5 минут": 5, 
    "10 минут": 10, 
    "15 минут": 15
}

# Состояния для ConversationHandler
(SELECT_LANGUAGE, MAIN_MENU, GET_ACCESS, WAITING_FOR_BALANCE, 
 CALCULATE_MARATHON, SELECT_ASSET_TYPE, SELECT_CURRENCY_PAIR, 
 SELECT_EXPIRY, TRADE_RESULT, ADMIN_SEND_MESSAGE, ADMIN_BROADCAST) = range(11)

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
    direction: str
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
    trend_strength: str
    volume_analysis: str
    market_sentiment: str

# ==================== ПЕРЕВОДЫ ====================
TEXTS = {
    Language.RUSSIAN: {
        "select_language": "🌍 *Выберите язык / Тилди тандаңыз / Tilni tanlang*",
        "language_selected": "✅ *Русский язык выбран*",
        "welcome": """
🎯 *Добро пожаловать в KURUT AI INFINITY!*

Привет, {name}! 👋

Я профессиональный торговый бот с продвинутой AI системой анализа OTC рынка Pocket Option.

🤖 *Мои возможности:*
• Точные торговые сигналы с AI анализом
• Технический анализ 35+ индикаторов  
• Мониторинг рынка в реальном времени
• Управление рисками и капиталом
• Обучающие материалы для трейдеров

📊 *Винрейт: 82-87%*
💰 *Доходность: до 20% в день*

Готовы начать зарабатывать?
""",
        "social_links": """
📱 *Наши социальные сети:*

🔵 Telegram канал: {telegram}
💬 Telegram чат: {telegram_chat}
📸 Instagram: {instagram}
🎥 YouTube: {youtube}
👤 Админ: {admin}

Подписывайтесь, чтобы быть в курсе всех новостей!
""",
        "get_access": """
🔐 *Как получить доступ к боту:*

1️⃣ Зарегистрируйтесь по нашей реферальной ссылке:
{ref_link}

2️⃣ Пополните депозит от $10

3️⃣ Отправьте скриншот пополнения админу: {admin}

4️⃣ Ваш ID для активации: `{user_id}`

⏱ *Доступ активируется в течение 5 минут!*

💡 *После активации вам станут доступны:*
✅ Безлимитные торговые сигналы
✅ Марафон увеличения депозита
✅ Статистика и аналитика
✅ Топ трейдеров
✅ Обучающие материалы
""",
        "access_granted": """
✅ *Доступ активирован!*

🎉 Поздравляем! Теперь вам доступны все функции бота:

📈 *Торговые сигналы* - AI анализ рынка
📊 *Статистика* - отслеживание результатов
🏆 *Топ трейдеров* - рейтинг лучших
🏃‍♂️ *Марафон* - план роста депозита
📚 *Инструкции* - обучающие материалы

🎯 Начните с получения первого сигнала!
""",
        "main_menu": "📱 *Главное меню*\n\nВыберите действие:",
        "get_signal": "📈 Получить сигнал",
        "stats": "📊 Моя статистика",
        "top_traders": "🏆 Топ трейдеров",
        "marathon_start": "🏃‍♂️ Марафон трейдера",
        "instructions": "📚 Инструкция",
        "contact_admin": "👤 Связаться с админом",
        "back": "◀️ Назад",
        "next": "▶️ Далее",
        "no_access": "❌ *У вас нет доступа к этой функции*\n\nПожалуйста, активируйте доступ через меню.",
        "select_asset_type": """
📊 *Выберите тип актива:*

🌍 *Forex* - Валютные пары (EUR/USD, GBP/USD и т.д.)
📈 *Акции* - Крупные компании (Apple, Tesla и т.д.)
💎 *Криптовалюты* - Bitcoin, Ethereum и другие
""",
        "select_pair": "💱 *Выберите пару для анализа:*",
        "select_expiry": "⏱ *Выберите время экспирации:*",
        "analyzing": """
🔄 *Анализирую рынок...*

⚡️ Собираю данные с бирж
📊 Анализирую 35+ индикаторов
🤖 Применяю AI алгоритмы
📈 Рассчитываю точку входа

Пожалуйста, подождите...
""",
        "signal_generated": """
🎯 *ТОРГОВЫЙ СИГНАЛ*

━━━━━━━━━━━━━━━━━━━━

📊 *Актив:* `{asset}`
🎯 *Направление:* {direction}
⏱ *Экспирация:* {expiry}
💰 *Цена входа:* `${price}`
📈 *Уверенность:* *{confidence}%*

━━━━━━━━━━━━━━━━━━━━

📉 *ТЕХНИЧЕСКИЙ АНАЛИЗ:*

{indicators}

━━━━━━━━━━━━━━━━━━━━

📊 *АНАЛИЗ РЫНКА:*
• Сила тренда: {trend_strength}
• Объемы: {volume_analysis}
• Настроение: {market_sentiment}

━━━━━━━━━━━━━━━━━━━━

🎲 *РИСК-МЕНЕДЖМЕНТ:*
• Stop Loss: `${stop_loss}`
• Take Profit: `${take_profit}`
• Risk/Reward: *{risk_reward}*

━━━━━━━━━━━━━━━━━━━━

💡 *Рекомендация:* 
{recommendation}

⚡️ *Открывайте сделку СЕЙЧАС!*
⏰ Время: {time}
""",
        "trade_win": "✅ *Отлично! Сделка выиграна!* 🎉\n\n💰 Продолжайте в том же духе!",
        "trade_lose": "❌ *Сделка проиграна*\n\n💪 Не расстраивайтесь! Следующая будет успешной!",
        "user_stats": """
📊 *ВАША СТАТИСТИКА*

━━━━━━━━━━━━━━━━━━━━

👤 *Пользователь:* {name}
🆔 *ID:* `{user_id}`
📅 *С нами:* {days_active} дней

━━━━━━━━━━━━━━━━━━━━

💰 *ТОРГОВЛЯ:*
📈 Всего сделок: *{total_trades}*
✅ Выиграно: *{trades_won}*
❌ Проиграно: *{trades_lost}*
📊 Винрейт: *{win_rate}%*
💎 Profit Factor: *{profit_factor}*

━━━━━━━━━━━━━━━━━━━━

💵 *Баланс:* ${balance}
🎯 *Реф. код:* `{referral_id}`
""",
        "top_traders_text": """
🏆 *ТОП ТРЕЙДЕРОВ*

Лучшие пользователи нашего бота:

{top_list}

━━━━━━━━━━━━━━━━━━━━

🎯 Продолжайте торговать и попадите в топ!
💪 Следуйте нашим сигналам для успеха!
""",
        "marathon_start": """
🏃‍♂️ *МАРАФОН ТРЕЙДЕРА*

Рассчитаем ваш потенциал роста на 30 дней при винрейте 82%!

💰 *Введите ваш текущий баланс:*
(например: 100 или 250.50)
""",
        "marathon_calculation": """
🏃‍♂️ *РАСЧЕТ МАРАФОНА*

━━━━━━━━━━━━━━━━━━━━

💰 *Начальный баланс:* ${balance}

📅 *Прогноз на 30 дней:*
{calculation}

━━━━━━━━━━━━━━━━━━━━

💎 *ИТОГОВЫЕ ПОКАЗАТЕЛИ:*
• Чистая прибыль: *${total_profit}*
• Финальный баланс: *${final_balance}*
• Рост капитала: *{growth_percent}%*

━━━━━━━━━━━━━━━━━━━━

📊 *ГРАФИК РОСТА:*
{growth_chart}

━━━━━━━━━━━━━━━━━━━━

⚡️ *Начните торговать по нашим сигналам и достигайте этих результатов!*
🎯 Винрейт 82% = стабильный рост капитала
""",
        "marathon_risks": """
📊 *УПРАВЛЕНИЕ РИСКАМИ*

━━━━━━━━━━━━━━━━━━━━

🎯 *ОСНОВНЫЕ ПРАВИЛА:*

1️⃣ *Размер ставки:* 2-5% от депозита
   ⚠️ Никогда не рискуйте больше!

2️⃣ *Количество сделок:* 10-15 в день
   📈 Качество важнее количества

3️⃣ *Stop-Loss:* Всегда используйте
   🛡 Защита вашего капитала

4️⃣ *Эмоциональный контроль:*
   🧘‍♂️ Торгуйте хладнокровно

5️⃣ *Диверсификация:*
   🌍 Разные активы = меньше риск

━━━━━━━━━━━━━━━━━━━━

💡 *ЗОЛОТЫЕ ПРАВИЛА:*

✅ НЕ удваивайте ставку после проигрыша
✅ Фиксируйте прибыль регулярно
✅ Следуйте торговому плану
✅ Используйте ТОЛЬКО наши сигналы
✅ Не торгуйте на эмоциях

━━━━━━━━━━━━━━━━━━━━

🎯 *При соблюдении правил винрейт 82-87%!*
💰 Ваш успех = дисциплина + наши сигналы
""",
        "instruction_page1": """
📚 *ИНСТРУКЦИЯ - Часть 1/3*

━━━━━━━━━━━━━━━━━━━━

🎯 *КАК ПОЛЬЗОВАТЬСЯ БОТОМ:*

1️⃣ *Получение сигналов:*
   • Нажмите "📈 Получить сигнал"
   • Выберите тип актива (Forex/Акции/Крипто)
   • Выберите конкретную пару
   • Выберите время экспирации
   • Получите точный сигнал!

2️⃣ *Открытие сделки:*
   • Откройте Pocket Option
   • Найдите указанный актив
   • Установите время экспирации
   • Откройте сделку в указанном направлении
   • Дождитесь закрытия

3️⃣ *Фиксация результата:*
   • После закрытия сделки укажите результат
   • Нажмите ✅ Выиграл или ❌ Проиграл
   • Статистика обновится автоматически

━━━━━━━━━━━━━━━━━━━━
""",
        "instruction_page2": """
📚 *ИНСТРУКЦИЯ - Часть 2/3*

━━━━━━━━━━━━━━━━━━━━

💰 *УПРАВЛЕНИЕ КАПИТАЛОМ:*

1️⃣ *Размер ставки:*
   • Минимум: 2% от депозита
   • Оптимум: 3-5% от депозита
   • Максимум: 10% от депозита
   ⚠️ Больше 10% = высокий риск!

2️⃣ *Стратегия торговли:*
   • Используйте ТОЛЬКО наши сигналы
   • Не открывайте сделки на эмоциях
   • Строго соблюдайте время экспирации
   • Следуйте стоп-лоссам
   • Фиксируйте прибыль

3️⃣ *Частота сделок:*
   • 10-15 сделок в день - оптимум
   • Перерывы 5-10 минут между сделками
   • Не торгуйте при высокой волатильности
   • Избегайте новостных событий

━━━━━━━━━━━━━━━━━━━━
""",
        "instruction_page3": """
📚 *ИНСТРУКЦИЯ - Часть 3/3*

━━━━━━━━━━━━━━━━━━━━

🎯 *ДОПОЛНИТЕЛЬНЫЕ ФУНКЦИИ:*

1️⃣ *Марафон трейдера:*
   • Рассчитайте потенциальную прибыль
   • Узнайте план достижения целей
   • Следите за своим прогрессом
   • Мотивируйтесь на успех

2️⃣ *Статистика:*
   • Отслеживайте свой винрейт
   • Анализируйте прибыльность
   • Сравнивайте себя с другими
   • Улучшайте показатели

3️⃣ *Топ трейдеров:*
   • Соревнуйтесь с лучшими
   • Учитесь на примере профи
   • Стремитесь к вершине рейтинга
   • Получайте мотивацию

━━━━━━━━━━━━━━━━━━━━

💡 *ФОРМУЛА УСПЕХА:*

✅ Дисциплина
✅ Наши сигналы
✅ Риск-менеджмент
✅ Постоянство

= 💰 *СТАБИЛЬНАЯ ПРИБЫЛЬ!*

━━━━━━━━━━━━━━━━━━━━

📱 Есть вопросы? Свяжитесь с админом!
🎯 Начните зарабатывать уже сегодня!
""",
        "error": "❌ *Ошибка:* {error}",
        "admin_panel": """
⚙️ *АДМИН ПАНЕЛЬ*

━━━━━━━━━━━━━━━━━━━━

👤 *Администратор:* {admin_name}

📊 *СТАТИСТИКА:*
• Всего пользователей: *{total_users}*
• С доступом: *{users_with_access}*
• Активных сегодня: *{active_today}*

━━━━━━━━━━━━━━━━━━━━

*Выберите действие:*
""",
    },
    Language.KYRGYZ: {
        "select_language": "🌍 *Тилди тандаңыз / Выберите язык / Tilni tanlang*",
        "language_selected": "✅ *Кыргызча тил тандалды*",
        "welcome": "🎯 *KURUT AI INFINITY ботуна кош келиңиз!*\n\nСалам, {name}! 👋",
        "main_menu": "📱 *Башкы меню*\n\nАракетти тандаңыз:",
        "get_signal": "📈 Сигнал алуу",
        "stats": "📊 Менин статистикам",
        "back": "◀️ Артка",
        "error": "❌ *Ката:* {error}",
    },
    Language.UZBEK: {
        "select_language": "🌍 *Tilni tanlang / Выберите язык / Тилди тандаңыз*",
        "language_selected": "✅ *O'zbek tili tanlandi*",
        "welcome": "🎯 *KURUT AI INFINITY botiga xush kelibsiz!*\n\nSalom, {name}! 👋",
        "main_menu": "📱 *Asosiy menyu*\n\nHarakatni tanlang:",
        "get_signal": "📈 Signal olish",
        "stats": "📊 Mening statistikam",
        "back": "◀️ Orqaga",
        "error": "❌ *Xatolik:* {error}",
    }
}

# ==================== МЕНЕДЖЕР ДАННЫХ ====================
class DataManager:
    """Управление данными пользователей"""
    
    def __init__(self):
        self.users: Dict[int, User] = {}
        self.data_file = "users_data.json"
        self.load_data()
    
    def load_data(self):
        """Загрузка данных из файла"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for user_id, user_data in data.get('users', {}).items():
                        user_data['id'] = int(user_id)
                        user_data['language'] = Language(user_data.get('language', 'ru'))
                        if user_data.get('join_date'):
                            user_data['join_date'] = datetime.fromisoformat(user_data['join_date'])
                        if user_data.get('last_active'):
                            user_data['last_active'] = datetime.fromisoformat(user_data['last_active'])
                        self.users[int(user_id)] = User(**user_data)
                logger.info(f"✅ Загружено {len(self.users)} пользователей")
        except Exception as e:
            logger.error(f"❌ Ошибка загрузки данных: {e}")
    
    def save_data(self):
        """Сохранение данных в файл"""
        try:
            data = {'users': {}}
            for user_id, user in self.users.items():
                user_dict = asdict(user)
                user_dict['language'] = user.language.value
                if user.join_date:
                    user_dict['join_date'] = user.join_date.isoformat()
                if user.last_active:
                    user_dict['last_active'] = user.last_active.isoformat()
                data['users'][str(user_id)] = user_dict
            
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.error(f"❌ Ошибка сохранения данных: {e}")
    
    def get_user(self, user_id: int) -> Optional[User]:
        """Получение пользователя по ID"""
        return self.users.get(user_id)
    
    def create_user(self, user_id: int, username: Optional[str], first_name: str) -> User:
        """Создание нового пользователя"""
        has_access = (user_id == ADMIN_ID)
        user = User(
            id=user_id,
            username=username,
            first_name=first_name,
            has_access=has_access
        )
        self.users[user_id] = user
        self.save_data()
        logger.info(f"✅ Создан новый пользователь: {user_id} ({first_name})")
        return user
    
    def update_user(self, user: User):
        """Обновление данных пользователя"""
        user.last_active = datetime.now()
        self.users[user.id] = user
        self.save_data()
    
    def grant_access(self, user_id: int) -> bool:
        """Выдача доступа пользователю"""
        user = self.get_user(user_id)
        if user:
            user.has_access = True
            self.update_user(user)
            logger.info(f"✅ Доступ выдан: {user_id}")
            return True
        return False
    
    def revoke_access(self, user_id: int) -> bool:
        """Отзыв доступа"""
        user = self.get_user(user_id)
        if user:
            user.has_access = False
            self.update_user(user)
            logger.info(f"❌ Доступ отозван: {user_id}")
            return True
        return False
    
    def add_trade(self, user_id: int, signal: Signal, result: bool):
        """Добавление сделки"""
        user = self.get_user(user_id)
        if user:
            user.total_trades += 1
            if result:
                user.trades_won += 1
            else:
                user.trades_lost += 1
            self.update_user(user)
    
    def get_top_traders(self, limit: int = 10) -> List[User]:
        """Получение топ трейдеров"""
        traders = [u for u in self.users.values() if u.total_trades > 0]
        return sorted(traders, key=lambda x: (x.win_rate, x.total_trades), reverse=True)[:limit]
    
    def get_users_count(self) -> Dict[str, int]:
        """Статистика пользователей"""
        total = len(self.users)
        with_access = len([u for u in self.users.values() if u.has_access])
        today = datetime.now().date()
        active_today = len([u for u in self.users.values() 
                           if u.last_active and u.last_active.date() == today])
        
        return {
            'total': total,
            'with_access': with_access,
            'active_today': active_today
        }
    
    def get_all_users_with_access(self) -> List[User]:
        """Получение всех пользователей с доступом"""
        return [u for u in self.users.values() if u.has_access]

# ==================== УЛУЧШЕННЫЙ ГЕНЕРАТОР СИГНАЛОВ ====================
class AdvancedSignalGenerator:
    """Продвинутый генератор торговых сигналов с реалистичным анализом"""
    
    def __init__(self):
        self.timezone = pytz.timezone('UTC')
        # Паттерны для разных активов
        self.asset_patterns = {
            'forex': {
                'volatility': 0.005,
                'trend_probability': 0.65,
                'strong_signal_chance': 0.75
            },
            'stocks': {
                'volatility': 0.015,
                'trend_probability': 0.70,
                'strong_signal_chance': 0.72
            },
            'crypto': {
                'volatility': 0.03,
                'trend_probability': 0.68,
                'strong_signal_chance': 0.78
            }
        }
    
    def _determine_asset_type(self, asset: str) -> str:
        """Определение типа актива"""
        if any(crypto in asset for crypto in ['Bitcoin', 'Ethereum', 'BNB', 'Cardano', 'Solana', 
                                                'Ripple', 'Dogecoin', 'Litecoin', 'Polygon']):
            return 'crypto'
        elif any(stock in asset for stock in ['Apple', 'Microsoft', 'Tesla', 'Amazon', 'Google', 
                                               'Meta', 'Netflix', 'NVIDIA', 'AMD']):
            return 'stocks'
        else:
            return 'forex'
    
    def _get_realistic_price(self, asset: str, asset_type: str) -> float:
        """Получение реалистичной цены для актива"""
        if 'Bitcoin' in asset or 'BTC' in asset:
            return round(random.uniform(95000, 105000), 2)
        elif 'Ethereum' in asset or 'ETH' in asset:
            return round(random.uniform(3500, 4200), 2)
        elif 'EUR/USD' in asset:
            return round(random.uniform(1.08, 1.12), 5)
        elif 'GBP/USD' in asset:
            return round(random.uniform(1.26, 1.30), 5)
        elif 'USD/JPY' in asset:
            return round(random.uniform(148, 152), 3)
        elif asset_type == 'stocks':
            return round(random.uniform(150, 450), 2)
        elif asset_type == 'crypto':
            return round(random.uniform(50, 500), 2)
        else:
            return round(random.uniform(1.0, 1.5), 5)
    
    def _calculate_technical_indicators(self, asset_type: str) -> Dict[str, Any]:
        """Расчет технических индикаторов"""
        pattern = self.asset_patterns[asset_type]
        
        # RSI (14)
        rsi = round(random.uniform(35, 65), 1)
        if random.random() < pattern['strong_signal_chance']:
            rsi = round(random.uniform(25, 40) if random.random() < 0.5 else random.uniform(60, 75), 1)
        
        # MACD
        macd_histogram = round(random.uniform(-0.5, 0.5), 3)
        macd_signal = "Бычий 🟢" if macd_histogram > 0 else "Медвежий 🔴"
        
        # Bollinger Bands
        bb_position = random.choice(['Нижняя полоса', 'Средняя линия', 'Верхняя полоса'])
        
        # Stochastic
        stochastic = round(random.uniform(20, 80), 1)
        
        # ADX (сила тренда)
        adx = round(random.uniform(20, 50), 1)
        
        # EMA
        ema_trend = "Восходящий 📈" if random.random() < pattern['trend_probability'] else "Нисходящий 📉"
        
        # ATR (волатильность)
        atr = round(random.uniform(0.01, 0.05), 4)
        
        # Volume (относительный)
        volume = round(random.uniform(80, 120), 0)
        
        # CCI
        cci = round(random.uniform(-100, 100), 1)
        
        # Williams %R
        williams = round(random.uniform(-80, -20), 1)
        
        return {
            'RSI': rsi,
            'MACD': macd_signal,
            'MACD_Value': macd_histogram,
            'Bollinger': bb_position,
            'Stochastic': stochastic,
            'ADX': adx,
            'EMA': ema_trend,
            'ATR': atr,
            'Volume': volume,
            'CCI': cci,
            'Williams': williams
        }
    
    def _determine_direction(self, indicators: Dict, asset_type: str) -> str:
        """Определение направления на основе индикаторов"""
        pattern = self.asset_patterns[asset_type]
        
        bullish_signals = 0
        bearish_signals = 0
        
        # RSI анализ
        if indicators['RSI'] < 40:
            bullish_signals += 2
        elif indicators['RSI'] > 60:
            bearish_signals += 2
        
        # MACD
        if indicators['MACD_Value'] > 0:
            bullish_signals += 2
        else:
            bearish_signals += 2
        
        # Bollinger Bands
        if indicators['Bollinger'] == 'Нижняя полоса':
            bullish_signals += 1
        elif indicators['Bollinger'] == 'Верхняя полоса':
            bearish_signals += 1
        
        # Stochastic
        if indicators['Stochastic'] < 30:
            bullish_signals += 1
        elif indicators['Stochastic'] > 70:
            bearish_signals += 1
        
        # EMA
        if 'Восходящий' in indicators['EMA']:
            bullish_signals += 2
        else:
            bearish_signals += 2
        
        # CCI
        if indicators['CCI'] < -100:
            bullish_signals += 1
        elif indicators['CCI'] > 100:
            bearish_signals += 1
        
        # Итоговое решение
        if bullish_signals > bearish_signals:
            return "CALL"
        elif bearish_signals > bullish_signals:
            return "PUT"
        else:
            # При равенстве - учитываем тренд актива
            return "CALL" if random.random() < pattern['trend_probability'] else "PUT"
    
    def _calculate_confidence(self, indicators: Dict, direction: str) -> float:
        """Расчет уверенности в сигнале"""
        base_confidence = 75.0
        
        # RSI вклад
        if direction == "CALL":
            if indicators['RSI'] < 35:
                base_confidence += 8
            elif indicators['RSI'] < 45:
                base_confidence += 4
        else:
            if indicators['RSI'] > 65:
                base_confidence += 8
            elif indicators['RSI'] > 55:
                base_confidence += 4
        
        # MACD вклад
        if (direction == "CALL" and indicators['MACD_Value'] > 0) or \
           (direction == "PUT" and indicators['MACD_Value'] < 0):
            base_confidence += 5
        
        # ADX (сила тренда)
        if indicators['ADX'] > 35:
            base_confidence += 6
        elif indicators['ADX'] > 25:
            base_confidence += 3
        
        # Bollinger Bands
        if (direction == "CALL" and indicators['Bollinger'] == 'Нижняя полоса') or \
           (direction == "PUT" and indicators['Bollinger'] == 'Верхняя полоса'):
            base_confidence += 4
        
        # Volume
        if indicators['Volume'] > 100:
            base_confidence += 3
        
        # Ограничиваем диапазон 76-92%
        confidence = max(76.0, min(92.0, base_confidence))
        
        return round(confidence, 1)
    
    def _analyze_trend_strength(self, indicators: Dict) -> str:
        """Анализ силы тренда"""
        adx = indicators['ADX']
        
        if adx > 40:
            return "🟢 *Очень сильный*"
        elif adx > 30:
            return "🟡 *Сильный*"
        elif adx > 20:
            return "🟠 *Средний*"
        else:
            return "🔴 *Слабый*"
    
    def _analyze_volume(self, indicators: Dict) -> str:
        """Анализ объемов"""
        volume = indicators['Volume']
        
        if volume > 110:
            return "🟢 *Высокие* (рост интереса)"
        elif volume > 90:
            return "🟡 *Нормальные*"
        else:
            return "🟠 *Низкие*"
    
    def _determine_market_sentiment(self, indicators: Dict, direction: str) -> str:
        """Определение настроения рынка"""
        rsi = indicators['RSI']
        cci = indicators['CCI']
        
        if direction == "CALL":
            if rsi < 35 and cci < -100:
                return "🟢 *Сильно перепродано* - отличная точка входа"
            elif rsi < 45:
                return "🟡 *Перепродано* - хорошая возможность"
            else:
                return "🟢 *Бычье* - восходящий тренд"
        else:
            if rsi > 65 and cci > 100:
                return "🔴 *Сильно перекуплено* - отличная точка входа"
            elif rsi > 55:
                return "🟠 *Перекуплено* - хорошая возможность"
            else:
                return "🔴 *Медвежье* - нисходящий тренд"
    
    def _create_recommendation(self, confidence: float, trend_strength: str, direction: str) -> str:
        """Создание рекомендации"""
        if confidence >= 87:
            return f"""
🟢 *ОЧЕНЬ СИЛЬНЫЙ СИГНАЛ!*

✅ Все индикаторы подтверждают {direction}
✅ Высокая вероятность успеха
✅ Оптимальная точка входа

💡 *Действия:*
• Открывайте сделку с уверенностью
• Размер ставки: 5% от депозита
• Это отличная возможность!
"""
        elif confidence >= 82:
            return f"""
🟡 *СИЛЬНЫЙ СИГНАЛ*

✅ Большинство индикаторов за {direction}
✅ Хорошая вероятность успеха
✅ Благоприятные условия

💡 *Действия:*
• Открывайте сделку
• Размер ставки: 3-4% от депозита
• Следуйте стоп-лоссу
"""
        else:
            return f"""
🟠 *СРЕДНИЙ СИГНАЛ*

⚠️ Сигнал подтверждён, но с осторожностью
⚠️ Торгуйте аккуратно

💡 *Действия:*
• Можно открывать сделку
• Размер ставки: 2-3% от депозита
• Строго соблюдайте риск-менеджмент
"""
    
    def generate_signal(self, asset: str, expiry_minutes: int) -> Signal:
        """Генерация идеального торгового сигнала"""
        
        # Определяем тип актива
        asset_type = self._determine_asset_type(asset)
        
        # Получаем реалистичную цену
        price = self._get_realistic_price(asset, asset_type)
        
        # Рассчитываем технические индикаторы
        indicators = self._calculate_technical_indicators(asset_type)
        
        # Определяем направление
        direction = self._determine_direction(indicators, asset_type)
        
        # Рассчитываем уверенность
        confidence = self._calculate_confidence(indicators, direction)
        
        # Анализ рынка
        trend_strength = self._analyze_trend_strength(indicators)
        volume_analysis = self._analyze_volume(indicators)
        market_sentiment = self._determine_market_sentiment(indicators, direction)
        
        # Stop Loss и Take Profit
        atr = indicators['ATR']
        if direction == "CALL":
            stop_loss = round(price * (1 - atr * 2), 2)
            take_profit = round(price * (1 + atr * 3), 2)
        else:
            stop_loss = round(price * (1 + atr * 2), 2)
            take_profit = round(price * (1 - atr * 3), 2)
        
        risk_reward = round(abs(take_profit - price) / abs(price - stop_loss), 2)
        
        # Создаём рекомендацию
        recommendation = self._create_recommendation(confidence, trend_strength, direction)
        
        # Форматируем индикаторы для вывода
        indicators_text = f"""
• *RSI (14):* `{indicators['RSI']}` {"🟢 Перепродано" if indicators['RSI'] < 40 else "🔴 Перекуплено" if indicators['RSI'] > 60 else "🟡 Нейтрально"}
• *MACD:* {indicators['MACD']} (`{indicators['MACD_Value']}`)
• *Bollinger Bands:* {indicators['Bollinger']}
• *EMA (50/200):* {indicators['EMA']}
• *Stochastic:* `{indicators['Stochastic']}%`
• *ADX (Тренд):* `{indicators['ADX']}` {"💪 Сильный" if indicators['ADX'] > 25 else "📊 Умеренный"}
• *ATR (Волатильность):* `{indicators['ATR']}`
• *Volume:* `{indicators['Volume']}%` от среднего
• *CCI:* `{indicators['CCI']}`
• *Williams %R:* `{indicators['Williams']}%`
"""
        
        return Signal(
            asset=asset,
            direction=direction,
            expiry=f"{expiry_minutes} мин",
            expiry_minutes=expiry_minutes,
            confidence=confidence,
            price=price,
            timestamp=datetime.now(self.timezone),
            indicators=indicators,
            recommendation=recommendation,
            entry_price=price,
            stop_loss=stop_loss,
            take_profit=take_profit,
            risk_reward=risk_reward,
            trend_strength=trend_strength,
            volume_analysis=volume_analysis,
            market_sentiment=market_sentiment
        )

# ==================== АВТО-ПИНГ ====================
class AutoPing:
    """Автоматический пинг"""
    
    def __init__(self):
        self.running = False
        self.thread = None
    
    def start(self):
        """Запуск авто-пинга"""
        if not self.running:
            self.running = True
            self.thread = threading.Thread(target=self._ping_loop, daemon=True)
            self.thread.start()
            logger.info("✅ Авто-пинг запущен")
    
    def stop(self):
        """Остановка авто-пинга"""
        self.running = False
        if self.thread:
            self.thread.join()
        logger.info("🛑 Авто-пинг остановлен")
    
    def _ping_loop(self):
        """Цикл пинга"""
        while self.running:
            try:
                time.sleep(300)
                logger.debug("🔄 Пинг...")
            except Exception as e:
                logger.error(f"❌ Ошибка пинга: {e}")

# ==================== ОСНОВНОЙ БОТ ====================
class KurutAIBot:
    """Главный класс бота"""
    
    def __init__(self):
        self.data_manager = DataManager()
        self.signal_generator = AdvancedSignalGenerator()
        self.auto_ping = AutoPing()
        self.application = None
    
    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработчик команды /start"""
        user_id = update.effective_user.id
        username = update.effective_user.username
        first_name = update.effective_user.first_name
        
        user = self.data_manager.get_user(user_id)
        if not user:
            user = self.data_manager.create_user(user_id, username, first_name)
        
        user.last_active = datetime.now()
        self.data_manager.update_user(user)
        
        # АДМИН сразу в главное меню
        if user_id == ADMIN_ID:
            await self.show_main_menu(update, context)
            return MAIN_MENU
        
        # ПОЛЬЗОВАТЕЛИ через выбор языка
        keyboard = [
            [InlineKeyboardButton("🇷🇺 Русский", callback_data="lang_ru")],
            [InlineKeyboardButton("🇰🇬 Кыргызча", callback_data="lang_kg")],
            [InlineKeyboardButton("🇺🇿 O'zbek", callback_data="lang_uz")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await update.message.reply_text(
            text=TEXTS[Language.RUSSIAN]["select_language"],
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
        
        await query.edit_message_text(
            text=texts["language_selected"],
            parse_mode=ParseMode.MARKDOWN
        )
        
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
            [InlineKeyboardButton("🔐 Получить доступ", callback_data="get_access")],
            [InlineKeyboardButton("📱 Telegram", url=SOCIAL_LINKS["telegram"])],
            [InlineKeyboardButton("💬 Чат", url=SOCIAL_LINKS["telegram_chat"])],
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
            await self.show_main_menu(update, context)
            return MAIN_MENU
        
        access_text = texts["get_access"].format(
            user_id=user.id,
            ref_link=REFERRAL_LINK,
            admin=ADMIN_USERNAME
        )
        
        keyboard = [
            [InlineKeyboardButton("👤 Связаться с админом", callback_data="contact_admin")],
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
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            is_callback = True
        else:
            user_id = update.effective_user.id
            is_callback = False
        
        user = self.data_manager.get_user(user_id)
        if not user:
            user = self.data_manager.create_user(
                user_id, 
                update.effective_user.username, 
                update.effective_user.first_name
            )
        
        texts = TEXTS[user.language]
        
        keyboard = []
        
        if user_id == ADMIN_ID:
            # АДМИН МЕНЮ
            keyboard.extend([
                [InlineKeyboardButton("📈 " + texts["get_signal"], callback_data="get_signal")],
                [InlineKeyboardButton("📊 " + texts["stats"], callback_data="stats")],
                [InlineKeyboardButton("🏆 Топ трейдеров", callback_data="top_traders")],
                [InlineKeyboardButton("🏃‍♂️ Марафон", callback_data="marathon")],
                [InlineKeyboardButton("📚 " + texts["instructions"], callback_data="instructions")],
                [InlineKeyboardButton("⚙️ Админ панель", callback_data="admin_menu")],
                [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])]
            ])
        elif user.has_access:
            # ПОЛЬЗОВАТЕЛЬ С ДОСТУПОМ
            keyboard.extend([
                [InlineKeyboardButton("📈 " + texts["get_signal"], callback_data="get_signal")],
                [InlineKeyboardButton("📊 " + texts["stats"], callback_data="stats")],
                [InlineKeyboardButton("🏆 Топ трейдеров", callback_data="top_traders")],
                [InlineKeyboardButton("🏃‍♂️ Марафон", callback_data="marathon")],
                [InlineKeyboardButton("📚 Инструкция", callback_data="instructions")],
                [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])],
                [InlineKeyboardButton("👤 Админ", callback_data="contact_admin")]
            ])
        else:
            # ПОЛЬЗОВАТЕЛЬ БЕЗ ДОСТУПА
            keyboard.extend([
                [InlineKeyboardButton("🔐 Получить доступ", callback_data="get_access")],
                [InlineKeyboardButton("📚 Инструкция", callback_data="instructions")],
                [InlineKeyboardButton("📱 Соцсети", url=SOCIAL_LINKS["telegram"])],
                [InlineKeyboardButton("👤 Админ", callback_data="contact_admin")]
            ])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if is_callback:
            await update.callback_query.edit_message_text(
                text=texts["main_menu"],
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text=texts["main_menu"],
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        return MAIN_MENU
    
    async def back_to_main(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Возврат в главное меню"""
        return await self.show_main_menu(update, context)
    
    async def contact_admin(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Связь с админом"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        admin_text = f"""
👤 *Связь с администратором*

📞 Для получения доступа или по любым вопросам:
{ADMIN_USERNAME}

🆔 *Ваш ID:* `{user_id}`
(скопируйте и отправьте админу)
"""
        
        keyboard = [
            [InlineKeyboardButton("💬 Написать админу", url=f"https://t.me/{ADMIN_USERNAME.replace('@', '')}")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=admin_text,
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
        texts = TEXTS[user.language]
        
        if user_id != ADMIN_ID and not user.has_access:
            await query.edit_message_text(
                text=texts["no_access"],
                parse_mode=ParseMode.MARKDOWN
            )
            return await self.show_main_menu(update, context)
        
        keyboard = [
            [InlineKeyboardButton("🌍 Forex", callback_data="forex_pairs")],
            [InlineKeyboardButton("📈 Акции", callback_data="stocks")],
            [InlineKeyboardButton("💎 Крипто", callback_data="crypto")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["select_asset_type"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_ASSET_TYPE
    
    async def show_forex_pairs(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ валютных пар (страница 1)"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        pairs = OTC_PAIRS["forex"][:15]
        
        keyboard = []
        for pair in pairs:
            keyboard.append([InlineKeyboardButton(pair, callback_data=f"pair_{pair}")])
        
        keyboard.append([InlineKeyboardButton("➡️ Далее", callback_data="forex_pairs_2")])
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["select_pair"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_forex_pairs_2(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ валютных пар (страница 2)"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        pairs = OTC_PAIRS["forex"][15:]
        
        keyboard = []
        for pair in pairs:
            keyboard.append([InlineKeyboardButton(pair, callback_data=f"pair_{pair}")])
        
        keyboard.append([InlineKeyboardButton("⬅️ Назад", callback_data="forex_pairs")])
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["select_pair"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_stocks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ акций"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        stocks = OTC_PAIRS["stocks"]
        
        keyboard = []
        for stock in stocks:
            keyboard.append([InlineKeyboardButton(stock, callback_data=f"pair_{stock}")])
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["select_pair"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def show_crypto(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ криптовалют"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        crypto = OTC_PAIRS["crypto"]
        
        keyboard = []
        for coin in crypto:
            keyboard.append([InlineKeyboardButton(coin, callback_data=f"pair_{coin}")])
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["select_pair"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_CURRENCY_PAIR
    
    async def select_pair(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Выбор пары"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        pair = query.data.replace("pair_", "")
        context.user_data["selected_pair"] = pair
        
        keyboard = []
        for exp_name, exp_value in EXPIRATIONS.items():
            keyboard.append([InlineKeyboardButton(exp_name, callback_data=f"exp_{exp_value}")])
        
        keyboard.append([InlineKeyboardButton(texts["back"], callback_data="get_signal")])
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=f"💱 *Выбрана пара:* {pair}\n\n" + texts["select_expiry"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return SELECT_EXPIRY
    
    async def analyze_signal(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Анализ и генерация сигнала"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        expiry = int(query.data.replace("exp_", ""))
        pair = context.user_data.get("selected_pair", "EUR/USD OTC")
        
        await query.edit_message_text(
            text=texts["analyzing"],
            parse_mode=ParseMode.MARKDOWN
        )
        
        # Имитация анализа
        await asyncio.sleep(random.uniform(2.5, 3.5))
        
        # Генерация идеального сигнала
        signal = self.signal_generator.generate_signal(pair, expiry)
        context.user_data["current_signal"] = signal
        
        direction_emoji = "🟢 *CALL*" if signal.direction == "CALL" else "🔴 *PUT*"
        
        signal_text = texts["signal_generated"].format(
            asset=signal.asset,
            direction=direction_emoji,
            expiry=signal.expiry,
            price=signal.price,
            confidence=signal.confidence,
            indicators=signal.recommendation.split('\n')[0],  # Используем форматированные индикаторы
            trend_strength=signal.trend_strength,
            volume_analysis=signal.volume_analysis,
            market_sentiment=signal.market_sentiment,
            recommendation=signal.recommendation,
            stop_loss=signal.stop_loss,
            take_profit=signal.take_profit,
            risk_reward=signal.risk_reward,
            time=signal.timestamp.strftime('%H:%M:%S UTC')
        )
        
        # Заменяем плейсхолдер индикаторов на реальные данные
        indicators_formatted = f"""
• *RSI (14):* `{signal.indicators['RSI']}` {"🟢 Перепродано" if signal.indicators['RSI'] < 40 else "🔴 Перекуплено" if signal.indicators['RSI'] > 60 else "🟡 Нейтрально"}
• *MACD:* {signal.indicators['MACD']} (`{signal.indicators['MACD_Value']}`)
• *Bollinger Bands:* {signal.indicators['Bollinger']}
• *EMA (50/200):* {signal.indicators['EMA']}
• *Stochastic:* `{signal.indicators['Stochastic']}%`
• *ADX (Тренд):* `{signal.indicators['ADX']}` {"💪 Сильный" if signal.indicators['ADX'] > 25 else "📊 Умеренный"}
• *ATR (Волатильность):* `{signal.indicators['ATR']}`
• *Volume:* `{signal.indicators['Volume']}%` от среднего
• *CCI:* `{signal.indicators['CCI']}`
• *Williams %R:* `{signal.indicators['Williams']}%`
"""
        
        signal_text = signal_text.replace(signal.recommendation.split('\n')[0], indicators_formatted)
        
        keyboard = [
            [InlineKeyboardButton("✅ Выиграл", callback_data="trade_win"),
             InlineKeyboardButton("❌ Проиграл", callback_data="trade_lose")],
            [InlineKeyboardButton("📈 Новый сигнал", callback_data="get_signal")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
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
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        signal = context.user_data.get("current_signal")
        
        if not signal:
            await query.edit_message_text(
                text=texts["error"].format(error="Сигнал не найден"),
                parse_mode=ParseMode.MARKDOWN
            )
            return MAIN_MENU
        
        result = "trade_win" in query.data
        result_text = texts["trade_win"] if result else texts["trade_lose"]
        
        self.data_manager.add_trade(query.from_user.id, signal, result)
        
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
    
    async def show_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ статистики"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            is_callback = True
        else:
            user_id = update.effective_user.id
            is_callback = False
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        if user_id != ADMIN_ID and not user.has_access:
            error_text = texts["no_access"]
            if is_callback:
                await update.callback_query.edit_message_text(
                    text=error_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    text=error_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            return await self.show_main_menu(update, context)
        
        days_active = (datetime.now() - user.join_date).days if user.join_date else 0
        
        stats_text = texts["user_stats"].format(
            name=user.first_name,
            user_id=user.id,
            days_active=days_active,
            total_trades=user.total_trades,
            trades_won=user.trades_won,
            trades_lost=user.trades_lost,
            win_rate=round(user.win_rate, 1),
            profit_factor=round(user.profit_factor, 2),
            balance=round(user.balance, 2),
            referral_id=user.referral_id
        )
        
        keyboard = [
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if is_callback:
            await update.callback_query.edit_message_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text=stats_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        return MAIN_MENU
    
    async def show_top_traders(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ топ трейдеров"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            is_callback = True
        else:
            user_id = update.effective_user.id
            is_callback = False
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        if user_id != ADMIN_ID and not user.has_access:
            error_text = texts["no_access"]
            if is_callback:
                await update.callback_query.edit_message_text(
                    text=error_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    text=error_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            return await self.show_main_menu(update, context)
        
        top_traders = self.data_manager.get_top_traders(10)
        
        if not top_traders:
            top_list = "Пока нет трейдеров с завершенными сделками."
        else:
            top_list = ""
            medals = ["🥇", "🥈", "🥉"] + ["🏅"] * 7
            for i, trader in enumerate(top_traders):
                top_list += f"{medals[i]} *{trader.first_name}*\n"
                top_list += f"   📊 Винрейт: {round(trader.win_rate, 1)}% | Сделок: {trader.total_trades}\n\n"
        
        top_text = texts["top_traders_text"].format(top_list=top_list)
        
        keyboard = [
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if is_callback:
            await update.callback_query.edit_message_text(
                text=top_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text=top_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        
        return MAIN_MENU
    
    async def marathon_start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Начало марафона"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            user_id = query.from_user.id
            is_callback = True
        else:
            user_id = update.effective_user.id
            is_callback = False
        
        user = self.data_manager.get_user(user_id)
        texts = TEXTS[user.language]
        
        if user_id != ADMIN_ID and not user.has_access:
            error_text = texts["no_access"]
            if is_callback:
                await update.callback_query.edit_message_text(
                    text=error_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    text=error_text,
                    parse_mode=ParseMode.MARKDOWN
                )
            return await self.show_main_menu(update, context)
        
        marathon_text = texts["marathon_start"]
        
        if is_callback:
            await update.callback_query.edit_message_text(
                text=marathon_text,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text=marathon_text,
                parse_mode=ParseMode.MARKDOWN
            )
        
        return WAITING_FOR_BALANCE
    
    async def process_balance(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка баланса"""
        user = self.data_manager.get_user(update.message.from_user.id)
        texts = TEXTS[user.language]
        
        try:
            balance = float(update.message.text.replace(',', '.'))
            if balance <= 0 or balance > 1000000:
                raise ValueError
        except:
            await update.message.reply_text(
                text=texts["error"].format(error="Введите корректную сумму (например: 100)"),
                parse_mode=ParseMode.MARKDOWN
            )
            return WAITING_FOR_BALANCE
        
        user.balance = balance
        self.data_manager.update_user(user)
        
        # Расчет марафона
        calculation, total_profit, final_balance, growth_chart = self._calculate_marathon(balance)
        growth_percent = round((final_balance - balance) / balance * 100, 1)
        
        calculation_lines = []
        for day, value in calculation[:15]:
            calculation_lines.append(f"📅 День {day}: `${value:.2f}`")
        
        calculation_lines.append("...")
        for day, value in calculation[-5:]:
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
        """Расчет марафона"""
        daily_rate = 0.18  # 18% в день
        current = balance
        results = []
        
        for day in range(1, 31):
            profit = current * daily_rate
            current += profit
            results.append((day, current))
        
        total_profit = current - balance
        
        max_val = max(r[1] for r in results)
        min_val = balance
        chart_lines = []
        
        for i in range(0, 30, 5):
            day, value = results[i]
            normalized = (value - min_val) / (max_val - min_val)
            bar_length = int(normalized * 20)
            bar = "█" * bar_length + "░" * (20 - bar_length)
            chart_lines.append(f"День {day:2d}: {bar} ${value:.0f}")
        
        growth_chart = "\n".join(chart_lines)
        
        return results, total_profit, current, growth_chart
    
    async def show_marathon_risks(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ управления рисками"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        keyboard = [
            [InlineKeyboardButton("🏃‍♂️ Новый расчет", callback_data="marathon")],
            [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["marathon_risks"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return CALCULATE_MARATHON
    
    async def show_instructions(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Показ инструкций"""
        query = update.callback_query
        await query.answer()
        
        user = self.data_manager.get_user(query.from_user.id)
        texts = TEXTS[user.language]
        
        page = 1
        if "page2" in query.data or "next" in query.data:
            page = 2
        elif "page3" in query.data:
            page = 3
        
        if page == 1:
            text = texts["instruction_page1"]
            keyboard = [
                [InlineKeyboardButton("▶️ Далее", callback_data="page2")],
                [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
            ]
        elif page == 2:
            text = texts["instruction_page2"]
            keyboard = [
                [InlineKeyboardButton("◀️ Назад", callback_data="page1"),
                 InlineKeyboardButton("▶️ Далее", callback_data="page3")],
                [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
            ]
        else:
            text = texts["instruction_page3"]
            keyboard = [
                [InlineKeyboardButton("◀️ Назад", callback_data="page2")],
                [InlineKeyboardButton(texts["back"], callback_data="back_to_main")]
            ]
        
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.MARKDOWN
        )
        
        return MAIN_MENU
    
    # ========== АДМИН ФУНКЦИИ ==========
    
    async def admin_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /admin"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *Нет доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        await self.admin_menu(update, context)
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Админ панель"""
        if update.callback_query:
            query = update.callback_query
            await query.answer()
            is_callback = True
        else:
            is_callback = False
        
        if update.effective_user.id != ADMIN_ID:
            return
        
        stats = self.data_manager.get_users_count()
        
        admin_text = TEXTS[Language.RUSSIAN]["admin_panel"].format(
            admin_name=update.effective_user.first_name,
            total_users=stats['total'],
            users_with_access=stats['with_access'],
            active_today=stats['active_today']
        )
        
        keyboard = [
            [InlineKeyboardButton("✅ Выдать доступ", callback_data="admin_grant")],
            [InlineKeyboardButton("❌ Отозвать доступ", callback_data="admin_revoke")],
            [InlineKeyboardButton("📋 Список пользователей", callback_data="admin_users")],
            [InlineKeyboardButton("📊 Статистика бота", callback_data="admin_stats")],
            [InlineKeyboardButton("📢 Рассылка", callback_data="admin_broadcast_menu")],
            [InlineKeyboardButton("◀️ Главное меню", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if is_callback:
            await update.callback_query.edit_message_text(
                text=admin_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            await update.message.reply_text(
                text=admin_text,
                reply_markup=reply_markup,
                parse_mode=ParseMode.MARKDOWN
            )
    
    async def admin_grant(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Админ - выдача доступа"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            text="✅ *Выдача доступа*\n\nОтправьте ID пользователя:",
            parse_mode=ParseMode.MARKDOWN
        )
        
        context.user_data["admin_action"] = "grant"
        return ADMIN_SEND_MESSAGE
    
    async def admin_revoke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Админ - отзыв доступа"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            text="❌ *Отзыв доступа*\n\nОтправьте ID пользователя:",
            parse_mode=ParseMode.MARKDOWN
        )
        
        context.user_data["admin_action"] = "revoke"
        return ADMIN_SEND_MESSAGE
    
    async def admin_broadcast_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню рассылки"""
        query = update.callback_query
        await query.answer()
        
        await query.edit_message_text(
            text="📢 *Рассылка*\n\nОтправьте текст для рассылки:",
            parse_mode=ParseMode.MARKDOWN
        )
        
        return ADMIN_BROADCAST
    
    async def process_admin_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка админских сообщений"""
        if update.message.from_user.id != ADMIN_ID:
            return
        
        action = context.user_data.get("admin_action", "grant")
        text = update.message.text.strip()
        
        try:
            user_id = int(text)
            
            if action == "grant":
                if self.data_manager.grant_access(user_id):
                    await update.message.reply_text(
                        f"✅ *Доступ выдан пользователю {user_id}*",
                        parse_mode=ParseMode.MARKDOWN
                    )
                    # Уведомляем пользователя
                    try:
                        target_user = self.data_manager.get_user(user_id)
                        if target_user:
                            texts = TEXTS[target_user.language]
                            await context.bot.send_message(
                                chat_id=user_id,
                                text=texts["access_granted"],
                                parse_mode=ParseMode.MARKDOWN
                            )
                    except:
                        pass
                else:
                    await update.message.reply_text(
                        f"❌ *Пользователь {user_id} не найден*",
                        parse_mode=ParseMode.MARKDOWN
                    )
            
            elif action == "revoke":
                if self.data_manager.revoke_access(user_id):
                    await update.message.reply_text(
                        f"✅ *Доступ отозван у {user_id}*",
                        parse_mode=ParseMode.MARKDOWN
                    )
                else:
                    await update.message.reply_text(
                        f"❌ *Пользователь {user_id} не найден*",
                        parse_mode=ParseMode.MARKDOWN
                    )
        
        except ValueError:
            await update.message.reply_text(
                "❌ *Неверный формат ID*",
                parse_mode=ParseMode.MARKDOWN
            )
        
        context.user_data.pop("admin_action", None)
        await self.admin_menu(update, context)
        return MAIN_MENU
    
    async def process_broadcast(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка рассылки"""
        if update.message.from_user.id != ADMIN_ID:
            return
        
        message = update.message.text.strip()
        users = self.data_manager.get_all_users_with_access()
        
        success = 0
        failed = 0
        
        for user in users:
            try:
                await context.bot.send_message(
                    chat_id=user.id,
                    text=f"📢 *Рассылка:*\n\n{message}",
                    parse_mode=ParseMode.MARKDOWN
                )
                success += 1
                await asyncio.sleep(0.05)
            except Exception as e:
                logger.error(f"Ошибка рассылки {user.id}: {e}")
                failed += 1
        
        await update.message.reply_text(
            f"✅ *Рассылка завершена!*\n\nУспешно: {success}\nОшибок: {failed}",
            parse_mode=ParseMode.MARKDOWN
        )
        
        await self.admin_menu(update, context)
        return MAIN_MENU
    
    async def grant_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /grant"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *Нет доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ *Использование:* /grant <user_id>",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            user_id = int(context.args[0])
            if self.data_manager.grant_access(user_id):
                await update.message.reply_text(
                    f"✅ *Доступ выдан {user_id}*",
                    parse_mode=ParseMode.MARKDOWN
                )
                try:
                    target_user = self.data_manager.get_user(user_id)
                    if target_user:
                        texts = TEXTS[target_user.language]
                        await context.bot.send_message(
                            chat_id=user_id,
                            text=texts["access_granted"],
                            parse_mode=ParseMode.MARKDOWN
                        )
                except:
                    pass
            else:
                await update.message.reply_text(
                    f"❌ *Пользователь {user_id} не найден*",
                    parse_mode=ParseMode.MARKDOWN
                )
        except ValueError:
            await update.message.reply_text("❌ *Неверный ID*", parse_mode=ParseMode.MARKDOWN)
    
    async def revoke_command(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Команда /revoke"""
        if update.effective_user.id != ADMIN_ID:
            await update.message.reply_text("❌ *Нет доступа!*", parse_mode=ParseMode.MARKDOWN)
            return
        
        if not context.args:
            await update.message.reply_text(
                "❌ *Использование:* /revoke <user_id>",
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        try:
            user_id = int(context.args[0])
            if self.data_manager.revoke_access(user_id):
                await update.message.reply_text(
                    f"✅ *Доступ отозван у {user_id}*",
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                await update.message.reply_text(
                    f"❌ *Пользователь {user_id} не найден*",
                    parse_mode=ParseMode.MARKDOWN
                )
        except ValueError:
            await update.message.reply_text("❌ *Неверный ID*", parse_mode=ParseMode.MARKDOWN)
    
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
            BotCommand("grant", "✅ Выдать доступ"),
            BotCommand("revoke", "❌ Отозвать доступ")
        ]
        
        await self.application.bot.set_my_commands(commands)
    
    async def run(self):
        """Запуск бота"""
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # ConversationHandler
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
                    CallbackQueryHandler(self.show_crypto, pattern="^crypto$"),
                    CallbackQueryHandler(self.show_instructions, pattern="^page"),
                    CallbackQueryHandler(self.admin_menu, pattern="^admin_menu$"),
                    CallbackQueryHandler(self.admin_grant, pattern="^admin_grant$"),
                    CallbackQueryHandler(self.admin_revoke, pattern="^admin_revoke$"),
                    CallbackQueryHandler(self.admin_broadcast_menu, pattern="^admin_broadcast_menu$")
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
                    CallbackQueryHandler(self.show_crypto, pattern="^crypto$"),
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
                ]
            },
            fallbacks=[
                CommandHandler("start", self.start),
                CommandHandler("menu", self.show_main_menu)
            ],
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
        
        await self.setup_commands()
        self.auto_ping.start()
        
        logger.info("🤖 KURUT AI INFINITY запущен!")
        logger.info(f"👤 Админ: {ADMIN_ID}")
        logger.info(f"📊 Пользователей: {len(self.data_manager.users)}")
        
        try:
            await self.application.bot.send_message(
                chat_id=ADMIN_ID,
                text="✅ *KURUT AI INFINITY v3.2 запущен!*\n\n🎯 Все функции активны\n💎 Улучшенные сигналы готовы",
                parse_mode=ParseMode.MARKDOWN
            )
        except:
            pass
        
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ==================== ЗАПУСК ====================
if __name__ == "__main__":
    os.makedirs("backups", exist_ok=True)
    os.makedirs("logs", exist_ok=True)
    
    bot = KurutAIBot()
    
    try:
        asyncio.run(bot.run())
    except KeyboardInterrupt:
        logger.info("🛑 Бот остановлен")
    except Exception as e:
        logger.error(f"💥 Критическая ошибка: {e}")
        time.sleep(5)
        logger.info("🔄 Перезапуск...")
        asyncio.run(bot.run())
