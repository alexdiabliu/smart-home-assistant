
from abc import ABC, abstractmethod
from pywhispercpp.model import Model
import pyttsx3

from voice_assistant.utils import record_audio


class VoiceIO(ABC):
    """
    Abstract base class for voice input/output operations.
    Note: This class is abstract and should not be instantiated directly.

    Subclasses must implement the `listen` and `speak` methods
    """

    @abstractmethod
    def listen(self) -> str:
        """Return recognized speech as text."""
        pass

    @abstractmethod
    def speak(self, text: str) -> None:
        """Takes a text string and “plays” it back."""
        pass


class MockVoiceIO(VoiceIO):
    """
    Mock implementation of VoiceIO for local development/testing purposes.
    """

    def listen(self) -> str:
        """Simulate listening by returning a fixed string."""
        return input("Mock Listen - Type a command: ")

    def speak(self, text: str) -> None:
        """Print the text to simulate speaking."""
        print(f"Speaking: {text}")


class WhisperVoiceIO(VoiceIO):
    """
    Implementation of VoiceIO using the Whisper ASR model.
    """
    def __init__(self, model_name: str = 'base.en'):
        """
        Initialize the Whisper model.
        :param model_name: Name of the Whisper model to use.
        """
        self.model = Model(model_name, print_realtime=False, print_progress=False)

    def listen(self) -> str:
        """Listen for audio input and return the transcribed text."""
        # If an audio file is provided, use it; otherwise, use the default audio file.
        path = record_audio(duration=2)
        
        segments = self.model.transcribe(path)
        return " ".join(segment.text for segment in segments)

    def speak(self, text: str) -> None:
        raise RuntimeError("WhisperVoiceIO is STT-only; use CompositeVoiceIO to combine STT+TTS")



class Pyttsx3VoiceIO(VoiceIO):
    def __init__(self):
        self.engine = pyttsx3.init()
    
    def listen(self, text: str) -> None:
        raise RuntimeError("Pyttsx3VoiceIO is TTS-only; use CompositeVoiceIO to combine STT+TTS")

    def speak(self, text: str) -> None:
        """Use pyttsx3 to speak the text."""
        self.engine.say(text)
        self.engine.runAndWait()
        return None


class CompositeVoiceIO(VoiceIO):
    """
    Composite implementation of VoiceIO that combines multiple voice I/O methods.
    This allows for flexibility in choosing the underlying implementation.
    """
    def __init__(self, stt: VoiceIO, tts: VoiceIO):
        self.tts = tts
        self.stt = stt

    def listen(self) -> str:
        """Use the selected speech-to-text engine to listen for commands."""
        return self.stt.listen()

    def speak(self, text: str) -> None:
        """Use the selected text-to-speech engine to speak the text."""
        return self.tts.speak(text)

