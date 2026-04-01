def ai_service(notes):
    from google import genai

    client = genai.Client(api_key="AIzaSyCdQFbav71D1e_Xwvh8Pm3O6rpQOt0Fm8M")

    response = client.models.generate_content(
        model="gemini-3-flash-preview",
        contents=f"Summarize this in short so i can easily understand:{notes}"
    )

    return response.text