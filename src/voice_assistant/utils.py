
import time
import sounddevice as sd, wavio, tempfile, scipy.signal

def record_audio(duration=10, out_fs=16000, channels=1) -> str:
    """
    Record from the default mic at 16 kHz mono and write out a WAV
    that Whisper will accept.
    """
    print(f"Recording {duration}s…")
    in_fs = 44100  # your mic’s native rate
    channels = 1

    data = sd.rec(int(duration * in_fs), samplerate=in_fs, channels=channels)
    time.sleep(1)
    sd.wait()

    if in_fs != out_fs:
        num_samples = int(len(data) * out_fs / in_fs)
        data = scipy.signal.resample(data, num_samples)

    wavio.write("input.wav", data, out_fs, sampwidth=2)
    return "input.wav"