from datetime import datetime

class Presence:
    def __init__(self, name, code, phone_number, chat_id):
        self.name = name
        self.code = code
        self.phone_number = phone_number
        self.chat_id = chat_id
        self.timestamp = datetime.now()
