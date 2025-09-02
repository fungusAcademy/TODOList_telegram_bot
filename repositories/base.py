# src/repositories/base.py
from abc import ABC, abstractmethod
from typing import List

class IRepository(ABC):
    @abstractmethod
    async def get_by_id(self, id: int):
        pass
    
    @abstractmethod
    async def get_all(self) -> List:
        pass
    
    @abstractmethod
    async def create(self, entity) -> int:
        pass
    
    @abstractmethod
    async def update(self, entity):
        pass
    
    @abstractmethod
    async def delete(self, id: int):
        pass