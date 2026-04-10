from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = Groq(api_key=api_key)

def ai_service(notes):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
    {"role": "user", "content": f"Summarize this in short so i can easily understand: {notes}"}
    ])
    return response.choices[0].message.content
        

def generate_quiz(notes):
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
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Answer questions using only these notes: {notes}"},
            {"role": "user", "content": Question}
        ]
    )
    return response.choices[0].message.content

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


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

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