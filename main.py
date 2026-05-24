from flask import Flask, request, render_template, jsonify, session, redirect, url_for
from flask_dance.consumer import oauth_authorized
from flask import flash
from database import init_db, save_session, get_sessions, get_session_by_id, delete_session, save_quiz_result, get_quiz_stats, get_or_create_user, get_user_by_id, rename_session
from test_gemini import ai_service, generate_quiz, chat_with_notes
import json
import fitz
from PIL import Image
import pytesseract
import io
import os
from dotenv import load_dotenv
from flask_dance.contrib.google import make_google_blueprint, google

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'  # for localhost

google_bp = make_google_blueprint(
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    scope=["https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email", "openid"],
)
os.environ['OAUTHLIB_RELAX_TOKEN_SCOPE'] = '1'
app.register_blueprint(google_bp, url_prefix="/login")

init_db()

def get_current_user():
    user_id = session.get('user_id')
    if user_id:
        return get_user_by_id(user_id)
    return None

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('user_id'):
            return redirect(url_for('login_page'))
        return f(*args, **kwargs)
    return decorated

@app.route("/login")
def login_page():
    if session.get('user_id'):
        return redirect(url_for('box'))
    return render_template("login.html")

@app.route("/login/google/start")
def google_login():
    return redirect(url_for("google.login"))

from flask_dance.consumer import oauth_authorized
from flask import flash

@oauth_authorized.connect_via(google_bp)
def google_logged_in(blueprint, token):
    if not token:
        return False
    resp = blueprint.session.get("/oauth2/v2/userinfo")
    if not resp.ok:
        return False
    info = resp.json()
    user = get_or_create_user(info["id"], info["name"], info["email"])
    session['user_id'] = user[0]
    session['user_name'] = user[1]
    return redirect(url_for("box"))

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login_page"))

@app.route("/")
@login_required
def box():
    user = get_current_user()
    sessions = get_sessions(user[0])
    return render_template("index.html", sessions=sessions, user=user)

@app.route("/summarize", methods=["POST"])
@login_required
def summarize():
    data = request.get_json()
    notes = data.get("notes", "")
    if not notes:
        return jsonify({"error": "No notes provided"}), 400
    result = ai_service(notes)
    user = get_current_user()
    session_id = save_session(notes, result, user[0])
    return jsonify({"summary": result, "session_id": session_id})

@app.route("/quiz", methods=["POST"])
@login_required
def quiz():
    data = request.get_json()
    notes = data.get("notes", "")
    if not notes:
        return jsonify({"error": "No notes provided"}), 400
    result = generate_quiz(notes)
    questions = json.loads(result)
    user = get_current_user()
    session_id = save_session(notes, result, user[0])
    return jsonify({"questions": questions, "session_id": session_id})

@app.route("/chat", methods=["POST"])
@login_required
def chat():
    data = request.get_json()
    notes = data.get("notes", "")
    if not notes:
        return jsonify({"error": "Please Provide Notes"}), 400
    question = data.get("message", "")
    result = chat_with_notes(notes, question)
    user = get_current_user()
    session_id = save_session(notes, result, user[0])
    return jsonify({"reply": result, "session_id": session_id})

@app.route("/sessions")
@login_required
def sessions():
    user = get_current_user()
    rows = get_sessions(user[0])
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "preview": row[1][:60],
            "created_at": row[2],
            "name": row[3] if row[3] else None
        })
    return jsonify(result)

@app.route("/session/<int:session_id>")
@login_required
def view_session(session_id):
    session_data = get_session_by_id(session_id)
    if not session_data:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": session_data[0],
        "notes": session_data[1],
        "summary": session_data[2],
        "created_at": session_data[3]
    })

@app.route("/session/<int:session_id>/delete", methods=["POST"])
@login_required
def delete_session_route(session_id):
    delete_session(session_id)
    return jsonify({"success": True})

@app.route("/session/<int:session_id>/rename", methods=["POST"])
@login_required
def rename_session_route(session_id):
    data = request.get_json()
    new_name = data.get("name", "").strip()
    if not new_name:
        return jsonify({"error": "Name cannot be empty"}), 400
    rename_session(session_id, new_name)
    return jsonify({"success": True})

@app.route("/upload", methods=["POST"])
@login_required
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    file = request.files['file']
    filename = file.filename.lower()
    try:
        if filename.endswith('.pdf'):
            pdf_bytes = file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            img = Image.open(io.BytesIO(file.read()))
            text = pytesseract.image_to_string(img)
        else:
            return jsonify({"error": "Only PDF and images supported"}), 400
        if not text.strip():
            return jsonify({"error": "Could not extract text from file"}), 400
        return jsonify({"text": text.strip()})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/quiz/save-score", methods=["POST"])
@login_required
def save_score():
    data = request.get_json()
    save_quiz_result(data.get("session_id"), data.get("score"), data.get("total"))
    return jsonify({"success": True})

@app.route("/quiz/stats")
@login_required
def quiz_stats():
    rows = get_quiz_stats()
    result = []
    for row in rows:
        result.append({
            "score": row[0],
            "total": row[1],
            "created_at": row[2],
            "percentage": round((row[0] / row[1]) * 100)
        })
    return jsonify(result)

print(__name__)
if __name__ == "__main__":
    app.run(debug=True)