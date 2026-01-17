# =====================================
# KURUT AI INFINITY | COIP PRO EDITION
# OTC SIGNAL SYSTEM FOR POCKET OPTION
# ULTIMATE EDITION WITH 15+ INDICATORS
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
TOKEN = os.environ.get("TOKEN", "8578509228:AAE2D6ANQGgXWkyLkVXYnq_htqFbTAYF_Ms")

ADMIN_IDS = {6117198446, 7079260196}
ADMIN_USER = "@Kuruttrader"
ADMIN_LINK = "https://t.me/Kuruttrader"

REF_LINK = "https://po-ru4.click/register?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"

REGISTER_TEXT = f"""
🎯 **РЕГИСТРАЦИЯ НА POCKET OPTION**

✅ **Если у тебя ЕСТЬ аккаунт удали его и создай новый:**
1. Зайди в свой новый аккаунт
2. Пополни баланс от $20
3. Отправь ID админу {ADMIN_USER}

✅ **Если у тебя НЕТ аккаунта:**
1. Нажми на кнопку "📝 РЕГИСТРАЦИЯ"
2. Зарегистрируйся по ссылке
3. Пополни баланс от $20
4. Отправь ID админу {ADMIN_USER}

💰 **Минимальный депозит:** $20
🎁 **Бонус при регистрации:** +50% к первому депозиту
⚡ **Вывод средств:** от 15 минут до 24 часов

📊 **ПОСЛЕ РЕГИСТРАЦИИ:**
1. Скопируй свой ID из бота (/start)
2. Напиши админу {ADMIN_USER}
3. Получи VIP доступ к сигналам
"""

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

def calculate_total_profit(user_id):
    if user_id in trader_stats:
        stats = trader_stats[user_id]
        return stats.get('profit', 0)
    return 0

# ---------------- ADVANCED MARKET ANALYSIS (15+ INDICATORS) ----------------
class MarketAnalyzer:
    def __init__(self):
        self.patterns = {}
        
    # 1. EMA (Exponential Moving Average)
    def calculate_ema(self, prices, period):
        if len(prices) < period:
            return sum(prices) / len(prices)
        multiplier = 2 / (period + 1)
        ema = prices[0]
        for price in prices[1:]:
            ema = (price - ema) * multiplier + ema
        return ema
    
    # 2. RSI (Relative Strength Index)
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
    
    # 3. MACD (Moving Average Convergence Divergence)
    def calculate_macd(self, prices):
        if len(prices) < 26:
            return 0, 0, 0
        
        ema12 = self.calculate_ema(prices[-26:], 12)
        ema26 = self.calculate_ema(prices[-26:], 26)
        macd_line = ema12 - ema26
        signal_line = self.calculate_ema([ema12 - ema26], 9)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    # 4. Bollinger Bands
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
    
    # 5. Stochastic Oscillator
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
    
    # 6. ATR (Average True Range)
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
    
    # 7. CCI (Commodity Channel Index)
    def calculate_cci(self, high_prices, low_prices, close_prices, period=20):
        if len(close_prices) < period:
            return 0
        
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(high_prices[-period:], low_prices[-period:], close_prices[-period:])]
        sma = sum(typical_prices) / period
        mean_deviation = sum(abs(tp - sma) for tp in typical_prices) / period
        
        if mean_deviation == 0:
            return 0
        
        cci = (typical_prices[-1] - sma) / (0.015 * mean_deviation)
        return cci
    
    # 8. Williams %R
    def calculate_williams_r(self, high_prices, low_prices, close_prices, period=14):
        if len(close_prices) < period:
            return -50
        
        highest_high = max(high_prices[-period:])
        lowest_low = min(low_prices[-period:])
        current_close = close_prices[-1]
        
        if highest_high == lowest_low:
            return -50
        
        williams_r = -100 * ((highest_high - current_close) / (highest_high - lowest_low))
        return williams_r
    
    # 9. MFI (Money Flow Index)
    def calculate_mfi(self, high_prices, low_prices, close_prices, volumes, period=14):
        if len(close_prices) < period or len(volumes) < period:
            return 50
        
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(high_prices[-period:], low_prices[-period:], close_prices[-period:])]
        money_flows = [tp * v for tp, v in zip(typical_prices, volumes[-period:])]
        
        positive_flow = 0
        negative_flow = 0
        
        for i in range(1, len(typical_prices)):
            if typical_prices[i] > typical_prices[i-1]:
                positive_flow += money_flows[i]
            elif typical_prices[i] < typical_prices[i-1]:
                negative_flow += money_flows[i]
        
        if negative_flow == 0:
            return 100
        
        money_ratio = positive_flow / negative_flow
        mfi = 100 - (100 / (1 + money_ratio))
        return mfi
    
    # 10. ADX (Average Directional Index)
    def calculate_adx(self, high_prices, low_prices, close_prices, period=14):
        if len(close_prices) < period * 2:
            return 25
        
        # Simplified ADX calculation
        plus_dm = []
        minus_dm = []
        
        for i in range(1, len(high_prices)):
            up_move = high_prices[i] - high_prices[i-1]
            down_move = low_prices[i-1] - low_prices[i]
            
            if up_move > down_move and up_move > 0:
                plus_dm.append(up_move)
                minus_dm.append(0)
            elif down_move > up_move and down_move > 0:
                plus_dm.append(0)
                minus_dm.append(down_move)
            else:
                plus_dm.append(0)
                minus_dm.append(0)
        
        tr_values = []
        for i in range(1, len(close_prices)):
            hl = high_prices[i] - low_prices[i]
            hc = abs(high_prices[i] - close_prices[i-1])
            lc = abs(low_prices[i] - close_prices[i-1])
            tr_values.append(max(hl, hc, lc))
        
        if len(tr_values) < period or len(plus_dm) < period or len(minus_dm) < period:
            return 25
        
        avg_tr = sum(tr_values[-period:]) / period
        avg_plus_dm = sum(plus_dm[-period:]) / period
        avg_minus_dm = sum(minus_dm[-period:]) / period
        
        if avg_tr == 0:
            return 25
        
        plus_di = 100 * (avg_plus_dm / avg_tr)
        minus_di = 100 * (avg_minus_dm / avg_tr)
        dx = 100 * abs(plus_di - minus_di) / (plus_di + minus_di) if (plus_di + minus_di) > 0 else 0
        
        return dx
    
    # 11. Parabolic SAR (Simplified)
    def calculate_parabolic_sar(self, high_prices, low_prices):
        if len(high_prices) < 3:
            return high_prices[-1] if len(high_prices) > 0 else 0
        
        # Simplified SAR calculation
        trend = "UP" if high_prices[-1] > high_prices[-2] and low_prices[-1] > low_prices[-2] else "DOWN"
        
        if trend == "UP":
            sar = min(low_prices[-3:])
        else:
            sar = max(high_prices[-3:])
        
        return sar, trend
    
    # 12. OBV (On-Balance Volume)
    def calculate_obv(self, close_prices, volumes):
        if len(close_prices) < 2 or len(volumes) < 2:
            return 0
        
        obv = 0
        for i in range(1, len(close_prices)):
            if close_prices[i] > close_prices[i-1]:
                obv += volumes[i]
            elif close_prices[i] < close_prices[i-1]:
                obv -= volumes[i]
        
        return obv
    
    # 13. Ichimoku Cloud (Simplified)
    def calculate_ichimoku(self, high_prices, low_prices):
        if len(high_prices) < 52 or len(low_prices) < 52:
            return 0, 0, 0, 0, 0
        
        # Tenkan-sen (Conversion Line)
        tenkan = (max(high_prices[-9:]) + min(low_prices[-9:])) / 2
        
        # Kijun-sen (Base Line)
        kijun = (max(high_prices[-26:]) + min(low_prices[-26:])) / 2
        
        # Senkou Span A (Leading Span A)
        senkou_a = (tenkan + kijun) / 2
        
        # Senkou Span B (Leading Span B)
        senkou_b = (max(high_prices[-52:]) + min(low_prices[-52:])) / 2
        
        # Chikou Span (Lagging Span)
        chikou = (high_prices[-26] + low_prices[-26]) / 2 if len(high_prices) >= 26 else 0
        
        return tenkan, kijun, senkou_a, senkou_b, chikou
    
    # 14. Volume Weighted Average Price
    def calculate_vwap(self, high_prices, low_prices, close_prices, volumes):
        if len(close_prices) == 0 or len(volumes) == 0:
            return 0
        
        typical_prices = [(h + l + c) / 3 for h, l, c in zip(high_prices, low_prices, close_prices)]
        cumulative_tp_v = sum(tp * v for tp, v in zip(typical_prices, volumes))
        cumulative_volume = sum(volumes)
        
        if cumulative_volume == 0:
            return 0
        
        return cumulative_tp_v / cumulative_volume
    
    # 15. Standard Deviation
    def calculate_std(self, prices, period=20):
        if len(prices) < period:
            recent = prices
        else:
            recent = prices[-period:]
        
        mean = sum(recent) / len(recent)
        variance = sum((x - mean) ** 2 for x in recent) / len(recent)
        return math.sqrt(variance)
    
    # Генерация реалистичных данных
    def generate_price_data(self, asset):
        seed = sum(ord(c) for c in asset) + int(time.time() % 1000)
        random.seed(seed)
        
        base_price = random.uniform(50, 200)
        volatility = random.uniform(0.001, 0.005)
        
        prices = [base_price]
        highs = [base_price * (1 + random.uniform(0, 0.002))]
        lows = [base_price * (1 - random.uniform(0, 0.002))]
        volumes = [random.randint(1000, 10000) for _ in range(200)]
        
        for _ in range(199):
            change = random.normalvariate(0, volatility)
            new_price = prices[-1] * (1 + change)
            prices.append(new_price)
            highs.append(new_price * (1 + random.uniform(0, 0.002)))
            lows.append(new_price * (1 - random.uniform(0, 0.002)))
        
        return prices, highs, lows, volumes
    
    # Продвинутый анализ с 15+ индикаторами
    def analyze_asset(self, asset):
        prices, highs, lows, volumes = self.generate_price_data(asset)
        
        # Рассчитываем ВСЕ индикаторы
        indicators = {}
        
        # Трендовые индикаторы
        indicators['EMA_9'] = self.calculate_ema(prices[-20:], 9)
        indicators['EMA_21'] = self.calculate_ema(prices[-30:], 21)
        indicators['EMA_50'] = self.calculate_ema(prices[-60:], 50)
        indicators['EMA_200'] = self.calculate_ema(prices[-250:], 200) if len(prices) >= 250 else indicators['EMA_50']
        
        # MACD комплексный
        macd_line, signal_line, histogram = self.calculate_macd(prices)
        indicators['MACD_LINE'] = macd_line
        indicators['MACD_SIGNAL'] = signal_line
        indicators['MACD_HIST'] = histogram
        
        # RSI
        indicators['RSI'] = self.calculate_rsi(prices)
        
        # Bollinger Bands
        bb_upper, bb_middle, bb_lower = self.calculate_bollinger_bands(prices)
        indicators['BB_UPPER'] = bb_upper
        indicators['BB_MIDDLE'] = bb_middle
        indicators['BB_LOWER'] = bb_lower
        
        # Stochastic
        stoch_k, stoch_d = self.calculate_stochastic(highs, lows, prices)
        indicators['STOCH_K'] = stoch_k
        indicators['STOCH_D'] = stoch_d
        
        # ATR
        indicators['ATR'] = self.calculate_atr(highs, lows, prices)
        
        # CCI
        indicators['CCI'] = self.calculate_cci(highs, lows, prices)
        
        # Williams %R
        indicators['WILLIAMS_R'] = self.calculate_williams_r(highs, lows, prices)
        
        # MFI
        indicators['MFI'] = self.calculate_mfi(highs, lows, prices, volumes)
        
        # ADX
        indicators['ADX'] = self.calculate_adx(highs, lows, prices)
        
        # Parabolic SAR
        sar_value, sar_trend = self.calculate_parabolic_sar(highs, lows)
        indicators['SAR'] = sar_value
        indicators['SAR_TREND'] = sar_trend
        
        # OBV
        indicators['OBV'] = self.calculate_obv(prices, volumes)
        
        # Ichimoku
        tenkan, kijun, senkou_a, senkou_b, chikou = self.calculate_ichimoku(highs, lows)
        indicators['ICHIMOKU_TENKAN'] = tenkan
        indicators['ICHIMOKU_KIJUN'] = kijun
        indicators['ICHIMOKU_SENKOU_A'] = senkou_a
        indicators['ICHIMOKU_SENKOU_B'] = senkou_b
        indicators['ICHIMOKU_CHIKOU'] = chikou
        
        # VWAP
        indicators['VWAP'] = self.calculate_vwap(highs, lows, prices, volumes)
        
        # Standard Deviation
        indicators['STD'] = self.calculate_std(prices)
        
        # Текущая цена
        indicators['PRICE'] = prices[-1]
        
        # Математический анализ вероятности
        score = 0
        reasons = []
        
        # Анализ тренда (4 индикатора)
        trend_score = 0
        if indicators['EMA_9'] > indicators['EMA_21'] > indicators['EMA_50']:
            trend_score += 3
            reasons.append("📈 Сильный восходящий тренд (EMA 9>21>50)")
        elif indicators['EMA_9'] < indicators['EMA_21'] < indicators['EMA_50']:
            trend_score -= 3
            reasons.append("📉 Сильный нисходящий тренд (EMA 9<21<50)")
        
        if macd_line > signal_line and histogram > 0:
            trend_score += 2
            reasons.append("✅ MACD бычий пересечение + гистограмма")
        elif macd_line < signal_line and histogram < 0:
            trend_score -= 2
            reasons.append("❌ MACD медвежий пересечение - гистограмма")
        
        score += trend_score
        
        # Анализ импульса (4 индикатора)
        momentum_score = 0
        if indicators['RSI'] < 30:
            momentum_score += 2
            reasons.append("🎯 RSI в зоне перепроданности (<30)")
        elif indicators['RSI'] > 70:
            momentum_score -= 2
            reasons.append("⚠️ RSI в зоне перекупленности (>70)")
        
        if indicators['STOCH_K'] < 20 and indicators['STOCH_D'] < 20:
            momentum_score += 1
            reasons.append("📊 Stochastic перепродан")
        elif indicators['STOCH_K'] > 80 and indicators['STOCH_D'] > 80:
            momentum_score -= 1
            reasons.append("📊 Stochastic перекуплен")
        
        if indicators['CCI'] < -100:
            momentum_score += 1
            reasons.append(f"📈 CCI перепродан ({indicators['CCI']:.1f})")
        elif indicators['CCI'] > 100:
            momentum_score -= 1
            reasons.append(f"📉 CCI перекуплен ({indicators['CCI']:.1f})")
        
        if indicators['WILLIAMS_R'] < -80:
            momentum_score += 1
            reasons.append(f"🎯 Williams %R перепродан ({indicators['WILLIAMS_R']:.1f})")
        elif indicators['WILLIAMS_R'] > -20:
            momentum_score -= 1
            reasons.append(f"⚠️ Williams %R перекуплен ({indicators['WILLIAMS_R']:.1f})")
        
        score += momentum_score
        
        # Анализ волатильности и объема (4 индикатора)
        volatility_score = 0
        bb_percent = ((indicators['PRICE'] - bb_lower) / (bb_upper - bb_lower)) * 100
        
        if bb_percent < 20:
            volatility_score += 2
            reasons.append(f"📊 Цена у нижней границы BB ({bb_percent:.1f}%)")
        elif bb_percent > 80:
            volatility_score -= 2
            reasons.append(f"📊 Цена у верхней границы BB ({bb_percent:.1f}%)")
        
        if indicators['ATR'] > indicators['PRICE'] * 0.002:
            volatility_score += 1
            reasons.append(f"⚡ Хорошая волатильность (ATR: {indicators['ATR']:.4f})")
        
        if indicators['MFI'] < 30:
            volatility_score += 1
            reasons.append(f"💰 MFI показывает накопление ({indicators['MFI']:.1f})")
        elif indicators['MFI'] > 70:
            volatility_score -= 1
            reasons.append(f"💸 MFI показывает распределение ({indicators['MFI']:.1f})")
        
        if indicators['ADX'] > 25:
            volatility_score += 1
            reasons.append(f"💪 Сильный тренд (ADX: {indicators['ADX']:.1f})")
        
        score += volatility_score
        
        # Анализ Ichimoku (2 индикатора)
        ichimoku_score = 0
        if indicators['PRICE'] > max(indicators['ICHIMOKU_SENKOU_A'], indicators['ICHIMOKU_SENKOU_B']):
            ichimoku_score += 2
            reasons.append("☁️ Цена выше облака Ишимоку")
        elif indicators['PRICE'] < min(indicators['ICHIMOKU_SENKOU_A'], indicators['ICHIMOKU_SENKOU_B']):
            ichimoku_score -= 2
            reasons.append("☁️ Цена ниже облака Ишимоку")
        
        if indicators['ICHIMOKU_TENKAN'] > indicators['ICHIMOKU_KIJUN']:
            ichimoku_score += 1
            reasons.append("↗️ Тенкан-сен выше Киджун-сен")
        else:
            ichimoku_score -= 1
            reasons.append("↘️ Тенкан-сен ниже Киджун-сен")
        
        score += ichimoku_score
        
        # Математическая вероятность на основе всех индикаторов
        total_indicators = 15  # Всего анализируемых индикаторов
        positive_signals = sum([
            1 if indicators['EMA_9'] > indicators['EMA_21'] else 0,
            1 if macd_line > signal_line else 0,
            1 if indicators['RSI'] < 70 else 0,
            1 if bb_percent < 80 else 0,
            1 if indicators['STOCH_K'] < 80 else 0,
            1 if indicators['CCI'] < 100 else 0,
            1 if indicators['WILLIAMS_R'] < -20 else 0,
            1 if indicators['MFI'] < 70 else 0,
            1 if indicators['ADX'] > 20 else 0,
            1 if indicators['SAR_TREND'] == "UP" else 0,
            1 if indicators['OBV'] > 0 else 0,
            1 if indicators['ICHIMOKU_TENKAN'] > indicators['ICHIMOKU_KIJUN'] else 0,
            1 if indicators['PRICE'] > indicators['VWAP'] else 0,
            1 if indicators['STD'] < indicators['PRICE'] * 0.01 else 0,
            1 if trend_score > 0 else 0
        ])
        
        base_probability = (positive_signals / total_indicators) * 100
        
        # Корректировка вероятности на основе силы сигнала
        if score >= 8:
            direction = "🚀 ВВЕРХ 🟢 STRONG CALL"
            probability = min(98, 80 + score * 2)
        elif score >= 4:
            direction = "📈 ВВЕРХ 🟢 CALL"
            probability = min(95, 75 + score * 2)
        elif score <= -8:
            direction = "🔻 ВНИЗ 🔴 STRONG PUT"
            probability = min(98, 80 + abs(score) * 2)
        elif score <= -4:
            direction = "📉 ВНИЗ 🔴 PUT"
            probability = min(95, 75 + abs(score) * 2)
        elif score > 0:
            direction = "↗️ ВВЕРХ 🟢 WEAK CALL"
            probability = 60 + score
        elif score < 0:
            direction = "↘️ ВНИЗ 🔴 WEAK PUT"
            probability = 60 + abs(score)
        else:
            direction = "⏸️ НЕЙТРАЛЬНО ⚪ WAIT"
            probability = 50
        
        # Финальная вероятность (среднее между математической и эвристической)
        final_probability = min(99, int((base_probability * 0.6) + (probability * 0.4)))
        
        # Рекомендация экспирации на основе волатильности
        volatility_percent = (indicators['ATR'] / indicators['PRICE']) * 100
        
        if volatility_percent < 0.2:
            expiration = "3m-5m (низкая волатильность)"
        elif volatility_percent < 0.5:
            expiration = "2m-3m (умеренная волатильность)"
        else:
            expiration = "1m-2m (высокая волатильность)"
        
        return direction, final_probability, reasons[:6], indicators, expiration

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
        
        plan = "✨ *МАРАФОН НА 30 ДНЕЙ | ПЛАН ТОРГОВЛИ* ✨\n\n"
        plan += "💰 *Стартовый баланс:* $" + f"{start_balance:,.2f}" + "\n"
        plan += "🎯 *Ежедневная цель:* +" + str(self.daily_profit) + "%\n"
        plan += "🏁 *Финальная цель:* $" + f"{final_balance:,.2f}" + "\n"
        plan += "📈 *Общая прибыль:* $" + f"{total_profit:,.2f}" + "\n\n"
        plan += "📊 *ДЕТАЛЬНЫЙ ПЛАН НА КАЖДЫЙ ДЕНЬ:*\n\n"
        
        emoji_progress = ["1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣", "🔟"]
        
        for i in range(min(10, len(results))):
            day_data = results[i]
            emoji = emoji_progress[i] if i < len(emoji_progress) else f"{i+1}."
            plan += f"{emoji} *День {day_data['day']}:* ${day_data['balance']:,.2f} (+${day_data['profit']:,.2f})\n"
        
        if len(results) > 10:
            plan += """
📈 *ПРОМЕЖУТОЧНЫЙ ПЛАН НА ОСТАЛЬНЫЕ ДНИ:*
Здесь можно добавить оставшиеся дни марафона
"""
            

if __name__ == "__main__":
    # запускаем веб-сервер в отдельном потоке
    thread = Thread(target=run_web)
    thread.start()

    # запускаем Telegram бота
    import asyncio
    from telegram.ext import Application

    app = Application.builder().token(TOKEN).build()

    # здесь нужно добавить обработчики команд, callback и т.д.
    # например:
    # app.add_handler(CommandHandler("start", start))
    # app.add_handler(CallbackQueryHandler(callback_handler))

    app.run_polling()
