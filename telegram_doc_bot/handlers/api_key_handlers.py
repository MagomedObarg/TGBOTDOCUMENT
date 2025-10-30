"""
Обработчики для управления API ключами Gemini
"""

import logging
import re
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from telegram_doc_bot.utils.keyboards import (
    get_main_keyboard,
    get_cancel_keyboard,
    get_api_key_management_keyboard,
    get_api_key_confirm_keyboard
)
from telegram_doc_bot.utils.user_storage import UserStorage
from telegram_doc_bot.utils.message_helpers import safe_edit_message

logger = logging.getLogger(__name__)

router = Router()

user_storage = UserStorage()


class APIKeySetup(StatesGroup):
    """Состояния для настройки API ключа"""
    entering_key = State()


@router.message(F.text == "🔑 Мой API ключ")
@router.message(Command("apikey"))
async def show_api_key_status(message: Message):
    """
    Показать статус API ключа пользователя
    
    Args:
        message: Сообщение пользователя
    """
    user_id = message.from_user.id
    has_key = user_storage.has_api_key(user_id)
    
    if has_key:
        status_text = (
            "🔑 <b>Ваш API ключ Gemini</b>\n\n"
            "✅ <b>Статус:</b> Активен\n\n"
            "📌 Ваш API ключ сохранён и используется для генерации документов.\n\n"
            "💡 Вы можете обновить или удалить ключ, используя кнопки ниже."
        )
    else:
        status_text = (
            "🔑 <b>API ключ Gemini</b>\n\n"
            "❌ <b>Статус:</b> Не настроен\n\n"
            "📌 Для работы бота необходим API ключ Google Gemini.\n\n"
            "🎯 <b>Почему это нужно?</b>\n"
            "• Ключ используется для генерации контента документов\n"
            "• Ваш ключ хранится безопасно и используется только вами\n"
            "• Это бесплатный сервис от Google (в пределах лимитов)\n\n"
            "👇 Нажмите кнопку ниже, чтобы добавить ключ"
        )
    
    await message.answer(
        status_text,
        parse_mode="HTML",
        reply_markup=get_api_key_management_keyboard(has_key=has_key)
    )
    
    logger.info(f"Пользователь {user_id} просмотрел статус API ключа")


@router.callback_query(F.data == "apikey_add")
@router.callback_query(F.data == "apikey_update")
async def start_api_key_setup(callback: CallbackQuery, state: FSMContext):
    """
    Начать процесс добавления/обновления API ключа
    
    Args:
        callback: Callback запрос
        state: Состояние FSM
    """
    is_update = callback.data == "apikey_update"
    action = "обновить" if is_update else "добавить"
    
    await safe_edit_message(
        callback.message,
        f"🔑 <b>{'Обновление' if is_update else 'Добавление'} API ключа</b>\n\n"
        f"📝 Отправьте ваш API ключ Google Gemini.\n\n"
        f"⚠️ <b>Важно:</b>\n"
        f"• Ключ должен начинаться с 'AIza'\n"
        f"• Будьте внимательны при вводе\n"
        f"• Ключ будет сохранён в защищённом хранилище\n"
        f"• Никто кроме вас не сможет использовать ваш ключ\n\n"
        f"❌ Используйте /cancel для отмены",
        parse_mode="HTML",
        send_new_on_fail=True
    )
    
    await state.set_state(APIKeySetup.entering_key)
    await callback.answer()
    
    logger.info(f"Пользователь {callback.from_user.id} начал {action} API ключ")


@router.callback_query(F.data == "apikey_help")
async def show_api_key_help(callback: CallbackQuery):
    """
    Показать инструкцию по получению API ключа
    
    Args:
        callback: Callback запрос
    """
    help_text = (
        "🔑 <b>Как получить API ключ Gemini?</b>\n\n"
        
        "📝 <b>Пошаговая инструкция:</b>\n\n"
        
        "1️⃣ Перейдите на сайт Google AI Studio:\n"
        "🔗 <code>https://aistudio.google.com/app/apikey</code>\n\n"
        
        "2️⃣ Войдите в свой Google аккаунт\n\n"
        
        "3️⃣ Нажмите кнопку <b>\"Create API key\"</b> или <b>\"Get API key\"</b>\n\n"
        
        "4️⃣ Выберите проект или создайте новый\n\n"
        
        "5️⃣ Скопируйте полученный ключ (начинается с AIza...)\n\n"
        
        "6️⃣ Вернитесь в бот и отправьте ключ\n\n"
        
        "💡 <b>Важная информация:</b>\n"
        "• API ключ предоставляется бесплатно\n"
        "• Есть лимиты запросов (достаточно для большинства пользователей)\n"
        "• Ключ привязан к вашему Google аккаунту\n"
        "• Не делитесь ключом с другими людьми\n\n"
        
        "❓ Если возникли проблемы, проверьте документацию Google AI Studio"
    )
    
    await safe_edit_message(
        callback.message,
        help_text,
        parse_mode="HTML",
        reply_markup=get_api_key_management_keyboard(has_key=False),
        send_new_on_fail=True
    )
    
    await callback.answer()


@router.message(APIKeySetup.entering_key, Command("cancel"))
async def cancel_api_key_setup(message: Message, state: FSMContext):
    """
    Отменить настройку API ключа
    
    Args:
        message: Сообщение пользователя
        state: Состояние FSM
    """
    await state.clear()
    
    await message.answer(
        "❌ Настройка API ключа отменена.",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"Пользователь {message.from_user.id} отменил настройку API ключа")


@router.message(APIKeySetup.entering_key, F.text)
async def process_api_key(message: Message, state: FSMContext):
    """
    Обработка введённого API ключа
    
    Args:
        message: Сообщение с API ключом
        state: Состояние FSM
    """
    api_key = message.text.strip()
    user_id = message.from_user.id
    
    if not api_key:
        await message.answer(
            "⚠️ API ключ не может быть пустым. Попробуйте ещё раз или используйте /cancel для отмены."
        )
        return
    
    if not re.match(r'^AIza[0-9A-Za-z_-]{35}$', api_key):
        await message.answer(
            "❌ <b>Неверный формат API ключа</b>\n\n"
            "API ключ Google Gemini должен:\n"
            "• Начинаться с 'AIza'\n"
            "• Содержать 39 символов\n"
            "• Состоять из букв, цифр, дефисов и подчёркиваний\n\n"
            "Пожалуйста, проверьте ключ и попробуйте снова.\n"
            "Или используйте /cancel для отмены.",
            parse_mode="HTML"
        )
        return
    
    try:
        await message.delete()
    except Exception:
        pass
    
    if user_storage.set_api_key(user_id, api_key):
        success_text = (
            "✅ <b>API ключ успешно сохранён!</b>\n\n"
            "🎉 Теперь вы можете создавать документы.\n\n"
            "📝 Нажмите \"Создать документ\" или используйте команду /generate\n\n"
            "🔒 Ваш ключ надёжно сохранён и будет использоваться только для ваших запросов."
        )
        
        await message.answer(
            success_text,
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )
        
        await state.clear()
        logger.info(f"API ключ успешно сохранён для пользователя {user_id}")
    else:
        await message.answer(
            "❌ <b>Ошибка при сохранении ключа</b>\n\n"
            "Произошла ошибка при сохранении API ключа. "
            "Пожалуйста, попробуйте ещё раз позже или обратитесь в поддержку.",
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        logger.error(f"Не удалось сохранить API ключ для пользователя {user_id}")


@router.callback_query(F.data == "apikey_delete")
async def confirm_api_key_deletion(callback: CallbackQuery):
    """
    Запрос подтверждения удаления API ключа
    
    Args:
        callback: Callback запрос
    """
    await safe_edit_message(
        callback.message,
        "🗑 <b>Удаление API ключа</b>\n\n"
        "⚠️ Вы уверены, что хотите удалить ваш API ключ?\n\n"
        "После удаления:\n"
        "• Вы не сможете создавать документы\n"
        "• Вам потребуется добавить ключ заново\n\n"
        "Подтвердите удаление:",
        parse_mode="HTML",
        reply_markup=get_api_key_confirm_keyboard(),
        send_new_on_fail=True
    )
    
    await callback.answer()


@router.callback_query(F.data == "apikey_delete_confirm")
async def delete_api_key(callback: CallbackQuery):
    """
    Удаление API ключа пользователя
    
    Args:
        callback: Callback запрос
    """
    user_id = callback.from_user.id
    
    if user_storage.delete_api_key(user_id):
        await safe_edit_message(
            callback.message,
            "✅ <b>API ключ удалён</b>\n\n"
            "Ваш API ключ был успешно удалён из системы.\n\n"
            "Чтобы снова использовать бот, добавьте новый ключ через:\n"
            "🔑 Мой API ключ",
            parse_mode="HTML",
            send_new_on_fail=True
        )
        
        logger.info(f"API ключ удалён для пользователя {user_id}")
    else:
        await safe_edit_message(
            callback.message,
            "❌ <b>Ошибка при удалении</b>\n\n"
            "Не удалось удалить API ключ. Попробуйте позже.",
            parse_mode="HTML",
            send_new_on_fail=True
        )
        
        logger.error(f"Не удалось удалить API ключ для пользователя {user_id}")
    
    await callback.answer()


@router.callback_query(F.data == "apikey_delete_cancel")
async def cancel_api_key_deletion(callback: CallbackQuery):
    """
    Отмена удаления API ключа
    
    Args:
        callback: Callback запрос
    """
    await safe_edit_message(
        callback.message,
        "✅ Удаление отменено. Ваш API ключ сохранён.",
        parse_mode="HTML",
        send_new_on_fail=True
    )
    
    await show_api_key_status(callback.message)
    await callback.answer()
