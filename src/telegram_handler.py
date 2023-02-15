import requests
import json
class TelegramHandler:
    def __init__(self):
        with open("src/config.json") as f:
            config = json.load(f)["telegram"]
        self.token = config["token"]
        self.chat_id = config["chat_id"]

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
