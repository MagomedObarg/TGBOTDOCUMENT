"""
Модуль для создания клавиатур Telegram бота
"""

from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardMarkup,
    InlineKeyboardButton
)
from telegram_doc_bot.config import Config


def get_main_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание главной клавиатуры бота
    
    Returns:
        Клавиатура с основными командами
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📝 Создать документ")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие..."
    )
    return keyboard


def get_template_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для выбора шаблона документа
    
    Returns:
        Inline клавиатура с шаблонами
    """
    buttons = []
    for key, value in Config.DOCUMENT_TEMPLATES.items():
        buttons.append([InlineKeyboardButton(
            text=value,
            callback_data=f"template_{key}"
        )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_document_type_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для выбора типа документа (Word/PDF)
    
    Returns:
        Inline клавиатура с типами документов
    """
    buttons = []
    for key, value in Config.DOCUMENT_TYPES.items():
        buttons.append([InlineKeyboardButton(
            text=value,
            callback_data=f"doctype_{key}"
        )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_cancel_keyboard() -> ReplyKeyboardMarkup:
    """
    Создание клавиатуры с кнопкой отмены
    
    Returns:
        Клавиатура с кнопкой "Отмена"
    """
    keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Отмена")]
        ],
        resize_keyboard=True
    )
    return keyboard


def get_document_actions_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры с действиями для документа после генерации
    
    Returns:
        Inline клавиатура с действиями (редактировать, создать новый, завершить)
    """
    buttons = [
        [InlineKeyboardButton(
            text="✏️ Редактировать документ",
            callback_data="action_edit"
        )],
        [InlineKeyboardButton(
            text="📝 Создать новый документ",
            callback_data="action_new"
        )],
        [InlineKeyboardButton(
            text="✅ Завершить",
            callback_data="action_finish"
        )]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
