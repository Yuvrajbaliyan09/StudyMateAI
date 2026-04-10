from flask import Flask,request,render_template ,jsonify
from database import init_db, save_session, get_sessions, get_session_by_id,delete_session,save_quiz_result,get_quiz_stats
from test_gemini import ai_service ,generate_quiz , chat_with_notes
import json
import fitz  # pymupdf
from PIL import Image
import pytesseract
import io

app = Flask(__name__)
init_db()

#Root Route or Main Route
@app.route("/")
def box():
    sessions = get_sessions()
    return render_template("index.html",sessions=sessions)

#Summarize Route
@app.route("/summarize", methods=["POST"])
def summarize():
    data = request.get_json()

    notes = data.get("notes","")
    if not notes:
        return jsonify({"error":"No notes provided"}),400
    result = ai_service(notes)
    session_id = save_session(notes,result)
    return jsonify({"summary": result ,"session_id":session_id})

#Quiz Route
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
  
#Chat Route
@app.route("/chat",methods=["POST"])
def chat():
    data = request.get_json()
    notes = data.get("notes","")
    if not notes:
        return jsonify({"error":"Please Provide Notes"}),400
    
    question = data.get("message","")
    result = chat_with_notes(notes,question)
    session_id = save_session(notes,result)

    return jsonify({"reply":result , "session_id": session_id})

#Show Session Route
@app.route("/sessions")
def sessions():
    rows = get_sessions()
    result = []
    for row in rows:
        result.append({
            "id": row[0],
            "preview": row[1][:60],
            "created_at": row[2]
        })
    return jsonify(result)

#Veiw Session Route
@app.route("/session/<int:session_id>")
def view_session(session_id):
    session = get_session_by_id(session_id)
    if not session:
        return jsonify({"error": "Not found"}), 404
    return jsonify({
        "id": session[0],
        "notes": session[1],
        "summary": session[2],
        "created_at": session[3]
    })

#Delete Session Route
@app.route("/session/<int:session_id>/delete", methods=["POST"])
def delete_session_route(session_id):
    delete_session(session_id)
    return jsonify({"success": True})

@app.route("/upload", methods=["POST"])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files['file']
    filename = file.filename.lower()
    
    try:
        if filename.endswith('.pdf'):
            # PDF extraction
            pdf_bytes = file.read()
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            text = ""
            for page in doc:
                text += page.get_text()
            doc.close()
            
        elif filename.endswith(('.png', '.jpg', '.jpeg', '.webp')):
            # Image OCR
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
def save_score():
    data = request.get_json()
    save_quiz_result(data.get("session_id"), data.get("score"), data.get("total"))
    return jsonify({"success": True})

@app.route("/quiz/stats")
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
    app.run(debug=True) #Run app and debug