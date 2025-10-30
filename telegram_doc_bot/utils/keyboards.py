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
            [KeyboardButton(text="📝 Создать документ"), KeyboardButton(text="📚 История")],
            [KeyboardButton(text="🔑 Мой API ключ"), KeyboardButton(text="⭐ Избранное")],
            [KeyboardButton(text="📊 Статистика"), KeyboardButton(text="⚙️ Настройки")],
            [KeyboardButton(text="❓ Помощь"), KeyboardButton(text="ℹ️ О боте")]
        ],
        resize_keyboard=True,
        input_field_placeholder="Выберите действие из меню..."
    )
    return keyboard


def get_template_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для выбора шаблона документа
    
    Returns:
        Inline клавиатура с шаблонами
    """
    buttons = []
    row = []
    for i, (key, value) in enumerate(Config.DOCUMENT_TEMPLATES.items()):
        row.append(InlineKeyboardButton(
            text=value,
            callback_data=f"template_{key}"
        ))
        if len(row) == 2 or i == len(Config.DOCUMENT_TEMPLATES) - 1:
            buttons.append(row)
            row = []
    
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
        [
            InlineKeyboardButton(
                text="✏️ Редактировать",
                callback_data="action_edit"
            ),
            InlineKeyboardButton(
                text="👁️ Предпросмотр",
                callback_data="action_preview"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ В избранное",
                callback_data="action_favorite"
            ),
            InlineKeyboardButton(
                text="🔄 Другой формат",
                callback_data="action_convert"
            )
        ],
        [
            InlineKeyboardButton(
                text="📝 Создать новый",
                callback_data="action_new"
            ),
            InlineKeyboardButton(
                text="✅ Завершить",
                callback_data="action_finish"
            )
        ]
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


def get_language_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для выбора языка документа
    
    Returns:
        Inline клавиатура с языками
    """
    buttons = []
    row = []
    for i, (key, value) in enumerate(Config.DOCUMENT_LANGUAGES.items()):
        row.append(InlineKeyboardButton(
            text=value,
            callback_data=f"lang_{key}"
        ))
        if len(row) == 2 or i == len(Config.DOCUMENT_LANGUAGES) - 1:
            buttons.append(row)
            row = []
    
    buttons.append([InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="settings_back"
    )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_style_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для выбора стиля документа
    
    Returns:
        Inline клавиатура со стилями
    """
    buttons = []
    for key, value in Config.DOCUMENT_STYLES.items():
        buttons.append([InlineKeyboardButton(
            text=value,
            callback_data=f"style_{key}"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="⬅️ Назад",
        callback_data="settings_back"
    )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_settings_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры настроек
    
    Returns:
        Inline клавиатура с настройками
    """
    buttons = [
        [InlineKeyboardButton(
            text="🌍 Язык документа",
            callback_data="settings_language"
        )],
        [InlineKeyboardButton(
            text="🎨 Стиль документа",
            callback_data="settings_style"
        )],
        [InlineKeyboardButton(
            text="🔔 Уведомления",
            callback_data="settings_notifications"
        )],
        [InlineKeyboardButton(
            text="🗑️ Очистить историю",
            callback_data="settings_clear_history"
        )]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_history_item_keyboard(doc_id: int) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для элемента истории
    
    Args:
        doc_id: ID документа
    
    Returns:
        Inline клавиатура с действиями для документа из истории
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="📥 Скачать снова",
                callback_data=f"history_download_{doc_id}"
            ),
            InlineKeyboardButton(
                text="✏️ Редактировать",
                callback_data=f"history_edit_{doc_id}"
            )
        ],
        [
            InlineKeyboardButton(
                text="⭐ В избранное",
                callback_data=f"history_favorite_{doc_id}"
            ),
            InlineKeyboardButton(
                text="🗑️ Удалить",
                callback_data=f"history_delete_{doc_id}"
            )
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_variants_keyboard(count: int = 3) -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для выбора варианта документа
    
    Args:
        count: Количество вариантов
    
    Returns:
        Inline клавиатура с вариантами
    """
    buttons = []
    for i in range(count):
        buttons.append([InlineKeyboardButton(
            text=f"📄 Вариант {i + 1}",
            callback_data=f"variant_{i}"
        )])
    
    buttons.append([InlineKeyboardButton(
        text="🔄 Сгенерировать ещё",
        callback_data="variant_regenerate"
    )])
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard


def get_preview_keyboard() -> InlineKeyboardMarkup:
    """
    Создание клавиатуры для предпросмотра документа
    
    Returns:
        Inline клавиатура с действиями предпросмотра
    """
    buttons = [
        [
            InlineKeyboardButton(
                text="✅ Сохранить",
                callback_data="preview_save"
            ),
            InlineKeyboardButton(
                text="✏️ Редактировать",
                callback_data="preview_edit"
            )
        ],
        [
            InlineKeyboardButton(
                text="🔄 Сгенерировать заново",
                callback_data="preview_regenerate"
            )
        ],
        [
            InlineKeyboardButton(
                text="❌ Отмена",
                callback_data="preview_cancel"
            )
        ]
    ]
    
    keyboard = InlineKeyboardMarkup(inline_keyboard=buttons)
    return keyboard
