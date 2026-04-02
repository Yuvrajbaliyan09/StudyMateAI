from flask import Flask
from test_gemini import ai_service
from test_gemini import generate_quiz
from test_gemini import chat_with_notes
app = Flask(__name__)

@app.route("/")
def box():
    return'''<form method="POST" action="/summarize">
    <textarea name="notes" rows="10" cols="50"></textarea>
    <button type="submit">Summarize</button>
    </form>

    <form method="POST" action="/quiz">
    <textarea name="notes" rows="10" cols="50"></textarea>
    <button type="submit"> Make Quiz</button>
    </form>

    <form method="POST" action="/chat">
    <textarea name="notes" rows="10" cols="50"></textarea>
    <textarea name="Question" placeholder ="Ask a Question" rows="7" cols="30"></textarea>
    <button type="submit"> Answer</button>
    </form>'''

@app.route("/summarize", methods=["POST"])
def summarize():
    from flask import request
    notes = request.form["notes"]
    result = ai_service(notes)
    return result

@app.route("/quiz",methods=["POST"] )
def quiz():
    from flask import request
    notes = request.form["notes"]
    result = generate_quiz(notes)
    return result

@app.route("/chat",methods=["POST"])
def chat():
    from flask import request
    notes = request.form["notes"]
    question = request.form["Question"]
    result = chat_with_notes(notes,question)
    return result

print(__name__)
if __name__ == "__main__":
    app.run(debug=True)