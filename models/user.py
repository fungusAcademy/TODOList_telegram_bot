from dataclasses import dataclass
from datetime import datetime

@dataclass
class User:
    user_id: int
    username: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    created_at: datetime | None = datetime.now()