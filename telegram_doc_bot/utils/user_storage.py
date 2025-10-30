"""
Модуль для хранения пользовательских данных (API ключи)
"""

import logging
import sqlite3
from typing import Optional
from pathlib import Path

logger = logging.getLogger(__name__)


class UserStorage:
    """Класс для работы с хранилищем пользовательских данных"""
    
    def __init__(self, db_path: str = "user_data.db"):
        """
        Инициализация хранилища
        
        Args:
            db_path: Путь к файлу базы данных
        """
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Инициализация базы данных и создание таблиц"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS users (
                        user_id INTEGER PRIMARY KEY,
                        gemini_api_key TEXT,
                        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                    )
                """)
                conn.commit()
                logger.info("База данных инициализирована")
        except Exception as e:
            logger.error(f"Ошибка при инициализации базы данных: {e}")
    
    def set_api_key(self, user_id: int, api_key: str) -> bool:
        """
        Сохранение API ключа пользователя
        
        Args:
            user_id: ID пользователя в Telegram
            api_key: API ключ Gemini
        
        Returns:
            True если сохранение успешно, False в случае ошибки
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO users (user_id, gemini_api_key)
                    VALUES (?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        gemini_api_key = excluded.gemini_api_key,
                        updated_at = CURRENT_TIMESTAMP
                """, (user_id, api_key))
                conn.commit()
                logger.info(f"API ключ сохранён для пользователя {user_id}")
                return True
        except Exception as e:
            logger.error(f"Ошибка при сохранении API ключа: {e}")
            return False
    
    def get_api_key(self, user_id: int) -> Optional[str]:
        """
        Получение API ключа пользователя
        
        Args:
            user_id: ID пользователя в Telegram
        
        Returns:
            API ключ или None если не найден
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT gemini_api_key FROM users WHERE user_id = ?
                """, (user_id,))
                result = cursor.fetchone()
                return result[0] if result and result[0] else None
        except Exception as e:
            logger.error(f"Ошибка при получении API ключа: {e}")
            return None
    
    def delete_api_key(self, user_id: int) -> bool:
        """
        Удаление API ключа пользователя
        
        Args:
            user_id: ID пользователя в Telegram
        
        Returns:
            True если удаление успешно, False в случае ошибки
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    UPDATE users SET gemini_api_key = NULL, updated_at = CURRENT_TIMESTAMP
                    WHERE user_id = ?
                """, (user_id,))
                conn.commit()
                logger.info(f"API ключ удалён для пользователя {user_id}")
                return True
        except Exception as e:
            logger.error(f"Ошибка при удалении API ключа: {e}")
            return False
    
    def has_api_key(self, user_id: int) -> bool:
        """
        Проверка наличия API ключа у пользователя
        
        Args:
            user_id: ID пользователя в Telegram
        
        Returns:
            True если ключ есть, False если нет
        """
        api_key = self.get_api_key(user_id)
        return api_key is not None and len(api_key) > 0
