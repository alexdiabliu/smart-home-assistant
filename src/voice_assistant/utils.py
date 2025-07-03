

import sounddevice as sd, wavio, tempfile
import json
from music_player.music_player import play_music
from voice_assistant.chatio import OllamaChatIO

def record_audio(duration=2, fs=16000, channels=1) -> str:
    """
    Record from the default mic at 16 kHz mono and write out a WAV
    that Whisper will accept.
    """
    print(f"Recording {duration}s @ {fs}Hz, {channels} channel(s)…")
    data = sd.rec(int(duration * fs), samplerate=fs, channels=channels)
    sd.wait()

    tmp = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
    wavio.write(tmp.name, data, fs, sampwidth=2)
    return tmp.name

def intent_handler(instructions: dict, message: str) -> None:
    """
    Handle the intent and parameters.
    This function can be extended to perform actions based on the intent.
    instructions example: {"intent":"play_music","params":{"artist":"Michael Jackson", "song":"Billie Jean"}}
    """
    try:
        parsed = json.loads(instructions)
    except json.JSONDecodeError:
        print("LLM failed to return valid JSON. Falling back to rules")
        instructions = rule_based_fallback(message)
        if isinstance(instructions, str):
            parsed = json.loads(instructions)
        else:
            parsed = instructions

    
    intent = parsed.get("intent")
    params = parsed.get("params", {})

    if intent == "other_intent":
        print("No intent matched, falling back to rule-based parsing")
        parsed = rule_based_fallback(message)
        intent = parsed.get("intent").strip()
        params = parsed.get("params", {})
        print(f"Intent: {intent}, Params: {params}")

    if intent == "play_music":
        return play_music(params=params)
    elif intent == "other_intent":
        chat = OllamaChatIO(model='mistral')
        return chat.ask(messages=message, classify=False)
    

def rule_based_fallback(message: str) -> str:
    msg = message.lower()
    if "play" in msg and "by" in msg:
        # naive parser for "play X by Y"
        song, artist = msg.split("play")[1].split("by")
        return {'intent':'play_music','params':{'artist':artist.strip(), 'song':song.strip()}}
    elif "set alarm" in msg:
        time = msg.split("set alarm for")[-1].strip()
        return {'intent':'set_alarm','params':{'time':time, 'label':""}}
    else:
        return {'intent':'other_intent'}
