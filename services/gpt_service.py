import requests
import logging
from typing import List, Dict

logging.basicConfig(level=logging.INFO)

class GPTService:
    def __init__(self, api_key: str, api_url: str = "https://api.openai.com/v1/chat/completions", system_message: str = "You are a helpful virtual assistant."):
      
        self.api_key = api_key
        self.api_url = api_url
        # Maintain a conversation history as a list of message dicts.
        self.conversation: List[Dict[str, str]] = [{"role": "system", "content": system_message}]
    
    def reset_conversation(self):
        """
        Resets the conversation context (keeping only the system message).
        """
        system_msg = self.conversation[0]
        self.conversation = [system_msg]
        logging.info("Conversation context reset.")
    
    def append_message(self, role: str, content: str):
        """
        Appends a message to the conversation history.
        :param role: The role of the message sender (system, user, or assistant).
        :param content: The message content.
        """
        self.conversation.append({"role": role, "content": content})
    
    def get_assistant_response(self, prompt: str, max_retries: int = 3) -> str:
        """
        Sends a prompt to the ChatGPT API and returns the assistant's response.
        Maintains conversation context across calls.
        :param prompt: The user's message.
        :param max_retries: Maximum number of retries for the API call.
        :return: The assistant's reply.
        """
        # Append user's prompt to conversation
        self.append_message("user", prompt)
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.api_key}"
        }
        
        payload = {
            "model": "gpt-3.5-turbo",
            "messages": self.conversation,
            "temperature": 0.7,
        }
        
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.post(self.api_url, headers=headers, json=payload, timeout=15)
                response.raise_for_status()
                data = response.json()
                assistant_reply = data["choices"][0]["message"]["content"].strip()
                # Append assistant reply to conversation history
                self.append_message("assistant", assistant_reply)
                logging.info("Assistant reply received successfully.")
                return assistant_reply
            except requests.exceptions.RequestException as e:
                logging.error(f"Attempt {attempt} - Error calling ChatGPT API: {e}")
                if attempt == max_retries:
                    # Append a default error message to conversation to maintain flow
                    error_message = "I'm sorry, I couldn't process your request at this time."
                    self.append_message("assistant", error_message)
                    return error_message
