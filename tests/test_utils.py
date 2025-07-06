import pytest
from voice_assistant.utils import intent_handler, rule_based_fallback
import builtins

# --- Tests for rule_based_fallback ---
def test_play_music_parsing():
    msg = "play Believer by Imagine Dragons"
    result = rule_based_fallback(msg)
    assert result["intent"] == "play_music"
    assert result["params"]["song"] == "believer"
    assert result["params"]["artist"] == "imagine dragons"

def test_set_alarm_parsing():
    msg = "set alarm for 9 AM"
    result = rule_based_fallback(msg)
    assert result["intent"] == "set_alarm"
    assert result["params"]["time"] == "9 am" or result["params"]["time"] == "9 AM"

def test_other_intent_fallback():
    msg = "tell me a joke"
    result = rule_based_fallback(msg)
    assert result["intent"] == "other_intent"

# --- Tests for intent_handler (with fake Mistral responses) ---
def test_valid_llm_intent():
    json_input = '{"intent":"play_music","params":{"artist":"The Beatles", "song":"Hey Jude"}}'
    msg = "Play Hey Jude by The Beatles"
    res = intent_handler(json_input, msg)
    assert "play_music" in res

def test_invalid_json_fallback():
    broken_json = '{"intent":"play_music", "params":'  # invalid
    msg = "play Believer by Imagine Dragons"
    res = intent_handler(broken_json, msg)
    assert "play_music" in res

def test_other_intent_triggers_fallback():
    json_input = '{"intent":"other_intent","params":{}}'
    msg = "play Believer by Imagine Dragons"
    res = intent_handler(json_input, msg)
    assert "play_music" in res
