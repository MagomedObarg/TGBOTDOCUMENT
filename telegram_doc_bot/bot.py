"""
Главный файл Telegram бота для генерации документов.
Инициализирует бота, подключает обработчики и запускает polling.
"""

import asyncio
import logging
import sys
from aiogram import Bot, Dispatcher
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

from telegram_doc_bot.config import Config
from telegram_doc_bot.services import GeminiService, DocumentService
from telegram_doc_bot.handlers import basic_handlers, document_handlers

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler('bot.log', encoding='utf-8')
    ]
)

logger = logging.getLogger(__name__)


async def main():
    """Главная функция для запуска бота"""
    
    try:
        # Валидация конфигурации
        Config.validate()
        logger.info("Конфигурация проверена успешно")
        
        # Инициализация бота
        bot = Bot(
            token=Config.TELEGRAM_BOT_TOKEN,
            default=DefaultBotProperties(parse_mode=ParseMode.HTML)
        )
        
        # Создание диспетчера
        dp = Dispatcher()
        
        # Инициализация сервисов
        gemini_service = GeminiService(api_key=Config.GEMINI_API_KEY)
        document_service = DocumentService(output_dir=Config.TEMP_DIR)
        
        logger.info("Сервисы инициализированы")
        
        # Регистрация обработчиков
        dp.include_router(basic_handlers.router)
        dp.include_router(document_handlers.router)
        
        logger.info("Обработчики зарегистрированы")
        
        # Получение информации о боте
        bot_info = await bot.get_me()
        logger.info(f"Бот запущен: @{bot_info.username}")
        logger.info(f"ID бота: {bot_info.id}")
        
        # Запуск polling
        logger.info("Начало polling...")
        await dp.start_polling(
            bot,
            gemini_service=gemini_service,
            document_service=document_service,
            allowed_updates=dp.resolve_used_update_types()
        )
        
    except ValueError as e:
        logger.error(f"Ошибка конфигурации: {e}")
        logger.error("Проверьте файл .env и убедитесь, что все необходимые переменные установлены")
        sys.exit(1)
        
    except Exception as e:
        logger.error(f"Критическая ошибка при запуске бота: {e}", exc_info=True)
        sys.exit(1)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Бот остановлен пользователем")
    except Exception as e:
        logger.error(f"Неожиданная ошибка: {e}", exc_info=True)
        sys.exit(1)
