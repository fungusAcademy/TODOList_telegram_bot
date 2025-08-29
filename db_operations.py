from database import get_connection

async def add_task_to_db(user_id, task_text):
    """Добавление задачи в базу"""
    conn = await get_connection()
    try:
        task_id = await conn.fetchval(
            'INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id',
            user_id, task_text
        )
        return task_id
    finally:
        await conn.close()

async def get_user_tasks_from_db(user_id):
    """Получение задач пользователя"""
    conn = await get_connection()
    try:
        tasks = await conn.fetch(
            'SELECT id, task_text, created_at FROM tasks WHERE user_id = $1 ORDER BY created_at DESC',
            user_id
        )
        return tasks
    finally:
        await conn.close()