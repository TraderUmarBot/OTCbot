#!/bin/bash
# Установка TA-Lib для KURUT AI INFINITY бота

echo "📦 Установка TA-Lib для торгового бота..."
echo "=========================================="

# Обновляем пакеты
echo "🔄 Обновление списка пакетов..."
apt-get update -y

# Устанавливаем зависимости
echo "🔧 Установка зависимостей..."
apt-get install -y \
    build-essential \
    wget \
    tar \
    gcc \
    g++ \
    make \
    python3-dev \
    python3-pip

# Скачиваем TA-Lib
echo "📥 Скачивание TA-Lib..."
cd /tmp
wget -q http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz

# Распаковываем
echo "📦 Распаковка TA-Lib..."
tar -xzf ta-lib-0.4.0-src.tar.gz
cd ta-lib/

# Конфигурируем и устанавливаем
echo "⚙️ Конфигурация TA-Lib..."
./configure --prefix=/usr
echo "🔨 Компиляция TA-Lib..."
make
echo "📦 Установка TA-Lib..."
make install

# Очищаем временные файлы
echo "🧹 Очистка временных файлов..."
cd ..
rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Устанавливаем Python пакет TA-Lib
echo "🐍 Установка Python пакета TA-Lib..."
pip3 install TA-Lib

# Проверяем установку
echo "✅ Проверка установки..."
python3 -c "import talib; print(f'✅ TA-Lib установлен версии: {talib.__version__}')"

echo "=========================================="
echo "🎉 TA-Lib успешно установлен!"
echo "Теперь можно запустить бота командой:"
echo "python bot.py"
