import requests

url = "http://localhost:11434/api/chat"

data = {
    "model": "llama3.2:3b",
    "messages": [
        {
            "role": "system",
            "content": "You are a helpful and honest AI. If you do not know something, say 'I don't know'."
        },
        {
            "role": "user",
            "content": "Hello, who are you?"
        }
    ],
    "stream": False
}

response = requests.post(url, json=data)
result = response.json()

print(result["message"]["content"])
