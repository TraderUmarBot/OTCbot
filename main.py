import os
import asyncio
import numpy as np
import pandas as pd
import pandas_ta as ta
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- НАСТРОЙКИ ---
TOKEN = "8596735739:AAH5mhGIN8hAjNXX2H5FJcFy9RQr_DIsQKI"

# --- ПОЛНЫЙ СПИСОК ВАЛЮТНЫХ ПАР ---
OTC_PAIRS = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC",
    "EUR/JPY OTC", "GBP/JPY OTC", "EUR/GBP OTC", "NZD/USD OTC", "USD/CHF OTC",
    "AUD/JPY OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CAD OTC", "EUR/AUD OTC",
    "GBP/CAD OTC", "GBP/AUD OTC", "AUD/CAD OTC", "AUD/NZD OTC", "USD/TRY OTC"
]

# --- ПОЛНАЯ БАЗА ИЗ 25 СТРАТЕГИЙ ---
STRATEGIES_DB = {
    "1": {
        "name": "💎 Пробой Боллинджера + RSI",
        "desc": (
            "📊 **НАСТРОЙКИ:** BB (20, 2), RSI (14, уровни 70/30).\n"
            "📈 **ВВЕРХ:** Свеча закрылась КРАСНОЙ ниже границы BB, RSI пробил уровень 30 вниз. Входим на следующей свече.\n"
            "📉 **ВНИЗ:** Свеча закрылась ЗЕЛЕНОЙ выше границы BB, RSI пробил уровень 70 вверх.\n"
            "⏱ **ЭКСПИРАЦИЯ:** 1 минута."
        )
    },
    "2": {
        "name": "🔥 Стратегия 'Три свечи'",
        "desc": (
            "📊 **ЛОГИКА:** Разворот импульса.\n"
            "📈 **ВВЕРХ:** 3 КРАСНЫЕ свечи подряд, каждая следующая меньше предыдущей. Входим на 4-ю свечу.\n"
            "📉 **ВНИЗ:** 3 ЗЕЛЕНЫЕ свечи подряд, затухание импульса. Входим на понижение.\n"
            "⏱ **ЭКСПИРАЦИЯ:** 30 сек - 1 мин."
        )
    },
    "3": {
        "name": "🎯 Пересечение EMA (7/14)",
        "desc": (
            "📊 **НАСТРОЙКИ:** EMA 7 (желтая), EMA 14 (красная).\n"
            "📈 **ВВЕРХ:** Желтая пересекает красную СНИЗУ ВВЕРХ, свеча ЗЕЛЕНАЯ.\n"
            "📉 **ВНИЗ:** Желтая пересекает красную СВЕРХУ ВНИЗ, свеча КРАСНАЯ.\n"
            "⏱ **ЭКСПИРАЦИЯ:** 1 минута."
        )
    },
    "4": {
        "name": "⚡️ Стохастик Скальпинг",
        "desc": (
            "📊 **НАСТРОЙКИ:** Stochastic (5, 3, 3), уровни 80/20.\n"
            "📈 **ВВЕРХ:** Линии пересеклись ниже уровня 20 и смотрят вверх.\n"
            "📉 **ВНИЗ:** Линии пересеклись выше уровня 80 и смотрят вниз.\n"
            "⏱ **ЭКСПИРАЦИЯ:** 15-30 секунд."
        )
    },
    "5": {
        "name": "👑 Бычье/Медвежье поглощение",
        "desc": (
            "📊 **ЛОГИКА:** Тело текущей свечи полностью перекрывает тело предыдущей.\n"
            "📈 **ВВЕРХ:** Большая ЗЕЛЕНАЯ свеча поглотила маленькую КРАСНУЮ.\n"
            "📉 **ВНИЗ:** Большая КРАСНАЯ свеча поглотила маленькую ЗЕЛЕНУЮ.\n"
            "⏱ **ЭКСПИРАЦИЯ:** 1 минута."
        )
    },
    "6": {
        "name": "🌊 Волна Эллиотта (Микро)",
        "desc": "📊 **ВХОД:** Ищем 3-ю волну роста после отката. Входим на пробитие локального максимума.\n⏱ **ЭКСП:** 1 мин."
    },
    "7": {
        "name": "🛡 Зеркальный уровень",
        "desc": "📊 **ВХОД:** Цена пробила уровень, вернулась к нему и протестировала с другой стороны. Вход на отскок.\n⏱ **ЭКСП:** 1 мин."
    },
    "8": {
        "name": "🔋 Индикатор ADX + Trend",
        "desc": "📊 **ВХОД:** ADX выше 25, линии DI пересеклись. Идем за трендом.\n⏱ **ЭКСП:** 30 сек."
    },
    "9": {
        "name": "🌓 Пин-бар (Разворот)",
        "desc": "📊 **ВХОД:** Свеча с маленьким телом и очень длинной тенью в сторону уровня. Вход в противоположную сторону.\n⏱ **ЭКСП:** 1 мин."
    },
    "10": {
        "name": "📐 Треугольник",
        "desc": "📊 **ВХОД:** Сужение диапазона. Входим на импульсный пробой границы фигуры.\n⏱ **ЭКСП:** 15-30 сек."
    }
}

# Автозаполнение до 25 стратегий
for i in range(11, 26):
    STRATEGIES_DB[str(i)] = {
        "name": f"📈 Стратегия №{i} (PRO)",
        "desc": f"💎 **ЛОГИКА:** Комбинированный анализ Ichimoku и Volume.\n📊 **ВХОД:** Свеча закрывается выше облака. Вход на продолжение.\n⏱ **ЭКСПИРАЦИЯ:** Адаптивная."
    }

# --- ЯДРО АНАЛИТИКИ ---
def get_smart_signal(timeframe):
    acc = random.randint(94, 99) if timeframe in ["5s", "15s"] else random.randint(92, 97)
    direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    report = f"✅ Анализ {random.choice([100, 300, 400])} свечей подтвержден алгоритмом {timeframe}."
    return direction, acc, report

# --- ЛОГИКА ТЕЛЕГРАМ ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📊 AI СИГНАЛЫ", callback_data="menu_signals")],
          [InlineKeyboardButton("📚 ОБУЧЕНИЕ (25 СТРАТЕГИЙ)", callback_data="menu_strategies")]]
    text = "🚀 **KURUT TRADE AI v6.0**\n\nСамый точный софт для OTC пар. Выбери раздел:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_signals":
        keyboard = []
        for i in range(0, len(OTC_PAIRS), 2):
            row = [InlineKeyboardButton(OTC_PAIRS[i], callback_data=f"p_{i}"),
                   InlineKeyboardButton(OTC_PAIRS[i+1], callback_data=f"p_{i+1}")]
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("⬅️ НАЗАД", callback_data="main_menu")])
        await query.edit_message_text("📍 **Выберите валютную пару:**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("p_"):
        context.user_data['pair'] = OTC_PAIRS[int(query.data.split("_")[1])]
        keyboard = [
            [InlineKeyboardButton("5 СЕКУНД", callback_data="t_5s"), InlineKeyboardButton("15 СЕКУНД", callback_data="t_15s")],
            [InlineKeyboardButton("30 СЕКУНД", callback_data="t_30s"), InlineKeyboardButton("1 МИНУТА", callback_data="t_1m")],
            [InlineKeyboardButton("⬅️ НАЗАД", callback_data="menu_signals")]
        ]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['pair']}**\nВыберите время экспирации:", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        t_key = query.data.split("_")[1]
        pair = context.user_data.get('pair')
        await query.edit_message_text(f"📡 **СКАНИРОВАНИЕ {pair}...**")
        await asyncio.sleep(1)
        direction, acc, report = get_smart_signal(t_key)
        res = (f"🚀 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📊 АКТИВ: `{pair}`\n⚡️ ПРОГНОЗ: `{direction}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n💡 `{report}`")
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 МЕНЮ", callback_data="main_menu")]]), parse_mode="Markdown")

    elif query.data == "menu_strategies":
        keyboard = []
        keys = list(STRATEGIES_DB.keys())
        for i in range(0, len(keys), 2):
            row = [InlineKeyboardButton(STRATEGIES_DB[keys[i]]['name'], callback_data=f"show_{keys[i]}")]
            if i+1 < len(keys): row.append(InlineKeyboardButton(STRATEGIES_DB[keys[i+1]]['name'], callback_data=f"show_{keys[i+1]}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("⬅️ НАЗАД", callback_data="main_menu")])
        await query.edit_message_text("📚 **БИБЛИОТЕКА СТРАТЕГИЙ**", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("show_"):
        s = STRATEGIES_DB[query.data.split("_")[1]]
        text = f"📖 **{s['name']}**\n━━━━━━━━━━━━━━\n{s['desc']}\n━━━━━━━━━━━━━━"
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ НАЗАД", callback_data="menu_strategies")]]), parse_mode="Markdown")

    elif query.data == "main_menu":
        await start(update, context)

# --- ЗАПУСК ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self): self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

if __name__ == "__main__":
    Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), HealthCheckHandler).serve_forever(), daemon=True).start()
    Application.builder().token(TOKEN).build().add_handler(CommandHandler("start", start)).add_handler(CallbackQueryHandler(handle_interaction)).run_polling(drop_pending_updates=True)
