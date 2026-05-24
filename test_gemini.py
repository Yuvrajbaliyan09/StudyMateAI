from groq import Groq
from dotenv import load_dotenv
import os

load_dotenv()
api_key = os.getenv("API_KEY")
client = Groq(api_key=api_key)

def clean_notes(notes, limit=4000):
    """Cut at sentence boundary instead of mid-word"""
    notes = notes[:limit]
    last_period = notes.rfind('.')
    if last_period > limit * 0.8:
        return notes[:last_period + 1]
    return notes

def ai_service(notes):
    notes = clean_notes(notes)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": """You are an expert study assistant. When given notes, you:
1. Extract the core concepts and key points
2. Organize them in a clear, logical structure
3. Use simple language a student can understand
4. Highlight important terms in **bold**
5. Keep it concise but complete — no fluff"""
            },
            {
                "role": "user",
                "content": f"Summarize these notes into clear, structured study material:\n\n{notes}"
            }
        ],
        temperature=0.3,
        max_tokens=2000
    )
    return response.choices[0].message.content

def generate_quiz(notes, count=5):
    notes = clean_notes(notes)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""You are a quiz generator. Generate exactly {count} multiple choice questions.
Rules:
- Questions must test understanding, not just memorization
- All 4 options must be plausible (no obviously wrong answers)
- Only one option is correct
- Return ONLY a valid JSON array, no markdown, no extra text"""
            },
            {
                "role": "user",
                "content": f"""Generate exactly {count} multiple choice questions from these notes.
Return ONLY this JSON format:
[
  {{
    "question": "question here",
    "options": ["A) option", "B) option", "C) option", "D) option"],
    "answer": "A) correct option"
  }}
]

Notes: {notes}"""
            }
        ],
        temperature=0.5,
        max_tokens=2500
    )
    return response.choices[0].message.content
def chat_with_notes(notes, question):
    notes = clean_notes(notes)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {
                "role": "system",
                "content": f"""You are a helpful study assistant. Answer the student's questions based on the notes provided.
Rules:
- Only use information from the notes
- If the answer is not in the notes, say "This isn't covered in your notes, but generally..." and give a brief answer
- Keep answers concise and clear
- Use examples from the notes when possible

Notes:
{notes}"""
            },
            {
                "role": "user",
                "content": question
            }
        ],
        temperature=0.4,
        max_tokens=512
    )
    return response.choices[0].message.content

def generate_schedule(syllabus):
    syllabus = clean_notes(syllabus, limit=3000)
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[
            {
                "role": "system",
                "content": "You are an expert academic planner. Create realistic, structured study schedules. Always return valid JSON only, no markdown, no extra text."
            },
            {
                "role": "user",
                "content": f"""Create a day-by-day study plan from this syllabus.
Return ONLY this JSON format:
{{
  "title": "Study Plan",
  "days": [
    {{
      "day": 1,
      "topics": ["topic 1", "topic 2"],
      "duration": "2 hours",
      "priority": "high"
    }}
  ],
  "total_days": 7,
  "daily_hours": 2
}}

Priority must be: "high", "medium", or "low".
Distribute topics logically — foundations first, complex topics later.
Syllabus: {syllabus}"""
            }
        ],
        temperature=0.3,
        max_tokens=2048
    )
    return response.choices[0].message.content