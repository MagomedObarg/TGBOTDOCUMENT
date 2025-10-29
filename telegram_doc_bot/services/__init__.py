"""Модуль сервисов для работы с API и генерации документов"""

from .gemini_service import GeminiService
from .document_service import DocumentService

__all__ = ['GeminiService', 'DocumentService']
