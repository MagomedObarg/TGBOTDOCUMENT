"""
Обработчики базовых команд бота (/start, /help)
"""

import logging
from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from telegram_doc_bot.utils.keyboards import get_main_keyboard
from telegram_doc_bot.config import Config

logger = logging.getLogger(__name__)

# Создание роутера для базовых команд
router = Router()


@router.message(Command("start"))
async def cmd_start(message: Message, state: FSMContext):
    """
    Обработчик команды /start
    
    Args:
        message: Сообщение пользователя
        state: Состояние FSM
    """
    # Очистка состояния при старте
    await state.clear()
    
    user_name = message.from_user.first_name or "Пользователь"
    
    welcome_text = (
        f"👋 Привет, {user_name}!\n\n"
        f"Я бот для автоматической генерации документов с помощью нейросети Google Gemini.\n\n"
        f"🚀 Что я умею:\n"
        f"• Создавать различные типы документов (договоры, заявления, резюме и др.)\n"
        f"• Генерировать контент с помощью ИИ\n"
        f"• Сохранять документы в форматах Word и PDF\n"
        f"• ✏️ Редактировать созданные документы по вашим инструкциям\n\n"
        f"📝 Чтобы создать документ, нажмите кнопку \"Создать документ\" или используйте команду /generate\n\n"
        f"❓ Для получения справки используйте команду /help"
    )
    
    await message.answer(
        welcome_text,
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"Пользователь {message.from_user.id} ({user_name}) запустил бота")


@router.message(Command("help"))
@router.message(F.text == "❓ Помощь")
async def cmd_help(message: Message):
    """
    Обработчик команды /help и кнопки "Помощь"
    
    Args:
        message: Сообщение пользователя
    """
    help_text = (
        "📖 <b>Руководство по использованию бота</b>\n\n"
        
        "<b>Основные команды:</b>\n"
        "/start - Запустить бота\n"
        "/help - Показать эту справку\n"
        "/generate - Начать создание документа\n"
        "/cancel - Отменить текущую операцию\n\n"
        
        "<b>Как создать документ:</b>\n"
        "1️⃣ Нажмите кнопку \"📝 Создать документ\" или введите /generate\n"
        "2️⃣ Выберите тип шаблона документа\n"
        "3️⃣ Опишите, какой документ вам нужен\n"
        "4️⃣ Выберите формат (Word или PDF)\n"
        "5️⃣ Дождитесь генерации и получите готовый документ\n"
        "6️⃣ При необходимости нажмите \"✏️ Редактировать\" и опишите изменения\n\n"
        
        "<b>Типы документов:</b>\n"
        "📄 Договор - юридический договор\n"
        "📋 Заявление - официальное заявление\n"
        "👔 Резюме - профессиональное резюме\n"
        "✉️ Деловое письмо - официальная переписка\n"
        "📊 Отчёт - структурированный отчёт\n"
        "📝 Произвольный - любой другой документ\n\n"
        
        "<b>Редактирование документов:</b>\n"
        "• Нажмите кнопку \"✏️ Редактировать документ\" после получения файла\n"
        "• Опишите, какие изменения нужно внести\n"
        "• Можно редактировать документ несколько раз подряд\n\n"
        
        "<b>Советы:</b>\n"
        "• Описывайте запрос максимально подробно\n"
        "• Указывайте все важные детали и требования\n"
        f"• Максимальная длина запроса: {Config.MAX_REQUEST_LENGTH} символов\n"
        "• Генерация может занять 10-30 секунд\n\n"
        
        "❓ Если возникли вопросы, свяжитесь с поддержкой"
    )
    
    await message.answer(
        help_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )


@router.message(F.text == "ℹ️ О боте")
async def cmd_about(message: Message):
    """
    Обработчик кнопки "О боте"
    
    Args:
        message: Сообщение пользователя
    """
    about_text = (
        "🤖 <b>О боте</b>\n\n"
        "Бот для автоматической генерации документов использует современные технологии:\n\n"
        "🔹 <b>Google Gemini AI</b> - для генерации и редактирования контента\n"
        "🔹 <b>Python-docx</b> - для создания Word документов\n"
        "🔹 <b>ReportLab</b> - для создания PDF документов\n"
        "🔹 <b>Aiogram 3.x</b> - для работы с Telegram API\n\n"
        "⚡ Быстрая генерация документов\n"
        "✏️ Интеллектуальное редактирование\n"
        "🎯 Высокое качество контента\n"
        "🔒 Безопасность данных\n\n"
        "Версия: 1.0.0\n"
        "Разработано с ❤️ для автоматизации работы с документами"
    )
    
    await message.answer(
        about_text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
