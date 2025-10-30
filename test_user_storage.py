"""
Простой тест для проверки работы UserStorage
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

from telegram_doc_bot.utils.user_storage import UserStorage


def test_user_storage():
    """Тестирование основных функций UserStorage"""
    
    db_path = "test_user_data.db"
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    storage = UserStorage(db_path)
    
    test_user_id = 12345
    test_api_key = "AIzaSyDEMOKEY1234567890abcdefghijklmn"
    
    print("1. Проверка отсутствия ключа для нового пользователя...")
    assert not storage.has_api_key(test_user_id), "Ключ не должен существовать"
    print("✅ Passed")
    
    print("\n2. Сохранение API ключа...")
    result = storage.set_api_key(test_user_id, test_api_key)
    assert result, "Сохранение должно быть успешным"
    print("✅ Passed")
    
    print("\n3. Проверка наличия ключа...")
    assert storage.has_api_key(test_user_id), "Ключ должен существовать"
    print("✅ Passed")
    
    print("\n4. Получение API ключа...")
    retrieved_key = storage.get_api_key(test_user_id)
    assert retrieved_key == test_api_key, "Ключ должен совпадать с сохранённым"
    print(f"✅ Passed (получен: {retrieved_key[:15]}...)")
    
    print("\n5. Обновление API ключа...")
    new_api_key = "AIzaSyNEWKEY9876543210zyxwvutsrqponml"
    result = storage.set_api_key(test_user_id, new_api_key)
    assert result, "Обновление должно быть успешным"
    updated_key = storage.get_api_key(test_user_id)
    assert updated_key == new_api_key, "Ключ должен быть обновлён"
    print("✅ Passed")
    
    print("\n6. Удаление API ключа...")
    result = storage.delete_api_key(test_user_id)
    assert result, "Удаление должно быть успешным"
    assert not storage.has_api_key(test_user_id), "Ключ не должен существовать после удаления"
    print("✅ Passed")
    
    print("\n7. Проверка работы с несколькими пользователями...")
    user1 = 111
    user2 = 222
    key1 = "AIzaSyUSER1KEY567890abcdefghijklmnopq"
    key2 = "AIzaSyUSER2KEY567890abcdefghijklmnopq"
    
    storage.set_api_key(user1, key1)
    storage.set_api_key(user2, key2)
    
    assert storage.get_api_key(user1) == key1, "Ключ пользователя 1 должен совпадать"
    assert storage.get_api_key(user2) == key2, "Ключ пользователя 2 должен совпадать"
    print("✅ Passed")
    
    if os.path.exists(db_path):
        os.remove(db_path)
    
    print("\n" + "="*50)
    print("🎉 Все тесты пройдены успешно!")
    print("="*50)


if __name__ == "__main__":
    try:
        test_user_storage()
    except AssertionError as e:
        print(f"\n❌ Тест провален: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Ошибка: {e}")
        sys.exit(1)
