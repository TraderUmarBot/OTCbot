import os
import time
import random
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# 1. Список из 20 OTC пар
OTC_PAIRS = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC",
    "EUR/JPY OTC", "GBP/JPY OTC", "EUR/GBP OTC", "NZD/USD OTC", "USD/CHF OTC",
    "AUD/JPY OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CAD OTC", "EUR/AUD OTC",
    "GBP/CAD OTC", "GBP/AUD OTC", "AUD/CAD OTC", "AUD/NZD OTC", "USD/TRY OTC"
]

# 2. Стартовая команда
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    # Создаем кнопки по 2 в ряд
    for i in range(0, len(OTC_PAIRS), 2):
        row = [
            InlineKeyboardButton(OTC_PAIRS[i], callback_data=f"pair_{OTC_PAIRS[i]}"),
            InlineKeyboardButton(OTC_PAIRS[i+1], callback_data=f"pair_{OTC_PAIRS[i+1]}")
        ]
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("👋 Привет! Выбери валютную пару OTC для анализа:", reply_markup=reply_markup)

# 3. Обработка выбора пары и времени
async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    # Если выбрали ПАРУ
    if data.startswith("pair_"):
        pair = data.split("_")[1]
        context.user_data['selected_pair'] = pair
        
        keyboard = [
            [InlineKeyboardButton("5 СЕК", callback_data="exp_5s"), 
             InlineKeyboardButton("15 СЕК", callback_data="exp_15s")],
            [InlineKeyboardButton("30 СЕК", callback_data="exp_30s"), 
             InlineKeyboardButton("1 МИН", callback_data="exp_1min")]
        ]
        await query.edit_message_text(
            f"✅ Выбрана пара: {pair}\nТеперь выбери время экспирации:",
            reply_markup=InlineKeyboardMarkup(keyboard)
        )

    # Если выбрали ВРЕМЯ (Сигнал)
    elif data.startswith("exp_"):
        exp_time = data.split("_")[1].replace("s", " сек").replace("1min", "1 мин")
        pair = context.user_data.get('selected_pair', 'Неизвестно')
        
        await query.edit_message_text(f"🔍 Анализирую {pair} на {exp_time}...")
        
        # Здесь должна быть логика анализа (RSI/Bollinger)
        # Пока сделаем имитацию задержки и результат
        time.sleep(1.5) 
        side = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
        power = random.randint(70, 95)
        
        result_text = (
            f"📊 **СИГНАЛ СФОРМИРОВАН**\n\n"
            f"📍 Пара: {pair}\n"
            f"⏱ Время: {exp_time}\n"
            f"📈 Направление: {side}\n"
            f"🔥 Сила сигнала: {power}%"
        )
        
        keyboard = [[InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="main_menu")]]
        await query.edit_message_text(result_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

    # Возврат в меню
    elif data == "main_menu":
        # Просто вызываем функцию старта заново (но через edit)
        keyboard = []
        for i in range(0, len(OTC_PAIRS), 2):
            row = [InlineKeyboardButton(OTC_PAIRS[i], callback_data=f"pair_{OTC_PAIRS[i]}"),
                   InlineKeyboardButton(OTC_PAIRS[i+1], callback_data=f"pair_{OTC_PAIRS[i+1]}")]
            keyboard.append(row)
        await query.edit_message_text("👋 Выбери валютную пару OTC для анализа:", reply_markup=InlineKeyboardMarkup(keyboard))

# 4. Запуск
if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN") # Токен берем из Render Env
    application = Application.builder().token(TOKEN).build()
    
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    
    print("Бот запущен...")
    application.run_polling()
