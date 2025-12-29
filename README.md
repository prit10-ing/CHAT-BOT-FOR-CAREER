🤖 AI Chatbot with Flask, TensorFlow & Browser Speech

This project is a web-based AI chatbot built using Flask, TensorFlow (Keras), and NLTK.
It supports real-time chat, intent-based responses, and browser text-to-speech for voice replies.

The chatbot is trained on a custom intents dataset and responds intelligently based on user input.

🚀 Features

🧠 Intent-based chatbot using TensorFlow (.h5 model)

🗣️ Browser Text-to-Speech (TTS) for bot responses

🌐 Web interface using HTML, CSS, JavaScript

⚡ Fast responses (model loaded once in memory)

🛡️ Stable setup for Windows + Python 3.12

🔤 NLP preprocessing using NLTK (punkt tokenizer)





⚙️ Tech Stack

Backend: Python, Flask

ML / NLP: TensorFlow (Keras), NLTK

Frontend: HTML, CSS, JavaScript

Speech: Browser SpeechSynthesis API



📦 Requirements

Install the required dependencies:

pip install flask tensorflow nltk numpy


🔧 NLTK Setup

This project uses only the punkt tokenizer.

import nltk
nltk.download('punkt')




▶️ How to Run the Project

1️⃣ Start the Flask server

Run the application using:
python app.py


2️⃣ Open in Browser

Visit: http://127.0.0.1:5000


💬 How It Works

User enters a message in the browser

Message is sent to Flask /chatbot route

Text is tokenized using NLTK punkt

Input is converted to Bag of Words

TensorFlow model predicts intent

Response is selected from job_intents.json

Bot message is returned + spoken using browser TTS



🔊 Browser Speech (Text-to-Speech)

The chatbot uses the Web Speech API:

Speech is unlocked on first user interaction

Bot responses are spoken automatically

No backend TTS required (browser handles it)


📄 License

This project is for learning and personal use.
You are free to modify and extend it.

🙌 Acknowledgements

TensorFlow & Keras

NLTK

Flask

Web Speech API