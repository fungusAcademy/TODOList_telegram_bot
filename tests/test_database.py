import pytest
import asyncpg

@pytest.mark.asyncio
async def test_add_task_to_test_db(test_db):
    """TEST adding task to DB"""
    
    # 1. check if DB is empty
    initial_tasks = await test_db.fetch("SELECT * FROM tasks")
    assert len(initial_tasks) == 0
    
    # 2. add task directly to test DB
    task_id = await test_db.fetchval(
        'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id',
        123, "Test task from pytest"
    )
    
    # 3. Check if task is added
    assert task_id is not None
    assert isinstance(task_id, int)
    
    # 4. Check if data is in DB
    tasks = await test_db.fetch("SELECT * FROM tasks")
    assert len(tasks) == 1
    
    # 5. Check task content
    task = tasks[0]
    assert task['id'] == task_id
    assert task['user_id'] == 123
    assert task['task_text'] == "Test task from pytest"
    assert task['created_at'] is not None

@pytest.mark.asyncio
async def test_multiple_tasks(test_db):
    """TEST adding several tasks"""
    
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
    
    # check number of tasks
    all_tasks = await test_db.fetch("SELECT * FROM tasks ORDER BY id")
    assert len(all_tasks) == 3
    
    # check tasks of specific user
    user_tasks = await test_db.fetch(
        "SELECT * FROM tasks WHERE user_id = $1 ORDER BY id",
        111
    )
    assert len(user_tasks) == 2
    assert user_tasks[0]['task_text'] == "Первая задача"
    assert user_tasks[1]['task_text'] == "Третья задача от того же пользователя"

@pytest.mark.asyncio
async def test_task_with_created_at(test_db):
    """TEST that created_at is assigned by default and is correct time"""
    
    task_id = await test_db.fetchval(
        'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id',
        999, "Задача с временем создания"
    )
    
    task = await test_db.fetchrow(
        "SELECT * FROM tasks WHERE id = $1",
        task_id
    )
    
    assert task['created_at'] is not None
    # Check if created_at is approximately correct (1 minute diff)
    import datetime
    assert abs(datetime.datetime.now() - task['created_at']) < datetime.timedelta(minutes=1)