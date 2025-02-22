// notification_service.ts
import axios from 'axios';

export class NotificationService {
  private telegramBotToken: string;
  private telegramChatId: string;

  constructor(telegramBotToken: string, telegramChatId: string) {
    this.telegramBotToken = telegramBotToken;
    this.telegramChatId = telegramChatId;
  }

  // Sends a message via Telegram Bot API.
  public async sendTelegramAlert(message: string): Promise<void> {
    const url = `https://api.telegram.org/bot${this.telegramBotToken}/sendMessage`;
    const payload = {
      chat_id: this.telegramChatId,
      text: message,
    };

    try {
      const response = await axios.post(url, payload);
      console.log('Telegram alert sent:', response.data);
    } catch (error) {
      console.error('Error sending Telegram alert:', error);
    }
  }
}
