import requests
from env import TELEGRAM_TOKEN, CHAT_ID, BOT_NAME
class TelegramHandler:
    def __init__(self):
        self.token = TELEGRAM_TOKEN
        self.chat_id = CHAT_ID

    def send_message(self, message, chat_id=None, retry=True):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"

        payload = {
            "text": message,
            "disable_web_page_preview": False,
            "disable_notification": False,
            "reply_to_message_id": None,
            "chat_id": "-"+self.chat_id if chat_id is None else chat_id,
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json"
        }

        response = requests.post(url, json=payload, headers=headers)
        if response.ok != True:
            print("Error sending message")
            print(response.text)
            if retry:
                self.send_message(message, retry=False)
