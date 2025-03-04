from flask import Flask, render_template, request, jsonify, session
import google.generativeai as genai
import os

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Generates a new secret key on every restart

# Configure Gemini API
genai.configure(api_key="AIzaSyCqM2i_9xqy2rTFdtigshIVp9PpZS2En0o")
model = genai.GenerativeModel("gemini-1.5-flash")

@app.route('/')
def home():
    session.clear()  # Clears chat on page refresh
    session["history"] = []  # Initialize chat history
    session.modified = True  # Ensure session updates persist
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    data = request.get_json()
    user_text = data.get('text', '').strip()

    if not user_text:
        return jsonify({"status": "error", "message": "No input provided"}), 400

    # Initialize history if not present
    if "history" not in session:
        session["history"] = []

    # Append user message
    session["history"].append({"role": "user", "parts": [{"text": user_text}]})
    session.modified = True  # Ensure Flask saves changes

    # Send the complete conversation history
    chat = model.start_chat(history=session["history"])
    response = chat.send_message(user_text)

    # Append bot response
    session["history"].append({"role": "model", "parts": [{"text": response.text}]})
    session.modified = True

    return jsonify({"status": "success", "message": response.text})

if __name__ == '__main__':
    app.run(debug=True)
