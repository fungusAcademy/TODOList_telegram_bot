import asyncpg
from repositories.task_repository import ITaskRepository
from models.task import Task
from database.pool import db_pool
from typing import List

class PostgresTaskRepository(ITaskRepository):
    def __init__(self):
        """Now we dont store pool here.
        Instead we use global one"""
        pass
    
    async def get_user_tasks(self, user_id: int) -> List[Task]:
        async with db_pool.acquire() as conn:
            try:
                records = await conn.fetch(
                    "SELECT * FROM tasks WHERE user_id = $1 ORDER BY created_at DESC",
                    user_id
                )
                return [Task(**dict(record)) for record in records]
            except asyncpg.PostgresError as e:
                print(f"Database error in get_user_tasks: {e}")
                raise
    
    # TO Add: use correct task id's when creating new task
    async def create_task(self, user_id: int, task_text: str) -> int:
        async with db_pool.acquire() as conn:
            try:
                # start transaction
                async with conn.transaction():
                    # Add user if not present already
                    await conn.execute(
                        """INSERT INTO users (user_id) VALUES ($1) 
                           ON CONFLICT (user_id) DO NOTHING""",
                           user_id
                    )

                # Create task
                task_id = await conn.fetchval(
                        "INSERT INTO tasks (user_id, task_text) VALUES ($1, $2) RETURNING id",
                        user_id, task_text
                    )
                    
                return task_id
            except asyncpg.PostgresError as e:
                print(f"Database error in create_task: {e}")
                raise
        
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        """Delete task from DB.
        Return True if succesful
        Return False if no such task"""
        async with db_pool.acquire() as conn:
            try:
                result = await conn.execute(
                    "DELETE FROM tasks WHERE id = $1 AND user_id = $2",
                    task_id, user_id
                )

                return result.split()[-1] == '1'
            except asyncpg.PostgresError as e:
                print(f"Database error in delete_task: {e}")
                raise