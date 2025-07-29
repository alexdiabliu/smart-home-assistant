
from voice_assistant.voiceio import VoiceIO, Pyttsx3VoiceIO, WhisperVoiceIO, AWSVoiceIO, CompositeVoiceIO, MockVoiceIO
from voice_assistant.chatio import OllamaChatIO
from intent_model.intent_utils import intent_handler, execute_intent
from music_player.music_player import MusicPlayer
from alarm.alarm import AlarmScheduler

def command_loop(voice: VoiceIO):
    """
    Main command loop for the voice assistant.
    Having voice: VoiceIO requires a VoiceIO instance to be passed in.
    Continuously listens for commands and processes them.
    """

    botchat = OllamaChatIO(model='mistral')
    music_player = MusicPlayer()
    alarm_clock = AlarmScheduler(music_player=music_player)
    temp_paused = False

    while True:
        alarm_clock.check_alarms()
        # Wake Word
        wake_phrase = voice.listen(duration=2, live=False).lower()
        if any(keyword in wake_phrase for keyword in ["smartrise", "smart rise", "jarvis"]):
            # pause music temporarily for better user listening
            if music_player.is_playing:
                temp_paused = True
                music_player.pause()
            
            voice.speak("Yes?")

            # full command
            text = voice.listen(duration=10).lower()
            if any(word in text for word in ("exit", "quit", "bye", "goodbye")):
                voice.speak("Exiting the command loop. Goodbye!")
                break
            else:
                if temp_paused:
                    music_player.resume()
                    temp_paused = False

                command_dict = intent_handler(text)
                # reply = botchat.ask(messages=text)
                print(command_dict)
                execution = execute_intent(intent=command_dict["intent"], params=command_dict["params"], message=text, music_player=music_player, alarm_scheduler=alarm_clock)
                voice.speak(execution)

if __name__ == "__main__":
    # voice = MockVoiceIO()
    voice = Pyttsx3VoiceIO()

    # ears = MockVoiceIO()
    # ears = WhisperVoiceIO()
    ears = AWSVoiceIO(public_ip="3.99.164.60")

    system = CompositeVoiceIO(stt=ears, tts=voice)
    command_loop(system)