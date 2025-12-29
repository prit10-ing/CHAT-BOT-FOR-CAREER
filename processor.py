import os
os.environ["DISABLE_TF_SIGNAL_HANDLER"] = "1"

import nltk
import tensorflow as tf
from nltk.stem import WordNetLemmatizer
import pickle
import numpy as np
import json
import random

# ONLY punkt (as requested)
nltk.download('punkt', quiet=True)

# Load model and data ONCE
model = tf.keras.models.load_model('ds_chatbot_model.h5')

intents = json.loads(open('job_intents.json', encoding='utf-8').read())
words = pickle.load(open('words.pkl', 'rb'))
classes = pickle.load(open('classes.pkl', 'rb'))

lemmatizer = WordNetLemmatizer()

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
    p = bow(sentence, words)
    p = np.array([p])  # ensure correct shape

    res = model.predict(p, verbose=0)[0]

    results = [[i, r] for i, r in enumerate(res) if r > error_threshold]
    results.sort(key=lambda x: x[1], reverse=True)

    return [{"intent": classes[i], "probability": float(r)} for i, r in results]

def getResponse(ints, intents_json):
    if not ints:
        return "Sorry, I didn't understand that. Can you rephrase?"

    tag = ints[0]['intent']
    for i in intents_json['intents']:
        if i['tag'] == tag:
            return random.choice(i['responses'])

    return "I couldn't find a matching response."

def chatbot_response(msg):
    ints = predict_class(msg)
    return getResponse(ints, intents)
