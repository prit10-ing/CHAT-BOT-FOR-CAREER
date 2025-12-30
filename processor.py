import os
import threading

# -------------------------
# ✅ FIX NLTK DATA PATH (CRITICAL FOR RENDER)
# -------------------------
BASE_DIR = os.getcwd()
NLTK_DATA_DIR = os.path.join(BASE_DIR, "nltk_data")
os.makedirs(NLTK_DATA_DIR, exist_ok=True)

os.environ["NLTK_DATA"] = NLTK_DATA_DIR
os.environ["DISABLE_TF_SIGNAL_HANDLER"] = "1"

import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import json
import random

# -------------------------
# ✅ DOWNLOAD REQUIRED NLTK FILES
# -------------------------
nltk.download("punkt", download_dir=NLTK_DATA_DIR, quiet=True)
nltk.download("punkt_tab", download_dir=NLTK_DATA_DIR, quiet=True)
nltk.download("wordnet", download_dir=NLTK_DATA_DIR, quiet=True)
nltk.download("omw-1.4", download_dir=NLTK_DATA_DIR, quiet=True)  # 🔥

lemmatizer = WordNetLemmatizer()

# -------------------------
# 🔥 GLOBAL VARIABLES (LAZY LOADED)
# -------------------------
model = None
intents = None
words = None
classes = None
_load_lock = threading.Lock()  # 🔥


def load_resources_once():
    global model, intents, words, classes

    if model is None:
        with _load_lock:  # 🔥 prevent race condition
            if model is None:
                model = tf.keras.models.load_model("ds_chatbot_model.h5")

                with open("job_intents.json", encoding="utf-8") as f:
                    intents = json.load(f)

                with open("words.pkl", "rb") as f:
                    words = pickle.load(f)

                with open("classes.pkl", "rb") as f:
                    classes = pickle.load(f)


def clean_up_sentence(sentence):
    sentence_words = nltk.word_tokenize(sentence)
    return [lemmatizer.lemmatize(word.lower()) for word in sentence_words]


def bow(sentence, words):
    sentence_words = clean_up_sentence(sentence)
    bag = [0] * len(words)
    for i, w in enumerate(words):
        if w in sentence_words:
            bag[i] = 1
    return np.array(bag)


def predict_class(sentence, error_threshold=0.25):
    load_resources_once()

    p = bow(sentence, words)
    p = np.array([p])

    res = model.predict(p, verbose=0)[0]

    results = [[i, r] for i, r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)

    return [{"intent": classes[i], "probability": float(r)} for i, r in results]


def getResponse(ints, intents_json):
    if not ints:
        return "Sorry, I didn't understand that. Can you rephrase?"

    tag = ints[0]["intent"]
    for i in intents_json["intents"]:
        if i["tag"] == tag:
            return random.choice(i["responses"])

    return "I couldn't find a matching response."


def chatbot_response(msg):
    load_resources_once()
    ints = predict_class(msg)
    return getResponse(ints, intents)
