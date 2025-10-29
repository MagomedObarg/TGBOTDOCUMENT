"""
Тесты для модуля конфигурации
"""

import pytest
import os


def test_config_imports():
    """Тест импорта модуля конфигурации"""
    from telegram_doc_bot.config import Config
    assert Config is not None


def test_document_templates():
    """Тест наличия шаблонов документов"""
    from telegram_doc_bot.config import Config
    
    assert 'contract' in Config.DOCUMENT_TEMPLATES
    assert 'statement' in Config.DOCUMENT_TEMPLATES
    assert 'resume' in Config.DOCUMENT_TEMPLATES
    assert 'letter' in Config.DOCUMENT_TEMPLATES
    assert 'report' in Config.DOCUMENT_TEMPLATES
    assert 'custom' in Config.DOCUMENT_TEMPLATES


def test_document_types():
    """Тест наличия типов документов"""
    from telegram_doc_bot.config import Config
    
    assert 'docx' in Config.DOCUMENT_TYPES
    assert 'pdf' in Config.DOCUMENT_TYPES


def test_max_request_length():
    """Тест настройки максимальной длины запроса"""
    from telegram_doc_bot.config import Config
    
    assert Config.MAX_REQUEST_LENGTH > 0
    assert isinstance(Config.MAX_REQUEST_LENGTH, int)
