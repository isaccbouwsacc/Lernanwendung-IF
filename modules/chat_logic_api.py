import requests

# API endpoint
api_url = "http://92.78.251.93:5000/v1/chat/completions"

def respond(history):
    # Prepare the request payload
    data = {
        "messages": history,
        "max_tokens": -1,
        "temperature": 0.8,
        "top_k": 40,
        "repeat_penalty": 1.1,
        "top_p": 0.95,
        "min_p": 0.05,
    }

    # Send the request to the remote server
    response = requests.post(api_url, json=data)

    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        history.append({'role': 'assistant', 'content': answer})
    else:
        print("Error:", response.status_code, response.text)

    return history

