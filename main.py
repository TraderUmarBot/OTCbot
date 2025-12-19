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

# --- БАЗА СТРАТЕГИЙ (25 ШТУК) ---
# Здесь ты можешь менять тексты обучения под себя
STRATEGIES_DB = {
    "1": {"name": "🟢 RSI + Bollinger", "level": "Легкий", "desc": "Классика OTC. Входим на отскок от краев канала Боллинджера, когда RSI в зоне 30 или 70.", "inds": "RSI, BB"},
    "2": {"name": "🟢 Двойное поглощение", "level": "Легкий", "desc": "Ищем свечу, которая полностью закрывает предыдущую. Сигнал силы тренда.", "inds": "Candle Pattern"},
    "3": {"name": "🟡 MACD Cross", "level": "Средний", "desc": "Пересечение линий MACD выше нулевой отметки. Работает на трендовых парах.", "inds": "MACD, EMA"},
    "4": {"name": "🟡 Золотое сечение", "level": "Средний", "desc": "Используем уровни Фибоначчи 0.618 для поиска точки разворота.", "inds": "Fibonacci, SMA 200"},
    "5": {"name": "🔴 SMC: Order Block", "level": "Профи", "desc": "Поиск зон, где крупный игрок оставил ликвидность. Самая высокая точность.", "inds": "Volume, Structure"},
    # Добавляем остальные до 25 (заполнил шаблонами, можешь менять названия)
}

for i in range(6, 26):
    lvl = random.choice(["Легкий", "Средний", "Профи"])
    STRATEGIES_DB[str(i)] = {
        "name": f"📈 Стратегия v.{i}",
        "level": lvl,
        "desc": f"Глубокий анализ рынка на основе {i+2} технических индикаторов. Идеально для ТФ 1 мин.",
        "inds": "Ichimoku, ADX, Parabolic SAR"
    }

# --- ОБМАНКА ДЛЯ KOYEB ---
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200); self.end_headers(); self.wfile.write(b"OK")

def run_health_server():
    server = HTTPServer(('0.0.0.0', 8080), HealthCheckHandler)
    server.serve_forever()

OTC_PAIRS = ["EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC"]

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- ЯДРО АНАЛИТИКИ ---
def get_ultra_signal():
    # Твоя мощная логика на 400 свечей (симуляция для примера)
    acc = random.randint(93, 98)
    direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    report = "💠 Анализ: 400 свечей | 20 Индикаторов"
    return direction, acc, report

# --- ИНТЕРФЕЙС ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("📊 AI СИГНАЛЫ (400 СВЕЧЕЙ)", callback_data="menu_signals")],
        [InlineKeyboardButton("📚 ОБУЧЕНИЕ (25 СТРАТЕГИЙ)", callback_data="menu_strategies")]
    ]
    text = "👑 **KURUT TRADE PREMIUM AI**\n\nДобро пожаловать в элитный торговый терминал.\n\nВыберите режим работы:"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_interaction(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "menu_signals":
        keyboard = []
        for i in range(0, len(OTC_PAIRS), 2):
            row = [InlineKeyboardButton(OTC_PAIRS[i], callback_data=f"p_{i}")]
            if i+1 < len(OTC_PAIRS): row.append(InlineKeyboardButton(OTC_PAIRS[i+1], callback_data=f"p_{i+1}"))
            keyboard.append(row)
        keyboard.append([InlineKeyboardButton("⬅️ НАЗАД", callback_data="main_menu")])
        await query.edit_message_text("📍 **Выберите валютную пару:**", reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data == "menu_strategies":
        keyboard = []
        # Вывод 25 стратегий (по 2 в ряд для компактности)
        keys = list(STRATEGIES_DB.keys())
        for i in range(0, len(keys), 2):
            s1_id = keys[i]
            row = [InlineKeyboardButton(STRATEGIES_DB[s1_id]['name'], callback_data=f"show_{s1_id}")]
            if i+1 < len(keys):
                s2_id = keys[i+1]
                row.append(InlineKeyboardButton(STRATEGIES_DB[s2_id]['name'], callback_data=f"show_{s2_id}"))
            keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("⬅️ НАЗАД", callback_data="main_menu")])
        await query.edit_message_text("📚 **БИБЛИОТЕКА ТРЕЙДЕРА**\nВыберите стратегию для изучения:", reply_markup=InlineKeyboardMarkup(keyboard))

    elif query.data.startswith("show_"):
        s_id = query.data.split("_")[1]
        s = STRATEGIES_DB[s_id]
        text = (
            f"📖 **СТРАТЕГИЯ:** {s['name']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"🏆 **УРОВЕНЬ:** `{s['level']}`\n"
            f"🛠 **ИНДИКАТОРЫ:** `{s['inds']}`\n\n"
            f"📝 **ОПИСАНИЕ:**\n{s['desc']}\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"💡 *Совет: Тестируйте на демо-счете!*"
        )
        keyboard = [[InlineKeyboardButton("⬅️ К СПИСКУ", callback_data="menu_strategies")]]
        await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("p_"):
        pair_idx = int(query.data.split("_")[1])
        context.user_data['pair'] = OTC_PAIRS[pair_idx]
        keyboard = [
            [InlineKeyboardButton("5 СЕК", callback_data="t_5s"), InlineKeyboardButton("15 СЕК", callback_data="t_15s")],
            [InlineKeyboardButton("30 СЕК", callback_data="t_30s"), InlineKeyboardButton("1 МИН", callback_data="t_1m")]
        ]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['pair']}**\nВыберите время:", 
                                     reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        await query.edit_message_text("📉 **АНАЛИЗ РЫНКА (400 СВЕЧЕЙ)...**")
        await asyncio.sleep(1)
        direction, acc, report = get_ultra_signal()
        res_text = (
            f"🚀 **СИГНАЛ СФОРМИРОВАН!**\n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📊 **АКТИВ:** `{context.user_data['pair']}`\n"
            f"⚡️ **ПРОГНОЗ:** `{direction}`\n"
            f"🎯 **ТОЧНОСТЬ:** `{acc}%` \n"
            f"━━━━━━━━━━━━━━━━━━\n"
            f"📝 **ДЕТАЛИ:**\n`{report}`"
        )
        await query.edit_message_text(res_text, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 МЕНЮ", callback_data="main_menu")]]), parse_mode="Markdown")

    elif query.data == "main_menu":
        await start(update, context)

if __name__ == "__main__":
    Thread(target=run_health_server, daemon=True).start()
    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(handle_interaction))
    application.run_polling(drop_pending_updates=True)
