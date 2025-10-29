# 🤝 Руководство по внесению вклада

Спасибо за интерес к улучшению проекта! Мы приветствуем любой вклад: от исправления опечаток до добавления новых функций.

## 📋 Содержание

- [Кодекс поведения](#кодекс-поведения)
- [Как помочь проекту](#как-помочь-проекту)
- [Процесс разработки](#процесс-разработки)
- [Стандарты кода](#стандарты-кода)
- [Коммиты](#коммиты)
- [Pull Requests](#pull-requests)
- [Тестирование](#тестирование)

## 🤝 Кодекс поведения

Участвуя в проекте, вы обязуетесь:

- ✅ Быть уважительным к другим участникам
- ✅ Конструктивно реагировать на критику
- ✅ Фокусироваться на том, что лучше для проекта
- ❌ Не использовать оскорбительные выражения
- ❌ Не публиковать личную информацию других людей

## 💡 Как помочь проекту

### Сообщения об ошибках

Если вы нашли баг:

1. Проверьте, не создан ли уже Issue по этой проблеме
2. Создайте новый Issue с подробным описанием:
   - Шаги для воспроизведения
   - Ожидаемое поведение
   - Фактическое поведение
   - Версия Python, ОС
   - Логи ошибок

### Предложения улучшений

Есть идея для новой функции?

1. Откройте Issue с меткой "enhancement"
2. Опишите:
   - Зачем нужна эта функция
   - Как она должна работать
   - Примеры использования

### Документация

- Исправление опечаток
- Улучшение примеров
- Перевод на другие языки
- Дополнение FAQ

## 🔧 Процесс разработки

### 1. Fork репозитория

```bash
# Нажмите кнопку "Fork" на GitHub
# Затем клонируйте свой fork
git clone https://github.com/YOUR_USERNAME/telegram_doc_bot.git
cd telegram_doc_bot
```

### 2. Создайте ветку

```bash
# Для новой функции
git checkout -b feature/amazing-feature

# Для исправления бага
git checkout -b fix/bug-description

# Для документации
git checkout -b docs/improvement
```

### 3. Настройте окружение

```bash
# Создайте виртуальное окружение
python3 -m venv venv
source venv/bin/activate

# Установите зависимости
pip install -r requirements.txt

# Установите dev зависимости
pip install black flake8 mypy pytest
```

### 4. Внесите изменения

Следуйте [стандартам кода](#стандарты-кода)

### 5. Протестируйте

```bash
# Запустите бота локально
python -m telegram_doc_bot.bot

# Проверьте форматирование
black telegram_doc_bot/

# Проверьте линтером
flake8 telegram_doc_bot/

# Проверьте типы
mypy telegram_doc_bot/
```

### 6. Зафиксируйте изменения

```bash
git add .
git commit -m "feat: add amazing feature"
```

См. [Коммиты](#коммиты) для форматирования сообщений

### 7. Отправьте изменения

```bash
git push origin feature/amazing-feature
```

### 8. Создайте Pull Request

Перейдите на GitHub и создайте Pull Request из вашей ветки в main

## 📝 Стандарты кода

### Стиль кода

- **PEP 8** - следуйте стандарту Python
- **Black** - используйте для форматирования (line length 100)
- **Type hints** - добавляйте аннотации типов
- **Docstrings** - документируйте функции и классы

### Пример хорошего кода

```python
from typing import Optional


async def create_document(
    content: str,
    title: str = "Документ",
    format: str = "docx"
) -> Optional[str]:
    """
    Создание документа в указанном формате.
    
    Args:
        content: Текстовое содержимое документа
        title: Заголовок документа
        format: Формат файла ('docx' или 'pdf')
    
    Returns:
        Путь к созданному файлу или None в случае ошибки
    """
    try:
        # Ваш код здесь
        logger.info(f"Создание документа {title} в формате {format}")
        return filepath
    except Exception as e:
        logger.error(f"Ошибка создания документа: {e}")
        return None
```

### Комментарии

- Комментарии на **русском языке**
- Объясняйте "почему", а не "что"
- Избегайте очевидных комментариев

```python
# ✅ Хорошо
# Используем кеш для предотвращения повторных запросов к API
cache = {}

# ❌ Плохо
# Создаём словарь
cache = {}
```

### Именование

```python
# Переменные и функции: snake_case
user_request = "..."
def generate_document():
    pass

# Классы: PascalCase
class DocumentService:
    pass

# Константы: UPPER_CASE
MAX_REQUEST_LENGTH = 1000

# Private методы: _leading_underscore
def _internal_method():
    pass
```

### Импорты

```python
# Стандартная библиотека
import os
import logging
from typing import Optional

# Сторонние библиотеки
from aiogram import Router
from aiogram.types import Message

# Локальные модули
from telegram_doc_bot.config import Config
from telegram_doc_bot.services import GeminiService
```

## 💬 Коммиты

Используйте [Conventional Commits](https://www.conventionalcommits.org/):

### Формат

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Типы

- `feat`: Новая функция
- `fix`: Исправление бага
- `docs`: Изменения в документации
- `style`: Форматирование кода (не влияет на логику)
- `refactor`: Рефакторинг кода
- `test`: Добавление тестов
- `chore`: Рутинные задачи (обновление зависимостей и т.д.)

### Примеры

```bash
# Новая функция
git commit -m "feat(handlers): add Excel export support"

# Исправление бага
git commit -m "fix(gemini): handle API timeout errors"

# Документация
git commit -m "docs(readme): add installation instructions"

# Рефакторинг
git commit -m "refactor(services): simplify document creation logic"
```

## 🔀 Pull Requests

### Требования

- ✅ Описание изменений
- ✅ Ссылка на Issue (если есть)
- ✅ Тесты пройдены
- ✅ Код отформатирован (black, flake8)
- ✅ Нет конфликтов с main веткой
- ✅ Коммиты следуют стандарту

### Шаблон PR

```markdown
## Описание
Краткое описание изменений

## Тип изменений
- [ ] Исправление бага
- [ ] Новая функция
- [ ] Критическое изменение (breaking change)
- [ ] Документация

## Связанные Issue
Closes #123

## Чеклист
- [ ] Код следует стилю проекта
- [ ] Код прокомментирован
- [ ] Обновлена документация
- [ ] Нет новых warnings
- [ ] Протестировано локально
```

### Процесс ревью

1. Maintainer рассмотрит ваш PR
2. Возможны запросы на изменения
3. После одобрения PR будет смержен
4. Ваш вклад появится в CHANGELOG

## 🧪 Тестирование

### Ручное тестирование

Обязательно протестируйте:

1. **Базовые команды**
   - `/start`
   - `/help`
   - `/generate`
   - `/cancel`

2. **Создание документов**
   - Все типы шаблонов
   - Оба формата (Word и PDF)
   - Различные длины запросов

3. **Обработка ошибок**
   - Неверные данные
   - Отмена операции
   - Длинные запросы

### Автоматические тесты (планируется)

```python
# tests/test_services.py
import pytest
from telegram_doc_bot.services import DocumentService

@pytest.mark.asyncio
async def test_create_word_document():
    service = DocumentService()
    filepath = await service.create_word_document(
        content="Тестовый контент",
        title="Тест"
    )
    assert filepath is not None
    assert filepath.endswith('.docx')
```

## 📚 Дополнительные ресурсы

- [Aiogram документация](https://docs.aiogram.dev/)
- [Google Gemini API](https://ai.google.dev/tutorials/python_quickstart)
- [PEP 8 Style Guide](https://peps.python.org/pep-0008/)
- [Conventional Commits](https://www.conventionalcommits.org/)

## ❓ Вопросы?

Если у вас есть вопросы:

1. Проверьте [FAQ](FAQ.md)
2. Создайте Issue с меткой "question"
3. Напишите в Discussions

---

**Спасибо за ваш вклад! 🎉**
