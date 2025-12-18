import requests

API_KEY = "ad95bf1ed83a495c1596b0796a81e9a60e7c16b139307243411974e221c76138"

url = "https://serpapi.com/search"

params = {
    "engine": "google",
    "q": "What is artificial intelligence?",
    "api_key": API_KEY,
    "num": 5
}

response = requests.get(url, params=params)
data = response.json()

for i, result in enumerate(data["organic_results"], start=1):
    print(f"{i}. {result['title']}")
    print(result['link'])
    print()
