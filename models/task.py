from dataclasses import dataclass
from datetime import datetime

@dataclass
class Task:
    id: int | None = None
    user_id: int | None = None
    task_text: str | None = None
    created_at: datetime | None = datetime.now()
    is_done: bool = False

    def __init__(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)