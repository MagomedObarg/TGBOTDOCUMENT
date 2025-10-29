"""
Модуль конфигурации бота.
Загружает переменные окружения и настройки приложения.
"""

import os
from dotenv import load_dotenv

# Загрузка переменных окружения из .env файла
load_dotenv()


class Config:
    """Класс для хранения конфигурации приложения"""
    
    # Токен Telegram бота
    TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
    
    # API ключ Google Gemini
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY')
    
    # Директория для временных файлов
    TEMP_DIR = 'generated_docs'
    
    # Максимальная длина запроса пользователя
    MAX_REQUEST_LENGTH = 1000
    
    # Шаблоны документов
    DOCUMENT_TEMPLATES = {
        'contract': 'Договор',
        'statement': 'Заявление',
        'resume': 'Резюме',
        'letter': 'Деловое письмо',
        'report': 'Отчёт',
        'custom': 'Произвольный документ'
    }
    
    # Типы документов
    DOCUMENT_TYPES = {
        'docx': 'Word документ (.docx)',
        'pdf': 'PDF документ (.pdf)'
    }
    
    @staticmethod
    def validate():
        """Проверка наличия обязательных переменных окружения"""
        if not Config.TELEGRAM_BOT_TOKEN:
            raise ValueError("TELEGRAM_BOT_TOKEN не установлен в .env файле")
        if not Config.GEMINI_API_KEY:
            raise ValueError("GEMINI_API_KEY не установлен в .env файле")


# Создание директории для временных файлов
os.makedirs(Config.TEMP_DIR, exist_ok=True)
