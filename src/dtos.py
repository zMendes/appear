from dataclasses import dataclass
from datetime import datetime

@dataclass
class Presence:
    name: str
    code: str
    phone_number: str
    chat_id: str
    timestamp: datetime = datetime.now()

@dataclass
class Identification:
    code: str
    name: str
    last_appearence: datetime
    times: int = 0

    def __str__(self) -> str:
        return f"{self.name}, found {self.times} times"