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
            [KeyboardButton(text="🔑 Мой API ключ")],
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


def get_api_key_management_keyboard(has_key: bool = False) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для управления API ключом
    
    Args:
        has_key: Есть ли у пользователя сохранённый ключ
    
    Returns:
        Inline клавиатура с действиями для управления API ключом
    """
    buttons = []
    
    if has_key:
        buttons.append([InlineKeyboardButton(
            text="🔄 Обновить API ключ",
            callback_data="apikey_update"
        )])
        buttons.append([InlineKeyboardButton(
            text="🗑 Удалить API ключ",
            callback_data="apikey_delete"
        )])
    else:
        buttons.append([InlineKeyboardButton(
            text="➕ Добавить API ключ",
            callback_data="apikey_add"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="ℹ️ Где получить ключ?",
        callback_data="apikey_help"
    )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_api_key_confirm_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для подтверждения удаления API ключа
    
    Returns:
        Inline клавиатура с кнопками подтверждения
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Да, удалить",
                callback_data="apikey_delete_confirm"
            ),
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="apikey_delete_cancel"
            )
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
