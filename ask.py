import requests
from memory import add_to_memory, get_context


# ===== CONFIG =====
SERPAPI_KEY = "ad95bf1ed83a495c1596b0796a81e9a60e7c16b139307243411974e221c76138"
OLLAMA_URL = "http://localhost:11434/api/chat"
MODEL = "llama3.2:3b"

# ===== USER QUESTION =====
question = "What is artificial intelligence?"

# ===== STEP 1: SEARCH INTERNET =====
search_url = "https://serpapi.com/search"

params = {
    "engine": "google",
    "q": question,
    "api_key": SERPAPI_KEY,
    "num": 4
}

search_response = requests.get(search_url, params=params)
search_data = search_response.json()

sources_text = ""
sources_list = []

for i, result in enumerate(search_data["organic_results"], start=1):
    sources_text += f"[{i}] {result['title']}\n{result['snippet']}\n\n"
    sources_list.append(result["link"])

# ===== STEP 2: ASK AI USING SOURCES =====
prompt = f"""
You are a professional research assistant.

Rules:
- Use ONLY the provided sources.
- Be confident if the sources clearly define something.
- Do NOT express uncertainty unless the sources truly disagree.
- Write ONE clear paragraph (3–4 lines).
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



data = {
    "model": MODEL,
    "messages": [
        {"role": "system", "content": "You answer only using provided sources."},
        {"role": "user", "content": prompt}
    ],
    "stream": False
}

ai_response = requests.post(OLLAMA_URL, json=data)
ai_result = ai_response.json()

print("ANSWER:\n")
print(ai_result["message"]["content"])

print("\nSOURCES:")
for i, link in enumerate(sources_list, start=1):
    print(f"[{i}] {link}")
