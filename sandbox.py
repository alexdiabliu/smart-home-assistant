

from utils import record_audio
import os

path = record_audio(duration=2)
os.startfile(path)  # Open the recorded file with the default application
print("Recorded file:", path)
