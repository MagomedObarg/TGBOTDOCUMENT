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
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS document_history (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        template_name TEXT,
                        template_type TEXT,
                        doc_type TEXT,
                        content TEXT,
                        user_request TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS favorites (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER,
                        template_name TEXT,
                        template_type TEXT,
                        doc_type TEXT,
                        content TEXT,
                        user_request TEXT,
                        date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS user_settings (
                        user_id INTEGER PRIMARY KEY,
                        language TEXT DEFAULT 'ru',
                        style TEXT DEFAULT 'formal',
                        notifications INTEGER DEFAULT 1,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
                    )
                """)
                
                cursor.execute("""
                    CREATE TABLE IF NOT EXISTS statistics (
                        user_id INTEGER PRIMARY KEY,
                        total_documents INTEGER DEFAULT 0,
                        total_edits INTEGER DEFAULT 0,
                        total_words INTEGER DEFAULT 0,
                        favorite_template TEXT,
                        last_used TIMESTAMP,
                        FOREIGN KEY (user_id) REFERENCES users(user_id)
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
    
    def add_to_history(self, user_id: int, doc_data: dict) -> bool:
        """Добавление документа в историю"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO document_history 
                    (user_id, template_name, template_type, doc_type, content, user_request)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    doc_data.get('template_name'),
                    doc_data.get('template_type'),
                    doc_data.get('doc_type'),
                    doc_data.get('content'),
                    doc_data.get('user_request')
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении в историю: {e}")
            return False
    
    def get_history(self, user_id: int) -> list:
        """Получение истории документов пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM document_history 
                    WHERE user_id = ? 
                    ORDER BY date DESC 
                    LIMIT 20
                """, (user_id,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Ошибка при получении истории: {e}")
            return []
    
    def clear_history(self, user_id: int) -> int:
        """Очистка истории пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT COUNT(*) FROM document_history WHERE user_id = ?", (user_id,))
                count = cursor.fetchone()[0]
                cursor.execute("DELETE FROM document_history WHERE user_id = ?", (user_id,))
                conn.commit()
                return count
        except Exception as e:
            logger.error(f"Ошибка при очистке истории: {e}")
            return 0
    
    def add_favorite(self, user_id: int, doc_data: dict) -> bool:
        """Добавление документа в избранное"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO favorites 
                    (user_id, template_name, template_type, doc_type, content, user_request)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    user_id,
                    doc_data.get('template_name'),
                    doc_data.get('template_type'),
                    doc_data.get('doc_type'),
                    doc_data.get('content'),
                    doc_data.get('user_request')
                ))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка при добавлении в избранное: {e}")
            return False
    
    def get_favorites(self, user_id: int) -> list:
        """Получение избранных документов пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("""
                    SELECT * FROM favorites 
                    WHERE user_id = ? 
                    ORDER BY date DESC
                """, (user_id,))
                rows = cursor.fetchall()
                return [dict(row) for row in rows]
        except Exception as e:
            logger.error(f"Ошибка при получении избранного: {e}")
            return []
    
    def get_settings(self, user_id: int) -> dict:
        """Получение настроек пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                else:
                    cursor.execute("""
                        INSERT INTO user_settings (user_id) VALUES (?)
                    """, (user_id,))
                    conn.commit()
                    return {'language': 'ru', 'style': 'formal', 'notifications': 1}
        except Exception as e:
            logger.error(f"Ошибка при получении настроек: {e}")
            return {'language': 'ru', 'style': 'formal', 'notifications': 1}
    
    def update_setting(self, user_id: int, key: str, value) -> bool:
        """Обновление настройки пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute(f"""
                    INSERT INTO user_settings (user_id, {key})
                    VALUES (?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET {key} = excluded.{key}
                """, (user_id, value))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка при обновлении настройки: {e}")
            return False
    
    def get_statistics(self, user_id: int) -> dict:
        """Получение статистики пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                conn.row_factory = sqlite3.Row
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM statistics WHERE user_id = ?", (user_id,))
                row = cursor.fetchone()
                if row:
                    return dict(row)
                else:
                    return {
                        'total_documents': 0,
                        'total_edits': 0,
                        'total_words': 0,
                        'favorite_template': 'Нет данных',
                        'last_used': 'Никогда'
                    }
        except Exception as e:
            logger.error(f"Ошибка при получении статистики: {e}")
            return {
                'total_documents': 0,
                'total_edits': 0,
                'total_words': 0,
                'favorite_template': 'Нет данных',
                'last_used': 'Никогда'
            }
    
    def update_statistics(self, user_id: int, template_type: str, word_count: int, is_edit: bool = False) -> bool:
        """Обновление статистики пользователя"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                if is_edit:
                    cursor.execute("""
                        INSERT INTO statistics (user_id, total_edits, last_used)
                        VALUES (?, 1, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id) DO UPDATE SET
                            total_edits = total_edits + 1,
                            last_used = CURRENT_TIMESTAMP
                    """, (user_id,))
                else:
                    cursor.execute("""
                        INSERT INTO statistics (user_id, total_documents, total_words, favorite_template, last_used)
                        VALUES (?, 1, ?, ?, CURRENT_TIMESTAMP)
                        ON CONFLICT(user_id) DO UPDATE SET
                            total_documents = total_documents + 1,
                            total_words = total_words + ?,
                            favorite_template = ?,
                            last_used = CURRENT_TIMESTAMP
                    """, (user_id, word_count, template_type, word_count, template_type))
                conn.commit()
                return True
        except Exception as e:
            logger.error(f"Ошибка при обновлении статистики: {e}")
            return False
