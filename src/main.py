
from voice_assistant.voiceio import VoiceIO, Pyttsx3VoiceIO, WhisperVoiceIO, CompositeVoiceIO, MockVoiceIO
from voice_assistant.chatio import OllamaChatIO
from intent_model.intent_utils import intent_handler, execute_intent


def command_loop(voice: VoiceIO):
    """
    Main command loop for the voice assistant.
    Having voice: VoiceIO requires a VoiceIO instance to be passed in.
    Continuously listens for commands and processes them.
    """

    botchat = OllamaChatIO(model='mistral')
    while True:
        text = voice.listen().lower()
        if any(word in text for word in ("exit", "quit", "bye", "goodbye")):
            voice.speak("Exiting the command loop. Goodbye!")
            break
        else:
            command_dict = intent_handler(text)
            # reply = botchat.ask(messages=text)
            print(command_dict)
            execution = execute_intent(intent=command_dict["intent"], params=command_dict["params"], message=text)
            voice.speak(execution)

if __name__ == "__main__":
    voice = MockVoiceIO()
    # voice = Pyttsx3VoiceIO()

    ears = MockVoiceIO()
    # ears = WhisperVoiceIO()

    system = CompositeVoiceIO(stt=ears, tts=voice)
    command_loop(system)