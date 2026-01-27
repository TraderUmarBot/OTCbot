FROM python:3.11-slim

WORKDIR /app

# Устанавливаем системные зависимости для TA-Lib
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    wget \
    tar \
    make \
    && rm -rf /var/lib/apt/lists/*

# СКАЧИВАЕМ И УСТАНАВЛИВАЕМ TA-Lib ВРУЧНУЮ
RUN wget http://prdownloads.sourceforge.net/ta-lib/ta-lib-0.4.0-src.tar.gz && \
    tar -xzf ta-lib-0.4.0-src.tar.gz && \
    cd ta-lib && \
    ./configure --prefix=/usr && \
    make && \
    make install && \
    cd .. && \
    rm -rf ta-lib ta-lib-0.4.0-src.tar.gz

# Копируем и устанавливаем зависимости
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем код
COPY . .

# Создаем папку для данных
RUN mkdir -p data

# Запускаем бота
CMD ["python", "bot.py"]
