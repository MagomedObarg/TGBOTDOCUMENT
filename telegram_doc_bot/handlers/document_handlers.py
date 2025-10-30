"""
Обработчики для генерации документов.
Использует FSM (Finite State Machine) для управления процессом создания документа.
"""

import logging
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, CallbackQuery, FSInputFile
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup

from telegram_doc_bot.services import GeminiService, DocumentService
from telegram_doc_bot.utils.keyboards import (
    get_main_keyboard,
    get_template_keyboard,
    get_document_type_keyboard,
    get_cancel_keyboard,
    get_document_actions_keyboard,
    get_api_key_management_keyboard
)
from telegram_doc_bot.utils.user_storage import UserStorage
from telegram_doc_bot.utils.message_helpers import safe_edit_message, safe_delete_message
from telegram_doc_bot.config import Config

logger = logging.getLogger(__name__)

# Создание роутера для обработчиков документов
router = Router()


class DocumentGeneration(StatesGroup):
    """Состояния для процесса генерации документа"""
    choosing_template = State()  # Выбор шаблона
    entering_request = State()   # Ввод описания документа
    choosing_doc_type = State()  # Выбор типа файла (Word/PDF)
    document_ready = State()     # Документ готов, можно редактировать


class DocumentEditing(StatesGroup):
    """Состояния для процесса редактирования документа"""
    entering_edit_instructions = State()  # Ввод инструкций по редактированию


@router.message(Command("generate"))
@router.message(F.text == "📝 Создать документ")
async def start_document_generation(message: Message, state: FSMContext, user_storage: UserStorage):
    """
    Начало процесса создания документа
    
    Args:
        message: Сообщение пользователя
        state: Состояние FSM
        user_storage: Хранилище пользовательских данных
    """
    user_id = message.from_user.id
    
    if not user_storage.has_api_key(user_id):
        await message.answer(
            "🔑 <b>API ключ не настроен</b>\n\n"
            "❗ Для создания документов необходим API ключ Google Gemini.\n\n"
            "🎯 <b>Что нужно сделать:</b>\n"
            "1. Нажмите кнопку \"🔑 Мой API ключ\"\n"
            "2. Следуйте инструкциям для получения ключа\n"
            "3. Добавьте ключ в бот\n"
            "4. Начните создавать документы!\n\n"
            "💡 Это займёт всего пару минут, и API предоставляется бесплатно.",
            parse_mode="HTML",
            reply_markup=get_api_key_management_keyboard(has_key=False)
        )
        logger.info(f"Пользователь {user_id} попытался создать документ без API ключа")
        return
    
    await state.clear()
    
    await message.answer(
        "📝 <b>Создание документа</b>\n\n"
        "Выберите тип шаблона документа:",
        parse_mode="HTML",
        reply_markup=get_template_keyboard()
    )
    
    await state.set_state(DocumentGeneration.choosing_template)
    logger.info(f"Пользователь {message.from_user.id} начал создание документа")


@router.callback_query(DocumentGeneration.choosing_template, F.data.startswith("template_"))
async def template_chosen(callback: CallbackQuery, state: FSMContext):
    """
    Обработка выбора шаблона документа
    
    Args:
        callback: Callback запрос
        state: Состояние FSM
    """
    template_type = callback.data.split("_")[1]
    template_name = Config.DOCUMENT_TEMPLATES.get(template_type, "Произвольный документ")
    
    # Сохранение выбранного шаблона в состояние
    await state.update_data(template_type=template_type, template_name=template_name)
    
    await safe_edit_message(
        callback.message,
        f"✅ Выбран шаблон: <b>{template_name}</b>",
        parse_mode="HTML"
    )
    
    await callback.message.answer(
        "📝 Теперь опишите, какой документ вам нужен.\n\n"
        "Укажите все важные детали:\n"
        "• Для договора: стороны, предмет, условия\n"
        "• Для заявления: кому, от кого, суть просьбы\n"
        "• Для резюме: ФИО, опыт, навыки, образование\n"
        "• Для письма: адресат, тема, основное содержание\n\n"
        f"Максимальная длина: {Config.MAX_REQUEST_LENGTH} символов",
        reply_markup=get_cancel_keyboard()
    )
    
    await state.set_state(DocumentGeneration.entering_request)
    await callback.answer()
    
    logger.info(f"Пользователь {callback.from_user.id} выбрал шаблон: {template_name}")


@router.message(DocumentGeneration.entering_request, F.text == "❌ Отмена")
@router.message(Command("cancel"))
async def cancel_generation(message: Message, state: FSMContext):
    """
    Отмена процесса генерации документа
    
    Args:
        message: Сообщение пользователя
        state: Состояние FSM
    """
    await state.clear()
    
    await message.answer(
        "❌ Создание документа отменено.",
        reply_markup=get_main_keyboard()
    )
    
    logger.info(f"Пользователь {message.from_user.id} отменил создание документа")


@router.message(DocumentGeneration.entering_request, F.text)
async def request_entered(message: Message, state: FSMContext):
    """
    Обработка введённого описания документа
    
    Args:
        message: Сообщение пользователя с описанием
        state: Состояние FSM
    """
    user_request = message.text
    
    # Проверка длины запроса
    if len(user_request) > Config.MAX_REQUEST_LENGTH:
        await message.answer(
            f"⚠️ Ваш запрос слишком длинный ({len(user_request)} символов).\n"
            f"Максимальная длина: {Config.MAX_REQUEST_LENGTH} символов.\n\n"
            "Пожалуйста, сократите описание и попробуйте снова."
        )
        return
    
    if len(user_request) < 10:
        await message.answer(
            "⚠️ Описание слишком короткое.\n"
            "Пожалуйста, опишите подробнее, какой документ вам нужен."
        )
        return
    
    # Сохранение запроса в состояние
    await state.update_data(user_request=user_request)
    
    await message.answer(
        "✅ Описание принято!\n\n"
        "Теперь выберите формат документа:",
        reply_markup=get_document_type_keyboard()
    )
    
    await state.set_state(DocumentGeneration.choosing_doc_type)
    
    logger.info(f"Пользователь {message.from_user.id} ввёл описание документа: {user_request[:50]}...")


@router.callback_query(DocumentGeneration.choosing_doc_type, F.data.startswith("doctype_"))
async def document_type_chosen(callback: CallbackQuery, state: FSMContext, 
                               user_storage: UserStorage, 
                               document_service: DocumentService):
    """
    Обработка выбора типа документа и генерация
    
    Args:
        callback: Callback запрос
        state: Состояние FSM
        user_storage: Хранилище пользовательских данных
        document_service: Сервис генерации документов
    """
    doc_type = callback.data.split("_")[1]
    user_id = callback.from_user.id
    
    # Проверка наличия API ключа
    api_key = user_storage.get_api_key(user_id)
    if not api_key:
        await safe_edit_message(
            callback.message,
            "❌ <b>API ключ не найден</b>\n\n"
            "Пожалуйста, добавьте API ключ перед созданием документов.",
            parse_mode="HTML",
            send_new_on_fail=True
        )
        await state.clear()
        await callback.answer()
        return
    
    # Инициализация Gemini сервиса с API ключом пользователя
    gemini_service = GeminiService(api_key=api_key)
    
    # Получение данных из состояния
    data = await state.get_data()
    template_type = data.get('template_type')
    template_name = data.get('template_name')
    user_request = data.get('user_request')
    
    await safe_edit_message(
        callback.message,
        f"✅ Формат: <b>{Config.DOCUMENT_TYPES[doc_type]}</b>",
        parse_mode="HTML"
    )
    
    # Отправка сообщения о начале генерации
    status_message = await callback.message.answer(
        "⏳ Генерирую документ...\n"
        "Это может занять 10-30 секунд. Пожалуйста, подождите.",
        reply_markup=get_main_keyboard()
    )
    
    try:
        # Генерация контента с помощью Gemini
        logger.info(f"Генерация контента для пользователя {callback.from_user.id}")
        content = await gemini_service.generate_document_content(user_request, template_type)
        
        if not content:
            await safe_edit_message(
                status_message,
                "❌ Ошибка при генерации контента.\n"
                "Пожалуйста, попробуйте ещё раз или измените запрос.",
                send_new_on_fail=True
            )
            await state.clear()
            return
        
        # Обновление статуса
        await safe_edit_message(
            status_message,
            "📄 Контент сгенерирован!\n"
            "⏳ Создаю документ...",
            send_new_on_fail=True
        )
        
        # Создание документа в выбранном формате
        if doc_type == 'docx':
            filepath = await document_service.create_word_document(
                content=content,
                title=template_name,
                user_id=callback.from_user.id
            )
        else:  # pdf
            filepath = await document_service.create_pdf_document(
                content=content,
                title=template_name,
                user_id=callback.from_user.id
            )
        
        if not filepath:
            await safe_edit_message(
                status_message,
                "❌ Ошибка при создании документа.\n"
                "Пожалуйста, попробуйте ещё раз.",
                send_new_on_fail=True
            )
            await state.clear()
            return
        
        # Обновление статуса
        await safe_edit_message(
            status_message,
            "📤 Отправляю документ...",
            send_new_on_fail=True
        )
        
        # Отправка документа пользователю
        document = FSInputFile(filepath)
        
        await callback.message.answer_document(
            document=document,
            caption=(
                f"✅ <b>Документ готов!</b>\n\n"
                f"📋 Тип: {template_name}\n"
                f"📄 Формат: {Config.DOCUMENT_TYPES[doc_type]}\n"
                f"📊 Размер контента: {len(content)} символов"
            ),
            parse_mode="HTML"
        )
        
        # Удаление сообщения о статусе
        await safe_delete_message(status_message)
        
        # Очистка временного файла
        document_service.cleanup_file(filepath)
        
        # Сохраняем данные документа для возможного редактирования
        await state.update_data(
            last_content=content,
            last_template_type=template_type,
            last_template_name=template_name,
            last_doc_type=doc_type,
            last_user_request=user_request
        )
        
        # Предложение действий с документом
        await callback.message.answer(
            "Что вы хотите сделать дальше?",
            reply_markup=get_document_actions_keyboard()
        )
        
        await state.set_state(DocumentGeneration.document_ready)
        
        logger.info(f"Документ успешно создан и отправлен пользователю {callback.from_user.id}")
        
    except Exception as e:
        logger.error(f"Ошибка при генерации документа: {e}")
        await safe_edit_message(
            status_message,
            "❌ Произошла ошибка при создании документа.\n"
            "Пожалуйста, попробуйте ещё раз позже.",
            send_new_on_fail=True
        )
        await state.clear()
    
    finally:
        await callback.answer()


@router.callback_query(DocumentGeneration.document_ready, F.data == "action_edit")
async def start_document_editing(callback: CallbackQuery, state: FSMContext):
    """Начало процесса редактирования документа"""
    data = await state.get_data()
    if not data.get('last_content'):
        await callback.answer("Нет данных для редактирования", show_alert=True)
        await state.clear()
        return
    
    await safe_edit_message(
        callback.message,
        "✏️ <b>Редактирование документа</b>\n\n"
        "Опишите, какие изменения нужно внести в документ.\n\n"
        "Примеры инструкций:\n"
        "• 'Добавь раздел о гарантиях'\n"
        "• 'Сделай текст короче и лаконичнее'\n"
        "• 'Измени тон на более формальный'\n"
        "• 'Добавь больше деталей о...'\n"
        "• 'Убери раздел о...'",
        parse_mode="HTML",
        reply_markup=None,
        send_new_on_fail=True
    )
    
    await callback.message.answer(
        "Введите инструкции по редактированию:",
        reply_markup=get_cancel_keyboard()
    )
    
    await state.set_state(DocumentEditing.entering_edit_instructions)
    await callback.answer()


@router.callback_query(DocumentGeneration.document_ready, F.data == "action_new")
async def start_new_document(callback: CallbackQuery, state: FSMContext, user_storage: UserStorage):
    """Запуск процесса создания нового документа"""
    await state.clear()
    await callback.answer()
    await start_document_generation(callback.message, state, user_storage)


@router.callback_query(DocumentGeneration.document_ready, F.data == "action_finish")
async def finish_document_flow(callback: CallbackQuery, state: FSMContext):
    """Завершение работы с документом"""
    await state.clear()
    await safe_edit_message(
        callback.message,
        "✅ Работа с документом завершена.",
        reply_markup=None,
        send_new_on_fail=True
    )
    await callback.message.answer(
        "Выберите действие:",
        reply_markup=get_main_keyboard()
    )
    await callback.answer()


@router.message(DocumentEditing.entering_edit_instructions, F.text == "❌ Отмена")
@router.message(DocumentEditing.entering_edit_instructions, Command("cancel"))
async def cancel_editing(message: Message, state: FSMContext):
    """Отмена редактирования"""
    data = await state.get_data()
    if data.get('last_content'):
        await message.answer(
            "❌ Редактирование отменено.",
            reply_markup=get_main_keyboard()
        )
        await message.answer(
            "Что вы хотите сделать дальше?",
            reply_markup=get_document_actions_keyboard()
        )
        await state.set_state(DocumentGeneration.document_ready)
    else:
        await message.answer(
            "❌ Редактирование отменено.",
            reply_markup=get_main_keyboard()
        )
        await state.clear()


@router.message(DocumentEditing.entering_edit_instructions, F.text)
async def process_edit_instructions(
    message: Message,
    state: FSMContext,
    user_storage: UserStorage,
    document_service: DocumentService
):
    """Обработка инструкций по редактированию документа"""
    instructions = message.text.strip()
    user_id = message.from_user.id
    
    if len(instructions) < 5:
        await message.answer(
            "⚠️ Инструкции слишком короткие. Опишите, что нужно изменить более подробно.",
            reply_markup=get_cancel_keyboard()
        )
        return
    
    # Проверка наличия API ключа
    api_key = user_storage.get_api_key(user_id)
    if not api_key:
        await message.answer(
            "❌ <b>API ключ не найден</b>\n\n"
            "Пожалуйста, добавьте API ключ перед редактированием документов.",
            parse_mode="HTML",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        return
    
    # Инициализация Gemini сервиса с API ключом пользователя
    gemini_service = GeminiService(api_key=api_key)
    
    data = await state.get_data()
    last_content = data.get('last_content')
    template_type = data.get('last_template_type', 'custom')
    template_name = data.get('last_template_name', 'Документ')
    doc_type = data.get('last_doc_type', 'docx')
    
    if not last_content:
        await message.answer(
            "❌ Не удалось получить текущий документ для редактирования. Начните генерацию заново.",
            reply_markup=get_main_keyboard()
        )
        await state.clear()
        return
    
    status_message = await message.answer(
        "✏️ Применяю изменения к документу...\n"
        "Это может занять 10-30 секунд."
    )
    
    try:
        logger.info(
            f"Редактирование документа пользователя {message.from_user.id} с инструкциями: {instructions[:50]}..."
        )
        updated_content = await gemini_service.edit_document_content(
            original_content=last_content,
            edit_instructions=instructions,
            template_type=template_type
        )
        
        if not updated_content:
            await safe_edit_message(
                status_message,
                "❌ Не удалось применить изменения. Попробуйте сформулировать инструкции иначе.",
                send_new_on_fail=True
            )
            await state.set_state(DocumentGeneration.document_ready)
            return
        
        await safe_edit_message(
            status_message,
            "📄 Изменения применены. Создаю обновлённый документ...",
            send_new_on_fail=True
        )
        
        if doc_type == 'docx':
            filepath = await document_service.create_word_document(
                content=updated_content,
                title=template_name,
                user_id=message.from_user.id
            )
        else:
            filepath = await document_service.create_pdf_document(
                content=updated_content,
                title=template_name,
                user_id=message.from_user.id
            )
        
        if not filepath:
            await safe_edit_message(
                status_message,
                "❌ Не удалось создать обновлённый документ. Попробуйте ещё раз.",
                send_new_on_fail=True
            )
            await state.set_state(DocumentGeneration.document_ready)
            return
        
        await safe_edit_message(
            status_message,
            "📤 Отправляю обновлённый документ...",
            send_new_on_fail=True
        )
        document = FSInputFile(filepath)
        
        await message.answer_document(
            document=document,
            caption=(
                f"✅ <b>Документ обновлён!</b>\n\n"
                f"📋 Тип: {template_name}\n"
                f"📄 Формат: {Config.DOCUMENT_TYPES.get(doc_type, doc_type)}\n"
                f"📊 Размер контента: {len(updated_content)} символов"
            ),
            parse_mode="HTML"
        )
        
        document_service.cleanup_file(filepath)
        await safe_delete_message(status_message)
        
        await state.update_data(
            last_content=updated_content,
            last_doc_type=doc_type
        )
        
        await message.answer(
            "Хотите продолжить редактирование или создать новый документ?",
            reply_markup=get_document_actions_keyboard()
        )
        await state.set_state(DocumentGeneration.document_ready)
        
        logger.info(f"Документ пользователя {message.from_user.id} успешно отредактирован")
        
    except Exception as e:
        logger.error(f"Ошибка при редактировании документа: {e}")
        await safe_edit_message(
            status_message,
            "❌ Произошла ошибка при редактировании. Попробуйте позже.",
            send_new_on_fail=True
        )
        await state.clear()
