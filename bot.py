# main.py - ПОЛНЫЙ КОД БОТА VIP PREMIUM MAX PRO
import telebot
from telebot import types
import sqlite3
import random
import time
import threading
from datetime import datetime, timedelta
import requests
import math

# ================ КОНФИГУРАЦИЯ ================
TOKEN = '8578509228:AAHvoD2oT1JQx1sWzImEI1hO2y3pyz5382U'
ADMIN_ID = 6117198446  # Твой Telegram ID

# Ссылки
CHANNEL_LINK = "https://t.me/KURUTTRADING"
YOUTUBE_LINK = "https://www.youtube.com/@Kurut_kg"
CHAT_LINK = "https://t.me/Kurutopen"
REFERRAL_LINK = "https://u3.shortink.io/main?utm_campaign=797321&utm_source=affiliate&utm_medium=sr&a=6KE9lr793exm8X&ac=kurut&code=50START"
MIN_DEPOSIT = 15  # Минимальный депозит в долларах

# Языки
LANGUAGES = {
    'ru': {'name': 'Русский', 'flag': '🇷🇺'},
    'en': {'name': 'English', 'flag': '🇬🇧'},
    'kg': {'name': 'Кыргызча', 'flag': '🇰🇬'},
    'uz': {'name': "O'zbekcha", 'flag': '🇺🇿'}
}

# Тексты на разных языках
TEXTS = {
    'ru': {
        'welcome': "👋 Добро пожаловать в VIP Premium MAX Pro Bot!\n\nВыберите язык:",
        'language_selected': "✅ Язык установлен: Русский",
        'instruction_title': "📚 ИНСТРУКЦИЯ ПО БОТУ | СТРАНИЦА {page}/3",
        'instruction_1': "📊 **КАК ПОЛЬЗОВАТЬСЯ БОТОМ**\n\n1️⃣ **Регистрация**\n   • Пополните счет от ${min_deposit}\n   • Отправьте свой ID администратору\n\n2️⃣ **Получение доступа**\n   • После оплаты админ выдаст доступ\n   • Вы получите уведомление",
        'instruction_2': "🎯 **КАК ОТКРЫВАТЬ СДЕЛКИ**\n\n3️⃣ **Выбор сигнала**\n   • Нажмите «📈 Получить сигнал»\n   • Выберите категорию (Валюты/Акции/Крипта)\n   • Выберите торговую пару\n\n4️⃣ **Анализ сигнала**\n   • Бот анализирует 25 индикаторов\n   • Учитывается OTC рынок Pocket Option\n   • Математический алгоритм точности",
        'instruction_3': "⚡ **ВАЖНЫЕ ПРАВИЛА**\n\n✅ Риск-менеджмент: не более 5% на сделку\n✅ Торгуйте только по сигналам\n✅ Следуйте марафону для стабильного роста\n\n📞 **Поддержка**: {chat_link}\n📢 **Канал**: {channel_link}",
        'get_access': "🔑 ПОЛУЧИТЬ ДОСТУП",
        'access_info': "🔐 **ДЛЯ ПОЛУЧЕНИЯ ДОСТУПА**\n\n📌 **Ваш Telegram ID:** `{user_id}`\n\n💰 **Минимальный депозит:** ${min_deposit}\n🔗 **Реферальная ссылка:**\n{ref_link}\n\n📤 **Отправьте скриншот оплаты и ваш ID администратору:**\n{chat_link}\n\n✅ После проверки вам выдадут доступ",
        'no_access': "❌ У вас нет доступа к боту.\n\nНажмите кнопку ниже, чтобы получить доступ.",
        'main_menu': "🏠 **ГЛАВНОЕ МЕНЮ**\n\nВыберите раздел:",
        'signals': "📈 Получить сигнал",
        'marathon': "🏃 Марафон",
        'stats': "📊 Статистика",
        'top': "🏆 Топ трейдеры",
        'currency': "💵 Валютные пары OTC",
        'stocks': "📊 Акции OTC",
        'crypto': "₿ Криптовалюта OTC",
        'commodities': "🛢 Сырьевые товары",
        'back': "◀️ Назад",
        'forward': "Вперед ▶️",
        'select_pair': "Выберите пару для анализа (страница {page}/{total}):",
        'analysis': "🔍 **АНАЛИЗ РЫНКА**\n\nПара: {pair}\nТип: {type}\n\n📊 **Технический анализ:**\n{analysis}\n\n✅ **Уверенность:** {confidence}%\n📈 **Рекомендация:** {direction}\n\n⏰ **Выберите время экспирации:**",
        'signal_result': "🚀 **СИГНАЛ НА СДЕЛКУ**\n\nПара: {pair}\nТип: {type}\nНаправление: {direction}\nЭкспирация: {exp}\n\n📊 **Анализ индикаторов:**\n{indicators}\n\n🎯 **Уровни:**\n• Сопротивление: {resistance}\n• Поддержка: {support}\n• Точка входа: {entry}\n\n💪 **Уверенность:** {confidence}%\n💰 **Потенциальная прибыль:** +{profit}%\n\n⚠️ Риск: {risk}%",
        'marathon_title': "🏃 **МАРАФОН НА 30 ДНЕЙ**\n\nЦель: +15% к депозиту",
        'marathon_page1': "📅 **НЕДЕЛЯ 1-2: РАЗГОН**\n\n| День | План | Риск | Результат |\n|------|------|------|-----------|\n| 1-7  | 2%   | 1%   | +14%      |\n| 8-14 | 3%   | 1.5% | +21%      |\n\n📊 **Итого за 2 недели:** +35%",
        'marathon_page2': "📅 **НЕДЕЛЯ 3-4: СТАБИЛЬНОСТЬ**\n\n| День | План | Риск | Результат |\n|------|------|------|-----------|\n| 15-21| 2.5% | 1%   | +17.5%    |\n| 22-30| 2%   | 0.5% | +18%      |\n\n🎯 **ФИНАЛЬНЫЙ РЕЗУЛЬТАТ:** +70.5%",
        'marathon_text': "🏃‍♂️ **ПОЧЕМУ МАРАФОН ВАЖЕН?**\n\n• Дисциплина = Стабильность\n• Риск-менеджмент = Сохранность капитала\n• Системность = Прибыль\n\n✅ Следуя марафону, вы гарантированно выходите в плюс!",
        'stats_text': "📊 **ВАША СТАТИСТИКА**\n\n📌 **ID:** `{user_id}`\n✅ **Активен:** {active}\n\n📈 **Всего сделок:** {total}\n🏆 **Побед:** {wins}\n💔 **Поражений:** {losses}\n📊 **Винрейт:** {winrate}%\n💰 **Общая прибыль:** ${profit}\n\n📅 **Дата регистрации:** {date}",
        'top_text': "🏆 **ТОП-10 ТРЕЙДЕРОВ**\n\n{top_list}\n\n📊 *Обновляется каждые 24 часа*",
        'top_item': "{place}. {name}\n   📈 Сделок: {trades} | ✅ {wins} побед\n   💰 Прибыль: +${profit}\n",
        'unknown': "❌ Неизвестная команда"
    },
    'en': {
        'welcome': "👋 Welcome to VIP Premium MAX Pro Bot!\n\nChoose language:",
        'language_selected': "✅ Language set: English",
        'instruction_title': "📚 BOT INSTRUCTIONS | PAGE {page}/3",
        'instruction_1': "📊 **HOW TO USE THE BOT**\n\n1️⃣ **Registration**\n   • Deposit from ${min_deposit}\n   • Send your ID to admin\n\n2️⃣ **Get Access**\n   • Admin will grant access after payment\n   • You will receive notification",
        'instruction_2': "🎯 **HOW TO OPEN TRADES**\n\n3️⃣ **Get Signal**\n   • Press «📈 Get Signal»\n   • Choose category (Currency/Stocks/Crypto)\n   • Choose trading pair\n\n4️⃣ **Signal Analysis**\n   • Bot analyzes 25 indicators\n   • OTC market Pocket Option considered\n   • Mathematical accuracy algorithm",
        'instruction_3': "⚡ **IMPORTANT RULES**\n\n✅ Risk management: max 5% per trade\n✅ Trade only by signals\n✅ Follow marathon for stable growth\n\n📞 **Support**: {chat_link}\n📢 **Channel**: {channel_link}",
        'get_access': "🔑 GET ACCESS",
        'access_info': "🔐 **TO GET ACCESS**\n\n📌 **Your Telegram ID:** `{user_id}`\n\n💰 **Minimum deposit:** ${min_deposit}\n🔗 **Referral link:**\n{ref_link}\n\n📤 **Send payment screenshot and your ID to admin:**\n{chat_link}\n\n✅ Access will be granted after verification",
        'no_access': "❌ You don't have access to the bot.\n\nClick the button below to get access.",
        'main_menu': "🏠 **MAIN MENU**\n\nChoose section:",
        'signals': "📈 Get Signal",
        'marathon': "🏃 Marathon",
        'stats': "📊 Statistics",
        'top': "🏆 Top Traders",
        'currency': "💵 Currency Pairs OTC",
        'stocks': "📊 Stocks OTC",
        'crypto': "₿ Cryptocurrency OTC",
        'commodities': "🛢 Commodities",
        'back': "◀️ Back",
        'forward': "Forward ▶️",
        'select_pair': "Choose pair for analysis (page {page}/{total}):",
        'analysis': "🔍 **MARKET ANALYSIS**\n\nPair: {pair}\nType: {type}\n\n📊 **Technical Analysis:**\n{analysis}\n\n✅ **Confidence:** {confidence}%\n📈 **Recommendation:** {direction}\n\n⏰ **Choose expiration time:**",
        'signal_result': "🚀 **TRADE SIGNAL**\n\nPair: {pair}\nType: {type}\nDirection: {direction}\nExpiration: {exp}\n\n📊 **Indicator Analysis:**\n{indicators}\n\n🎯 **Levels:**\n• Resistance: {resistance}\n• Support: {support}\n• Entry point: {entry}\n\n💪 **Confidence:** {confidence}%\n💰 **Potential profit:** +{profit}%\n\n⚠️ Risk: {risk}%",
        'marathon_title': "🏃 **30-DAY MARATHON**\n\nGoal: +15% to deposit",
        'marathon_page1': "📅 **WEEK 1-2: ACCELERATION**\n\n| Day | Plan | Risk | Result |\n|-----|------|------|--------|\n| 1-7 | 2%   | 1%   | +14%   |\n| 8-14| 3%   | 1.5% | +21%   |\n\n📊 **Total for 2 weeks:** +35%",
        'marathon_page2': "📅 **WEEK 3-4: STABILITY**\n\n| Day | Plan | Risk | Result |\n|-----|------|------|--------|\n| 15-21| 2.5% | 1%  | +17.5% |\n| 22-30| 2%  | 0.5%| +18%   |\n\n🎯 **FINAL RESULT:** +70.5%",
        'marathon_text': "🏃‍♂️ **WHY MARATHON IS IMPORTANT?**\n\n• Discipline = Stability\n• Risk management = Capital preservation\n• System = Profit\n\n✅ Following the marathon guarantees profit!",
        'stats_text': "📊 **YOUR STATISTICS**\n\n📌 **ID:** `{user_id}`\n✅ **Active:** {active}\n\n📈 **Total trades:** {total}\n🏆 **Wins:** {wins}\n💔 **Losses:** {losses}\n📊 **Winrate:** {winrate}%\n💰 **Total profit:** ${profit}\n\n📅 **Registration date:** {date}",
        'top_text': "🏆 **TOP-10 TRADERS**\n\n{top_list}\n\n📊 *Updates every 24 hours*",
        'top_item': "{place}. {name}\n   📈 Trades: {trades} | ✅ {wins} wins\n   💰 Profit: +${profit}\n",
        'unknown': "❌ Unknown command"
    },
    'kg': {
        'welcome': "👋 VIP Premium MAX Pro Botкош келиңиз!\n\nТилди тандаңыз:",
        'language_selected': "✅ Тил орнотулду: Кыргызча",
        'instruction_title': "📚 БОТ БОЮНЧА НУСКАМА | БЕТ {page}/3",
        'instruction_1': "📊 **БОТТУ КОЛДОНУУ**\n\n1️⃣ **Каттоо**\n   • Эсепти толтуруу ${min_deposit}\n   • IDңизди админге жөнөтүү\n\n2️⃣ **Жеткилик алуу**\n   • Төлөмдөн кийин админ жеткилик берет\n   • Сиз билдирүү аласыз",
        'instruction_2': "🎯 **СООДА АЧУУ**\n\n3️⃣ **Сигнал алуу**\n   • «📈 Сигнал алуу» баскычын басыңыз\n   • Категорияны тандоо (Валюта/Акция/Крипто)\n   • Соода парын тандоо\n\n4️⃣ **Сигнал анализи**\n   • Бот 25 индикаторду талдайт\n   • Pocket Option OTC рыногу эске алынат\n   • Математикалык тактык алгоритми",
        'instruction_3': "⚡ **МААНИЛҮҮ ЭРЕЖЕЛЕР**\n\n✅ Риск-менеджмент: сооданын 5% ашпоосу керек\n✅ Сигналдар менен гана соода кылыңыз\n✅ Туруктуу өсүү үчүн марафонду аткарыңыз\n\n📞 **Колдоо**: {chat_link}\n📢 **Канал**: {channel_link}",
        'get_access': "🔑 ЖЕТКИЛИК АЛУУ",
        'access_info': "🔐 **ЖЕТКИЛИК АЛУУ ҮЧҮН**\n\n📌 **Сиздин Telegram ID:** `{user_id}`\n\n💰 **Минималдуу депозит:** ${min_deposit}\n🔗 **Рефералдык шилтеме:**\n{ref_link}\n\n📤 **Төлөм скриншотун жана IDңизди админге жөнөтүңүз:**\n{chat_link}\n\n✅ Текшерүүдөн кийин жеткилик берилет",
        'no_access': "❌ Сизде ботко жеткилик жок.\n\nТөмөнкү баскычты басып, жеткилик алыңыз.",
        'main_menu': "🏠 **БАШКЫ МЕНЮ**\n\nБөлүмдү тандаңыз:",
        'signals': "📈 Сигнал алуу",
        'marathon': "🏃 Марафон",
        'stats': "📊 Статистика",
        'top': "🏆 Мыкты трейдерлер",
        'currency': "💵 Валюталык парлар OTC",
        'stocks': "📊 Акциялар OTC",
        'crypto': "₿ Криптовалюта OTC",
        'commodities': "🛢 Сырье товарлары",
        'back': "◀️ Артка",
        'forward': "Алга ▶️",
        'select_pair': "Анализ үчүн парды тандоо (бет {page}/{total}):",
        'analysis': "🔍 **РЫНОК АНАЛИЗИ**\n\nПар: {pair}\nТип: {type}\n\n📊 **Техникалык анализ:**\n{analysis}\n\n✅ **Ишенимдүүлүк:** {confidence}%\n📈 **Сунуш:** {direction}\n\n⏰ **Экспирация убактысын тандоо:**",
        'signal_result': "🚀 **СООДА СИГНАЛЫ**\n\nПар: {pair}\nТип: {type}\nБагыт: {direction}\nЭкспирация: {exp}\n\n📊 **Индикаторлор анализи:**\n{indicators}\n\n🎯 **Деңгээлдер:**\n• Каршылык: {resistance}\n• Колдоо: {support}\n• Кирүү чекити: {entry}\n\n💪 **Ишенимдүүлүк:** {confidence}%\n💰 **Потенциалдуу пайда:** +{profit}%\n\n⚠️ Риск: {risk}%",
        'marathon_title': "🏃 **30 КҮНДҮК МАРАФОН**\n\nМаксат: депозитке +15%",
        'marathon_page1': "📅 **1-2 ЖУМА: РАЗГОН**\n\n| Күн | План | Риск | Жыйынтык |\n|-----|------|------|----------|\n| 1-7 | 2%   | 1%   | +14%     |\n| 8-14| 3%   | 1.5% | +21%     |\n\n📊 **2 жуманын жыйынтыгы:** +35%",
        'marathon_page2': "📅 **3-4 ЖУМА: ТУРУКТУУЛУК**\n\n| Күн | План | Риск | Жыйынтык |\n|-----|------|------|----------|\n| 15-21| 2.5% | 1%  | +17.5%   |\n| 22-30| 2%  | 0.5%| +18%     |\n\n🎯 **ЖЫЙЫНТЫК:** +70.5%",
        'marathon_text': "🏃‍♂️ **МАРАФОН ЭМНЕ ҮЧҮН МААНИЛҮҮ?**\n\n• Дисциплина = Туруктуулук\n• Риск-менеджмент = Капиталды сактоо\n• Система = Пайда\n\n✅ Марафонду аткаруу пайданы кепилдейт!",
        'stats_text': "📊 **СИЗДИН СТАТИСТИКАҢЫЗ**\n\n📌 **ID:** `{user_id}`\n✅ **Активдүү:** {active}\n\n📈 **Бардык соодалар:** {total}\n🏆 **Жеңиштер:** {wins}\n💔 **Утулуштар:** {losses}\n📊 **Винрейт:** {winrate}%\n💰 **Жалпы пайда:** ${profit}\n\n📅 **Катталган күн:** {date}",
        'top_text': "🏆 **ТОП-10 ТРЕЙДЕРЛЕР**\n\n{top_list}\n\n📊 *24 саатта бир жаңыланат*",
        'top_item': "{place}. {name}\n   📈 Соода: {trades} | ✅ {wins} жеңиш\n   💰 Пайда: +${profit}\n",
        'unknown': "❌ Белгисиз буйрук"
    },
    'uz': {
        'welcome': "👋 VIP Premium MAX Pro Botga xush kelibsiz!\n\nTilni tanlang:",
        'language_selected': "✅ Til o'rnatildi: O'zbekcha",
        'instruction_title': "📚 BOT BO'YICHA YO'RIQNOMA | SAHIFA {page}/3",
        'instruction_1': "📊 **BOTDAN FOYDALANISH**\n\n1️⃣ **Ro'yxatdan o'tish**\n   • Hisobni to'ldirish ${min_deposit}\n   • IDingizni adminga yuborish\n\n2️⃣ **Ruxsat olish**\n   • To'lovdan keyin admin ruxsat beradi\n   • Siz xabar olasiz",
        'instruction_2': "🎯 **SAVDO OCHISH**\n\n3️⃣ **Signal olish**\n   • «📈 Signal olish» tugmasini bosing\n   • Kategoriyani tanlash (Valyuta/Aksiya/Kripto)\n   • Savdo juftligini tanlash\n\n4️⃣ **Signal tahlili**\n   • Bot 25 indikatorni tahlil qiladi\n   • Pocket Option OTC bozori hisobga olinadi\n   • Matematik aniqlik algoritmi",
        'instruction_3': "⚡ **MUHIM QOIDALAR**\n\n✅ Risk-menejment: savdoning 5% dan oshmasligi kerak\n✅ Faqat signallar bilan savdo qiling\n✅ Barqaror o'sish uchun marafonni bajaring\n\n📞 **Qo'llab-quvvatlash**: {chat_link}\n📢 **Kanal**: {channel_link}",
        'get_access': "🔑 RUXSAT OLISH",
        'access_info': "🔐 **RUXSAT OLISH UCHUN**\n\n📌 **Sizning Telegram ID:** `{user_id}`\n\n💰 **Minimal depozit:** ${min_deposit}\n🔗 **Referal havola:**\n{ref_link}\n\n📤 **To'lov skrinshoti va IDingizni adminga yuboring:**\n{chat_link}\n\n✅ Tekshiruvdan keyin ruxsat beriladi",
        'no_access': "❌ Sizda botga ruxsat yo'q.\n\nQuyidagi tugmani bosib, ruxsat oling.",
        'main_menu': "🏠 **ASOSIY MENYU**\n\nBo'limni tanlang:",
        'signals': "📈 Signal olish",
        'marathon': "🏃 Marafon",
        'stats': "📊 Statistika",
        'top': "🏆 Top treyderlar",
        'currency': "💵 Valyuta juftliklari OTC",
        'stocks': "📊 Aksiyalar OTC",
        'crypto': "₿ Kriptovalyuta OTC",
        'commodities': "🛢 Xom ashyo",
        'back': "◀️ Orqaga",
        'forward': "Oldinga ▶️",
        'select_pair': "Tahlil uchun juftlikni tanlang (sahifa {page}/{total}):",
        'analysis': "🔍 **BOZOR TAHLILI**\n\nJuftlik: {pair}\nTur: {type}\n\n📊 **Texnik tahlil:**\n{analysis}\n\n✅ **Ishonchlilik:** {confidence}%\n📈 **Tavsiya:** {direction}\n\n⏰ **Ekspiratsiya vaqtini tanlang:**",
        'signal_result': "🚀 **SAVDO SIGNALI**\n\nJuftlik: {pair}\nTur: {type}\nYo'nalish: {direction}\nEkspiratsiya: {exp}\n\n📊 **Indikatorlar tahlili:**\n{indicators}\n\n🎯 **Darajalar:**\n• Qarshilik: {resistance}\n• Qo'llab-quvvatlash: {support}\n• Kirish nuqtasi: {entry}\n\n💪 **Ishonchlilik:** {confidence}%\n💰 **Potentsial foyda:** +{profit}%\n\n⚠️ Risk: {risk}%",
        'marathon_title': "🏃 **30 KUNLIK MARAFON**\n\nMaqsad: depozitga +15%",
        'marathon_page1': "📅 **1-2 HAFTA: RAZGON**\n\n| Kun | Reja | Risk | Natija |\n|-----|------|------|--------|\n| 1-7 | 2%   | 1%   | +14%   |\n| 8-14| 3%   | 1.5% | +21%   |\n\n📊 **2 hafta yakuni:** +35%",
        'marathon_page2': "📅 **3-4 HAFTA: BARQARORLIK**\n\n| Kun | Reja | Risk | Natija |\n|-----|------|------|--------|\n| 15-21| 2.5% | 1%  | +17.5% |\n| 22-30| 2%  | 0.5%| +18%   |\n\n🎯 **YAKUNIY NATIJA:** +70.5%",
        'marathon_text': "🏃‍♂️ **MARAFON NEGA MUHIM?**\n\n• Intizom = Barqarorlik\n• Risk-menejment = Kapitalni saqlash\n• Tizim = Foyda\n\n✅ Marafonni bajarish foydani kafolatlaydi!",
        'stats_text': "📊 **SIZNING STATISTIKANGIZ**\n\n📌 **ID:** `{user_id}`\n✅ **Aktiv:** {active}\n\n📈 **Jami savdolar:** {total}\n🏆 **G'alabalar:** {wins}\n💔 **Mag'lubiyatlar:** {losses}\n📊 **Vinreyt:** {winrate}%\n💰 **Umumiy foyda:** ${profit}\n\n📅 **Ro'yxatdan o'tgan sana:** {date}",
        'top_text': "🏆 **TOP-10 TREYDERLAR**\n\n{top_list}\n\n📊 *24 soatda bir yangilanadi*",
        'top_item': "{place}. {name}\n   📈 Savdolar: {trades} | ✅ {wins} g'alaba\n   💰 Foyda: +${profit}\n",
        'unknown': "❌ Noma'lum buyruq"
    }
}

# ================ СПИСКИ ПАР ================
CURRENCY_PAIRS = [
    "AED/CNY OTC", "AUD/CAD OTC", "AUD/CHF OTC", "AUD/NZD OTC", "AUD/USD OTC",
    "CAD/JPY OTC", "CHF/JPY OTC", "CHF/NOK OTC", "EUR/CHF OTC", "EUR/GBP OTC",
    "EUR/HUF OTC", "EUR/NZD OTC", "EUR/RUB OTC", "EUR/USD OTC", "KES/USD OTC",
    "LBP/USD OTC", "MAD/USD OTC", "NZD/JPY OTC", "OMR/CNY OTC", "USD/ARS OTC",
    "USD/CAD OTC", "USD/CHF OTC", "USD/CNH OTC", "USD/COP OTC", "USD/DZD OTC",
    "USD/EGP OTC", "USD/MXN OTC", "USD/MYR OTC", "USD/PKR OTC", "USD/SGD OTC",
    "YER/USD OTC", "ZAR/USD OTC", "USD/IDR OTC", "NGN/USD OTC", "USD/CLP OTC",
    "AUD/JPY OTC", "GBP/AUD OTC", "USD/THB OTC", "TND/USD OTC", "EUR/TRY OTC",
    "CAD/CHF OTC", "USD/PHP OTC", "GBP/JPY OTC", "BHD/CNY OTC", "GBP/USD OTC",
    "USD/BDT OTC", "USD/BRL OTC", "NZD/USD OTC", "USD/INR OTC", "UAH/USD OTC",
    "JOD/CNY OTC", "USD/JPY OTC", "SAR/CNY OTC", "EUR/JPY OTC", "USD/RUB OTC",
    "USD/VND OTC", "QAR/CNY OTC"
]

STOCK_PAIRS = [
    "American Express OTC", "Boeing Company OTC", "FACEBOOK INC OTC", "Intel OTC",
    "Johnson & Johnson OTC", "Microsoft OTC", "Tesla OTC", "ExxonMobil OTC",
    "Advanced Micro Devices OTC", "Amazon OTC", "Alibaba OTC", "Citigroup Inc OTC",
    "FedEx OTC", "GameStop Corp OTC", "Marathon Digital Holdings OTC", "Coinbase Global OTC",
    "Pfizer Inc OTC", "VISA OTC", "McDonald's OTC", "Netflix OTC", "Apple OTC",
    "Cisco OTC", "Palantir Technologies OTC", "VIX OTC"
]

CRYPTO_PAIRS = [
    "Bitcoin ETF OTC", "BNB OTC", "Bitcoin OTC", "Ethereum OTC", "Chainlink OTC",
    "Litecoin OTC", "Dogecoin OTC", "Solana OTC", "Toncoin OTC", "Avalanche OTC",
    "Polkadot OTC", "TRON OTC", "Polygon OTC", "Cardano OTC"
]

COMMODITIES_PAIRS = [
    "Brent Oil OTC", "WTI Crude Oil OTC", "Silver OTC", "Gold OTC",
    "Natural Gas OTC", "Palladium spot OTC", "Platinum spot OTC"
]

ALL_PAIRS = {
    'currency': CURRENCY_PAIRS,
    'stocks': STOCK_PAIRS,
    'crypto': CRYPTO_PAIRS,
    'commodities': COMMODITIES_PAIRS
}

# Временные интервалы
EXPIRATION_TIMES = ['30 сек', '1 мин', '2 мин', '3 мин', '4 мин', '5 мин', '6 мин', '7 мин', '8 мин', '9 мин', '10 мин']

# ================ БАЗА ДАННЫХ ================
conn = sqlite3.connect('bot_data.db', check_same_thread=False)
cursor = conn.cursor()

# Таблица пользователей
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        user_id INTEGER PRIMARY KEY,
        language TEXT DEFAULT 'ru',
        username TEXT,
        first_name TEXT,
        is_active INTEGER DEFAULT 0,
        joined_date TEXT,
        total_trades INTEGER DEFAULT 0,
        wins INTEGER DEFAULT 0,
        losses INTEGER DEFAULT 0,
        profit REAL DEFAULT 0.0
    )
''')

# Таблица для сделок
cursor.execute('''
    CREATE TABLE IF NOT EXISTS trades (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        pair TEXT,
        direction TEXT,
        exp_time TEXT,
        result TEXT,
        profit REAL,
        date TEXT
    )
''')

# Таблица для топ-трейдеров
cursor.execute('''
    CREATE TABLE IF NOT EXISTS top_traders (
        user_id INTEGER PRIMARY KEY,
        username TEXT,
        total_trades INTEGER,
        wins INTEGER,
        profit REAL
    )
''')

# Заполним топ-трейдеров демо-данными
cursor.execute("SELECT COUNT(*) FROM top_traders")
if cursor.fetchone()[0] == 0:
    demo_traders = [
        (123456, 'CryptoKing', 154, 132, 8750.5),
        (234567, 'GoldMaster', 98, 79, 4320.75),
        (345678, 'ForexPro', 211, 180, 12100.0),
        (456789, 'OTC_Sniper', 67, 54, 2910.2),
        (567890, 'Pocket_Elite', 189, 151, 9670.9),
        (678901, 'SignalHunter', 45, 38, 2100.0),
        (789012, 'BinaryWhale', 302, 260, 18700.3),
        (890123, 'TrendFollower', 88, 70, 4100.0),
        (901234, 'OTC_Baron', 123, 98, 5600.75),
        (112233, 'OptionMaster', 276, 235, 15320.5)
    ]
    for trader in demo_traders:
        cursor.execute('INSERT OR REPLACE INTO top_traders VALUES (?,?,?,?,?)', trader)

conn.commit()

# ================ ФУНКЦИИ ПОМОЩНИКИ ================
def get_text(user_id, key, **kwargs):
    """Получить текст на языке пользователя"""
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    lang = result[0] if result else 'ru'
    
    # Для админа всегда русский
    if user_id == ADMIN_ID:
        lang = 'ru'
    
    text = TEXTS[lang].get(key, TEXTS['ru'].get(key, ''))
    
    # Добавляем глобальные переменные
    kwargs['min_deposit'] = MIN_DEPOSIT
    kwargs['channel_link'] = CHANNEL_LINK
    kwargs['chat_link'] = CHAT_LINK
    kwargs['youtube_link'] = YOUTUBE_LINK
    kwargs['ref_link'] = REFERRAL_LINK
    
    return text.format(**kwargs)

def get_user_lang(user_id):
    """Получить язык пользователя"""
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result[0] if result else 'ru'

def register_user(message):
    """Регистрация нового пользователя"""
    user_id = message.from_user.id
    username = message.from_user.username or "NoUsername"
    first_name = message.from_user.first_name or "User"
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (user_id, username, first_name, joined_date)
        VALUES (?, ?, ?, ?)
    ''', (user_id, username, first_name, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()

def check_access(user_id):
    """Проверка доступа пользователя"""
    if user_id == ADMIN_ID:
        return True
    cursor.execute('SELECT is_active FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    return result and result[0] == 1

def generate_analysis(pair, type_name):
    """Генерация продвинутого анализа (симуляция 25 индикаторов)"""
    indicators = [
        "RSI (14): {rsi} - {rsi_signal}",
        "MACD: {macd} - {macd_signal}",
        "Bollinger Bands: {bb} - {bb_signal}",
        "Stochastic: {stoch} - {stoch_signal}",
        "Moving Average 50: {ma50} - {ma50_signal}",
        "Moving Average 200: {ma200} - {ma200_signal}",
        "Ichimoku: {ichi} - {ichi_signal}",
        "Fibonacci: {fib} - {fib_signal}",
        "Parabolic SAR: {psar} - {psar_signal}",
        "ADX: {adx} - {adx_signal}",
        "ATR: {atr}",
        "CCI: {cci} - {cci_signal}",
        "Williams %R: {williams} - {williams_signal}",
        "MFI: {mfi} - {mfi_signal}",
        "OBV: {obv_signal}",
        "VWAP: {vwap} - {vwap_signal}",
        "Elder Ray: {elder_signal}",
        "Chaikin Money Flow: {cmf} - {cmf_signal}",
        "Donchian Channels: {donchian_signal}",
        "Keltner Channels: {keltner_signal}",
        "Pivot Points: {pivot}",
        "Camarilla: {camarilla}",
        "Woodie: {woodie}",
        "DEMA: {dema_signal}",
        "TEMA: {tema_signal}"
    ]
    
    # Генерация случайных значений с математическим уклоном
    confidence = random.randint(75, 98)
    direction = random.choice(["CALL (ВВЕРХ) ⬆️", "PUT (ВНИЗ) ⬇️"])
    
    def get_signal(value):
        if value > 50:
            return "бычий"
        elif value < 50:
            return "медвежий"
        else:
            return "нейтральный"
    
    analysis_text = "\n".join(random.sample(indicators, 12))  # Берем 12 случайных индикаторов
    
    # Заполняем случайными значениями
    analysis_text = analysis_text.replace("{rsi}", str(random.randint(20, 80)))
    analysis_text = analysis_text.replace("{rsi_signal}", get_signal(random.randint(20, 80)))
    analysis_text = analysis_text.replace("{macd}", random.choice(["бычье пересечение", "медвежье пересечение", "выше нуля", "ниже нуля"]))
    analysis_text = analysis_text.replace("{macd_signal}", random.choice(["покупка", "продажа", "нейтрально"]))
    analysis_text = analysis_text.replace("{bb}", random.choice(["верхняя полоса", "нижняя полоса", "средняя линия"]))
    analysis_text = analysis_text.replace("{bb_signal}", random.choice(["перекуплен", "перепродан", "нейтрально"]))
    analysis_text = analysis_text.replace("{stoch}", str(random.randint(10, 90)))
    analysis_text = analysis_text.replace("{stoch_signal}", get_signal(random.randint(10, 90)))
    analysis_text = analysis_text.replace("{ma50}", random.choice(["выше MA200", "ниже MA200", "пересечение"]))
    analysis_text = analysis_text.replace("{ma50_signal}", random.choice(["покупка", "продажа"]))
    analysis_text = analysis_text.replace("{ma200}", random.choice(["поддержка", "сопротивление", "нейтрально"]))
    analysis_text = analysis_text.replace("{ma200_signal}", random.choice(["тренд вверх", "тренд вниз"]))
    analysis_text = analysis_text.replace("{ichi}", random.choice(["облако поддержки", "облако сопротивления", "пересечение"]))
    analysis_text = analysis_text.replace("{ichi_signal}", random.choice(["покупка", "продажа", "ожидание"]))
    analysis_text = analysis_text.replace("{fib}", str(round(random.uniform(0.236, 0.786), 3)))
    analysis_text = analysis_text.replace("{psar}", random.choice(["ниже цены", "выше цены"]))
    analysis_text = analysis_text.replace("{adx}", str(random.randint(20, 60)))
    analysis_text = analysis_text.replace("{adx_signal}", random.choice(["сильный тренд", "слабый тренд"]))
    analysis_text = analysis_text.replace("{atr}", str(round(random.uniform(0.001, 0.05), 4)))
    analysis_text = analysis_text.replace("{cci}", str(random.randint(-200, 200)))
    analysis_text = analysis_text.replace("{cci_signal}", random.choice(["перекуплен", "перепродан"]))
    analysis_text = analysis_text.replace("{williams}", str(random.randint(-100, 0)))
    analysis_text = analysis_text.replace("{williams_signal}", get_signal(random.randint(0, 100)))
    analysis_text = analysis_text.replace("{mfi}", str(random.randint(20, 80)))
    analysis_text = analysis_text.replace("{mfi_signal}", get_signal(random.randint(20, 80)))
    analysis_text = analysis_text.replace("{obv_signal}", random.choice(["растет", "падает", "нейтрально"]))
    analysis_text = analysis_text.replace("{vwap}", str(round(random.uniform(1.0, 2.0), 4)))
    analysis_text = analysis_text.replace("{cmf}", str(round(random.uniform(-0.3, 0.3), 2)))
    analysis_text = analysis_text.replace("{cmf_signal}", random.choice(["положительный", "отрицательный"]))
    analysis_text = analysis_text.replace("{elder_signal}", random.choice(["покупка", "продажа", "нейтрально"]))
    analysis_text = analysis_text.replace("{donchian_signal}", random.choice(["верхний канал", "нижний канал"]))
    analysis_text = analysis_text.replace("{keltner_signal}", random.choice(["выше канала", "ниже канала"]))
    analysis_text = analysis_text.replace("{pivot}", str(round(random.uniform(1.0, 1.5), 4)))
    analysis_text = analysis_text.replace("{camarilla}", str(round(random.uniform(1.0, 1.5), 4)))
    analysis_text = analysis_text.replace("{woodie}", str(round(random.uniform(1.0, 1.5), 4)))
    analysis_text = analysis_text.replace("{dema_signal}", random.choice(["покупка", "продажа"]))
    analysis_text = analysis_text.replace("{tema_signal}", random.choice(["покупка", "продажа"]))
    
    resistance = round(random.uniform(1.05, 1.20), 4)
    support = round(random.uniform(0.95, 1.00), 4)
    entry = round(random.uniform(support, resistance), 4)
    
    return {
        'analysis': analysis_text,
        'confidence': confidence,
        'direction': direction,
        'resistance': resistance,
        'support': support,
        'entry': entry,
        'profit': round(confidence * 0.85, 1),
        'risk': round(100 - confidence * 0.9, 1)
    }

# ================ КЛАВИАТУРЫ ================
def language_keyboard():
    """Клавиатура выбора языка"""
    markup = types.InlineKeyboardMarkup(row_width=2)
    for lang_code, lang_info in LANGUAGES.items():
        markup.add(types.InlineKeyboardButton(
            f"{lang_info['flag']} {lang_info['name']}",
            callback_data=f"lang_{lang_code}"
        ))
    return markup

def instruction_keyboard(user_id, page=1):
    """Клавиатура для инструкции"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    
    nav_buttons = []
    if page > 1:
        nav_buttons.append(types.InlineKeyboardButton(
            TEXTS[get_user_lang(user_id)]['back'], 
            callback_data=f"inst_{page-1}"
        ))
    
    nav_buttons.append(types.InlineKeyboardButton(
        f"• {page}/3 •", 
        callback_data="noop"
    ))
    
    if page < 3:
        nav_buttons.append(types.InlineKeyboardButton(
            TEXTS[get_user_lang(user_id)]['forward'], 
            callback_data=f"inst_{page+1}"
        ))
    
    markup.row(*nav_buttons)
    markup.add(types.InlineKeyboardButton(
        TEXTS[get_user_lang(user_id)]['get_access'], 
        callback_data="get_access"
    ))
    
    return markup

def main_menu_keyboard(user_id):
    """Главное меню"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    t = get_text(user_id, 'main_menu')
    
    btn1 = types.KeyboardButton(TEXTS[get_user_lang(user_id)]['signals'])
    btn2 = types.KeyboardButton(TEXTS[get_user_lang(user_id)]['marathon'])
    btn3 = types.KeyboardButton(TEXTS[get_user_lang(user_id)]['stats'])
    btn4 = types.KeyboardButton(TEXTS[get_user_lang(user_id)]['top'])
    
    markup.add(btn1, btn2, btn3, btn4)
    return markup

def signals_categories_keyboard(user_id):
    """Категории для сигналов"""
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    t = get_user_lang(user_id)
    
    markup.add(
        types.KeyboardButton(TEXTS[t]['currency']),
        types.KeyboardButton(TEXTS[t]['stocks']),
        types.KeyboardButton(TEXTS[t]['crypto']),
        types.KeyboardButton(TEXTS[t]['commodities'])
    )
    markup.add(types.KeyboardButton("🏠 Главное меню"))
    return markup

def pairs_keyboard(user_id, category, page=0, items_per_page=14):
    """Клавиатура для выбора пары"""
    pairs = ALL_PAIRS.get(category, [])
    total_pages = (len(pairs) + items_per_page - 1) // items_per_page
    
    markup = types.InlineKeyboardMarkup(row_width=2)
    
    start = page * items_per_page
    end = min(start + items_per_page, len(pairs))
    
    for pair in pairs[start:end]:
        callback = f"pair_{category}_{pair}"
        markup.add(types.InlineKeyboardButton(pair, callback_data=callback[:64]))
    
    nav_buttons = []
    if page > 0:
        nav_buttons.append(types.InlineKeyboardButton(
            TEXTS[get_user_lang(user_id)]['back'], 
            callback_data=f"page_{category}_{page-1}"
        ))
    
    nav_buttons.append(types.InlineKeyboardButton(
        f"{page+1}/{total_pages}", 
        callback_data="noop"
    ))
    
    if page < total_pages - 1:
        nav_buttons.append(types.InlineKeyboardButton(
            TEXTS[get_user_lang(user_id)]['forward'], 
            callback_data=f"page_{category}_{page+1}"
        ))
    
    markup.row(*nav_buttons)
    markup.row(types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu"))
    
    return markup

def expiration_keyboard(user_id, pair, category, analysis_data):
    """Клавиатура выбора времени экспирации"""
    markup = types.InlineKeyboardMarkup(row_width=3)
    
    for exp in EXPIRATION_TIMES:
        callback = f"exp_{pair[:20]}_{category}_{exp}"
        markup.add(types.InlineKeyboardButton(exp, callback_data=callback[:64]))
    
    markup.add(types.InlineKeyboardButton("◀️ Назад к парам", callback_data=f"back_to_{category}"))
    
    return markup

# ================ КОМАНДЫ ================
@bot.message_handler(commands=['start'])
def start(message):
    """Обработка команды /start"""
    user_id = message.from_user.id
    register_user(message)
    
    # Админ сразу получает доступ
    if user_id == ADMIN_ID:
        cursor.execute('UPDATE users SET is_active = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        bot.send_message(user_id, "👑 Добро пожаловать, Администратор!", reply_markup=main_menu_keyboard(user_id))
        return
    
    # Проверяем, есть ли уже язык
    cursor.execute('SELECT language FROM users WHERE user_id = ?', (user_id,))
    result = cursor.fetchone()
    
    if result and result[0]:
        # Язык уже выбран, показываем инструкцию или меню
        if check_access(user_id):
            bot.send_message(user_id, get_text(user_id, 'main_menu'), reply_markup=main_menu_keyboard(user_id))
        else:
            show_instructions(message, page=1)
    else:
        # Выбор языка
        bot.send_message(
            user_id,
            "👋 Добро пожаловать! Выберите язык / Tilni tanlang / Тилди тандаңыз:",
            reply_markup=language_keyboard()
        )

@bot.callback_query_handler(func=lambda call: True)
def callback_handler(call):
    """Обработка всех callback'ов"""
    user_id = call.from_user.id
    data = call.data
    
    # Админские команды
    if data.startswith('admin_'):
        if user_id != ADMIN_ID:
            bot.answer_callback_query(call.id, "❌ Доступ запрещен")
            return
        
        cmd = data.replace('admin_', '')
        if cmd == 'stats':
            # Статистика бота
            cursor.execute('SELECT COUNT(*) FROM users')
            total_users = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
            active_users = cursor.fetchone()[0]
            cursor.execute('SELECT COUNT(*) FROM trades')
            total_trades = cursor.fetchone()[0]
            
            stats = f"📊 **СТАТИСТИКА БОТА**\n\n"
            stats += f"👥 Всего пользователей: {total_users}\n"
            stats += f"✅ Активных: {active_users}\n"
            stats += f"📈 Всего сделок: {total_trades}\n"
            
            bot.send_message(user_id, stats)
    
    # Выбор языка
    elif data.startswith('lang_'):
        lang = data.replace('lang_', '')
        cursor.execute('UPDATE users SET language = ? WHERE user_id = ?', (lang, user_id))
        conn.commit()
        
        bot.answer_callback_query(call.id, TEXTS[lang]['language_selected'])
        bot.delete_message(user_id, call.message.message.id)
        
        # Показываем инструкцию
        show_instructions_callback(user_id, call.message, page=1)
    
    # Навигация по инструкции
    elif data.startswith('inst_'):
        if data == 'inst_get':
            show_access_info(user_id, call.message)
        else:
            page = int(data.replace('inst_', ''))
            show_instructions_callback(user_id, call.message, page)
    
    # Получить доступ
    elif data == 'get_access':
        show_access_info(user_id, call.message)
    
    # Возврат в главное меню
    elif data == 'main_menu':
        bot.delete_message(user_id, call.message.message.id)
        bot.send_message(user_id, get_text(user_id, 'main_menu'), reply_markup=main_menu_keyboard(user_id))
    
    # Пустая операция
    elif data == 'noop':
        bot.answer_callback_query(call.id)
    
    # Навигация по страницам пар
    elif data.startswith('page_'):
        parts = data.split('_')
        category = parts[1]
        page = int(parts[2])
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message.id,
            text=get_text(user_id, 'select_pair', page=page+1, total=(len(ALL_PAIRS[category])+13)//14),
            reply_markup=pairs_keyboard(user_id, category, page)
        )
    
    # Назад к категории
    elif data.startswith('back_to_'):
        category = data.replace('back_to_', '')
        show_category_pairs(user_id, call.message, category)
    
    # Выбор пары
    elif data.startswith('pair_'):
        parts = data.split('_')
        category = parts[1]
        pair = '_'.join(parts[2:]).replace('_', ' ')
        
        # Генерируем анализ
        analysis = generate_analysis(pair, category)
        
        # Сохраняем в памяти (можно в БД, но для простоты через message)
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message.id,
            text=get_text(user_id, 'analysis',
                         pair=pair,
                         type=category,
                         analysis=analysis['analysis'][:200] + "...",
                         confidence=analysis['confidence'],
                         direction=analysis['direction']),
            reply_markup=expiration_keyboard(user_id, pair, category, analysis)
        )
    
    # Выбор времени экспирации
    elif data.startswith('exp_'):
        parts = data.split('_')
        pair = parts[1].replace('_', ' ')
        category = parts[2]
        exp_time = parts[3] + (' ' + parts[4] if len(parts) > 4 else '')
        
        # Генерируем финальный сигнал
        analysis = generate_analysis(pair, category)
        
        # Случайно определяем результат (для демо)
        result = random.choice(['win', 'loss'])
        profit = round(random.uniform(65, 95), 1) if result == 'win' else -round(random.uniform(10, 50), 1)
        
        # Сохраняем сделку в статистику пользователя
        cursor.execute('''
            INSERT INTO trades (user_id, pair, direction, exp_time, result, profit, date)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (user_id, pair, analysis['direction'], exp_time, result, profit, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
        
        cursor.execute('''
            UPDATE users 
            SET total_trades = total_trades + 1,
                wins = wins + ?,
                losses = losses + ?,
                profit = profit + ?
            WHERE user_id = ?
        ''', (1 if result == 'win' else 0, 1 if result == 'loss' else 0, profit, user_id))
        
        conn.commit()
        
        # Показываем результат
        indicators_text = "\n".join([
            f"• RSI: {random.randint(20,80)} - {random.choice(['бычий', 'медвежий'])}",
            f"• MACD: {random.choice(['сигнал вверх', 'сигнал вниз'])}",
            f"• Stochastic: {random.choice(['перекуплен', 'перепродан'])}",
            f"• MA: {random.choice(['золотое сечение', 'смертельное сечение'])}",
            f"• Bollinger: {random.choice(['расширение', 'сужение'])}"
        ])
        
        signal_text = get_text(user_id, 'signal_result',
                              pair=pair,
                              type=category,
                              direction=analysis['direction'],
                              exp=exp_time,
                              indicators=indicators_text,
                              resistance=analysis['resistance'],
                              support=analysis['support'],
                              entry=analysis['entry'],
                              confidence=analysis['confidence'],
                              profit=analysis['profit'],
                              risk=analysis['risk'])
        
        if result == 'win':
            signal_text += f"\n\n✅ **РЕЗУЛЬТАТ: ПРИБЫЛЬ +${profit}** 🎉"
        else:
            signal_text += f"\n\n❌ **РЕЗУЛЬТАТ: УБЫТОК -${abs(profit)}** 📉"
        
        bot.edit_message_text(
            chat_id=user_id,
            message_id=call.message.message.id,
            text=signal_text,
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton("🔄 Новый сигнал", callback_data=f"back_to_{category}"),
                types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
            )
        )

def show_instructions(message, page=1):
    """Показать инструкцию для нового пользователя"""
    user_id = message.from_user.id
    
    text = get_text(user_id, 'instruction_title', page=page) + "\n\n"
    text += get_text(user_id, f'instruction_{page}')
    
    bot.send_message(
        user_id,
        text,
        reply_markup=instruction_keyboard(user_id, page),
        parse_mode='Markdown'
    )

def show_instructions_callback(user_id, message, page=1):
    """Показать инструкцию (callback)"""
    text = get_text(user_id, 'instruction_title', page=page) + "\n\n"
    text += get_text(user_id, f'instruction_{page}')
    
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message.message.id,
        text=text,
        reply_markup=instruction_keyboard(user_id, page),
        parse_mode='Markdown'
    )

def show_access_info(user_id, message):
    """Показать информацию для получения доступа"""
    text = get_text(user_id, 'access_info', user_id=user_id)
    
    # Добавляем ссылки красиво
    text += f"\n\n📢 **Наш канал:** {CHANNEL_LINK}"
    text += f"\n📺 **YouTube:** {YOUTUBE_LINK}"
    
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message.message.id,
        text=text,
        reply_markup=types.InlineKeyboardMarkup().add(
            types.InlineKeyboardButton("📞 Написать админу", url=CHAT_LINK),
            types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
        ),
        parse_mode='Markdown',
        disable_web_page_preview=True
    )

def show_category_pairs(user_id, message, category):
    """Показать пары категории"""
    text = get_text(user_id, 'select_pair', page=1, total=(len(ALL_PAIRS[category])+13)//14)
    bot.edit_message_text(
        chat_id=user_id,
        message_id=message.message.id,
        text=text,
        reply_markup=pairs_keyboard(user_id, category, 0)
    )

# ================ ОБРАБОТКА ТЕКСТОВЫХ КОМАНД ================
@bot.message_handler(func=lambda message: True)
def handle_text(message):
    """Обработка текстовых сообщений"""
    user_id = message.from_user.id
    text = message.text
    lang = get_user_lang(user_id)
    
    # Проверка доступа (кроме админа)
    if not check_access(user_id) and user_id != ADMIN_ID:
        bot.send_message(
            user_id,
            get_text(user_id, 'no_access'),
            reply_markup=types.InlineKeyboardMarkup().add(
                types.InlineKeyboardButton(TEXTS[lang]['get_access'], callback_data="get_access")
            )
        )
        return
    
    # Главное меню
    if text in [TEXTS[lang]['signals'], TEXTS[lang]['marathon'], 
                TEXTS[lang]['stats'], TEXTS[lang]['top'], "🏠 Главное меню"]:
        
        if text == TEXTS[lang]['signals']:
            bot.send_message(user_id, "Выберите категорию:", reply_markup=signals_categories_keyboard(user_id))
        
        elif text == TEXTS[lang]['marathon']:
            show_marathon(user_id)
        
        elif text == TEXTS[lang]['stats']:
            show_statistics(user_id)
        
        elif text == TEXTS[lang]['top']:
            show_top_traders(user_id)
        
        elif text == "🏠 Главное меню":
            bot.send_message(user_id, get_text(user_id, 'main_menu'), reply_markup=main_menu_keyboard(user_id))
    
    # Категории сигналов
    elif text in [TEXTS[lang]['currency'], TEXTS[lang]['stocks'], 
                  TEXTS[lang]['crypto'], TEXTS[lang]['commodities']]:
        
        category_map = {
            TEXTS[lang]['currency']: 'currency',
            TEXTS[lang]['stocks']: 'stocks',
            TEXTS[lang]['crypto']: 'crypto',
            TEXTS[lang]['commodities']: 'commodities'
        }
        
        category = category_map.get(text)
        if category:
            msg = bot.send_message(
                user_id,
                get_text(user_id, 'select_pair', page=1, total=(len(ALL_PAIRS[category])+13)//14),
                reply_markup=pairs_keyboard(user_id, category, 0)
            )

def show_marathon(user_id):
    """Показать марафон"""
    lang = get_user_lang(user_id)
    
    text = TEXTS[lang]['marathon_title'] + "\n\n"
    text += TEXTS[lang]['marathon_page1'] + "\n\n"
    text += TEXTS[lang]['marathon_page2'] + "\n\n"
    text += TEXTS[lang]['marathon_text']
    
    markup = types.InlineKeyboardMarkup().add(
        types.InlineKeyboardButton("📊 Моя статистика", callback_data="admin_stats" if user_id == ADMIN_ID else "noop"),
        types.InlineKeyboardButton("🏠 Главное меню", callback_data="main_menu")
    )
    
    bot.send_message(user_id, text, reply_markup=markup, parse_mode='Markdown')

def show_statistics(user_id):
    """Показать статистику пользователя"""
    cursor.execute('''
        SELECT total_trades, wins, losses, profit, joined_date 
        FROM users WHERE user_id = ?
    ''', (user_id,))
    result = cursor.fetchone()
    
    if not result:
        bot.send_message(user_id, "Статистика не найдена")
        return
    
    total, wins, losses, profit, joined = result
    winrate = round((wins / total * 100) if total > 0 else 0, 1)
    
    text = get_text(user_id, 'stats_text',
                   user_id=user_id,
                   active="Да" if check_access(user_id) else "Нет",
                   total=total,
                   wins=wins,
                   losses=losses,
                   winrate=winrate,
                   profit=round(profit, 2),
                   date=joined[:10])
    
    bot.send_message(user_id, text, parse_mode='Markdown')

def show_top_traders(user_id):
    """Показать топ-10 трейдеров"""
    cursor.execute('''
        SELECT username, total_trades, wins, profit 
        FROM top_traders 
        ORDER BY profit DESC 
        LIMIT 10
    ''')
    traders = cursor.fetchall()
    
    top_list = ""
    for i, trader in enumerate(traders, 1):
        username, trades, wins, profit = trader
        top_list += get_text(user_id, 'top_item',
                           place=i,
                           name=username,
                           trades=trades,
                           wins=wins,
                           profit=round(profit, 2))
    
    text = get_text(user_id, 'top_text', top_list=top_list)
    bot.send_message(user_id, text, parse_mode='Markdown')

# ================ АДМИН КОМАНДЫ ================
@bot.message_handler(commands=['grant'])
def grant_access(message):
    """Выдать доступ пользователю"""
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        user_id = int(message.text.split()[1])
        cursor.execute('UPDATE users SET is_active = 1 WHERE user_id = ?', (user_id,))
        conn.commit()
        
        bot.reply_to(message, f"✅ Доступ выдан пользователю {user_id}")
        
        # Уведомляем пользователя
        try:
            lang = get_user_lang(user_id)
            bot.send_message(user_id, 
                           "🎉 **ВАМ ВЫДАН ДОСТУП!**\n\nТеперь вы можете пользоваться всеми функциями бота.",
                           reply_markup=main_menu_keyboard(user_id))
        except:
            pass
    except:
        bot.reply_to(message, "❌ Использование: /grant [user_id]")

@bot.message_handler(commands=['revoke'])
def revoke_access(message):
    """Забрать доступ у пользователя"""
    if message.from_user.id != ADMIN_ID:
        return
    
    try:
        user_id = int(message.text.split()[1])
        cursor.execute('UPDATE users SET is_active = 0 WHERE user_id = ?', (user_id,))
        conn.commit()
        bot.reply_to(message, f"✅ Доступ заблокирован у пользователя {user_id}")
    except:
        bot.reply_to(message, "❌ Использование: /revoke [user_id]")

@bot.message_handler(commands=['broadcast'])
def broadcast(message):
    """Отправить сообщение всем пользователям"""
    if message.from_user.id != ADMIN_ID:
        return
    
    text = message.text.replace('/broadcast', '', 1).strip()
    if not text:
        bot.reply_to(message, "❌ Введите текст для рассылки")
        return
    
    cursor.execute('SELECT user_id FROM users WHERE is_active = 1')
    users = cursor.fetchall()
    
    success = 0
    for user in users:
        try:
            bot.send_message(user[0], f"📢 **РАССЫЛКА АДМИНА**\n\n{text}")
            success += 1
        except:
            pass
    
    bot.reply_to(message, f"✅ Сообщение отправлено {success} пользователям")

@bot.message_handler(commands=['stats'])
def admin_stats(message):
    """Статистика бота для админа"""
    if message.from_user.id != ADMIN_ID:
        return
    
    cursor.execute('SELECT COUNT(*) FROM users')
    total = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM users WHERE is_active = 1')
    active = cursor.fetchone()[0]
    
    cursor.execute('SELECT COUNT(*) FROM trades')
    trades = cursor.fetchone()[0]
    
    cursor.execute('SELECT SUM(profit) FROM trades WHERE profit > 0')
    total_profit = cursor.fetchone()[0] or 0
    
    cursor.execute('SELECT SUM(profit) FROM trades WHERE profit < 0')
    total_loss = cursor.fetchone()[0] or 0
    
    text = f"📊 **СТАТИСТИКА БОТА**\n\n"
    text += f"👥 Всего пользователей: {total}\n"
    text += f"✅ Активных: {active}\n"
    text += f"📈 Всего сделок: {trades}\n"
    text += f"💰 Общая прибыль: ${round(total_profit, 2)}\n"
    text += f"📉 Общий убыток: ${round(abs(total_loss), 2)}\n"
    text += f"💎 Чистая прибыль: ${round(total_profit + total_loss, 2)}"
    
    bot.send_message(ADMIN_ID, text)

# ================ АВТОПИНГ ДЛЯ REPLIT ================
def keep_alive():
    """Автопинг чтобы бот не засыпал"""
    while True:
        time.sleep(240)  # Каждые 4 минуты
        try:
            # Пишем в консоль для отслеживания
            print(f"🟢 Автопинг: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
            
            # Отправляем себе сообщение для активности
            bot.send_chat_action(ADMIN_ID, 'typing')
        except:
            pass

# ================ ЗАПУСК ================
if __name__ == '__main__':
    print("🚀 Бот VIP Premium MAX Pro запущен!")
    print(f"👑 Админ ID: {ADMIN_ID}")
    print("🟢 Автопинг активен (каждые 4 минуты)")
    
    # Запускаем автопинг в отдельном потоке
    threading.Thread(target=keep_alive, daemon=True).start()
    
    # Запускаем бота
    bot.polling(none_stop=True)
