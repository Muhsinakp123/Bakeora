import os
import requests

HF_API_TOKEN = os.getenv("HF_API_TOKEN")

API_URL = "https://router.huggingface.co/hf-inference/models/mistralai/Mistral-7B-Instruct-v0.2"

headers = {
    "Authorization": f"Bearer {HF_API_TOKEN}",
    "Content-Type": "application/json"
}


def generate_cake_suggestion(cake_type, size, flavor, cream_type, message):
    prompt = f"""
You are a professional cake designer.

Generate a detailed custom cake idea based on the following details:

Cake Type: {cake_type}
Size: {size}
Flavor: {flavor}
Cream Type: {cream_type}
Message on Cake: {message}

Provide:
1. Cake design description
2. Suggested flavor combination
3. Decoration ideas
4. A creative cake name

Keep it elegant and attractive.
"""

    payload = {
        "inputs": prompt,
        "parameters": {
            "max_new_tokens": 300,
            "temperature": 0.7
        }
    }
    

    response = requests.post(API_URL, headers=headers, json=payload)
    print("Status Code:", response.status_code)
    print("Response Text:", response.text)

    if response.status_code != 200:
        return f"Error from AI API: {response.text}"
    result = response.json()
    if isinstance(result, list):
        return result[0]["generated_text"]
    elif "error" in result:
        return f"AI Error: {result['error']}"
    else:
       return "AI is currently unavailable."