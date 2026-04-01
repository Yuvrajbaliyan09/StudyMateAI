from flask import Flask
from test_gemini import ai_service
app = Flask(__name__)

@app.route("/")
def hello_world():
    return'''<form method="POST" action="/summarize">
    <textarea name="notes" rows="10" cols="50"></textarea>
    <button type="submit">Summarize</button>
    </form>'''

@app.route("/summarize", methods=["POST"])
def summarize():
    from flask import request
    notes = request.form["notes"]
    result = ai_service(notes)
    return result
print(__name__)
if __name__ == "__main__":
    app.run(debug=True)