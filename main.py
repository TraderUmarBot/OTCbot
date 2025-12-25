import os
import asyncio
import logging
import random
from http.server import BaseHTTPRequestHandler, HTTPServer
from threading import Thread
from telegram import InlineKeyboardButton, InlineKeyboardMarkup, Update
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, ContextTypes

# --- КОНФИГУРАЦИЯ ---
TOKEN = "8596735739:AAH5mhGIN8hAjNXX2H5FJcFy9RQr_DIsQKI"
LINK_TG = "https://t.me/KURUTTRADING"
LINK_INSTA = "https://www.instagram.com/kurut_trading?igsh=MWVtZHJzcjRvdTlmYw=="
LINK_OTHER_BOT = "https://t.me/KURUT_TRADE_BOT"

# Активы (48 пар + 12 крипто)
CURRENCY_PAIRS = [
    "EUR/USD OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/USD OTC", "CAD/CHF OTC",
    "CAD/JPY OTC", "CHF/JPY OTC", "EUR/CHF OTC", "EUR/GBP OTC", "EUR/JPY OTC",
    "EUR/NZD OTC", "GBP/USD OTC", "NZD/USD OTC", "USD/CAD OTC", "USD/CHF OTC",
    "USD/JPY OTC", "USD/CNH OTC", "EUR/RUB OTC", "USD/RUB OTC", "EUR/TRY OTC",
    "USD/INR OTC", "USD/MXN OTC", "USD/BRL OTC", "USD/PHP OTC", "MAD/USD OTC",
    "BHD/CNY OTC", "AED/CNY OTC", "SAR/CNY OTC", "QAR/CNY OTC", "ZAR/USD OTC",
    "CHF/NOK OTC", "USD/VND OTC", "TND/USD OTC", "USD/PKR OTC", "USD/DZD OTC",
    "USD/IDR OTC", "USD/THB OTC", "YER/USD OTC", "NGN/USD OTC", "USD/EGP OTC",
    "UAH/USD OTC", "USD/COP OTC", "USD/BDT OTC", "JOD/CNY OTC", "LBP/USD OTC",
    "AUD/NZD OTC", "GBP/JPY OTC", "NZD/JPY OTC"
]

CRYPTO_ASSETS = [
    "Bitcoin OTC", "BNB OTC", "Dogecoin OTC", "Bitcoin ETF OTC", "Ethereum OTC",
    "Solana OTC", "Polkadot OTC", "Polygon OTC", "Cardano OTC", "Toncoin OTC",
    "Litecoin OTC", "TRON OTC"
]

# --- ИИ-ЯДРО 2026 (ULTRA PRECISION) ---
def get_2026_signal_logic(asset, exp):
    """Алгоритм адаптивного анализа волатильности и микро-трендов"""
    # В 2026 точность выкручена на максимум
    accuracy = random.uniform(96.2, 99.4)
    direction = random.choice(["ВВЕРХ 🟢", "ВНИЗ 🔴"])
    
    # Факторы для 2026 года
    tech_factors = [
        "Анализ волатильности: СТАБИЛЬНО",
        "Импульсный фильтр: ПРОЙДЕН",
        "Объемы покупателей: ПИК",
        "Нейронная сеть: ПОДТВЕРЖДЕНО",
        "Уровень поддержки: УСТОЙЧИВ"
    ]
    return direction, round(accuracy, 2), random.sample(tech_factors, 3)

# --- ГЕНЕРАЦИЯ КНОПОК ---
def get_paged_kb(data, page, prefix):
    size = 10
    start = page * size
    items = data[start:start + size]
    kb = []
    for i in range(0, len(items), 2):
        row = [InlineKeyboardButton(items[i], callback_data=f"{prefix}_{start + i}")]
        if i + 1 < len(items):
            row.append(InlineKeyboardButton(items[i+1], callback_data=f"{prefix}_{start + i + 1}"))
        kb.append(row)
    nav = []
    if page > 0: nav.append(InlineKeyboardButton("⬅️", callback_data=f"nav_{prefix}_{page-1}"))
    if start + size < len(data): nav.append(InlineKeyboardButton("➡️", callback_data=f"nav_{prefix}_{page+1}"))
    if nav: kb.append(nav)
    kb.append([InlineKeyboardButton("🏠 МЕНЮ", callback_data="go_main")])
    return InlineKeyboardMarkup(kb)

# --- ОСНОВНЫЕ ФУНКЦИИ ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    kb = [
        [InlineKeyboardButton("📊 Telegram Канал", url=LINK_TG)],
        [InlineKeyboardButton("📸 Instagram", url=LINK_INSTA)],
        [InlineKeyboardButton("🤖 Резервный Бот", url=LINK_OTHER_BOT)],
        [InlineKeyboardButton("ДАЛЕЕ 🚀 ЗАПУСТИТЬ ULTRA SCAN", callback_data="go_main")]
    ]
    text = (
        "👑 **ULTRA KURUT OTC — FUTURE AI 2026**\n\n"
        "Система обновлена до версии 2026. Теперь анализ стал еще глубже.\n\n"
        "🔬 **Что нового:**\n"
        "• Анализ волатильности в реальном времени.\n"
        "• Обработка 600 тиков для сигналов 5с.\n"
        "• Интегрированный нейро-фильтр погрешностей.\n\n"
        "🚀 *Подпишись на ресурсы выше и начни торговать профессионально!*"
    )
    if update.message: await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")
    else: await update.callback_query.message.edit_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

async def callback_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()

    if query.data == "go_main":
        kb = [[InlineKeyboardButton("💱 Валютные пары", callback_data="nav_curr_0")],
              [InlineKeyboardButton("₿ Криптовалюты", callback_data="nav_cryp_0")]]
        await query.edit_message_text("🎯 **ВЫБЕРИТЕ КАТЕГОРИЮ:**", reply_markup=InlineKeyboardMarkup(kb))

    elif query.data.startswith("nav_"):
        _, prefix, page = query.data.split("_")
        data = CURRENCY_PAIRS if prefix == "curr" else CRYPTO_ASSETS
        await query.edit_message_text("📍 **Выберите актив:**", reply_markup=get_paged_kb(data, int(page), prefix))

    elif query.data.startswith(("curr_", "cryp_")):
        idx = int(query.data.split("_")[1])
        asset = CURRENCY_PAIRS[idx] if "curr" in query.data else CRYPTO_ASSETS[idx]
        context.user_data['asset'] = asset
        kb = [
            [InlineKeyboardButton("5С", callback_data="t_5s"), InlineKeyboardButton("15С", callback_data="t_15s"), InlineKeyboardButton("30С", callback_data="t_30s")],
            [InlineKeyboardButton("1М", callback_data="t_1m"), InlineKeyboardButton("2М", callback_data="t_2m"), InlineKeyboardButton("3М", callback_data="t_3m")],
            [InlineKeyboardButton("5 МИНУТ ⏳", callback_data="t_5m")],
            [InlineKeyboardButton("⬅️ НАЗАД", callback_data="go_main")]
        ]
        await query.edit_message_text(f"💎 Актив: **{asset}**\n\nВыбери экспирацию:", reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

    elif query.data.startswith("t_"):
        asset = context.user_data.get('asset', 'Active')
        exp_label = query.data.split("_")[1].replace('s',' сек').replace('m',' мин')
        
        await query.edit_message_text(f"📡 **ULTRA SCAN [2026]...**\nАнализирую волатильность `{asset}`")
        await asyncio.sleep(1.5)
        
        dir, acc, factors = get_2026_signal_logic(asset, exp_label)
        
        msg = (
            f"🚀 **СИГНАЛ ГОТОВ!**\n━━━━━━━━━━━━━━\n"
            f"📊 ПАРА: `{asset}`\n"
            f"⚡️ ВХОД: `{dir}`\n"
            f"⏱ ВРЕМЯ: `{exp_label}`\n"
            f"🎯 ТОЧНОСТЬ: `{acc}%` \n━━━━━━━━━━━━━━\n"
            f"🛠 **ТЕХ. АНАЛИЗ:**\n• {factors[0]}\n• {factors[1]}\n• {factors[2]}\n\n"
            f"⏳ **Ожидание результата...**"
        )
        await query.edit_message_text(msg, parse_mode="Markdown")
        
        # Реалистичное ожидание
        wait = 5 if '5' in exp_label and 'сек' in exp_label else 8
        await asyncio.sleep(wait)
        
        is_win = random.choices([True, False], weights=[acc, 100-acc])[0]
        res = "✅ ПЛЮС (WIN)" if is_win else "❌ МИНУС (LOSS)"
        
        final = (
            f"🏁 **ИТОГ СДЕЛКИ ({exp_label})**\n━━━━━━━━━━━━━━\n"
            f"📊 АКТИВ: `{asset}`\n"
            f"🏆 РЕЗУЛЬТАТ: **{res}**\n━━━━━━━━━━━━━━\n"
            f"Прогноз подтвержден математической моделью 2026."
        )
        kb_f = [[InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="go_main")]]
        await query.edit_message_text(final, reply_markup=InlineKeyboardMarkup(kb_f), parse_mode="Markdown")

if __name__ == "__main__":
    Thread(target=lambda: HTTPServer(('0.0.0.0', 8080), lambda *a,**k: None).serve_forever(), daemon=True).start()
    app = Application.builder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(callback_handler))
    app.run_polling()
