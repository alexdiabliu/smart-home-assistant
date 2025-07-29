
import numpy as np
import sounddevice as sd
import queue
import time
import wavio

SAMPLERATE = 44100
BLOCKSIZE = 256
CHANNELS = 1
SILENCE_THRESHOLD = 0.01
SILENCE_TIMEOUT = 2.0  # seconds

q = queue.Queue()
while not q.empty():
    q.get()

def audio_callback(indata, frames, time_info, status):

    q.put(indata.copy())

def record_until_silence():

    print("🎙️ Listening... Start speaking.")

    audio = []
    last_spoke = time.time()

    with sd.InputStream(callback=audio_callback, samplerate=SAMPLERATE, channels=CHANNELS, blocksize=BLOCKSIZE):
        while True:
            block = q.get()
            rms = np.sqrt(np.mean(block**2))
            audio.append(block)

            if rms > SILENCE_THRESHOLD:
                last_spoke = time.time()

            if time.time() - last_spoke > SILENCE_TIMEOUT:
                print("🛑 Detected end of speech.")
                break

    full_audio = np.concatenate(audio, axis=0)
    wavio.write("output.wav", full_audio, SAMPLERATE, sampwidth=2)
    return "output.wav"

