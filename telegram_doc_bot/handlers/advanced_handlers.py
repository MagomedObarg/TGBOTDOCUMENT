"""
Обработчики расширенных функций бота: история, избранное, статистика, настройки
"""

import logging
from datetime import datetime
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext

from telegram_doc_bot.utils.keyboards import (
    get_main_keyboard,
    get_settings_keyboard,
    get_language_keyboard,
    get_style_keyboard,
    get_history_item_keyboard
)
from telegram_doc_bot.utils.user_storage import UserStorage
from telegram_doc_bot.utils.message_helpers import safe_edit_message
from telegram_doc_bot.config import Config

logger = logging.getLogger(__name__)

router = Router()


@router.message(F.text == "📚 История")
async def show_history(message: Message, user_storage: UserStorage):
    """Показать историю созданных документов"""
    user_id = message.from_user.id
    history = user_storage.get_history(user_id)
    
    if not history:
        await message.answer(
            "📚 <b>История документов</b>\n\n"
            "У вас пока нет созданных документов.\n\n"
            "Нажмите \"📝 Создать документ\", чтобы начать!",
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )
        return
    
    text = "📚 <b>История ваших документов</b>\n\n"
    for i, doc in enumerate(history[-10:], 1):
        date = doc.get('date', 'Неизвестно')
        template = doc.get('template_name', 'Документ')
        doc_type = doc.get('doc_type', 'docx')
        
        text += f"{i}. <b>{template}</b>\n"
        text += f"   📅 {date}\n"
        text += f"   📄 Формат: {doc_type.upper()}\n\n"
    
    text += f"📊 Всего документов: {len(history)}"
    
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"Пользователь {user_id} просмотрел историю ({len(history)} документов)")


@router.message(F.text == "⭐ Избранное")
async def show_favorites(message: Message, user_storage: UserStorage):
    """Показать избранные документы"""
    user_id = message.from_user.id
    favorites = user_storage.get_favorites(user_id)
    
    if not favorites:
        await message.answer(
            "⭐ <b>Избранные документы</b>\n\n"
            "У вас пока нет избранных документов.\n\n"
            "После создания документа нажмите \"⭐ В избранное\", "
            "чтобы сохранить его в этом разделе.",
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )
        return
    
    text = "⭐ <b>Ваши избранные документы</b>\n\n"
    for i, doc in enumerate(favorites, 1):
        template = doc.get('template_name', 'Документ')
        date = doc.get('date', 'Неизвестно')
        
        text += f"{i}. <b>{template}</b>\n"
        text += f"   📅 {date}\n\n"
    
    text += "💡 Нажмите на документ, чтобы скачать его снова"
    
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"Пользователь {user_id} просмотрел избранное ({len(favorites)} документов)")


@router.message(F.text == "📊 Статистика")
async def show_statistics(message: Message, user_storage: UserStorage):
    """Показать статистику использования"""
    user_id = message.from_user.id
    stats = user_storage.get_statistics(user_id)
    
    total_docs = stats.get('total_documents', 0)
    total_edits = stats.get('total_edits', 0)
    favorite_template = stats.get('favorite_template', 'Нет данных')
    total_words = stats.get('total_words', 0)
    last_used = stats.get('last_used', 'Никогда')
    
    text = (
        "📊 <b>Ваша статистика</b>\n\n"
        f"📝 Всего документов: <b>{total_docs}</b>\n"
        f"✏️ Редактирований: <b>{total_edits}</b>\n"
        f"⭐ Любимый шаблон: <b>{favorite_template}</b>\n"
        f"📖 Слов написано: <b>{total_words:,}</b>\n"
        f"🕒 Последнее использование: <b>{last_used}</b>\n\n"
    )
    
    if total_docs > 0:
        text += "🎉 <b>Достижения:</b>\n"
        if total_docs >= 10:
            text += "🏆 Создано 10+ документов\n"
        if total_docs >= 50:
            text += "🏆 Создано 50+ документов\n"
        if total_edits >= 20:
            text += "✨ Мастер редактирования\n"
        if total_words >= 10000:
            text += "📚 Написано 10,000+ слов\n"
    else:
        text += "💡 Создайте свой первый документ, чтобы начать собирать статистику!"
    
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"Пользователь {user_id} просмотрел статистику")


@router.message(F.text == "⚙️ Настройки")
async def show_settings(message: Message, user_storage: UserStorage):
    """Показать настройки пользователя"""
    user_id = message.from_user.id
    settings = user_storage.get_settings(user_id)
    
    language = Config.DOCUMENT_LANGUAGES.get(settings.get('language', 'ru'), '🇷🇺 Русский')
    style = Config.DOCUMENT_STYLES.get(settings.get('style', 'formal'), '🎩 Официальный')
    notifications = "✅ Включены" if settings.get('notifications', True) else "❌ Выключены"
    
    text = (
        "⚙️ <b>Настройки</b>\n\n"
        f"🌍 Язык документа: <b>{language}</b>\n"
        f"🎨 Стиль документа: <b>{style}</b>\n"
        f"🔔 Уведомления: <b>{notifications}</b>\n\n"
        "Выберите, что хотите изменить:"
    )
    
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_settings_keyboard()
    )
    
    logger.info(f"Пользователь {user_id} открыл настройки")


@router.callback_query(F.data == "settings_language")
async def settings_language(callback: CallbackQuery):
    """Выбор языка документа"""
    await safe_edit_message(
        callback.message,
        "🌍 <b>Выберите язык для генерации документов:</b>\n\n"
        "Документы будут создаваться на выбранном языке.",
        parse_mode="HTML",
        reply_markup=get_language_keyboard(),
        send_new_on_fail=True
    )
    await callback.answer()


@router.callback_query(F.data.startswith("lang_"))
async def language_selected(callback: CallbackQuery, user_storage: UserStorage):
    """Обработка выбора языка"""
    language = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    user_storage.update_setting(user_id, 'language', language)
    
    lang_name = Config.DOCUMENT_LANGUAGES.get(language, 'Неизвестный')
    
    await safe_edit_message(
        callback.message,
        f"✅ Язык документов изменён на <b>{lang_name}</b>",
        parse_mode="HTML",
        send_new_on_fail=True
    )
    
    await callback.message.answer(
        "Настройки сохранены!",
        reply_markup=get_main_keyboard()
    )
    
    await callback.answer()
    logger.info(f"Пользователь {user_id} изменил язык на {language}")


@router.callback_query(F.data == "settings_style")
async def settings_style(callback: CallbackQuery):
    """Выбор стиля документа"""
    await safe_edit_message(
        callback.message,
        "🎨 <b>Выберите стиль для генерации документов:</b>\n\n"
        "Стиль влияет на тон и формальность текста.",
        parse_mode="HTML",
        reply_markup=get_style_keyboard(),
        send_new_on_fail=True
    )
    await callback.answer()


@router.callback_query(F.data.startswith("style_"))
async def style_selected(callback: CallbackQuery, user_storage: UserStorage):
    """Обработка выбора стиля"""
    style = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    user_storage.update_setting(user_id, 'style', style)
    
    style_name = Config.DOCUMENT_STYLES.get(style, 'Неизвестный')
    
    await safe_edit_message(
        callback.message,
        f"✅ Стиль документов изменён на <b>{style_name}</b>",
        parse_mode="HTML",
        send_new_on_fail=True
    )
    
    await callback.message.answer(
        "Настройки сохранены!",
        reply_markup=get_main_keyboard()
    )
    
    await callback.answer()
    logger.info(f"Пользователь {user_id} изменил стиль на {style}")


@router.callback_query(F.data == "settings_notifications")
async def settings_notifications(callback: CallbackQuery, user_storage: UserStorage):
    """Переключение уведомлений"""
    user_id = callback.from_user.id
    settings = user_storage.get_settings(user_id)
    
    current = settings.get('notifications', True)
    new_value = not current
    
    user_storage.update_setting(user_id, 'notifications', new_value)
    
    status = "включены" if new_value else "выключены"
    emoji = "✅" if new_value else "❌"
    
    await safe_edit_message(
        callback.message,
        f"{emoji} Уведомления <b>{status}</b>",
        parse_mode="HTML",
        send_new_on_fail=True
    )
    
    await callback.message.answer(
        "Настройки сохранены!",
        reply_markup=get_main_keyboard()
    )
    
    await callback.answer()
    logger.info(f"Пользователь {user_id} изменил уведомления на {new_value}")


@router.callback_query(F.data == "settings_clear_history")
async def settings_clear_history(callback: CallbackQuery, user_storage: UserStorage):
    """Очистка истории"""
    user_id = callback.from_user.id
    
    count = user_storage.clear_history(user_id)
    
    await safe_edit_message(
        callback.message,
        f"🗑️ История очищена!\n\n"
        f"Удалено записей: <b>{count}</b>",
        parse_mode="HTML",
        send_new_on_fail=True
    )
    
    await callback.message.answer(
        "История документов очищена.",
        reply_markup=get_main_keyboard()
    )
    
    await callback.answer()
    logger.info(f"Пользователь {user_id} очистил историю ({count} записей)")


@router.callback_query(F.data == "settings_back")
async def settings_back(callback: CallbackQuery, user_storage: UserStorage):
    """Вернуться к меню настроек"""
    user_id = callback.from_user.id
    settings = user_storage.get_settings(user_id)
    
    language = Config.DOCUMENT_LANGUAGES.get(settings.get('language', 'ru'), '🇷🇺 Русский')
    style = Config.DOCUMENT_STYLES.get(settings.get('style', 'formal'), '🎩 Официальный')
    notifications = "✅ Включены" if settings.get('notifications', True) else "❌ Выключены"
    
    text = (
        "⚙️ <b>Настройки</b>\n\n"
        f"🌍 Язык документа: <b>{language}</b>\n"
        f"🎨 Стиль документа: <b>{style}</b>\n"
        f"🔔 Уведомления: <b>{notifications}</b>\n\n"
        "Выберите, что хотите изменить:"
    )
    
    await safe_edit_message(
        callback.message,
        text,
        parse_mode="HTML",
        reply_markup=get_settings_keyboard(),
        send_new_on_fail=True
    )
    
    await callback.answer()


@router.callback_query(F.data == "action_favorite")
async def action_favorite(callback: CallbackQuery, state: FSMContext, user_storage: UserStorage):
    """Добавить документ в избранное"""
    user_id = callback.from_user.id
    data = await state.get_data()
    
    if not data.get('last_content'):
        await callback.answer("Нет документа для добавления в избранное", show_alert=True)
        return
    
    doc_data = {
        'content': data.get('last_content'),
        'template_name': data.get('last_template_name', 'Документ'),
        'template_type': data.get('last_template_type', 'custom'),
        'doc_type': data.get('last_doc_type', 'docx'),
        'user_request': data.get('last_user_request', ''),
        'date': datetime.now().strftime("%Y-%m-%d %H:%M")
    }
    
    user_storage.add_favorite(user_id, doc_data)
    
    await callback.answer("⭐ Документ добавлен в избранное!", show_alert=True)
    logger.info(f"Пользователь {user_id} добавил документ в избранное")


@router.callback_query(F.data == "action_preview")
async def action_preview(callback: CallbackQuery, state: FSMContext):
    """Показать предпросмотр содержимого документа"""
    data = await state.get_data()
    content = data.get('last_content', '')
    
    if not content:
        await callback.answer("Нет контента для предпросмотра", show_alert=True)
        return
    
    preview = content[:1000] + "..." if len(content) > 1000 else content
    
    await callback.message.answer(
        f"👁️ <b>Предпросмотр документа:</b>\n\n"
        f"<pre>{preview}</pre>\n\n"
        f"📊 Длина: {len(content)} символов",
        parse_mode="HTML"
    )
    
    await callback.answer()
    logger.info(f"Пользователь {callback.from_user.id} запросил предпросмотр")
