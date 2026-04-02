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
    response.choices[0].message.content
        

def generate_quiz(notes):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
    {"role": "user", "content": f'''Create 5 multiple choice questions from these notes.each question must have 4 options (A, B, C, D) and indicate the correct answer.
    Notes: {notes}'''}
    ])
    response.choices[0].message.content

def chat_with_notes(notes,Question):
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {"role": "system", "content": f"Answer questions using only these notes: {notes}"},
            {"role": "user", "content": Question}
        ]
    )
    return response.choices[0].message.content
