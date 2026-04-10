from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = Groq(api_key=api_key)

def ai_service(notes):
    notes = notes[:3000]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
    {"role": "user", "content": f"Summarize this in short so i can easily understand: {notes}"}
    ])
    return response.choices[0].message.content
        

def generate_quiz(notes):
    notes = notes[:3000]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{
            "role": "user",
            "content": f"""Create 5 multiple choice questions from these notes.
                Return ONLY a JSON array, no extra text, no markdown, exactly like this:
            [
            {{
        "question": "question here",
        "options": ["A) option", "B) option", "C) option", "D) option"],
        "answer": "A) option"
        }}
        ]
        Notes: {notes}"""
                }]
        )
    return response.choices[0].message.content

def chat_with_notes(notes,Question):
    notes = notes[:3000]
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Answer questions using only these notes: {notes}"},
            {"role": "user", "content": Question}
        ]
    )
    return response.choices[0].message.content