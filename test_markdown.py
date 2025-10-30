#!/usr/bin/env python3
"""
Тестовый скрипт для проверки форматирования Markdown в документах Word
"""

import asyncio
import sys
import os

# Добавляем путь к модулям
sys.path.insert(0, '/home/engine/project')

from telegram_doc_bot.services.document_service import DocumentService


async def test_markdown_formatting():
    """Тестирование форматирования markdown в Word документе"""
    
    # Создаем тестовый контент с различной markdown разметкой
    test_content = """
## Введение

Это **вводная часть** документа с *курсивным текстом* и обычным текстом.

## Основные разделы

### Раздел 1: Списки

Вот маркированный список:

* Первый пункт списка
* Второй пункт с **жирным текстом**
* Третий пункт с *курсивом*

А вот нумерованный список:

1. Первый пункт
2. Второй пункт
3. Третий пункт

### Раздел 2: Форматирование текста

Этот параграф содержит **жирный текст**, *курсив*, и `код`.

Можно комбинировать: **жирный текст с *курсивом* внутри**.

## Заключение

Это заключительная часть документа.
"""
    
    # Создаем сервис
    doc_service = DocumentService(output_dir='test_output')
    
    print("Создание тестового Word документа...")
    filepath = await doc_service.create_word_document(
        content=test_content,
        title="Тестовый документ с Markdown",
        user_id=12345
    )
    
    if filepath:
        print(f"✅ Документ успешно создан: {filepath}")
        print(f"Размер файла: {os.path.getsize(filepath)} байт")
        return True
    else:
        print("❌ Ошибка при создании документа")
        return False


if __name__ == "__main__":
    success = asyncio.run(test_markdown_formatting())
    sys.exit(0 if success else 1)
