import asyncpg
from repositories.task_repository import ITaskRepository
from models.task import Task
from typing import List

class PostgresTaskRepository(ITaskRepository):
    def __init__(self, pool: asyncpg.Pool):
        self.pool = pool
    
    async def get_user_tasks(self, user_id: int) -> List[Task]:
        async with self.pool.acquire() as conn:
            records = await conn.fetch(
                "SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC",
                user_id
            )
            return [Task(**dict(record)) for record in records]
    
    # Add: use correct task id's when creating new task
    async def create_task(self, user_id: int, task_text: str) -> int:
        async with self.pool.acquire() as conn:
            task_id = await conn.fetchval(
                "INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id",
                user_id, task_text
            )
            return task_id
        
    # Add: Delete function
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        async with self.pool.acquire() as conn:
            result = await conn.execute(
            "DELETE FROM tasks WHERE id = $1 AND user_id = $2",
            task_id, user_id
            )
        return result.split()[-1] == '1'