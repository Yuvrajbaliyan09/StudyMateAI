# @app.route("/")
# def box():
#     sessions = get_sessions()
    
#     sessions_html = ""
#     for session in sessions:
#        sessions_html += f'<p><a href="/session/{session[0]}">{session[2]} | {session[1][:50]}...</a></p>'
    
#     return f'''
#     <h2>Summarize Notes</h2>
#     <form method="POST" action="/summarize">
#     <textarea name="notes" rows="10" cols="50"></textarea>
#     <button type="submit">Summarize</button>
#     </form>

#     <h2>Generate Quiz</h2>
#     <form method="POST" action="/quiz">
#     <textarea name="notes" rows="10" cols="50"></textarea>
#     <button type="submit"> Make Quiz</button>
#     </form>

#     <h2>Chat With Notes</h2>
#     <form method="POST" action="/chat">
#     <textarea name="notes" rows="10" cols="50"></textarea>
#     <textarea name="Question" placeholder ="Ask a Question" rows="7" cols="30"></textarea>
#     <button type="submit"> Answer</button>
#     </form>
    
#     <h2>Previous Sessions</h2>
#     {sessions_html}
#     '''
