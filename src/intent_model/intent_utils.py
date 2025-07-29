
import joblib
import string
import spacy
import json
import copy
import os
import time

import json

from voice_assistant.chatio import OllamaChatIO
from alarm.alarm import Alarm

import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='sklearn')

this_dir = os.path.dirname(__file__)
encoder = joblib.load(os.path.join(this_dir, "label_encoder.pkl"))
vectorizer = joblib.load(os.path.join(this_dir, "tfidf_vectorizer.pkl"))
model = joblib.load(os.path.join(this_dir, "intent_classifier.pkl"))

nlp = spacy.load(os.path.join(this_dir, "param_classifier"))



def intent_handler(text: str) -> dict:
    """
    Handle the intent and parameters.
    This function can be extended to perform actions based on the intent.
    instructions example: {"intent":"play_music","params":{"artist":"Michael Jackson", "song":"Billie Jean"}}
    """
    # 1. Preprocess the input text
    processed_text = preprocess_text(text)

    # 2. Vectorize it using the loaded TF-IDF vectorizer
    vectorized_text = vectorizer.transform([processed_text])

    # 3. Predict the class index using the classifier
    predicted_intent = model.predict(vectorized_text)

    # 4. Decode the label using the label encoder
    predicted_label = encoder.inverse_transform(predicted_intent)[0]

    with open(os.path.join(this_dir, "actions.json"), 'r') as f:
        data = json.load(f)
    params = copy.deepcopy(data[predicted_label]['params']) # to not change actions.json
    

    if predicted_label in ("play_music", "set_alarm", "adjust_volume", "cancel_alarm"):
        # 5. Retrieve the parameters from the nlp model
        doc = nlp(text)
        for ent in doc.ents:
            print(ent.label_, ent.text)

        for ent in doc.ents:
            if ent.label_.lower() in params.keys():
                params[ent.label_] = ent.text

    # 6. Return the label + params dictionary
    return {"intent": predicted_label, "params": params}


def preprocess_text(text):
    # Lowercase
    text = text.lower()
    # Remove punctuation
    text = text.translate(str.maketrans('', '', string.punctuation))
    # Remove extra spaces
    text = ' '.join(text.split())
    return text



def execute_intent(intent: str, params: dict, message: str, music_player = None, alarm_scheduler = None) -> None:
    """
    Execute the intent based on the instructions.
    This function can be extended to perform actions based on the intent.
    """
    if intent == "play_music":
        time.sleep(1)
        music_player.play(artist=params.get('artist', ''), title=params.get('song', ''))
        return
    elif intent == "pause_music":
        if music_player:
            music_player.pause()
        else:
            print("Nothing is currently playing")
            return
    elif intent == "stop_music":
        if music_player:
            music_player.stop()
        else:
            print("Nothing is currently playing")
            return
    elif intent == "resume_music":
        if music_player:
            music_player.resume()
        else:
            print("Nothing is has been paused playing")
            return
    elif intent == "set_alarm":
        alarm = Alarm(time=params.get('time', ''), label=params.get('label', ''))
        alarm_scheduler.add_alarm(alarm)
    elif intent == "stop_alarm":
        alarm_scheduler.stop_alarms()
    elif intent == "cancel_alarm":
        alarm_scheduler.remove_alarm(time=params.get('time', ''), label=params.get('label', ''))
    elif intent == "adjust_volume":
        volume = params.get('volume', 0.3)
        music_player.change_volume(volume)
    elif intent == "other_intent":
        # chat = OllamaChatIO(model='mistral')
        # return chat.ask(messages=message)
        return None
    
if __name__ == "__main__":
    print(intent_handler("i am hungry"))