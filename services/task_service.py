from repositories.task_repository import InMemoryTaskRepository
from models.task import Task

class TaskService:
    def __init__(self, repository: InMemoryTaskRepository):
        self._repository = repository
    
    async def create_task(self, text: str, user_id: int) -> Task:
        task = Task(id=0, text=text, user_id=user_id)
        await self._repository.add(task)
        return task
    
    async def delete_task(self, id: int) -> None:
        await self._repository.delete(id)
    
    async def get_user_tasks(self, user_id: int) -> list[Task]:
        return await self._repository.get_all(user_id)