import pytest
import pytest_asyncio
import asyncpg
from unittest.mock import AsyncMock
import os
from dotenv import load_dotenv
from services.task_service import TaskService

load_dotenv()

# сейчас я подключаюсь к главное базе данных Postgres
# нужно создать другую БД для тестов
@pytest_asyncio.fixture
async def test_db():
    """Фикстура для тестовой базы данных"""
    # Создаем отдельную тестовую базу
    test_db_name = "test_telegram_bot"
    
    # Подключаемся к основной базе чтобы создать тестовую
    conn = await asyncpg.connect(
        database=os.getenv('MAIN_DB_NAME'),
        user=os.getenv('MAIN_DB_USER'),
        password=os.getenv('MAIN_DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    
    await conn.execute(f"DROP DATABASE IF EXISTS {test_db_name}")
    await conn.execute(f"CREATE DATABASE {test_db_name}")
    await conn.close()
    
    # Подключаемся к тестовой базе
    test_conn = await asyncpg.connect(
        database=test_db_name,
        user=os.getenv('MAIN_DB_USER'),
        password=os.getenv('MAIN_DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    
    # Создаем таблицы
    await test_conn.execute('''
        CREATE TABLE tasks (
            id SERIAL PRIMARY KEY,
            user_id BIGINT NOT NULL,
            task_text TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT NOW()
        )
    ''')
    
    yield test_conn
    
    # Очистка после тестов
    await test_conn.close()
    
    # Удаляем тестовую базу
    clean_conn = await asyncpg.connect(
        database=os.getenv('MAIN_DB_NAME'),
        user=os.getenv('MAIN_DB_USER'),
        password=os.getenv('MAIN_DB_PASSWORD'),
        host=os.getenv('DB_HOST')
    )
    await clean_conn.execute(f"DROP DATABASE {test_db_name}")
    await clean_conn.close()

@pytest.mark.asyncio
async def test_database_isolation(test_db):
    """Тест что данные изолированы в тестовой БД"""
    
    # Добавляем задачу в тестовую БД
    await test_db.execute(
        'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2)',
        123, "Изолированная задача"
    )
    
    # Проверяем что в тестовой БД есть данные
    test_tasks = await test_db.fetch("SELECT * FROM tasks")
    assert len(test_tasks) == 1
    assert test_tasks[0]['task_text'] == "Изолированная задача"
    
    # Теперь попробуем подключиться к основной БД и убедимся, что там этих данных нет
    # (Это дополнительная проверка изоляции)
    try:
        main_conn = await asyncpg.connect(
            database=os.getenv('MAIN_DB_NAME'),
            user=os.getenv('MAIN_DB_USER'),
            password=os.getenv('MAIN_DB_PASSWORD'),
            host=os.getenv('DB_HOST')
        )
        
        # Проверяем что в основной БД нет нашей тестовой таблицы или данных
        # (это зависит от вашей структуры основной БД)
        main_tasks = await main_conn.fetch("SELECT * FROM tasks WHERE task_text = $1", "Изолированная задача")
        assert len(main_tasks) == 0  # В основной БД не должно быть тестовых данных
        
        await main_conn.close()
        
    except asyncpg.PostgresError:
        # Если в основной БД нет таблицы tasks - это нормально
        pass

@pytest.fixture
def mock_task_service():
    """Mock task_service fixture"""
    mock_service = AsyncMock(spec=TaskService)
    mock_service.create_task.return_value = 1
    return mock_service
    
@pytest.fixture
def mock_message():
    """ Mock message fixture.
    No need to set message text as it is being set in test functions directly"""
    message = AsyncMock()
    message.from_user.id = 12345
    message.answer = AsyncMock()
    return message