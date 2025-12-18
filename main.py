from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests

from memory import add_to_memory, get_context

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ===== CONFIG =====
SERPAPI_KEY = "ad95bf1ed83a495c1596b0796a81e9a60e7c16b139307243411974e221c76138"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

# ===== REQUEST BODY =====
class Question(BaseModel):
    question: str

# ===== API ENDPOINT =====
@app.post("/ask")
def ask_ai(data: Question):
    question = data.question

    # ---- MEMORY ----
    context = get_context()
    full_question = f"""
Previous conversation:
{context}

Current question:
{question}
"""

    # ---- SEARCH ----
    search_url = "https://serpapi.com/search"
    params = {
        "engine": "google",
        "q": full_question,
        "api_key": SERPAPI_KEY,
        "num": 2
    }

    search_response = requests.get(search_url, params=params)
    search_data = search_response.json()

    sources_text = ""
    sources_list = []

    for i, result in enumerate(search_data["organic_results"], start=1):
        sources_text += f"[{i}] {result['title']}\n{result.get('snippet', '')}\n\n"
        sources_list.append(result["link"])

    # ---- AI PROMPT ----
    prompt = f"""
You are a professional research assistant.

Rules:
- Use ONLY the provided sources.
- Be confident if the sources define something clearly.
- Write ONE clear paragraph.
- Do NOT repeat ideas.
- Do NOT add opinions.

Question:
{question}

Sources:
{sources_text}

Output format:
Answer:
<your answer here>
"""

    ai_data = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You answer only using provided sources."},
            {"role": "user", "content": prompt}
        ],
        "stream": False
    }

    ai_response = requests.post(OLLAMA_URL, json=ai_data)
    ai_result = ai_response.json()

    answer = ai_result["message"]["content"]

    # ---- SAVE MEMORY ----
    add_to_memory(question, answer)

    return {
        "answer": answer,
        "sources": sources_list
    }
