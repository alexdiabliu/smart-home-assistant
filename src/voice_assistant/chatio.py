
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

    def ask(self, messages, classify=False):
        with open('voice_assistant/actions.json', 'r') as f:
            ACTIONS = json.load(f)
        
        CLASSIFY = f"You are an assistant that maps user requests to one of these intents: {json.dumps(ACTIONS, indent=2)}" + """
        Respond ONLY with the intent key and any parameters in JSON, like:
        {"intent":"play_music","params":{"artist":"The Beatles", "song":"Hey Jude"}}
        """
        if classify:
            prompt = [{"role": "system", "content": CLASSIFY}, {"role": "user", "content": messages}]
        else:
            prompt = [{"role": "user", "content": messages}]

        return ollama.chat(model=self.model, messages=prompt)['message']['content']
    



# while True:
#     chat = OllamaChat(model='mistral')
#     message = input("You: ")
#     if message in ("exit","quit"): break
#     message = [{"role": "user", "content": message}]
#     reply = chat.ask(messages=message)
#     print("Bot:", reply)
