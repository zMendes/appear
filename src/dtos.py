from datetime import datetime

class Presence:
    name: str
    code: str
    phone_number: str
    chat_id: str
    timestamp: datetime = datetime.now()

class Identification:
    code: str
    name: str
    timestamp: datetime
    times: int = 0

    def __str__(self) -> str:
        return f"{self.name}, found {self.times} times"