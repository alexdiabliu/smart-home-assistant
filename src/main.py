
from voice_assistant.voiceio import VoiceIO, Pyttsx3VoiceIO, WhisperVoiceIO, CompositeVoiceIO, MockVoiceIO


def command_loop(voice: VoiceIO):
    """
    Main command loop for the voice assistant.
    Having voice: VoiceIO requires a VoiceIO instance to be passed in.
    Continuously listens for commands and processes them.
    """
    while True:
        text = voice.listen().lower()
        if "play music" in text:
            voice.speak("Playing music now.")
        elif "exit" in text or "quit" in text:
            voice.speak("Exiting the command loop. Goodbye!")
            break
        else:
            voice.speak(f"You said: {text}. I didn't understand that command.")


if __name__ == "__main__":
    # voice = MockVoiceIO()
    voice = Pyttsx3VoiceIO()

    # ears = MockVoiceIO()
    ears = WhisperVoiceIO()

    system = CompositeVoiceIO(stt=ears, tts=voice)
    command_loop(system)