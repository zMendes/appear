from dataclasses import dataclass
from datetime import datetime
import numpy as np

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

@dataclass
class RegistrationData:
    def __init__(self, name: str, id: str, telegram_chat_id: str, image: np.ndarray, phone_number: str):
        self.name = name
        self.id = id
        self.telegram_chat_id = telegram_chat_id
        self.image = image
        self.phone_number = phone_number
    
    def __str__(self):
        return f"Name: {self.name}, Id: {self.id}, Telegram Chat Id: {self.telegram_chat_id}, Image: {self.image is not None}"