

import sounddevice as sd, wavio, tempfile

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
