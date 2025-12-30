import os
os.environ["DISABLE_TF_SIGNAL_HANDLER"] = "1"

import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import json
import random

# Download tokenizer safely
nltk.download("punkt", quiet=True)
nltk.download("punkt_tab", quiet=True)


lemmatizer = WordNetLemmatizer()

# -------------------------
# 🔥 GLOBAL VARIABLES (lazy loaded)
# -------------------------
model = None
intents = None
words = None
classes = None


def load_resources_once():
    """
    Load ML model and resources only once,
    AFTER the server has started.
    """
    global model, intents, words, classes

    if model is None:
        model = tf.keras.models.load_model("ds_chatbot_model.h5")

        with open("job_intents.json", encoding="utf-8") as f:
            intents = json.load(f)

        words = pickle.load(open("words.pkl", "rb"))
        classes = pickle.load(open("classes.pkl", "rb"))


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
    load_resources_once()  # ✅ lazy load here

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
    load_resources_once()  # ✅ safe even if called multiple times
    ints = predict_class(msg)
    return getResponse(ints, intents)
