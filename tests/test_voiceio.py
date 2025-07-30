

"""
Test cases for MockVoiceIO class in voiceio module.
Note: PyTest looks for files that start with test_ or end with _test.py
"""

import builtins # contains the input() function
import pytest
import voice_assistant.voiceio as vi
from types import SimpleNamespace

# monkeypatch lets you temporarily override attributes like input() with another function for the duration of a test
# capsys is a pytest fixture that captures stdout/stderr
def test_mock_listen_and_speak(monkeypatch, capsys):
    """Test the MockVoiceIO class for listening and speaking functionality."""
    monkeypatch.setattr(builtins, 'input', lambda prompt='': "hello world")
    # 1) input() was replaced with anonymous lambda function with any prompt, returning "hello world"
    mock = vi.MockVoiceIO()

    # 2) verify listen()
    result = mock.listen(duration=2, live=False)
    assert result == "hello world"

    # 3) verify speak() prints the right prefix
    mock.speak("foo")
    captured = capsys.readouterr()
    assert "Speaking: foo" in captured.out

def test_whisper_listen(monkeypatch):
    """Test the WhisperVoiceIO class for listening functionality."""
    whisper = vi.WhisperVoiceIO(model_name='base.en')
    monkeypatch.setattr(vi, 'record_audio', lambda duration=2: "Recording.mp3")

    fake_segments = [SimpleNamespace(text="play"), SimpleNamespace(text="music")]
    monkeypatch.setattr(whisper.model, 'transcribe', lambda path: fake_segments)
    transcription = whisper.listen(duration=2).lower()
    assert "play music" in transcription


def test_composite(monkeypatch, capsys):
    """Test the CompositeVoiceIO class for both listening and speaking functionality."""
    ears = voice = vi.MockVoiceIO()
    comp = vi.CompositeVoiceIO(stt=ears, tts=voice)
    commands = ['test', 'play music', 'exit']

    for command in commands:
        monkeypatch.setattr(builtins, 'input', lambda prompt='': command)
        result = comp.listen(duration=2).lower()
        assert command in result
    
        comp.speak(command)
        captured = capsys.readouterr()
        assert f"Speaking: {command}" in captured.out