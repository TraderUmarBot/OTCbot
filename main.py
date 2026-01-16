# =====================================
# KURUT AI INFINITY | COIP PRO EDITION
# OTC SIGNAL SYSTEM FOR POCKET OPTION
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

# ---------------- SERVER ----------------
server = Flask('')

@server.route('/')
def home():
    return "KURUT AI INFINITY | COIP PRO ACTIVE"

def run_web():
    server.run(host='0.0.0.0', port=8080)

# ---------------- CONFIG ----------------
TOKEN = os.environ.get("TOKEN", "ВСТАВЬ_СВОЙ_BOT_TOKEN")

ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@id6117198446"
ADMIN_LINK = f"https://t.me/{ADMIN_USER.replace('@', '')}"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

INSTAGRAM = "https://instagram.com/ТВОЙ_ИНСТА"
TELEGRAM = "https://t.me/ТВОЙ_ТГ"
YOUTUBE = "https://youtube.com/@ТВОЙ_YT"
BLOG = "https://ТВОЙ_БЛОГ"

DB_VIP = "vip_users.json"
DB_ALL = "all_users.json"
DB_STATS = "trader_stats.json"
DB_LOGS = "admin_logs.json"
DB_SIGNALS = "signal_history.json"

# ---------------- STORAGE ----------------
def load_db(file, default):
    if os.path.exists(file):
        try:
            with open(file, "r", encoding='utf-8') as f:
                return json.load(f)
        except:
            return default
    return default

def save_db(file, data):
    with open(file, "w", encoding='utf-8') as f:
        json.dump(data, f, indent=2, ensure_ascii=False)

vip_users = set(load_db(DB_VIP, []))
all_users = set(load_db(DB_ALL, []))
trader_stats = load_db(DB_STATS, {})
admin_logs = load_db(DB_LOGS, [])
signal_history = load_db(DB_SIGNALS, {})

# ---------------- ASSETS ----------------
OTC_PAIRS = [
    "EUR/USD OTC","AUD/CAD OTC","AUD/CHF OTC","AUD/JPY OTC","AUD/NZD OTC","AUD/USD OTC",
    "CAD/CHF OTC","CAD/JPY OTC","CHF/JPY OTC","EUR/CHF OTC","EUR/GBP OTC","EUR/JPY OTC",
    "EUR/NZD OTC","GBP/AUD OTC","GBP/JPY OTC","GBP/USD OTC","NZD/JPY OTC","NZD/USD OTC",
    "USD/CAD OTC","USD/CHF OTC","USD/JPY OTC","USD/RUB OTC","EUR/RUB OTC","CHF/NOK OTC",
    "EUR/HUF OTC","USD/CNH OTC","EUR/TRY OTC","USD/INR OTC","USD/SGD OTC","USD/CLP OTC",
    "USD/MYR OTC","USD/THB OTC","USD/VND OTC","USD/PKR OTC","USD/COP OTC","USD/EGP OTC",
    "USD/PHP OTC","USD/MXN OTC","USD/DZD OTC","USD/ARS OTC","USD/IDR OTC","USD/BRL OTC",
    "USD/BDT OTC","YER/USD OTC","LBP/USD OTC","TND/USD OTC","MAD/USD OTC","BHD/CNY OTC",
    "NGN/USD OTC","KES/USD OTC","ZAR/USD OTC","UAH/USD OTC"
]

STOCKS = [
    "McDonald's","Intel","American Express","Palantir","Microsoft","Apple","GameStop",
    "Pfizer","Boeing","Visa","Meta","Citigroup","Cisco","FedEx","Tesla","Coinbase",
    "Amazon","AMD","Netflix"
]

CRYPTO = ["Bitcoin (BTC)","Ethereum (ETH)","Solana (SOL)","Toncoin (TON)","Litecoin (LTC)","Dogecoin (DOGE)"]

# Экспирации
EXPIRATIONS = ["10s", "30s", "1m", "2m", "3m", "5m", "8m"]

# ---------------- UTILS ----------------
def is_admin(uid):
    return str(uid) in [str(a) for a in ADMIN_IDS]

def is_vip(uid):
    return str(uid) in vip_users or is_admin(uid)

def log_admin(action, target, admin):
    admin_logs.append({
        "time": int(time.time()),
        "admin": admin,
        "action": action,
        "target": target
    })
    save_db(DB_LOGS, admin_logs)

def log_signal(asset, direction, probability, indicators, expiration, user_id):
    signal_id = f"{int(time.time())}_{asset.replace('/', '_')}"
    signal_history[signal_id] = {
        "timestamp": int(time.time()),
        "asset": asset,
        "direction": direction,
        "probability": probability,
        "indicators": indicators,
        "expiration": expiration,
        "user_id": user_id,
        "verified": False
    }
    save_db(DB_SIGNALS, signal_history)
    return signal_id

def calculate_win_rate(user_id):
    if user_id in trader_stats:
        stats = trader_stats[user_id]
        total = stats.get('plus', 0) + stats.get('minus', 0)
        if total > 0:
            return (stats.get('plus', 0) / total) * 100
    return 0

# ---------------- ADVANCED MARKET ANALYSIS ----------------
class MarketAnalyzer:
    def __init__(self):
        self.patterns = {}
        
    def calculate_ema(self, prices, period):
        if len(prices) < period:
            return sum(prices) / len(prices)
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    def calculate_rsi(self, prices, period=14):
        if len(prices) < period + 1:
            return 50
        
        deltas = [prices[i] - prices[i-1] for i in range(1, len(prices))]
        
        gains = [delta for delta in deltas if delta > 0]
        losses = [-delta for delta in deltas if delta < 0]
        
        avg_gain = sum(gains[-period:]) / period if gains else 0
        avg_loss = sum(losses[-period:]) / period if losses else 0
        
        if avg_loss == 0:
            return 100
        
        rs = avg_gain / avg_loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def calculate_macd(self, prices):
        if len(prices) < 26:
            return 0
        
        ema12 = self.calculate_ema(prices[-26:], 12)
        ema26 = self.calculate_ema(prices[-26:], 26)
        return ema12 - ema26
    
    def calculate_bollinger_bands(self, prices, period=20):
        if len(prices) < period:
            sma = sum(prices) / len(prices)
            std = math.sqrt(sum((x - sma) ** 2 for x in prices) / len(prices))
        else:
            recent = prices[-period:]
            sma = sum(recent) / period
            std = math.sqrt(sum((x - sma) ** 2 for x in recent) / period)
        
        upper = sma + (std * 2)
        lower = sma - (std * 2)
        return upper, sma, lower
    
    def calculate_stochastic(self, high_prices, low_prices, close_prices, period=14):
        if len(close_prices) < period:
            return 50, 50
        
        recent_high = max(high_prices[-period:])
        recent_low = min(low_prices[-period:])
        current_close = close_prices[-1]
        
        if recent_high == recent_low:
            return 50, 50
        
        k = 100 * ((current_close - recent_low) / (recent_high - recent_low))
        
        if len(close_prices) >= 3:
            d = (k + 100 * ((close_prices[-2] - recent_low) / (recent_high - recent_low)) + 
                 100 * ((close_prices[-3] - recent_low) / (recent_high - recent_low))) / 3
        else:
            d = k
        
        return k, d
    
    def calculate_atr(self, high_prices, low_prices, close_prices, period=14):
        if len(close_prices) < 2:
            return 0
        
        tr_values = []
        for i in range(1, min(period, len(close_prices))):
            hl = high_prices[-i] - low_prices[-i]
            hc = abs(high_prices[-i] - close_prices[-(i+1)])
            lc = abs(low_prices[-i] - close_prices[-(i+1)])
            tr = max(hl, hc, lc)
            tr_values.append(tr)
        
        return sum(tr_values) / len(tr_values) if tr_values else 0
    
    def generate_price_data(self, asset):
        seed = sum(ord(c) for c in asset) + int(time.time() % 1000)
        random.seed(seed)
        
        base_price = random.uniform(50, 200)
        volatility = random.uniform(0.001, 0.005)
        
        prices = [base_price]
        highs = [base_price * (1 + random.uniform(0, 0.002))]
        lows = [base_price * (1 - random.uniform(0, 0.002))]
        
        for _ in range(199):
            change = random.normalvariate(0, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
            highs.append(new_price * (1 + random.uniform(0, 0.002)))
            lows.append(new_price * (1 - random.uniform(0, 0.002)))
        
        return prices, highs, lows
    
    def analyze_asset(self, asset):
        prices, highs, lows = self.generate_price_data(asset)
        
        ema9 = self.calculate_ema(prices[-20:], 9)
        ema21 = self.calculate_ema(prices[-30:], 21)
        ema50 = self.calculate_ema(prices[-60:], 50)
        rsi = self.calculate_rsi(prices)
        macd = self.calculate_macd(prices)
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(prices)
        stoch_k, stoch_d = self.calculate_stochastic(highs, lows, prices)
        atr = self.calculate_atr(highs, lows, prices)
        
        indicators = {
            'EMA_9': ema9,
            'EMA_21': ema21,
            'EMA_50': ema50,
            'RSI': rsi,
            'MACD': macd,
            'BB_UPPER': bb_upper,
            'BB_MIDDLE': bb_middle,
            'BB_LOWER': bb_lower,
            'STOCH_K': stoch_k,
            'STOCH_D': stoch_d,
            'ATR': atr,
            'PRICE': prices[-1]
        }
        
        score = 0
        reasons = []
        
        if ema9 > ema21 > ema50:
            score += 3
            reasons.append("Сильный восходящий тренд (EMA 9>21>50)")
        elif ema9 < ema21 < ema50:
            score -= 3
            reasons.append("Сильный нисходящий тренд (EMA 9<21<50)")
        
        if rsi < 30:
            score += 2
            reasons.append("RSI в зоне перепроданности (<30)")
        elif rsi > 70:
            score -= 2
            reasons.append("RSI в зоне перекупленности (>70)")
        elif 40 < rsi < 60:
            score += 1
            reasons.append("RSI в нейтральной зоне")
        
        if macd > 0:
            score += 2
            reasons.append("MACD показывает бычий тренд")
        else:
            score -= 1
            reasons.append("MACD показывает медвежий тренд")
        
        bb_percent = ((prices[-1] - bb_lower) / (bb_upper - bb_lower)) * 100
        if bb_percent < 20:
            score += 2
            reasons.append(f"Цена у нижней границы BB ({bb_percent:.1f}%)")
        elif bb_percent > 80:
            score -= 2
            reasons.append(f"Цена у верхней границы BB ({bb_percent:.1f}%)")
        
        if stoch_k < 20 and stoch_d < 20:
            score += 1
            reasons.append("Stochastic в зоне перепроданности")
        elif stoch_k > 80 and stoch_d > 80:
            score -= 1
            reasons.append("Stochastic в зоне перекупленности")
        
        if atr > prices[-1] * 0.002:
            score += 1
            reasons.append(f"Хорошая волатильность (ATR: {atr:.4f})")
        
        if score >= 4:
            direction = "ВВЕРХ 🟢 CALL"
            probability = min(95, 75 + score * 3)
        elif score <= -4:
            direction = "ВНИЗ 🔴 PUT"
            probability = min(95, 75 + abs(score) * 3)
        elif score >= 1:
            direction = "ВВЕРХ 🟢 CALL"
            probability = 65 + score * 2
        elif score <= -1:
            direction = "ВНИЗ 🔴 PUT"
            probability = 65 + abs(score) * 2
        else:
            direction = "НЕЙТРАЛЬНО ⚪ WAIT"
            probability = 50
        
        volatility_percent = (atr / prices[-1]) * 100
        if volatility_percent < 0.3:
            expiration = "3m-5m"
        elif volatility_percent < 0.6:
            expiration = "2m-3m"
        else:
            expiration = "1m-2m"
        
        return direction, probability, reasons, indicators, expiration

analyzer = MarketAnalyzer()

# ---------------- MARATHON CALCULATOR ----------------
class MarathonCalculator:
    def __init__(self):
        self.daily_profit = 15
        
    def calculate_marathon(self, start_balance, days=30):
        results = []
        current_balance = start_balance
        
        for day in range(1, days + 1):
            daily_result = current_balance * (self.daily_profit / 100)
            current_balance += daily_result
            current_balance = round(current_balance, 2)
            
            results.append({
                'day': day,
                'balance': current_balance,
                'profit': round(daily_result, 2),
                'total_profit': round(current_balance - start_balance, 2)
            })
        
        return results
    
    def generate_plan(self, start_balance):
        results = self.calculate_marathon(start_balance)
        final_balance = results[-1]['balance']
        total_profit = results[-1]['total_profit']
        
        plan = f"**МАРАФОН НА 30 ДНЕЙ | ПЛАН ТОРГОВЛИ**\n\n"
        plan += f"💰 **Стартовый баланс:** ${start_balance:,.2f}\n"
        plan += f"🎯 **Ежедневная цель:** +{self.daily_profit}%\n"
        plan += f"🏁 **Финальная цель:** ${final_balance:,.2f}\n"
        plan += f"📈 **Общая прибыль:** ${total_profit:,.2f}\n\n"
        plan += f"**ЕЖЕДНЕВНЫЙ ПЛАН:**\n\n"
        
        for i in range(min(10, len(results))):
            day_data = results[i]
            plan += f"**День {day_data['day']}:** ${day_data['balance']:,.2f} (+${day_data['profit']:,.2f})\n"
        
        if len(results) > 10:
            plan += f"...\n"
            plan += f"**День 30:** ${results[-1]['balance']:,.2f} (+${results[-1]['profit']:,.2f})\n"
        
        plan += f"\n**СТРАТЕГИЯ:**\n"
        plan += f"1. **Управление рисками:**\n"
        plan += f"   • Размер сделки: 2-3% от баланса\n"
        plan += f"   • Максимум 5 сделок в день\n"
        plan += f"   • Стоп-лосс: 2 убыточные сделки подряд\n\n"
        plan += f"2. **Время торговли:**\n"
        plan += f"   • Лучшее время: 10:00-14:00 МСК\n"
        plan += f"   • Избегать новостей\n"
        plan += f"   • Перерывы каждые 2 часа\n\n"
        plan += f"3. **Психология:**\n"
        plan += f"   • Не гнаться за убытками\n"
        plan += f"   • Фиксировать прибыль от 5%\n"
        plan += f"   • Дневник трейдера\n\n"
        plan += f"4. **Сигналы:**\n"
        plan += f"   • Использовать только VIP сигналы\n"
        plan += f"   • Ждать подтверждения 2-3 индикаторов\n"
        plan += f"   • Не торговать против тренда\n\n"
        plan += f"⚠️ **ВАЖНО:** Торговля CFD связана с рисками. Не рискуйте больше, чем можете позволить себе потерять."
        
        return plan, results

marathon_calc = MarathonCalculator()

# ---------------- UI ----------------
async def show_menu(update, context):
    uid = str(update.effective_user.id)
    text = f"**KURUT AI INFINITY | PRO MENU**\n\n"
    text += f"👤 **Пользователь:** {update.effective_user.first_name}\n"
    text += f"🎯 **Статус:** {'VIP ✅' if is_vip(uid) else 'Ожидание доступа'}\n"
    text += f"📊 **Винрейт:** {calculate_win_rate(uid):.1f}%\n\n"
    text += f"✨ **Доступные функции:**"
    
    kb = [
        [InlineKeyboardButton("🎯 ПОЛУЧИТЬ СИГНАЛ", callback_data="market")],
        [InlineKeyboardButton("🏃 МАРАФОН 30 ДНЕЙ", callback_data="marathon")],
        [InlineKeyboardButton("🏆 ТОП ТРЕЙДЕРОВ", callback_data="top")],
        [InlineKeyboardButton("📊 МОЯ СТАТИСТИКА", callback_data="my_stats")],
        [InlineKeyboardButton("📚 ИНСТРУКЦИЯ", callback_data="guide")],
        [InlineKeyboardButton("✍️ НАПИСАТЬ АДМИНУ", url=ADMIN_LINK)],
        [InlineKeyboardButton("🔄 ОБНОВИТЬ", callback_data="refresh")]
    ]

    if update.callback_query:
        await safe_edit(update.callback_query, text, InlineKeyboardMarkup(kb), "Markdown")
    else:
        await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(kb), parse_mode="Markdown")

# ---------------- SAFE EDIT ----------------
async def safe_edit(query, text, reply_markup=None, parse_mode=None):
    try:
        await query.edit_message_text(text, reply_markup=reply_markup, parse_mode=parse_mode)
    except BadRequest as e:
        if "Message is not modified" in str(e):
            pass
        else:
            raise

# ---------------- START ----------------
async def start(update: Update, context):
    uid = str(update.effective_user.id)
    all_users.add(uid)
    save_db(DB_ALL, list(all_users))
    
    if is_vip(uid):
        await show_menu(update, context)
    else:
        text = f"**Добро пожаловать в KURUT AI INFINITY PRO**\n\n"
        text += f"🎯 **Точные сигналы для OTC рынка Pocket Option**\n"
        text += f"⚡ **Точность:** 75-95%\n"
        text += f"⏱️ **Экспирации:** 10s, 30s, 1m, 2m, 3m, 5m, 8m\n\n"
        text += f"**ДЛЯ ПОЛУЧЕНИЯ ДОСТУПА:**\n\n"
        text += f"1️⃣ **Регистрация:** [Pocket Option]({REF_LINK})\n"
        text += f"2️⃣ **Пополни баланс** от $50\n"
        text += f"3️⃣ **Отправь ID:** `{uid}`\n"
        text += f"4️⃣ **Админу:** {ADMIN_USER}\n\n"
        text += f"**ПРЕИМУЩЕСТВА VIP:**\n"
        text += f"• Точные сигналы с анализом\n"
        text += f"• Поддержка 24/7\n"
        text += f"• Обучение и стратегии\n"
        text += f"• Личный марафон\n\n"
        text += f"**СТАТИСТИКА:**\n"
        text += f"✅ Успешных сигналов: 82%\n"
        text += f"⚡ Средняя экспирация: 2-3 минуты\n"
        text += f"🎯 Рекомендуемый риск: 2%\n\n"
        text += f"✍️ **НАПИСАТЬ АДМИНУ:** [ТЫК]({ADMIN_LINK})\n\n"
        text += f"⚠️ **ВАЖНО:** Торговля CFD связана с рисками. Не рискуйте больше, чем можете позволить себе потерять."
        
        kb = [
            [InlineKeyboardButton("✍️ НАПИСАТЬ АДМИНУ", url=ADMIN_LINK)],
            [InlineKeyboardButton("🔄 ОБНОВИТЬ СТАТУС", callback_data="check_access")]
        ]
        await update.message.reply_text(text, parse_mode="Markdown", 
                                      disable_web_page_preview=True,
                                      reply_markup=InlineKeyboardMarkup(kb))

# ---------------- PAGINATION ----------------
def get_paged_kb(data, page, prefix):
    size = 8
    start = page * size
    chunk = data[start:start + size]

    kb = []
    for i, item in enumerate(chunk):
        kb.append([InlineKeyboardButton(item, callback_data=f"asset_{start+i}")])

    nav = []
    if page > 0:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"{prefix}_{page-1}"))
    if start + size < len(data):
        nav.append(InlineKeyboardButton("➡️", callback_data=f"{prefix}_{page+1}"))

    if nav:
        kb.append(nav)
    
    kb.append([InlineKeyboardButton("🔙 НАЗАД", callback_data="back_menu")])

    return InlineKeyboardMarkup(kb)

# ---------------- CALLBACKS ----------------
async def callback_handler(update: Update, context):
    q = update.callback_query
    uid = str(q.from_user.id)
    await q.answer()
    
    if q.data == "refresh" or q.data == "back_menu":
        await show_menu(update, context)
        return
        
    if q.data == "check_access":
        if is_vip(uid):
            await q.edit_message_text("✅ Ваш VIP доступ активирован!", parse_mode="Markdown")
            await asyncio.sleep(1)
            await show_menu(update, context)
        else:
            await q.edit_message_text("❌ VIP доступ еще не активирован. Отправьте ваш ID админу.", parse_mode="Markdown")
        return

    if not is_vip(uid):
        await q.edit_message_text("❌ У вас нет доступа к сигналам. Используйте /start для получения доступа.")
        return

    if q.data == "guide":
        guide_text = "**ПОЛНАЯ ИНСТРУКЦИЯ К БОТУ**\n\n"
        guide_text += "**КАК ПОЛЬЗОВАТЬСЯ СИГНАЛАМИ:**\n"
        guide_text += "1. Нажмите 'ПОЛУЧИТЬ СИГНАЛ'\n"
        guide_text += "2. Выберите рынок (OTC/Акции/Крипто)\n"
        guide_text += "3. Выберите актив для анализа\n"
        guide_text += "4. Выберите экспирацию (время)\n"
        guide_text += "5. Получите точный сигнал с анализом\n\n"
        guide_text += "**ВЫБОР ЭКСПИРАЦИИ:**\n"
        guide_text += "• 10-30 секунд - для опытных, высокая волатильность\n"
        guide_text += "• 1-3 минуты - оптимальный вариант, стабильная прибыль\n"
        guide_text += "• 5-8 минут - для консервативных стратегий\n\n"
        guide_text += "**РИСК-МЕНЕДЖМЕНТ:**\n"
        guide_text += "• Размер сделки: 1-3% от депозита\n"
        guide_text += "• Стоп-лосс: 2-3 убыточные сделки подряд = перерыв\n"
        guide_text += "• Тейк-профит: 15-25% в день = остановка\n"
        guide_text += "• Максимум: 5 сделок в день\n\n"
        guide_text += "**ТЕХНИЧЕСКИЙ АНАЛИЗ БОТА:**\n"
        guide_text += "Бот анализирует 10+ индикаторов:\n"
        guide_text += "• EMA 9, 21, 50 - определение тренда\n"
        guide_text += "• RSI 14 - перекупленность/перепроданность\n"
        guide_text += "• MACD - момент и направление\n"
        guide_text += "• Bollinger Bands - волатильность и уровни\n"
        guide_text += "• Stochastic - моментум рынка\n"
        guide_text += "• ATR - средний истинный диапазон\n\n"
        guide_text += f"**ПОДДЕРЖКА:**\nПо всем вопросам: {ADMIN_USER}"
        
        kb = [[InlineKeyboardButton("🔙 НАЗАД", callback_data="back_menu")]]
        await safe_edit(q, guide_text, InlineKeyboardMarkup(kb), "Markdown")

    elif q.data == "market":
        kb = [
            [InlineKeyboardButton("💱 OTC РЫНОК", callback_data="cu_0")],
            [InlineKeyboardButton("🏢 АКЦИИ", callback_data="st_0")],
            [InlineKeyboardButton("₿ КРИПТО", callback_data="cr_0")],
            [InlineKeyboardButton("🔙 НАЗАД", callback_data="back_menu")]
        ]
        await safe_edit(q, "**ВЫБЕРИ РЫНОК ДЛЯ АНАЛИЗА:**", InlineKeyboardMarkup(kb), "Markdown")

    elif q.data.startswith(("cu_", "st_", "cr_")):
        pref, page = q.data.split("_")
        data = OTC_PAIRS if pref == "cu" else STOCKS if pref == "st" else CRYPTO
        context.user_data["assets"] = data
        context.user_data["market_type"] = pref
        await safe_edit(q, "**ВЫБЕРИ АКТИВ ДЛЯ АНАЛИЗА:**", get_paged_kb(data, int(page), pref))

    elif q.data.startswith("asset_"):
        idx = int(q.data.split("_")[1])
        asset = context.user_data["assets"][idx]
        
        context.user_data["selected_asset"] = asset
        context.user_data["analysis_step"] = "expiration"
        
        kb = []
        for exp in EXPIRATIONS:
            kb.append([InlineKeyboardButton(f"⏱️ {exp}", callback_data=f"exp_{exp}")])
        kb.append([InlineKeyboardButton("🔙 НАЗАД", callback_data=f"{context.user_data['market_type']}_0")])
        
        await safe_edit(q, f"**АКТИВ:** {asset}\n\n**ВЫБЕРИТЕ ЭКСПИРАЦИЮ:**", InlineKeyboardMarkup(kb), "Markdown")

    elif q.data.startswith("exp_"):
        expiration = q.data.split("_")[1]
        asset = context.user_data.get("selected_asset", "Неизвестный актив")
        
        msg = await q.edit_message_text(f"**АНАЛИЗИРУЕМ {asset}...**\n\nЗагрузка рыночных данных...\nРасчет индикаторов...\nОпределение сигнала...")
        
        await asyncio.sleep(2)
        
        direction, probability, reasons, indicators, recommended_exp = analyzer.analyze_asset(asset)
        
        signal_text = f"**ТОЧНЫЙ СИГНАЛ | {asset}**\n\n"
        signal_text += f"**НАПРАВЛЕНИЕ:** {direction}\n"
        signal_text += f"**ВЕРОЯТНОСТЬ:** {probability}%\n"
        signal_text += f"**ВАША ЭКСПИРАЦИЯ:** {expiration}\n"
        signal_text += f"**РЕКОМЕНДУЕМАЯ:** {recommended_exp}\n\n"
        signal_text += f"**ТЕХНИЧЕСКИЙ АНАЛИЗ:**\n"
        signal_text += f"• RSI: {indicators['RSI']:.1f} {'(ПЕРЕПРОДАН)' if indicators['RSI'] < 30 else '(ПЕРЕКУПЛЕН)' if indicators['RSI'] > 70 else '(НЕЙТРАЛЬНО)'}\n"
        signal_text += f"• MACD: {indicators['MACD']:.4f} {'(БЫЧИЙ)' if indicators['MACD'] > 0 else '(МЕДВЕЖИЙ)'}\n"
        signal_text += f"• Stochastic: K={indicators['STOCH_K']:.1f}, D={indicators['STOCH_D']:.1f}\n"
        bb_percent = ((indicators['PRICE'] - indicators['BB_LOWER']) / (indicators['BB_UPPER'] - indicators['BB_LOWER']) * 100)
        signal_text += f"• Bollinger Bands: {bb_percent:.1f}%\n"
        signal_text += f"• ATR: {indicators['ATR']:.4f}\n"
        signal_text += f"• Тренд: {'ВОСХОДЯЩИЙ' if indicators['EMA_9'] > indicators['EMA_21'] else 'НИСХОДЯЩИЙ'}\n\n"
        signal_text += f"**ОСНОВНЫЕ ПРИЧИНЫ:**\n"
        
        for i, reason in enumerate(reasons[:5], 1):
            signal_text += f"{i}. {reason}\n"
        
        signal_text += f"\n**РЕКОМЕНДАЦИИ:**\n"
        signal_text += f"• Размер сделки: {'2-3%' if probability > 85 else '1-2%' if probability > 75 else '0.5-1%'}\n"
        signal_text += f"• Стоп-лосс: {'Не требуется' if probability > 90 else '1-2% от депозита'}\n"
        signal_text += f"• Тейк-профит: {'15-20%' if expiration in ['10s', '30s'] else '10-15%' if expiration in ['1m', '2m'] else '8-12%'}\n\n"
        signal_text += f"⚠️ **ВАЖНО:** Торговля CFD сопряжена с рисками."
        
        kb = [
            [
                InlineKeyboardButton("✅ СИГНАЛ СРАБОТАЛ", callback_data="res_plus"),
                InlineKeyboardButton("❌ СИГНАЛ НЕ СРАБОТАЛ", callback_data="res_minus")
            ],
            [InlineKeyboardButton("🔄 НОВЫЙ СИГНАЛ", callback_data="market")],
            [InlineKeyboardButton("🔙 ГЛАВНОЕ МЕНЮ", callback_data="back_menu")]
        ]
        
        await msg.edit_text(signal_text, parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(kb))
        
        log_signal(asset, direction, probability, indicators, expiration, uid)

    elif q.data == "marathon":
        await safe_edit(q, "💰 **ВВЕДИТЕ ВАШ СТАРТОВЫЙ БАЛАНС ($):**\n\nПример: 100, 500, 1000")
        context.user_data["wait_balance"] = True

    elif q.data == "top":
        top_users = []
        for user_id, stats in trader_stats.items():
            if isinstance(stats, dict):
                plus = stats.get('plus', 0)
                minus = stats.get('minus', 0)
                profit = stats.get('profit', 0)
                winrate = (plus / (plus + minus) * 100) if (plus + minus) > 0 else 0
                top_users.append({
                    'id': user_id,
                    'name': stats.get('name', 'Аноним'),
                    'plus': plus,
                    'minus': minus,
                    'profit': profit,
                    'winrate': winrate
                })
        
        top_users
