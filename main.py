from flask import Flask
from test_gemini import ai_service
from test_gemini import generate_quiz
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

print(__name__)
if __name__ == "__main__":
    app.run(debug=True)