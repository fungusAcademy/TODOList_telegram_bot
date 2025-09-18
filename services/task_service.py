from repositories.task_repository import ITaskRepository
from models.task import Task

class TaskService:
    def __init__(self, task_repository: ITaskRepository):
        self.task_repository = task_repository

    async def create_task(self, user_id: int, text: str) -> int:
        if not text.strip():
            raise TypeError("Task text cannot be empty")
        return await self.task_repository.create_task(user_id, text)
    
    async def get_user_tasks(self, user_id: int) -> list[Task]:
        return await self.task_repository.get_user_tasks(user_id)   

    async def delete_task(self, user_id: int, task_id: int) -> bool:
        return await self.task_repository.delete_task(user_id, task_id)
    
