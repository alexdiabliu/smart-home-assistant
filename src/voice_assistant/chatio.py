
from abc import ABC, abstractmethod
import ollama
import json


class ChatIO(ABC):
    @abstractmethod
    def ask(self, prompt: str) -> str:
        """Send a prompt to the chat model and return its reply."""
        pass


class OllamaChatIO(ChatIO):
    def __init__(self, model='mistral'):
        self.model = model

    def ask(self, messages):
        prompt = [{"role": "user", "content": messages}]

        return ollama.chat(model=self.model, messages=prompt)['message']['content']
    



# while True:
#     chat = OllamaChat(model='mistral')
#     message = input("You: ")
#     if message in ("exit","quit"): break
#     message = [{"role": "user", "content": message}]
#     reply = chat.ask(messages=message)
#     print("Bot:", reply)
