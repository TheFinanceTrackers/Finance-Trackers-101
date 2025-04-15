import requests

headers = {
    "Authorization": "Bearer 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",  # 👈 Replace with your key
    "Content-Type": "application/json"
}

payload = {
    "model": "mistralai/mistral-7b-instruct",
    "messages": [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "What's a good way to save money each week?"}
    ]
}

res = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)

print(res.json())
