import pytest
from intent_model.intent_utils import intent_handler
import builtins


# --- Tests for intent_handler ---
def test_valid_intent():
    msg = "Play despacito by luis fonsi"
    res = intent_handler(msg)
    print(res)
    assert {'intent': 'play_music', 'params': {'artist': 'luis fonsi', 'song': 'despacito'}} == res

