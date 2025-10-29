# 🚀 Быстрый старт

Следуйте этим шагам для быстрого запуска бота.

## ⚡ 5 минут до запуска

### Шаг 1: Клонирование и установка

```bash
# Клонируйте репозиторий
git clone <repository-url>
cd telegram_doc_bot

# Используйте скрипт быстрого запуска
chmod +x start.sh
./start.sh
```

### Шаг 2: Получите API ключи

**Telegram Bot Token:**
1. Откройте https://t.me/BotFather
2. Отправьте `/newbot`
3. Придумайте имя и username
4. Скопируйте токен

**Google Gemini API:**
1. Откройте https://makersuite.google.com/app/apikey
2. Войдите через Google
3. Нажмите "Create API Key"
4. Скопируйте ключ

### Шаг 3: Настройте .env файл

```bash
# Скопируйте пример
cp .env.example .env

# Отредактируйте файл
nano .env  # или используйте другой редактор
```

Вставьте ваши ключи:
```env
TELEGRAM_BOT_TOKEN=1234567890:ABCdefGHIjklMNOpqrsTUVwxyz
GEMINI_API_KEY=AIza...ваш_ключ
```

### Шаг 4: Запустите бота

```bash
# Через скрипт
./start.sh

# Или вручную
source venv/bin/activate
python -m telegram_doc_bot.bot
```

### Шаг 5: Тестируйте!

1. Откройте Telegram
2. Найдите вашего бота по username
3. Отправьте `/start`
4. Нажмите "📝 Создать документ"
5. Следуйте инструкциям

## 🐳 Запуск с Docker (альтернатива)

```bash
# Создайте .env файл с ключами
cp .env.example .env
nano .env

# Запустите с Docker Compose
docker-compose up -d

# Проверьте логи
docker-compose logs -f
```

## 🎯 Первый документ

После запуска бота:

1. **Отправьте** `/start` боту
2. **Нажмите** "📝 Создать документ"
3. **Выберите** "Резюме"
4. **Напишите**:
   ```
   Составь резюме на позицию Python разработчика.
   ФИО: Иванов Иван Иванович, 30 лет
   Опыт: 5 лет Python, Django, PostgreSQL
   Образование: МГУ, факультет ВМК
   ```
5. **Выберите** формат Word или PDF
6. **Получите** готовый документ!

## ⚙️ Используя Makefile

Если установлен `make`:

```bash
# Первоначальная настройка
make setup

# Запуск бота
make run

# Все доступные команды
make help
```

## 📱 Настройка команд бота в Telegram

Для удобства пользователей настройте меню команд через @BotFather:

1. Откройте @BotFather
2. Отправьте `/setcommands`
3. Выберите вашего бота
4. Вставьте:
   ```
   start - 🚀 Запустить бота
   generate - 📝 Создать документ
   help - ❓ Помощь
   cancel - ❌ Отмена
   ```

## 🔍 Проверка работы

Если что-то не работает:

```bash
# Проверьте логи
tail -f bot.log

# Проверьте .env
cat .env

# Проверьте зависимости
pip list | grep -E "aiogram|google-generativeai|python-docx|reportlab"

# Проверьте соединение
python -c "import google.generativeai as genai; print('OK')"
```

## 🆘 Помощь

Если возникли проблемы:

1. Проверьте [FAQ.md](FAQ.md)
2. Посмотрите [README.md](README.md) для подробностей
3. Создайте Issue на GitHub

## 🎉 Готово!

Теперь у вас работает бот для генерации документов!

### Что дальше?

- 📚 Изучите [EXAMPLES.md](EXAMPLES.md) для примеров запросов
- ⚙️ Настройте параметры в `telegram_doc_bot/config.py`
- 🚀 Разверните на сервере (см. README.md)
- 🤝 Внесите улучшения (см. CONTRIBUTING.md)

---

**Время запуска: ~5 минут** ⏱️

**Сложность: 🟢 Легко**
