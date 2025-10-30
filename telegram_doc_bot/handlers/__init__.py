"""Модуль обработчиков команд и сообщений"""

from . import basic_handlers
from . import document_handlers
from . import api_key_handlers
from . import advanced_handlers

__all__ = ['basic_handlers', 'document_handlers', 'api_key_handlers', 'advanced_handlers']
