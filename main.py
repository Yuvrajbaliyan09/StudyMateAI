from flask import Flask,request,render_template ,jsonify
from database import init_db, save_session, get_sessions, get_session_by_id
from test_gemini import ai_service ,generate_quiz , chat_with_notes
import json
app = Flask(__name__)
init_db()

@app.route("/")
def box():
    sessions = get_sessions()
    return render_template("index.html",sessions=sessions)

@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()

    notes = data.get("notes","")
    if not notes:
        return jsonify({"error":"No notes provided"}),400
    result = ai_service(notes)
    session_id = save_session(notes,result)
    return jsonify({"summary": result ,"session_id":session_id})


@app.route("/quiz",methods=["POST"] )
def quiz():
    data = request.get_json()
    notes = data.get("notes","")
    if not notes:
        return jsonify({"error": "No notes provided"}),400
    
    result = generate_quiz(notes)
    questions = json.loads(result)
    
    session_id = save_session(notes,result)
    return jsonify({"questions":questions, "session_id": session_id})
  

@app.route("/answers", methods=["POST"])
def show_answers():
    from flask import request
    answers = request.form["answers"]
    return f'''
        <h2>Correct Answers</h2>
        <pre>{answers}</pre>
        <a href="/">Go Back</a>
    '''

@app.route("/chat",methods=["POST"])
def chat():
    from flask import request
    notes = request.form["notes"]
    question = request.form["Question"]
    result = chat_with_notes(notes,question)
    save_session(notes,result)
    return f'''
        <h2>Chat With Notes</h2>
        <p>{result}</p>
        <a href="/">Go Back</a>
    '''
@app.route("/session/<int:session_id>")
def view_session(session_id):
    session = get_session_by_id(session_id)
    return f'''
        <h2>Session {session[0]}</h2>
        <h3>Notes:</h3>
        <pre>{session[1]}</pre>
        <h3>Summary:</h3>
        <pre>{session[2]}</pre>
        <a href="/">Go Back</a>
    '''

print(__name__)
if __name__ == "__main__":
    app.run(debug=True)