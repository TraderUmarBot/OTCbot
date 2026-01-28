#!/usr/bin/env python3
"""
🤖 KURUT AI INFINITY - Самый точный бот для OTC рынка Pocket Option
ИСПРАВЛЕННАЯ ВЕРСИЯ - С работающими админскими командами
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
from enum import Enum
from collections import defaultdict

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

# ==================== ДОБАВЛЕНО: ФУНКЦИИ АДМИНА ====================

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /admin - доступна только админу"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав доступа к админ-панели!")
        return
    
    keyboard = [
        [InlineKeyboardButton("👤 Выдать доступ", callback_data="admin_grant")],
        [InlineKeyboardButton("🚫 Забрать доступ", callback_data="admin_revoke")],
        [InlineKeyboardButton("📢 Отправить сообщение", callback_data="admin_send")],
        [InlineKeyboardButton("📊 Статистика бота", callback_data="admin_stats")],
        [InlineKeyboardButton("📋 Список пользователей", callback_data="admin_users")],
        [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    await update.message.reply_text(
        text="⚙️ АДМИН ПАНЕЛЬ\n\nВыберите действие:",
        reply_markup=reply_markup,
        parse_mode=ParseMode.HTML
    )

async def grant_access_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /grant - выдать доступ пользователю"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав доступа!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Использование: /grant <ID пользователя>")
        return
    
    try:
        target_user_id = int(context.args[0])
        data_manager = context.bot_data.get("data_manager")
        
        if data_manager:
            success = data_manager.grant_access(target_user_id)
            
            if success:
                # Отправляем уведомление пользователю
                try:
                    await context.bot.send_message(
                        chat_id=target_user_id,
                        text="🎉 ВАМ ВЫДАН ДОСТУП К СИГНАЛАМ KURUT AI INFINITY!\n\nТеперь вам доступны все функции бота. Нажмите /start"
                    )
                except Exception as e:
                    await update.message.reply_text(f"✅ Доступ выдан, но не удалось отправить уведомление: {e}")
                else:
                    await update.message.reply_text(f"✅ Доступ выдан пользователю ID: {target_user_id}")
            else:
                await update.message.reply_text(f"❌ Пользователь с ID {target_user_id} не найден")
        else:
            await update.message.reply_text("❌ Ошибка: DataManager не доступен")
    
    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID пользователя (только цифры)")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def revoke_access_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /revoke - забрать доступ у пользователя"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав доступа!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Использование: /revoke <ID пользователя>")
        return
    
    try:
        target_user_id = int(context.args[0])
        data_manager = context.bot_data.get("data_manager")
        
        if data_manager:
            user = data_manager.get_user(target_user_id)
            
            if user:
                user.has_access = False
                data_manager.update_user(user)
                
                await update.message.reply_text(f"✅ Доступ забран у пользователя ID: {target_user_id}")
            else:
                await update.message.reply_text(f"❌ Пользователь с ID {target_user_id} не найден")
        else:
            await update.message.reply_text("❌ Ошибка: DataManager не доступен")
    
    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID пользователя (только цифры)")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def send_message_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /send - отправить сообщение пользователю"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав доступа!")
        return
    
    if len(context.args) < 2:
        await update.message.reply_text("⚠️ Использование: /send <ID пользователя> <сообщение>")
        return
    
    try:
        target_user_id = int(context.args[0])
        message = " ".join(context.args[1:])
        
        try:
            await context.bot.send_message(
                chat_id=target_user_id,
                text=f"📢 СООБЩЕНИЕ ОТ АДМИНА:\n\n{message}"
            )
            await update.message.reply_text(f"✅ Сообщение отправлено пользователю ID: {target_user_id}")
        except Exception as e:
            await update.message.reply_text(f"❌ Не удалось отправить сообщение: {e}")
    
    except ValueError:
        await update.message.reply_text("❌ Введите корректный ID пользователя (только цифры)")
    except Exception as e:
        await update.message.reply_text(f"❌ Ошибка: {e}")

async def broadcast_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /broadcast - отправить сообщение всем пользователям"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав доступа!")
        return
    
    if not context.args:
        await update.message.reply_text("⚠️ Использование: /broadcast <сообщение>")
        return
    
    message = " ".join(context.args)
    data_manager = context.bot_data.get("data_manager")
    
    if not data_manager:
        await update.message.reply_text("❌ Ошибка: DataManager не доступен")
        return
    
    users = list(data_manager.users.values())
    success_count = 0
    fail_count = 0
    
    await update.message.reply_text(f"📢 Начинаю рассылку для {len(users)} пользователей...")
    
    for user in users:
        try:
            await context.bot.send_message(
                chat_id=user.id,
                text=f"📢 ОБЪЯВЛЕНИЕ ОТ KURUT AI INFINITY:\n\n{message}"
            )
            success_count += 1
        except Exception as e:
            fail_count += 1
        
        # Небольшая задержка, чтобы не спамить
        await asyncio.sleep(0.1)
    
    await update.message.reply_text(
        f"✅ Рассылка завершена!\n\n"
        f"✅ Успешно: {success_count}\n"
        f"❌ Не удалось: {fail_count}"
    )

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /stats - статистика бота (админ)"""
    user_id = update.effective_user.id
    
    if user_id != ADMIN_ID:
        await update.message.reply_text("❌ У вас нет прав доступа!")
        return
    
    data_manager = context.bot_data.get("data_manager")
    
    if not data_manager:
        await update.message.reply_text("❌ Ошибка: DataManager не доступен")
        return
    
    users = list(data_manager.users.values())
    total = len(users)
    with_access = len([u for u in users if u.has_access])
    active_today = len([u for u in users if datetime.fromisoformat(u.last_active).date() == datetime.now().date()])
    
    stats_text = f"""
📊 СТАТИСТИКА БОТА (АДМИН):

👥 Всего пользователей: {total}
✅ С доступом: {with_access}
❌ Без доступа: {total - with_access}
📈 Активных сегодня: {active_today}

📊 Всего сделок: {len(data_manager.trades)}
💰 Средний баланс: ${np.mean([u.balance for u in users if u.balance > 0]) or 0:.2f}
🎯 Средний Win Rate: {np.mean([u.win_rate for u in users if u.total_trades > 0]) or 0:.1f}%

🏆 Топ-5 трейдеров:
"""
    
    top_traders = data_manager.get_top_traders(5)
    for i, trader in enumerate(top_traders, 1):
        name = trader.first_name[:15]
        stats_text += f"{i}. {name} (ID: {trader.id}) - {trader.win_rate:.1f}% ({trader.total_trades} сделок)\n"
    
    # Новые пользователи за последние 7 дней
    week_ago = datetime.now() - timedelta(days=7)
    new_users = [u for u in users if datetime.fromisoformat(u.join_date) > week_ago]
    
    stats_text += f"\n📅 Новых пользователей за 7 дней: {len(new_users)}"
    
    await update.message.reply_text(
        text=stats_text,
        parse_mode=ParseMode.HTML
    )

# ==================== ОСТАЛЬНОЙ КОД (НЕ ИЗМЕНЯЕМ) ====================

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
        "Coca-Cola OTC", "VISA OTC", "Mastercard OTC", "JP Morgan OTC"
    ],
    "crypto": [
        "Bitcoin OTC", "Ethereum OTC", "Ripple OTC", "Cardano OTC",
        "Solana OTC", "Polkadot OTC", "Dogecoin OTC", "Shiba Inu OTC",
        "Litecoin OTC", "Chainlink OTC", "Polygon OTC", "Avalanche OTC",
        "Tron OTC", "Toncoin OTC", "BNB OTC"
    ]
}

EXPIRATIONS = {
    "M1": 1, "M2": 2, "M3": 3, "M4": 4, "M5": 5,
    "M6": 6, "M7": 7, "M8": 8, "M9": 9, "M10": 10,
    "M15": 15, "M30": 30, "H1": 60
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
class Language(Enum):
    RUSSIAN = "ru"
    KYRGYZ = "kg"
    
    def __str__(self):
        return self.value

@dataclass
class User:
    id: int
    username: Optional[str]
    first_name: str
    language: str = "ru"  # Храним как строку, а не Enum
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
    
    @property
    def language_enum(self):
        """Конвертируем строку в Enum при необходимости"""
        return Language(self.language)

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
        # ... остальные тексты без изменений ...
        "admin_menu": "⚙️ АДМИН ПАНЕЛЬ\n\nВыберите действие:",
        "admin_grant": "Введите ID пользователя для выдачи доступа:",
        "admin_revoke": "Введите ID пользователя для снятия доступа:",
        "admin_send": "Введите ID пользователя и сообщение (через пробел):",
        "admin_granted": "✅ Доступ выдан пользователю ID: {user_id}",
        "admin_revoked": "✅ Доступ снят у пользователя ID: {user_id}",
        "admin_sent": "✅ Сообщение отправлено пользователю ID: {user_id}",
        "admin_stats": "📊 СТАТИСТИКА БОТА:\n\n👥 Пользователей: {total}\n✅ С доступом: {with_access}\n📈 Сделок: {trades}",
    },
    "kg": {
        # ... остальные тексты без изменений ...
        "admin_menu": "⚙️ АДМИН ПАНЕЛИ\n\nТандоо жасаңыз:",
        "admin_grant": "Достук берүү үчүн колдонуучунун IDсин киргизиңиз:",
        "admin_revoke": "Достук алуу үчүн колдонуучунун IDсин киргизиңиз:",
        "admin_send": "Колдонуучунун IDсин жана билдирүүнү киргизиңиз (боштук менен):",
        "admin_granted": "✅ ID колдонуучуга достук берилди: {user_id}",
        "admin_revoked": "✅ ID колдонуучудан достук алынды: {user_id}",
        "admin_sent": "✅ ID колдонуучуга билдирүү жөнөтүлдү: {user_id}",
        "admin_stats": "📊 БОТТУН СТАТИСТИКАСЫ:\n\n👥 Колдонуучулар: {total}\n✅ Достугу бар: {with_access}\n📈 Сделкалар: {trades}",
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
        
        with open("data.json", "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    
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
    
    def revoke_access(self, user_id: int):
        """Забрать доступ у пользователя"""
        user = self.get_user(user_id)
        if user:
            user.has_access = False
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

# ==================== ОСТАЛЬНЫЕ КЛАССЫ БЕЗ ИЗМЕНЕНИЙ ====================
# ... (OTC_Analyzer и остальные классы остаются без изменений) ...

# ==================== ГЛАВНЫЙ КЛАСС БОТА ====================
class KurutAIBot:
    def __init__(self):
        self.application = None
        self.data_manager = DataManager()
        self.analyzer = OTC_Analyzer()
    
    # ==================== ДОБАВЛЕНО: АДМИН ОБРАБОТЧИКИ ДЛЯ КНОПОК ====================
    
    async def admin_revoke_access(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Забрать доступ (админ - через кнопку)"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        texts = TEXTS[user.language]
        
        await query.edit_message_text(
            text=texts["admin_revoke"],
            parse_mode=ParseMode.HTML
        )
        
        context.user_data["awaiting_revoke_id"] = True
        return ADMIN_ACTIONS
    
    async def admin_send_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Отправить сообщение (админ - через кнопку)"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        texts = TEXTS[user.language]
        
        await query.edit_message_text(
            text=texts["admin_send"],
            parse_mode=ParseMode.HTML
        )
        
        context.user_data["awaiting_send"] = True
        return ADMIN_ACTIONS
    
    async def admin_list_users(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Список пользователей (админ)"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return
        
        users = list(self.data_manager.users.values())
        users.sort(key=lambda u: datetime.fromisoformat(u.join_date), reverse=True)
        
        text = "📋 ПОСЛЕДНИЕ 10 ПОЛЬЗОВАТЕЛЕЙ:\n\n"
        
        for i, user_data in enumerate(users[:10], 1):
            join_date = datetime.fromisoformat(user_data.join_date).strftime("%d.%m.%Y %H:%M")
            status = "✅" if user_data.has_access else "❌"
            text += f"{i}. ID: {user_data.id} | {user_data.first_name}\n"
            text += f"   Дата: {join_date} | Доступ: {status}\n"
            text += f"   Сделки: {user_data.total_trades} | Win Rate: {user_data.win_rate:.1f}%\n\n"
        
        text += f"\n📊 Всего пользователей: {len(users)}"
        
        keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="admin_menu")]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=text,
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return ADMIN_ACTIONS
    
    async def admin_process_revoke(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка отзыва доступа от админа"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет прав доступа!")
            return MAIN_MENU
        
        try:
            target_user_id = int(update.message.text)
            user = self.data_manager.get_user(target_user_id)
            
            if user:
                user.has_access = False
                self.data_manager.update_user(user)
                
                await update.message.reply_text(f"✅ Доступ забран у пользователя ID: {target_user_id}")
            else:
                await update.message.reply_text(f"❌ Пользователь с ID {target_user_id} не найден")
        
        except ValueError:
            await update.message.reply_text("❌ Введите корректный ID пользователя (только цифры)")
        
        return await self.admin_menu(update, context)
    
    async def admin_process_send(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка отправки сообщения от админа"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет прав доступа!")
            return MAIN_MENU
        
        try:
            parts = update.message.text.split()
            if len(parts) < 2:
                await update.message.reply_text("❌ Введите ID и сообщение")
                return
            
            target_user_id = int(parts[0])
            message = " ".join(parts[1:])
            
            try:
                await context.bot.send_message(
                    chat_id=target_user_id,
                    text=f"📢 СООБЩЕНИЕ ОТ АДМИНА:\n\n{message}"
                )
                await update.message.reply_text(f"✅ Сообщение отправлено пользователю ID: {target_user_id}")
            except Exception as e:
                await update.message.reply_text(f"❌ Не удалось отправить сообщение: {e}")
        
        except ValueError:
            await update.message.reply_text("❌ Введите корректный ID пользователя (только цифры)")
        
        return await self.admin_menu(update, context)
    
    # ==================== ОСТАЛЬНЫЕ МЕТОДЫ БЕЗ ИЗМЕНЕНИЙ ====================
    # ... (остальные методы вашего класса остаются без изменений) ...
    
    async def admin_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Меню админа"""
        query = update.callback_query
        await query.answer()
        
        user_id = query.from_user.id
        user = self.data_manager.get_user(user_id)
        
        if user_id != ADMIN_ID:
            await query.edit_message_text("❌ У вас нет прав доступа!")
            return MAIN_MENU
        
        texts = TEXTS[user.language]
        
        keyboard = [
            [InlineKeyboardButton("👤 Выдать доступ", callback_data="admin_grant")],
            [InlineKeyboardButton("🚫 Забрать доступ", callback_data="admin_revoke")],
            [InlineKeyboardButton("📢 Отправить сообщение", callback_data="admin_send")],
            [InlineKeyboardButton("📊 Статистика бота", callback_data="admin_stats")],
            [InlineKeyboardButton("📋 Список пользователей", callback_data="admin_users")],
            [InlineKeyboardButton("🏠 Главное меню", callback_data="back_to_main")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        await query.edit_message_text(
            text=texts["admin_menu"],
            reply_markup=reply_markup,
            parse_mode=ParseMode.HTML
        )
        
        return ADMIN_ACTIONS
    
    async def admin_process_user_id(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Обработка ID пользователя от админа"""
        user_id = update.effective_user.id
        
        if user_id != ADMIN_ID:
            await update.message.reply_text("❌ У вас нет прав доступа!")
            return MAIN_MENU
        
        try:
            target_user_id = int(update.message.text)
            user = self.data_manager.get_user(target_user_id)
            
            if user:
                self.data_manager.grant_access(target_user_id)
                
                # Отправляем уведомление пользователю
                try:
                    await context.bot.send_message(
                        chat_id=target_user_id,
                        text="🎉 ВАМ ВЫДАН ДОСТУП К СИГНАЛАМ KURUT AI INFINITY!\n\nТеперь вам доступны все функции бота. Нажмите /start"
                    )
                except:
                    pass
                
                await update.message.reply_text(f"✅ Доступ выдан пользователю ID: {target_user_id}")
            else:
                await update.message.reply_text(f"❌ Пользователь с ID {target_user_id} не найден")
        
        except ValueError:
            await update.message.reply_text("❌ Введите корректный ID пользователя (только цифры)")
        
        return await self.admin_menu(update, context)
    
    async def setup_commands(self):
        """Настройка команд бота"""
        commands = [
            BotCommand("start", "Запустить бота"),
            BotCommand("stats", "Моя статистика"),
            BotCommand("top", "Топ трейдеров"),
            BotCommand("marathon", "Марафон трейдера"),
            BotCommand("instruction", "Инструкция"),
            BotCommand("admin", "Админ панель (только для админа)"),
            BotCommand("grant", "Выдать доступ пользователю (админ)"),
            BotCommand("revoke", "Забрать доступ у пользователя (админ)"),
            BotCommand("send", "Отправить сообщение пользователю (админ)"),
            BotCommand("broadcast", "Рассылка всем пользователям (админ)"),
            BotCommand("statistics", "Статистика бота (админ)")
        ]
        
        await self.application.bot.set_my_commands(commands)
    
    async def run(self):
        """Запуск бота"""
        # Создаем приложение
        self.application = Application.builder().token(BOT_TOKEN).build()
        
        # Сохраняем DataManager в bot_data для доступа из команд
        self.application.bot_data["data_manager"] = self.data_manager
        
        # ДОБАВЛЕНО: Регистрируем админские команды
        self.application.add_handler(CommandHandler("admin", admin_command))
        self.application.add_handler(CommandHandler("grant", grant_access_command))
        self.application.add_handler(CommandHandler("revoke", revoke_access_command))
        self.application.add_handler(CommandHandler("send", send_message_command))
        self.application.add_handler(CommandHandler("broadcast", broadcast_command))
        self.application.add_handler(CommandHandler("statistics", stats_command))
        
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
                    CallbackQueryHandler(self.show_instruction, pattern="^instruction$"),
                    CallbackQueryHandler(self.show_top_traders, pattern="^top_traders$"),
                    CallbackQueryHandler(self.show_stats, pattern="^stats$"),
                    CallbackQueryHandler(self.admin_menu, pattern="^admin_menu$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                WAITING_FOR_BALANCE: [
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.process_balance)
                ],
                SELECT_ASSET_TYPE: [
                    CallbackQueryHandler(self.show_forex_pairs, pattern="^forex_pairs$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                SELECT_CURRENCY_PAIR: [
                    CallbackQueryHandler(self.select_pair, pattern="^pair_"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                SELECT_EXPIRY: [
                    CallbackQueryHandler(self.analyze_signal, pattern="^exp_"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                TRADE_RESULT: [
                    CallbackQueryHandler(self.process_trade_result, pattern="^trade_"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$")
                ],
                ADMIN_ACTIONS: [
                    CallbackQueryHandler(self.admin_grant_access, pattern="^admin_grant$"),
                    CallbackQueryHandler(self.admin_revoke_access, pattern="^admin_revoke$"),
                    CallbackQueryHandler(self.admin_send_message, pattern="^admin_send$"),
                    CallbackQueryHandler(self.admin_stats_command, pattern="^admin_stats$"),
                    CallbackQueryHandler(self.admin_list_users, pattern="^admin_users$"),
                    CallbackQueryHandler(self.back_to_main, pattern="^back_to_main$"),
                    MessageHandler(filters.TEXT & ~filters.COMMAND, self.admin_process_user_id)
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
        self.application.add_handler(CommandHandler("instruction", self.show_instruction))
        
        # Обработчик ошибок
        self.application.add_error_handler(self.error_handler)
        
        # Настраиваем команды
        await self.setup_commands()
        
        # Запускаем автопининг для Replit
        def start_ping():
            while True:
                try:
                    requests.get("https://google.com", timeout=5)
                    logger.info("✅ Ping sent")
                except:
                    pass
                time.sleep(180)  # 3 минуты
        
        ping_thread = threading.Thread(target=start_ping, daemon=True)
        ping_thread.start()
        
        # Запускаем бота
        logger.info("🤖 KURUT AI INFINITY запущен!")
        logger.info(f"👤 Админ ID: {ADMIN_ID}")
        logger.info("✅ Бот готов к работе 24/7 с автопинингом")
        logger.info("✅ Админские команды активны: /grant, /revoke, /send, /broadcast, /statistics")
        
        await self.application.run_polling(allowed_updates=Update.ALL_TYPES)

# ==================== ЗАПУСК ПРИЛОЖЕНИЯ ====================
if __name__ == "__main__":
    # Создаем папку для логов если нет
    if not os.path.exists("data"):
        os.makedirs("data")
    
    # Запускаем бота
    bot = KurutAIBot()
    
    # Бесконечный цикл с перезапуском при ошибках
    while True:
        try:
            asyncio.run(bot.run())
        except KeyboardInterrupt:
            logger.info("🛑 Бот остановлен пользователем")
            break
        except Exception as e:
            logger.error(f"⚠️ Критическая ошибка: {e}")
            logger.info("🔄 Перезапуск бота через 10 секунд...")
            time.sleep(10)
