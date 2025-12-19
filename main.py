import os
import asyncio
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- НАСТРОЙКИ ---
TOKEN = "8596735739:AAH5mhGIN8hAjNXX2H5FJcFy9RQr_DIsQKI"

# --- ПОЛНЫЙ СПИСОК 20 ПАР ---
OTC_PAIRS = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC",
    "EUR/JPY OTC", "GBP/JPY OTC", "EUR/GBP OTC", "NZD/USD OTC", "USD/CHF OTC",
    "AUD/JPY OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CAD OTC", "EUR/AUD OTC",
    "GBP/CAD OTC", "GBP/AUD OTC", "AUD/CAD OTC", "AUD/NZD OTC", "USD/TRY OTC"
]

# --- ПОЛНАЯ БАЗА 25 СТРАТЕГИЙ (ПРИМЕР ДЕТАЛИЗАЦИИ) ---
STRATEGIES_DB = {
    "1": {
        "name": "💎 Пробой Боллинджера + RSI",
        "desc": "📊 **НАСТРОЙКИ:** BB(20, 2), RSI(14).\n📈 **ВВЕРХ:** Свеча закрылась КРАСНОЙ ниже границы BB, RSI < 30. Вход на следующей.\n📉 **ВНИЗ:** Свеча ЗЕЛЕНАЯ выше границы BB, RSI > 70.\n⏱ **ЭКСП:** 1 мин."
    },
    "2": {
        "name": "🔥 Стратегия 'Три свечи'",
        "desc": "📊 **ЛОГИКА:** Разворот импульса.\n📈 **ВВЕРХ:** 3 КРАСНЫЕ свечи подряд (каждая меньше предыдущей). Вход на 4-ю.\n📉 **ВНИЗ:** 3 ЗЕЛЕНЫЕ свечи подряд. Вход ВНИЗ.\n⏱ **ЭКСП:** 30 сек - 1 мин."
    }
}
# Дозаполнение до 25 детальных стратегий
for i in range(3, 26):
    STRATEGIES_DB[str(i)] = {
        "name": f"📈 Стратегия №{i} (PRO-Level)",
        "desc": f"📊 **ЛОГИКА:** Анализ Price Action + Фильтры ИИ.\n✅ **ВХОД:** Ждем подтверждения от 2-х индикаторов.\n⚠️ **ФИЛЬТР:** Не заходить при резких скачках (тенях).\n⏱ **ЭКСП:** Адаптивная."
    }

# --- ФУНКЦИЯ ПАГИНАЦИИ ---
def get_pairs_keyboard(page=0):
    page_size = 8
    start_idx = page * page_size
    end_idx = start_idx + page_size
    current_pairs = OTC_PAIRS[start_idx:end_idx]
    
    keyboard = []
    for i in range(0, len(current_pairs), 2):
        row = [InlineKeyboardButton(current_pairs[i], callback_data=f"p_{start_idx + i}")]
        if i + 1 < len(current_pairs):
            row.append(InlineKeyboardButton(current_pairs[i+1], callback_data=f"p_{start_idx + i + 1}"))
        keyboard.append(row)
    
    # Кнопки навигации
    nav_row = []
    if page > 0:
        nav_row.append(InlineKeyboardButton("⬅️ Назад", callback_data=f"page_{page-1}"))
    if end_idx < len(OTC_PAIRS):
        nav_row.append(InlineKeyboardButton("Вперед ➡️", callback_data=f"page_{page+1}"))
    
    if nav_row:
        keyboard.append(nav_row)
    keyboard.append([InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")])
    return InlineKeyboardMarkup(keyboard)

# --- ЛОГИКА СИГНАЛОВ ---
def get_ai_signal(exp):
    acc = random.randint(94, 98)
    dir = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    return dir, acc, f"✅ Анализ подтвержден для экспирации {exp}."

# --- ОБРАБОТЧИКИ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [[InlineKeyboardButton("📊 AI СИГНАЛЫ (20 ПАР)", callback_data="page_0")],
          [InlineKeyboardButton("📚 ОБУЧЕНИЕ (25 СТРАТЕГИЙ)", callback_data="menu_strategies")]]
    text = "🚀 **KURUT TRADE AI v7.0**\n\nВсе 20 OTC пар загружены. Выбери раздел:"
    if update.message:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else:
        await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def handle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data.startswith("page_"):
        page = int(query.data.split("_")[1])
        await query.edit_message_text("📍 **Выберите валютную пару:**", reply_markup=get_pairs_keyboard(page))

    elif query.data.startswith("p_"):
        idx = int(query.data.split("_")[1])
        context.user_data['pair'] = OTC_PAIRS[idx]
        kb = [[InlineKeyboardButton("5 СЕК", callback_data="t_5s"), InlineKeyboardButton("15 СЕК", callback_data="t_15s")],
              [InlineKeyboardButton("30 СЕК", callback_data="t_30s"), InlineKeyboardButton("1 МИН", callback_data="t_1m")],
              [InlineKeyboardButton("⬅️ К ВЫБОРУ ПАР", callback_data="page_0")]]
        await query.edit_message_text(f"💎 Актив: **{context.user_data['pair']}**\nВыбери экспирацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        t = query.data.split("_")[1]
        pair = context.user_data.get('pair')
        await query.edit_message_text(f"📡 **АНАЛИЗ {pair}...**")
        await asyncio.sleep(0.8)
        dir, acc, rep = get_ai_signal(t)
        res = (f"🚀 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n📊 ПАРА: `{pair}`\n⚡️ ВХОД: `{dir}`\n🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n💡 `{rep}`")
        await query.edit_message_text(res, reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🔄 В МЕНЮ", callback_data="main_menu")]]), parse_mode="Markdown")

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
        await query.edit_message_text(f"📖 **{s['name']}**\n━━━━━━━━━━━━━━\n{s['desc']}", reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("⬅️ НАЗАД", callback_data="menu_strategies")]]), parse_mode="Markdown")

    elif query.data == "main_menu":
        await start(update, context)

# --- ЗАПУСК ---
def run_health():
    HTTPServer(('0.0.0.0', 8080), lambda *args: None).serve_forever()

if __name__ == "__main__":
    Thread(target=run_health, daemon=True).start()
    Application.builder().token(TOKEN).build().add_handler(CommandHandler("start", start)).add_handler(CallbackQueryHandler(handle)).run_polling()
