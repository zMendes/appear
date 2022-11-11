import requests
from env import TELEGRAM_TOKEN, CHAT_ID, BOT_NAME
class TelegramHandler:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = CHAT_ID

    def send_message(self, message):
        url = "https://api.telegram.org/bot{}/sendMessage?chat_id=-{}&text={}".format(self.token, self.chat_id, message)
        return requests.get(url).status_code