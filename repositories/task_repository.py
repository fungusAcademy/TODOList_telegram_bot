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

# class InMemoryTaskRepository(ITaskRepository):
#     def __init__(self):
#         self._tasks = []
#         self._next_id = 1
    
#     async def add(self, task: Task) -> None:
#         task.id = self._next_id
#         self._next_id += 1
#         self._tasks.append(task)
    
#     async def get_all(self, user_id: int) -> List[Task]:
#         return [t for t in self._tasks if t.user_id == user_id]
    
#     async def delete(self, task_id: int) -> None:
#         # Добавить флаг, если заметки с таким номером не существует
#         self._tasks = [t for t in self._tasks if t.id != task_id]