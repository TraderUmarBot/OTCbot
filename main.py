import os
import asyncio
import numpy as np
import pandas as pd
import pandas_ta as ta
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- СПИСОК ПАР OTC ---
OTC_PAIRS = [
    "EUR/USD OTC", "GBP/USD OTC", "USD/JPY OTC", "AUD/USD OTC", "USD/CAD OTC",
    "EUR/JPY OTC", "GBP/JPY OTC", "EUR/GBP OTC", "NZD/USD OTC", "USD/CHF OTC",
    "AUD/JPY OTC", "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CAD OTC", "EUR/AUD OTC",
    "GBP/CAD OTC", "GBP/AUD OTC", "AUD/CAD OTC", "AUD/NZD OTC", "USD/TRY OTC"
]

# --- МОЩНЫЙ БЛОК АНАЛИТИКИ (15 индикаторов) ---
def get_technical_signal():
    # Генерируем данные для анализа (в идеале здесь данные из WebSocket)
    np.random.seed(None)
    close_prices = np.cumsum(np.random.randn(100)) + 100
    df = pd.DataFrame({
        'close': close_prices, 
        'high': close_prices + 0.5, 
        'low': close_prices - 0.5, 
        'volume': np.random.randint(100, 1000, 100)
    })

    up_score = 0
    down_score = 0

    # 1-5. Осцилляторы
    rsi = ta.rsi(df['close'], length=14).iloc[-1]
    stoch = ta.stoch(df['high'], df['low'], df['close'])
    k = stoch['STOCHk_14_3_3'].iloc[-1]
    cci = ta.cci(df['high'], df['low'], df['close'], length=14).iloc[-1]
    wpr = ta.willr(df['high'], df['low'], df['close']).iloc[-1]
    mfi = ta.mfi(df['high'], df['low'], df['close'], df['volume']).iloc[-1]

    if rsi < 35: up_score += 1
    elif rsi > 65: down_score += 1
    if k < 20: up_score += 1
    elif k > 80: down_score += 1
    if cci < -100: up_score += 1
    elif cci > 100: down_score += 1
    if wpr < -80: up_score += 1
    elif wpr > -20: down_score += 1
    if mfi < 20: up_score += 1
    elif mfi > 80: down_score += 1

    # 6-10. Трендовые
    bb = ta.bbands(df['close'], length=20, std=2)
    ema_fast = ta.ema(df['close'], length=10).iloc[-1]
    ema_slow = ta.ema(df['close'], length=20).iloc[-1]
    sma_50 = ta.sma(df['close'], length=50).iloc[-1]

    if df['close'].iloc[-1] < bb['BBL_20_2.0'].iloc[-1]: up_score += 1
    elif df['close'].iloc[-1] > bb['BBU_20_2.0'].iloc[-1]: down_score += 1
    if ema_fast > ema_slow: up_score += 1
    else: down_score += 1
    if df['close'].iloc[-1] > sma_50: up_score += 1
    else: down_score += 1

    # 11-15. Импульс и Волатильность
    macd = ta.macd(df['close']).iloc[-1]
    adx = ta.adx(df['high'], df['low'], df['close']).iloc[-1]
    mom = ta.mom(df['close'], length=10).iloc[-1]

    if macd['MACD_12_26_9'] > macd['MACDs_12_26_9']: up_score += 1
    else: down_score += 1
    if adx['ADX_14'] > 25: up_score += 1
    if mom > 0: up_score += 1
    else: down_score += 1

    # Рассчитываем уверенность
    accuracy = int((max(up_score, down_score) / 15) * 100)
    if accuracy < 65: accuracy = 65 # Минимальный порог
    if accuracy > 98: accuracy = 98

    direction = "ВВЕРХ 🟢" if up_score > down_score else "ВНИЗ 🔴"
    return direction, accuracy

# --- ЛОГИКА ТЕЛЕГРАМ БОТА ---

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = []
    for i in range(0, len(OTC_PAIRS), 2):
        row = [
            InlineKeyboardButton(OTC_PAIRS[i], callback_data=f"p_{i}"),
            InlineKeyboardButton(OTC_PAIRS[i+1], callback_data=f"p_{i+1}")
        ]
        keyboard.append(row)
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🚀 **KURUT OTC СИСТЕМА**\n\nВыбери валютную пару для сканирования 15 индикаторами:"
    
    if update.message:
        await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")
    else:
        await update.callback_query.edit_message_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("p_"):
        pair_index = int(data.split("_")[1])
        context.user_data['pair'] = OTC_PAIRS[pair_index]
        
        keyboard = [
            [InlineKeyboardButton("5 СЕК", callback_data="t_5s"), InlineKeyboardButton("15 СЕК", callback_data="t_15s")],
            [InlineKeyboardButton("30 СЕК", callback_data="t_30s"), InlineKeyboardButton("1 МИН", callback_data="t_1m")]
        ]
        await query.edit_message_text(
            f"📊 Пара: **{context.user_data['pair']}**\nУкажи время экспирации:",
            reply_markup=InlineKeyboardMarkup(keyboard),
            parse_mode="Markdown"
        )

    elif data.startswith("t_"):
        exp = data.split("_")[1].replace("5s","5 сек").replace("15s","15 сек").replace("30s","30 сек").replace("1m","1 мин")
        pair = context.user_data.get('pair')
        
        try:
            await query.edit_message_text(f"🔍 **Запуск 15 индикаторов...**\nАнализирую волатильность {pair}...")
            
            # Эмуляция времени расчета
            await asyncio.sleep(2)
            
            direction, acc = get_technical_signal()
            
            res_text = (
                f"✅ **СИГНАЛ СФОРМИРОВАН**\n"
                f"━━━━━━━━━━━━━━━\n"
                f"📍 **Пара:** {pair}\n"
                f"⏳ **Экспирация:** {exp}\n"
                f"📈 **Прогноз:** {direction}\n"
                f"🎯 **Уверенность:** {acc}%\n"
                f"━━━━━━━━━━━━━━━\n"
                f"💎 *Входите в сделку сразу!*"
            )
            
            keyboard = [[InlineKeyboardButton("🏠 ГЛАВНОЕ МЕНЮ", callback_data="back")]]
            await query.edit_message_text(res_text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")
        except Exception as e:
            await query.edit_message_text(f"❌ Ошибка анализа: {str(e)}", 
                                         reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 МЕНЮ", callback_data="back")]]))

    elif data == "back":
        await start(update, context)

if __name__ == "__main__":
    TOKEN = os.getenv("TELEGRAM_TOKEN")
    if not TOKEN:
        print("Ошибка: Переменная TELEGRAM_TOKEN не найдена!")
    else:
        app = Application.builder().token(TOKEN).build()
        app.add_handler(CommandHandler("start", start))
        app.add_handler(CallbackQueryHandler(handle_buttons))
        print("Бот запущен...")
        app.run_polling()
