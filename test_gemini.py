from google import genai

client = genai.Client(api_key="AIzaSyCRdXbFzuztq72G94jI2QyVxLJaf_5DMVg")

def ai_service(notes):


    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Summarize this in short so i can easily understand:{notes}"
    )
    return response.text

def generate_quiz(notes):
    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"""
        Create 5 multiple choice questions from these notes.
        Each question must have 4 options (A, B, C, D) and indicate the correct answer.
        
        Notes: {notes}
        """
    )

    return response.text
