# StudyMateAI

Paste in your notes, get back a clean summary, a quiz, and answers to questions about them. Paste a syllabus and get a day-by-day study plan.

**Live demo:** https://studymateai-48rm.onrender.com/

I built this for a hackathon (TheDevArena) because my own notes were a mess and I wanted something that would turn them into something I'd actually revise from.

## What it does

- **Summarize**: turns raw notes into structured study material with key terms in bold
- **Quiz**: generates multiple choice questions from your notes
- **Chat**: ask questions about your notes; if the answer isn't in them, it says so before answering from general knowledge
- **Schedule**: splits a syllabus into a study plan, foundations first

## Stack

Flask, Groq API for the LLM calls, PostgreSQL, Google OAuth for login, deployed on Render.

## Things I got wrong

**The models disappeared.** In November 2026 the app started returning 500s on every summarize. Groq had retired the Llama models I hardcoded, so the API returned a 404. I switched to the replacement models and moved the model names into environment variables, so the next deprecation is a config change instead of a code hunt.

**The login code isn't fully mine yet.** I wrote the Google OAuth part under hackathon time pressure and leaned on copy-pasted code I didn't fully understand. It works, but I can't properly explain or defend it. It also turns on `OAUTHLIB_INSECURE_TRANSPORT` for every environment, which is only meant for localhost. I'm rebuilding auth from the docs in the next version.

**Input is truncated.** Notes are cut at about 4000 characters before going to the model, so long notes silently lose their tail.

## What's next

I'm rebuilding this as a separate project, studymate-v2: FastAPI, Postgres with pgvector, Docker, and RAG, so it can work over whole uploaded documents instead of a pasted chunk. This repo stays as it is.

## Author

Yuvraj