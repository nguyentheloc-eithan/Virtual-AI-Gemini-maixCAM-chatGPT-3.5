import requests

class NotificationService:
    def __init__(self, telegram_bot_token: str, telegram_chat_id: str):
        """
        Initializes the NotificationService with Telegram credentials.
        :param telegram_bot_token: Your Telegram Bot API token.
        :param telegram_chat_id: The chat ID where alerts should be sent.
        """
        self.telegram_bot_token = telegram_bot_token
        self.telegram_chat_id = telegram_chat_id

    def send_telegram_alert(self, message: str) -> None:
        """
        Sends an alert message to a Telegram chat using the Telegram Bot API.
        :param message: The alert message to be sent.
        """
        url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
        payload = {
            "chat_id": self.telegram_chat_id,
            "text": message
        }

        try:
            response = requests.post(url, json=payload)
            response.raise_for_status()
            print("Telegram alert sent:", response.json())
        except Exception as e:
            print("Error sending Telegram alert:", e)
