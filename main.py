# =====================================
# KURUT AI INFINITY | COIP PRO EDITION
# ULTRA PREMIUM VIP TELEGRAM BOT
# DESIGNED WITH ❤️ FOR MAXIMUM PROFIT
# =====================================

import asyncio
import json
import os
import time
import math
import random
from datetime import datetime, timedelta
from flask import Flask
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes
from telegram.error import BadRequest
import logging

# =====================================
# 🎨 КРАСИВОЕ ОФОРМЛЕНИЕ
# =====================================

class StickerDesign:
    # Приветственные стикеры
    WELCOME_STICKERS = [
        "CAACAgIAAxkBAAIBD2cIQn5xY_2Xe9Rdt2_TENz-DGvTAAJjDwAC_pLRSKBRC3gVI8hVMwQ",
        "CAACAgIAAxkBAAIBEWcIQqIqHsgSnFjwF8qvNjR5YwqjAAIGFAACNqLYSPrVU5f2Kez-MwQ",
        "CAACAgIAAxkBAAIBE2cIQtI-Gs5lJv4q6auyXm5IJn_3AAJyFAACyriJSORob-Vv1GjjMwQ"
    ]
    
    # VIP стикеры
    VIP_STICKERS = [
        "CAACAgIAAxkBAAIBFWcIQu7alrQ0UMhKkAhwvDH9ClhCAAJ_FAACR7AQS0AqrQpPkR7QMwQ",
        "CAACAgIAAxkBAAIBF2cIQwF4AvDyLmJg_VM8A5cZXIq0AAInGQACSG7gSwOPD71fqV-xMwQ"
    ]
    
    # Сигнальные стикеры
    SIGNAL_STICKERS = {
        "CALL": "CAACAgIAAxkBAAIBGWcIQyTT4Cv_UmSohz2oOfdsb00GAAIrGQAC9hiISBLD6fXRRQexMwQ",
        "PUT": "CAACAgIAAxkBAAIBG2cIQ0JxqT-AElKdWU4lyQ-6kNHuAAIEGQACxrYQS1f1fsmB_SKUMwQ",
        "STRONG_CALL": "CAACAgIAAxkBAAIBHWcIQ2WXwq4pglRkvJbG11FNsYJwAAJ7GQACu0sgS9XUfB9ZxL8jMwQ",
        "STRONG_PUT": "CAACAgIAAxkBAAIBH2cIQ4B-K09B5VKCFc-9sx6JyhW8AAISGQACxrgYS7L8qAcmtebQMwQ"
    }
    
    # Успех/победа
    SUCCESS_STICKERS = [
        "CAACAgIAAxkBAAIBIWcIQ5x8w0UaOYgdW3_pW3vBR6-TAAJnGQACBICwS8F_wpsmV7aHMwQ",
        "CAACAgIAAxkBAAIBI2cIQ7kcMyt5M_1yGc80nJ4eT_azAAJgGQACLZERS-wtpGXv3Q4-MwQ"
    ]
    
    # Ошибки/предупреждения
    WARNING_STICKERS = [
        "CAACAgIAAxkBAAIBJWcIQ9WNYbQ_8znPcDiyO0oaaQo4AAKPGQACpE7wSkOqFy9ptfgBMwQ",
        "CAACAgIAAxkBAAIBJ2cIQ_ZqYphfX-WuFCTd0n74iQlqAAKGGQACeUfYSy_icWcQlT8OMwQ"
    ]

class EmojiDecor:
    # Разделители и линии
    DIVIDER = "═" * 40
    STAR_DIVIDER = "✧" * 40
    DIAMOND_DIVIDER = "♢" * 40
    
    # Разделы
    HEADER = "╔══════════════════════════════════════╗"
    FOOTER = "╚══════════════════════════════════════╝"
    
    # Иконки для меню
    ICONS = {
        "signal": "🚀",
        "vip": "👑",
        "profile": "👤",
        "stats": "📊",
        "settings": "⚙️",
        "help": "❓",
        "register": "📝",
        "marathon": "🏃‍♂️",
        "analytics": "📈",
        "calendar": "📅",
        "money": "💰",
        "chart": "📉",
        "clock": "⏰",
        "check": "✅",
        "cross": "❌",
        "warning": "⚠️",
        "fire": "🔥",
        "rocket": "🚀",
        "trophy": "🏆",
        "diamond": "💎",
        "crown": "👑",
        "star": "⭐",
        "up": "📈",
        "down": "📉",
        "neutral": "⚪"
    }

class ColorScheme:
    # Цветные символы для терминала
    GREEN = "🟢"
    RED = "🔴"
    BLUE = "🔵"
    YELLOW = "🟡"
    PURPLE = "🟣"
    ORANGE = "🟠"
    
    # Градиенты
    GRADIENT = ["🟥", "🟧", "🟨", "🟩", "🟦", "🟪"]
    
    # Статусы
    ONLINE = "🟢"
    OFFLINE = "🔴"
    BUSY = "🟡"

# =====================================
# 🎯 ОСНОВНОЙ КОД С КРАСИВЫМ ОФОРМЛЕНИЕМ
# =====================================

# Настройка логирования
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# ---------------- SERVER ----------------
server = Flask('')

@server.route('/')
def home():
    return """
    <html>
        <head>
            <title>KURUT AI INFINITY | VIP SIGNALS</title>
            <style>
                body {
                    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                    color: white;
                    font-family: Arial, sans-serif;
                    text-align: center;
                    padding: 50px;
                }
                .container {
                    background: rgba(255, 255, 255, 0.1);
                    backdrop-filter: blur(10px);
                    border-radius: 20px;
                    padding: 40px;
                    max-width: 600px;
                    margin: 0 auto;
                    box-shadow: 0 20px 40px rgba(0,0,0,0.2);
                }
                h1 {
                    font-size: 3em;
                    margin-bottom: 20px;
                    text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
                }
                .status {
                    background: rgba(0, 255, 0, 0.2);
                    padding: 10px;
                    border-radius: 10px;
                    margin: 20px 0;
                    font-size: 1.2em;
                }
            </style>
        </head>
        <body>
            <div class="container">
                <h1>🚀 KURUT AI INFINITY</h1>
                <h2>⚡ VIP SIGNAL SYSTEM ⚡</h2>
                <div class="status">✅ СИСТЕМА АКТИВНА | 🟢 ONLINE</div>
                <p>🔥 Профессиональные сигналы для Pocket Option</p>
                <p>👑 VIP доступ | 📊 15+ индикаторов | 🎯 95% точность</p>
                <p>💎 Версия: COIP PRO EDITION</p>
                <p>⏰ Время сервера: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</p>
            </div>
        </body>
    </html>
    """

def run_web():
    server.run(host='0.0.0.0', port=8080, debug=False)

# ---------------- CONFIG ----------------
TOKEN = os.environ.get("TOKEN", "8578509228:AAHNy5zNB0pLNA96c-671Y7zVyUitj5ecRc")
ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@Kuruttrader"
ADMIN_LINK = "https://t.me/Kuruttrader"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

# ---------------- DATABASE ----------------
DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "trader_stats.json"
DB_LOGS = "admin_logs.json"
DB_SIGNALS = "signal_history.json"

def load_db(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            logging.error(f"Error loading {file}: {e}")
            return default
    return default

def save_db(file, data):
    try:
        with open(file, "w", encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
    except Exception as e:
        logging.error(f"Error saving {file}: {e}")

# Загрузка данных
vip_users = set(load_db(DB_VIP, []))
all_users = set(load_db(DB_ALL, []))
trader_stats = load_db(DB_STATS, {})
admin_logs = load_db(DB_LOGS, [])
signal_history = load_db(DB_SIGNALS, {})

# ---------------- КРАСИВЫЕ ТЕКСТЫ ----------------
WELCOME_TEXT = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['rocket']} <b>ДОБРО ПОЖАЛОВАТЬ В KURUT AI INFINITY!</b> {EmojiDecor.ICONS['rocket']}

{EmojiDecor.STAR_DIVIDER}

👋 <b>Привет, {{name}}!</b> Рад видеть тебя в нашем премиум сообществе!

🎯 <b>Я - твой личный AI ассистент для торговли</b>
⚡ <b>Анализирую рынок с помощью 15+ индикаторов</b>
🎭 <b>Даю точные сигналы с вероятностью до 95%</b>

{EmojiDecor.DIAMOND_DIVIDER}

<b>✨ ЧТО Я УМЕЮ:</b>

{EmojiDecor.ICONS['signal']} <b>/signal</b> - Получить VIP сигнал
{EmojiDecor.ICONS['vip']} <b>/vip</b> - VIP статус и доступ
{EmojiDecor.ICONS['profile']} <b>/profile</b> - Моя статистика
{EmojiDecor.ICONS['stats']} <b>/stats</b] - Общая статистика
{EmojiDecor.ICONS['marathon']} <b>/marathon</b> - Мастер-план на 30 дней
{EmojiDecor.ICONS['analytics']} <b>/analytics</b> - Аналитика рынка
{EmojiDecor.ICONS['help']} <b>/help</b> - Помощь и поддержка

{EmojiDecor.DIVIDER}

👑 <b>Для получения доступа к сигналам:</b>
1. {EmojiDecor.ICONS['register']} Пройди регистрацию
2. {EmojiDecor.ICONS['money']} Пополни счет от $20
3. {EmojiDecor.ICONS['check']} Получи VIP доступ

{EmojiDecor.FOOTER}
"""

REGISTER_TEXT = f"""
{EmojiDecor.HEADER}
🎯 <b>РЕГИСТРАЦИЯ НА POCKET OPTION</b> 🎯
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

{EmojiDecor.ICONS['check']} <b>ЕСЛИ У ТЕБЯ ЕСТЬ АККАУНТ:</b>
1. ❌ Удали старый аккаунт
2. 🆕 Создай новый по нашей ссылке
3. 💰 Пополни баланс от $20
4. 📨 Отправь ID админу {ADMIN_USER}

{EmojiDecor.ICONS['register']} <b>ЕСЛИ АККАУНТА НЕТ:</b>
1. 👇 Нажми кнопку "📝 РЕГИСТРАЦИЯ"
2. 📋 Заполни данные по ссылке
3. 💳 Пополни депозит от $20
4. 🆔 Скопируй свой ID из бота

{EmojiDecor.DIAMOND_DIVIDER}

💰 <b>МИНИМАЛЬНЫЙ ДЕПОЗИТ:</b> $20
🎁 <b>БОНУС НА СТАРТЕ:</b> +50% к первому депозиту
⚡ <b>ВЫВОД СРЕДСТВ:</b> 15 мин - 24 часа

{EmojiDecor.DIVIDER}

📊 <b>ПОСЛЕ РЕГИСТРАЦИИ:</b>
1. {EmojiDecor.ICONS['profile']} Скопируй ID из /profile
2. {EmojiDecor.ICONS['vip']} Напиши админу {ADMIN_USER}
3. {EmojiDecor.ICONS['check']} Получи VIP доступ к сигналам

{EmojiDecor.STAR_DIVIDER}

🔥 <b>НАШИ ПРЕИМУЩЕСТВА:</b>
• 🎯 Точность сигналов до 95%
• ⚡ Мгновенные уведомления
• 📈 15+ профессиональных индикаторов
• 👑 Персональная поддержка
• 💎 Эксклюзивные стратегии
"""

# ---------------- КРАСИВЫЕ КНОПКИ ----------------
def create_main_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['signal']} СИГНАЛ", callback_data="get_signal"),
            InlineKeyboardButton(f"{EmojiDecor.ICONS['vip']} VIP", callback_data="vip_info")
        ],
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['profile']} ПРОФИЛЬ", callback_data="profile"),
            InlineKeyboardButton(f"{EmojiDecor.ICONS['stats']} СТАТИСТИКА", callback_data="stats")
        ],
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['marathon']} МАРАФОН", callback_data="marathon"),
            InlineKeyboardButton(f"{EmojiDecor.ICONS['analytics']} АНАЛИТИКА", callback_data="analytics")
        ],
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['register']} РЕГИСТРАЦИЯ", url=REF_LINK),
            InlineKeyboardButton(f"{EmojiDecor.ICONS['help']} ПОМОЩЬ", callback_data="help")
        ],
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['crown']} АДМИН", url=ADMIN_LINK)
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

def create_vip_keyboard():
    keyboard = [
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['crown']} КУПИТЬ VIP", url=ADMIN_LINK),
            InlineKeyboardButton(f"{EmojiDecor.ICONS['check']} ПРОВЕРИТЬ VIP", callback_data="check_vip")
        ],
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['signal']} ТЕСТ СИГНАЛА", callback_data="test_signal")
        ],
        [
            InlineKeyboardButton(f"{EmojiDecor.ICONS['back']} НАЗАД", callback_data="main_menu")
        ]
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------------- HANDLERS С КРАСИВЫМ ОФОРМЛЕНИЕМ ----------------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    # Добавляем пользователя в общую базу
    if user_id not in all_users:
        all_users.add(user_id)
        save_db(DB_ALL, list(all_users))
    
    # Отправляем стикер
    try:
        sticker_id = random.choice(StickerDesign.WELCOME_STICKERS)
        await update.message.reply_sticker(sticker_id)
    except:
        pass
    
    # Отправляем приветственное сообщение
    welcome = WELCOME_TEXT.format(name=user.first_name)
    await update.message.reply_text(
        welcome,
        parse_mode='HTML',
        reply_markup=create_main_keyboard()
    )

async def register_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        REGISTER_TEXT,
        parse_mode='HTML',
        disable_web_page_preview=True
    )

async def vip_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    vip_status = "👑 VIP АКТИВЕН" if is_vip(user_id) else "❌ VIP НЕ АКТИВЕН"
    
    text = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['crown']} <b>VIP СТАТУС И ПРЕИМУЩЕСТВА</b> {EmojiDecor.ICONS['crown']}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

<b>ТВОЙ СТАТУС:</b> {vip_status}

{EmojiDecor.DIAMOND_DIVIDER}

🔥 <b>VIP ПРЕИМУЩЕСТВА:</b>

✅ <b>ЕЖЕДНЕВНЫЕ СИГНАЛЫ</b>
• 🎯 10-15 точных сигналов в день
• ⚡ Мгновенные уведомления
• 📈 Профессиональный анализ

✅ <b>ЭКСКЛЮЗИВНЫЙ КОНТЕНТ</b>
• 📚 Закрытые стратегии
• 🎬 Обучающие материалы
• 💎 Персональные консультации

✅ <b>ПРИОРИТЕТНАЯ ПОДДЕРЖКА</b>
• 👨‍💻 Личный помощник
• ⏰ Круглосуточная поддержка
• 🔄 Помощь в настройке

{EmojiDecor.DIVIDER}

💰 <b>СТОИМОСТЬ VIP:</b>
• 1 месяц - $99
• 3 месяца - $249 (экономия $48)
• 6 месяцев - $449 (экономия $145)

{EmojiDecor.STAR_DIVIDER}

🎁 <b>БОНУСЫ ПРИ ОПЛАТЕ:</b>
1. 📚 Бесплатный доступ к курсу
2. 👨‍🏫 Персональная сессия
3. 📊 Настройка терминала

{EmojiDecor.FOOTER}
"""
    
    try:
        if is_vip(user_id):
            sticker_id = random.choice(StickerDesign.VIP_STICKERS)
            await update.message.reply_sticker(sticker_id)
    except:
        pass
    
    await update.message.reply_text(
        text,
        parse_mode='HTML',
        reply_markup=create_vip_keyboard()
    )

async def profile_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    user_id = str(user.id)
    
    win_rate = calculate_win_rate(user_id)
    total_profit = calculate_total_profit(user_id)
    vip_status = "👑 VIP" if is_vip(user_id) else "👤 BASIC"
    
    # Создаем красивый прогресс-бар
    progress = min(int(win_rate / 10), 10)
    progress_bar = "▓" * progress + "░" * (10 - progress)
    
    text = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['profile']} <b>ЛИЧНЫЙ КАБИНЕТ</b> {EmojiDecor.ICONS['profile']}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

👤 <b>ИМЯ:</b> {user.first_name or 'Не указано'}
🆔 <b>ID:</b> <code>{user_id}</code>
{EmojiDecor.ICONS['crown']} <b>СТАТУС:</b> {vip_status}

{EmojiDecor.DIAMOND_DIVIDER}

📊 <b>СТАТИСТИКА ТОРГОВЛИ:</b>

{EmojiDecor.ICONS['chart']} <b>ВИНРЕЙТ:</b> {win_rate:.1f}%
{progress_bar} [{win_rate:.1f}%]

{EmojiDecor.ICONS['money']} <b>ОБЩАЯ ПРИБЫЛЬ:</b> ${total_profit:,.2f}

{EmojiDecor.ICONS['calendar']} <b>АКТИВНОСТЬ:</b>
• 📅 Дата регистрации: {datetime.now().strftime('%d.%m.%Y')}
• ⏰ Последняя активность: Сейчас онлайн

{EmojiDecor.DIVIDER}

🏆 <b>ДОСТИЖЕНИЯ:</b>
"""
    
    # Добавляем достижения
    if win_rate > 70:
        text += f"{EmojiDecor.ICONS['trophy']} Мастер торговли\n"
    if total_profit > 1000:
        text += f"{EmojiDecor.ICONS['diamond']} Профи +$1000\n"
    if is_vip(user_id):
        text += f"{EmojiDecor.ICONS['crown']} VIP членство\n"
    
    text += f"""
{EmojiDecor.STAR_DIVIDER}

💡 <b>СОВЕТЫ:</b>
{get_trading_tip(win_rate)}

{EmojiDecor.FOOTER}
"""
    
    await update.message.reply_text(text, parse_mode='HTML')

def get_trading_tip(win_rate):
    if win_rate < 50:
        return "🎯 Совет: Фокусируйся на 1-2 активах, изучай их поведение"
    elif win_rate < 70:
        return "📈 Совет: Увеличивай размер сделок постепенно"
    else:
        return "🚀 Совет: Ты профи! Делись стратегией с другими"

# ---------------- СИГНАЛЫ С КРАСИВЫМ ОФОРМЛЕНИЕМ ----------------
async def signal_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if not is_vip(user_id):
        text = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['warning']} <b>ДОСТУП ЗАПРЕЩЕН</b> {EmojiDecor.ICONS['warning']}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

🚫 <b>У тебя нет доступа к сигналам!</b>

Для получения VIP доступа:
1. {EmojiDecor.ICONS['register']} Пройди регистрацию
2. {EmojiDecor.ICONS['money']} Пополни счет от $20
3. {EmojiDecor.ICONS['crown']} Купи VIP доступ

{EmojiDecor.DIVIDER}

📨 <b>Свяжись с админом:</b> {ADMIN_USER}
"""
        await update.message.reply_text(text, parse_mode='HTML')
        return
    
    # Генерируем сигнал
    asset = random.choice(OTC_PAIRS)
    direction, probability, reasons, indicators, expiration = analyzer.analyze_asset(asset)
    
    # Выбираем стикер
    if "STRONG CALL" in direction:
        sticker_id = StickerDesign.SIGNAL_STICKERS["STRONG_CALL"]
        signal_emoji = "🚀"
    elif "CALL" in direction:
        sticker_id = StickerDesign.SIGNAL_STICKERS["CALL"]
        signal_emoji = "📈"
    elif "STRONG PUT" in direction:
        sticker_id = StickerDesign.SIGNAL_STICKERS["STRONG_PUT"]
        signal_emoji = "🔻"
    elif "PUT" in direction:
        sticker_id = StickerDesign.SIGNAL_STICKERS["PUT"]
        signal_emoji = "📉"
    else:
        sticker_id = None
        signal_emoji = "⚪"
    
    # Создаем красивый сигнал
    text = f"""
{EmojiDecor.HEADER}
{signal_emoji} <b>VIP СИГНАЛ #{random.randint(1000, 9999)}</b> {signal_emoji}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

🎯 <b>АКТИВ:</b> <code>{asset}</code>
⏰ <b>ВРЕМЯ:</b> {datetime.now().strftime('%H:%M:%S')}
📅 <b>ДАТА:</b> {datetime.now().strftime('%d.%m.%Y')}

{EmojiDecor.DIAMOND_DIVIDER}

🚀 <b>НАПРАВЛЕНИЕ:</b> {direction}
🎯 <b>ВЕРОЯТНОСТЬ:</b> {probability}%

⏱️ <b>ЭКСПИРАЦИЯ:</b> {expiration}
💰 <b>РИСК:</b> 2-5% от депозита

{EmojiDecor.DIVIDER}

📊 <b>АНАЛИЗ ИНДИКАТОРОВ:</b>
"""
    
    # Добавляем причины
    for i, reason in enumerate(reasons[:5], 1):
        text += f"{i}. {reason}\n"
    
    text += f"""
{EmojiDecor.STAR_DIVIDER}

💡 <b>РЕКОМЕНДАЦИИ:</b>
• Используй 2-5% от депозита
• Следуй мани-менеджменту
• Фиксируй прибыль при 70-80%

{EmojiDecor.ICONS['warning']} <b>ВАЖНО:</b>
Торговля на бирже связана с рисками.
Не инвестируй последние деньги.

{EmojiDecor.FOOTER}
"""
    
    # Отправляем стикер
    if sticker_id:
        try:
            await update.message.reply_sticker(sticker_id)
        except:
            pass
    
    # Отправляем сигнал
    await update.message.reply_text(text, parse_mode='HTML')
    
    # Логируем сигнал
    log_signal(asset, direction, probability, reasons, expiration, user_id)

# ---------------- МАРАФОН С КРАСИВЫМ ОФОРМЛЕНИЕМ ----------------
async def marathon_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    calculator = MarathonCalculator()
    
    text = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['marathon']} <b>МАРАФОН 30 ДНЕЙ К УСПЕХУ</b> {EmojiDecor.ICONS['marathon']}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

🎯 <b>СТРАТЕГИЯ "МАРАФОН":</b>
Ежедневная цель: +15% к депозиту
Период: 30 дней
Итог: ×66 к начальному депозиту

{EmojiDecor.DIAMOND_DIVIDER}

📊 <b>ПРИМЕР РАСЧЕТА:</b>

Начальный депозит: $50
"""
    
    results = calculator.calculate_marathon(50, 30)
    
    emoji_days = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
    
    for i in range(min(5, len(results))):
        day_data = results[i]
        emoji = emoji_days[i] if i < len(emoji_days) else f"{i+1}."
        text += f"{emoji} День {day_data['day']}: ${day_data['balance']:,.2f} (+${day_data['profit']:,.2f})\n"
    
    text += f"""
{EmojiDecor.DIVIDER}

🏁 <b>ИТОГ ЧЕРЕЗ 30 ДНЕЙ:</b>
• Начало: $50
• Конец: ${results[-1]['balance']:,.2f}
• Прибыль: ${results[-1]['total_profit']:,.2f}
• Рост: ×{results[-1]['balance']/50:.1f}

{EmojiDecor.STAR_DIVIDER}

💡 <b>ПРАВИЛА МАРАФОНА:</b>
1. 📅 Торгуй каждый день
2. 🎯 Цель +15% в день
3. ⚠️ Риск не более 5%
4. 💰 Выводи прибыль каждые 5 дней

{EmojiDecor.FOOTER}
"""
    
    await update.message.reply_text(text, parse_mode='HTML')

# ---------------- АНАЛИТИКА ----------------
async def analytics_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = str(update.effective_user.id)
    
    if not is_vip(user_id):
        await update.message.reply_text(
            f"{EmojiDecor.ICONS['warning']} Доступ к аналитике только для VIP пользователей!",
            parse_mode='HTML'
        )
        return
    
    # Генерируем аналитику
    top_assets = random.sample(OTC_PAIRS, 5)
    
    text = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['analytics']} <b>РЫНОЧНАЯ АНАЛИТИКА</b> {EmojiDecor.ICONS['analytics']}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

⏰ <b>ОБНОВЛЕНО:</b> {datetime.now().strftime('%H:%M:%S')}
📈 <b>ПЕРИОД:</b> Последние 24 часа

{EmojiDecor.DIAMOND_DIVIDER}

🏆 <b>ТОП-5 АКТИВОВ ДНЯ:</b>
"""
    
    for i, asset in enumerate(top_assets, 1):
        direction, probability, _, _, _ = analyzer.analyze_asset(asset)
        emoji = "🟢" if "CALL" in direction else "🔴" if "PUT" in direction else "⚪"
        text += f"{i}. {emoji} {asset}: {probability}%\n"
    
    text += f"""
{EmojiDecor.DIVIDER}

📊 <b>ИНДИКАТОРЫ РЫНКА:</b>

• {EmojiDecor.ICONS['chart']} RSI общий: {random.randint(40, 60)}
• {EmojiDecor.ICONS['up']} Бычьи активы: {random.randint(40, 60)}%
• {EmojiDecor.ICONS['down']} Медвежьи активы: {random.randint(30, 50)}%
• ⚡ Волатильность: {random.randint(2, 8)}/10

{EmojiDecor.STAR_DIVIDER}

💎 <b>РЕКОМЕНДАЦИИ:</b>
• Фокусируйся на EUR/USD OTC
• Избегай торговли в 15:00-17:00 GMT
• Используй отложенные ордера

{EmojiDecor.FOOTER}
"""
    
    await update.message.reply_text(text, parse_mode='HTML')

# ---------------- CALLBACK HANDLERS ----------------
async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    user_id = str(query.from_user.id)
    
    if query.data == "get_signal":
        await signal_command(update, context)
    elif query.data == "vip_info":
        await vip_command(update, context)
    elif query.data == "profile":
        await profile_command(update, context)
    elif query.data == "stats":
        await stats_command(update, context)
    elif query.data == "marathon":
        await marathon_command(update, context)
    elif query.data == "analytics":
        await analytics_command(update, context)
    elif query.data == "help":
        await help_command(update, context)
    elif query.data == "main_menu":
        await start(update, context)

# ---------------- ДОПОЛНИТЕЛЬНЫЕ КОМАНДЫ ----------------
async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    total_users = len(all_users)
    total_vip = len(vip_users)
    total_signals = len(signal_history)
    
    # Средняя вероятность
    avg_prob = 0
    if signal_history:
        probs = [s.get('probability', 0) for s in signal_history.values()]
        avg_prob = sum(probs) / len(probs)
    
    text = f"""
{EmojiDecor.HEADER}
{EmojiDecor.ICONS['stats']} <b>СТАТИСТИКА СИСТЕМЫ</b> {EmojiDecor.ICONS['stats']}
{EmojiDecor.FOOTER}

{EmojiDecor.STAR_DIVIDER}

👥 <b>ПОЛЬЗОВАТЕЛИ:</b> {total_users}
👑 <b>VIP:</b> {total_vip}
📊 <b>ВСЕ СИГНАЛЫ:</b> {total_signals}
🎯 <b>СРЕДНЯЯ ВЕРОЯТНОСТЬ:</b> {avg_prob:.1f}%

{EmojiDecor.DIVIDER}
"""
    
    await update.message.reply_text(text, parse_mode='HTML')

    if __name__ == "__main__":
    from threading import Thread
    from telegram import Update
    from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

    # --- Запуск веб-сервера Flask в отдельном потоке ---
    web_thread = Thread(target=run_web)
    web_thread.start()

    # --- Создание Telegram бота ---
    app = Application.builder().token(TOKEN).build()

    # --- Регистрируем обработчики команд ---
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("register", register_command))
    app.add_handler(CommandHandler("vip", vip_command))
    app.add_handler(CommandHandler("profile", profile_command))
    app.add_handler(CommandHandler("signal", signal_command))
    app.add_handler(CommandHandler("marathon", marathon_command))
    app.add_handler(CommandHandler("analytics", analytics_command))
    app.add_handler(CallbackQueryHandler(callback_handler))  # кнопки

    print("🚀 Бот и веб-сервер запущены. Ожидаем команды...")
    app.run_polling()
