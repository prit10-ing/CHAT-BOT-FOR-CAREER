from flask import Flask, render_template, jsonify, request
import processor

app = Flask(__name__)

@app.route("/", methods=["GET"])
def index():
    return render_template("index.html")


@app.route("/chatbot", methods=["POST"])
def chatbot_response():
    try:
        # ✅ Support both JSON (fetch API) and form submission
        data = request.get_json(silent=True)

        if data and "question" in data:
            user_question = data.get("question", "").strip()
        else:
            user_question = request.form.get("question", "").strip()

        if not user_question:
            return jsonify({"response": "Please ask a valid question."})

        response = processor.chatbot_response(user_question)
        return jsonify({"response": response})

    except Exception as e:
        # 🔴 Prevent 500 error and log issue
        print("Chatbot error:", e)
        return jsonify({
            "response": "Sorry, something went wrong. Please try again."
        }), 500


