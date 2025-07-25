
from voice_assistant.voiceio import VoiceIO, Pyttsx3VoiceIO, WhisperVoiceIO, AWSVoiceIO, CompositeVoiceIO, MockVoiceIO
from voice_assistant.chatio import OllamaChatIO
from intent_model.intent_utils import intent_handler, execute_intent
from music_player.music_player import MusicPlayer

def command_loop(voice: VoiceIO):
    """
    Main command loop for the voice assistant.
    Having voice: VoiceIO requires a VoiceIO instance to be passed in.
    Continuously listens for commands and processes them.
    """

    botchat = OllamaChatIO(model='mistral')
    while True:
        music_player = MusicPlayer()
        
        # Wake Word
        wake_phrase = voice.listen(duration=2).lower()
        if any(keyword in wake_phrase for keyword in ["smartrise", "smart rise", "jarvis"]):
            voice.speak("Yes?")

            # full command
            text = voice.listen(duration=10).lower()
            if any(word in text for word in ("exit", "quit", "bye", "goodbye")):
                voice.speak("Exiting the command loop. Goodbye!")
                break
            else:
                command_dict = intent_handler(text)
                # reply = botchat.ask(messages=text)
                print(command_dict)
                execution = execute_intent(intent=command_dict["intent"], params=command_dict["params"], message=text, music_player=music_player)
                voice.speak(execution)

if __name__ == "__main__":
    # voice = MockVoiceIO()
    voice = Pyttsx3VoiceIO()

    # ears = MockVoiceIO()
    # ears = WhisperVoiceIO()
    ears = AWSVoiceIO(public_ip="35.183.23.203")

    system = CompositeVoiceIO(stt=ears, tts=voice)
    command_loop(system)