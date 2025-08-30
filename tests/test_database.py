import pytest
import asyncpg

@pytest.mark.asyncio
async def test_add_task_to_test_db(test_db):
    """Простой тест записи в тестовую базу данных"""
    
    # 1. Проверяем, что база пустая в начале
    initial_tasks = await test_db.fetch("SELECT * FROM tasks")
    assert len(initial_tasks) == 0
    
    # 2. Добавляем задачу напрямую в тестовую базу
    task_id = await test_db.fetchval(
        'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id',
        123, "Test task from pytest"
    )
    
    # 3. Проверяем, что задача добавилась
    assert task_id is not None
    assert isinstance(task_id, int)
    
    # 4. Проверяем, что данные действительно в базе
    tasks = await test_db.fetch("SELECT * FROM tasks")
    assert len(tasks) == 1
    
    # 5. Проверяем содержимое задачи
    task = tasks[0]
    assert task['id'] == task_id
    assert task['user_id'] == 123
    assert task['task_text'] == "Test task from pytest"
    assert task['created_at'] is not None

@pytest.mark.asyncio
async def test_multiple_tasks(test_db):
    """Тест добавления нескольких задач"""
    
    # Добавляем несколько задач
    tasks_data = [
        (111, "Первая задача"),
        (222, "Вторая задача"),
        (111, "Третья задача от того же пользователя")
    ]
    
    for user_id, task_text in tasks_data:
        await test_db.execute(
            'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2)',
            user_id, task_text
        )
    
    # Проверяем общее количество задач
    all_tasks = await test_db.fetch("SELECT * FROM tasks ORDER BY id")
    assert len(all_tasks) == 3
    
    # Проверяем задачи конкретного пользователя
    user_tasks = await test_db.fetch(
        "SELECT * FROM tasks WHERE user_id = $1 ORDER BY id",
        111
    )
    assert len(user_tasks) == 2
    assert user_tasks[0]['task_text'] == "Первая задача"
    assert user_tasks[1]['task_text'] == "Третья задача от того же пользователя"

@pytest.mark.asyncio
async def test_task_with_created_at(test_db):
    """Тест что created_at автоматически заполняется"""
    
    task_id = await test_db.fetchval(
        'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id',
        999, "Задача с временем создания"
    )
    
    task = await test_db.fetchrow(
        "SELECT * FROM tasks WHERE id = $1",
        task_id
    )
    
    assert task['created_at'] is not None
    # Проверяем что created_at примерно сейчас (в пределах минуты)
    import datetime
    assert abs(datetime.datetime.now() - task['created_at']) < datetime.timedelta(minutes=1)