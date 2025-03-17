import requests
import os

# API endpoint - Update this to the correct IP address
api_url = "http://192.168.1.187:8080/v1/chat/completions"

# Get the API key from the file
try:
    with open("temp_api_key.txt", "r") as f:
        API_KEY = f.read().strip()
except FileNotFoundError:
    print("API key file not found")
    API_KEY = ""

def respond(history):
    # Prepare the request payload
    data = {
        "messages": history,
        "max_tokens": -1,
        "temperature": 0.4,  # More deterministic
        "top_k": 40,
        "repeat_penalty": 1.1,
        "top_p": 0.95,
        "min_p": 0.05,
    }

    # Include the API key in the headers
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Send the request to the remote server
    response = requests.post(api_url, json=data, headers=headers)

    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        history.append({'role': 'assistant', 'content': answer})
    else:
        print("Error:", response.status_code, response.text)

    return history
