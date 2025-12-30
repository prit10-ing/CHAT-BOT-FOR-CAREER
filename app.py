from flask import Flask, render_template, jsonify, request
import processor
import os

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")

@app.route("/chatbot", methods=["POST"])
def chatbot_response():
    user_question = request.form.get("question", "").strip()

    if not user_question:
        return jsonify({"response": "Please ask a valid question."})

    response = processor.chatbot_response(user_question)
    return jsonify({"response": response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))  # works locally & on cloud
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False
    )
