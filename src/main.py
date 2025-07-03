
from voice_assistant.voiceio import VoiceIO, Pyttsx3VoiceIO, WhisperVoiceIO, CompositeVoiceIO, MockVoiceIO
from voice_assistant.chatio import OllamaChatIO
from voice_assistant.utils import intent_handler


def command_loop(voice: VoiceIO):
    """
    Main command loop for the voice assistant.
    Having voice: VoiceIO requires a VoiceIO instance to be passed in.
    Continuously listens for commands and processes them.
    """

    botchat = OllamaChatIO(model='mistral')
    while True:
        text = voice.listen().lower()
        if "exit" in text or "quit" in text:
            voice.speak("Exiting the command loop. Goodbye!")
            break
        else:
            reply = botchat.ask(messages=text, classify=True)
            voice.speak(reply)
            execution = intent_handler(reply, text)
            voice.speak(execution)

if __name__ == "__main__":
    voice = MockVoiceIO()
    # voice = Pyttsx3VoiceIO()

    ears = MockVoiceIO()
    # ears = WhisperVoiceIO()

    system = CompositeVoiceIO(stt=ears, tts=voice)
    command_loop(system)