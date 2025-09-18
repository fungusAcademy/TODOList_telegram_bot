from abc import ABC, abstractmethod
from typing import List
from models.task import Task

class ITaskRepository(ABC):
    @abstractmethod
    async def create_task(self, user_id: int, text: str) -> int:
        pass

    @abstractmethod
    async def get_user_tasks(self, user_id: int) -> List[Task]:
        pass
    
    @abstractmethod
    async def delete_task(self, user_id: int, task_id: int) -> bool:
        pass