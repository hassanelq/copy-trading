# notifier.py

import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID
from utils import setup_logger

logger = setup_logger("notifier")


class Notifier:
    def __init__(self):
        self.token = TELEGRAM_BOT_TOKEN
        self.chat_id = TELEGRAM_CHAT_ID
        self.base_url = f"https://api.telegram.org/bot{self.token}/sendMessage"

    def send(self, message: str):
        if not self.token or not self.chat_id:
            logger.warning("Telegram not configured. Skipping notification.")
            return

        try:
            payload = {
                "chat_id": self.chat_id,
                "text": message,
                "parse_mode": "Markdown",
            }
            response = requests.post(self.base_url, data=payload)
            if response.status_code != 200:
                logger.error(f"Telegram error: {response.text}")
        except Exception as e:
            logger.error(f"Failed to send Telegram message: {e}")
