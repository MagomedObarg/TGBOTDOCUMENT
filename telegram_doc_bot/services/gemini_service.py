"""
Сервис для работы с Google Gemini API.
Генерирует текстовый контент на основе запросов пользователя.
"""

import logging
import google.generativeai as genai
from typing import Optional

logger = logging.getLogger(__name__)


class GeminiService:
    """Класс для взаимодействия с Google Gemini API"""
    
    def __init__(self, api_key: str):
        """
        Инициализация сервиса Gemini
        
        Args:
            api_key: API ключ Google Gemini
        """
        self.api_key = api_key
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel('gemini-pro')
        logger.info("Gemini сервис инициализирован")
    
    async def generate_document_content(
        self,
        user_request: str,
        template_type: str = 'custom'
    ) -> Optional[str]:
        """
        Генерация содержимого документа на основе запроса пользователя
        
        Args:
            user_request: Запрос пользователя с описанием документа
            template_type: Тип шаблона документа
        
        Returns:
            Сгенерированный текст документа или None в случае ошибки
        """
        try:
            # Формирование промпта в зависимости от типа шаблона
            prompt = self._create_prompt(user_request, template_type)
            
            logger.info(f"Генерация документа типа '{template_type}' для запроса: {user_request[:50]}...")
            
            # Генерация контента
            response = await self._generate_async(prompt)
            
            if response:
                logger.info(f"Документ успешно сгенерирован, длина: {len(response)} символов")
                return response
            else:
                logger.error("Не удалось получить ответ от Gemini API")
                return None
                
        except Exception as e:
            logger.error(f"Ошибка при генерации контента: {e}")
            return None
    
    async def _generate_async(self, prompt: str) -> Optional[str]:
        """
        Асинхронная генерация текста через Gemini API
        
        Args:
            prompt: Промпт для генерации
        
        Returns:
            Сгенерированный текст или None
        """
        try:
            # Используем синхронный метод в асинхронной обёртке
            # так как библиотека google-generativeai не поддерживает async/await
            response = self.model.generate_content(prompt)
            
            if response and response.text:
                return response.text
            return None
            
        except Exception as e:
            logger.error(f"Ошибка API Gemini: {e}")
            return None
    
    def _create_prompt(self, user_request: str, template_type: str) -> str:
        """
        Создание промпта для Gemini на основе типа документа
        
        Args:
            user_request: Запрос пользователя
            template_type: Тип шаблона документа
        
        Returns:
            Сформированный промпт
        """
        base_prompts = {
            'contract': """
Ты - профессиональный юрист. Создай юридически грамотный договор на основе следующего запроса:

{request}

Документ должен содержать:
- Заголовок
- Преамбулу с указанием сторон
- Предмет договора
- Права и обязанности сторон
- Срок действия договора
- Порядок разрешения споров
- Заключительные положения
- Подписи сторон

Используй формальный юридический язык. Текст должен быть структурированным и профессиональным.
""",
            'statement': """
Создай официальное заявление на основе следующего запроса:

{request}

Документ должен содержать:
- Кому адресовано (наименование организации, должность, ФИО руководителя)
- От кого (ФИО заявителя, адрес, контакты)
- Заголовок "ЗАЯВЛЕНИЕ"
- Основной текст с изложением просьбы/требования
- Дата и подпись

Используй официально-деловой стиль.
""",
            'resume': """
Создай профессиональное резюме на основе следующих данных:

{request}

Документ должен содержать:
- ФИО и контактные данные
- Желаемая должность
- Краткое резюме (Summary)
- Опыт работы (в обратном хронологическом порядке)
- Образование
- Профессиональные навыки
- Дополнительная информация

Используй современный формат резюме. Текст должен быть лаконичным и информативным.
""",
            'letter': """
Создай деловое письмо на основе следующего запроса:

{request}

Документ должен содержать:
- Дату
- Адресата
- Приветствие
- Основной текст письма
- Заключительную формулу вежливости
- Подпись отправителя

Используй официально-деловой стиль, соблюдай этикет деловой переписки.
""",
            'report': """
Создай структурированный отчёт на основе следующего запроса:

{request}

Документ должен содержать:
- Заголовок отчёта
- Введение (цель и задачи)
- Основную часть с разделами
- Выводы и рекомендации
- Заключение

Используй деловой стиль. Структурируй информацию логично и последовательно.
""",
            'custom': """
Создай документ на основе следующего запроса:

{request}

Создай качественный, структурированный документ, соответствующий запросу.
Используй подходящий стиль и форматирование.
Добавь все необходимые разделы и элементы для полноценного документа.
"""
        }
        
        prompt_template = base_prompts.get(template_type, base_prompts['custom'])
        return prompt_template.format(request=user_request)
