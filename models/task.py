from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int
    text: str
    user_id: int = 1
    created_at: datetime = datetime.now()
    is_done: bool = False

    def __str__(self):
        return f"{self.id}: {self.text}"