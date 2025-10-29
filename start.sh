#!/bin/bash

# Скрипт для запуска Telegram бота

echo "🤖 Запуск Telegram бота для генерации документов..."

# Проверка наличия виртуального окружения
if [ ! -d "venv" ]; then
    echo "📦 Создание виртуального окружения..."
    python3 -m venv venv
fi

# Активация виртуального окружения
echo "🔧 Активация виртуального окружения..."
source venv/bin/activate

# Установка/обновление зависимостей
echo "📥 Установка зависимостей..."
pip install -r requirements.txt --quiet

# Проверка наличия .env файла
if [ ! -f ".env" ]; then
    echo "⚠️  Файл .env не найден!"
    echo "📋 Создаю .env из примера..."
    cp .env.example .env
    echo ""
    echo "❗ ВАЖНО: Отредактируйте файл .env и добавьте ваши API ключи!"
    echo "   - TELEGRAM_BOT_TOKEN (получите у @BotFather)"
    echo "   - GEMINI_API_KEY (получите на https://makersuite.google.com/app/apikey)"
    echo ""
    exit 1
fi

# Создание необходимых директорий
mkdir -p generated_docs logs

echo "✅ Все готово!"
echo "🚀 Запуск бота..."
echo ""

# Запуск бота
python -m telegram_doc_bot.bot
