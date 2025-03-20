import requests

# globale Variablen, die von außen gesetzt werden können
API_KEY = ""
API_ENDPOINT = ""  # Standardwert


def respond(history):
    """
    Sendet eine Anfrage an einen externen API-Endpunkt und gibt die Antwort zurück

    in:
        history - Liste von Nachrichten im Format [{"role": "...", "content": "..."}]
    out:
        history - Aktualisierte Nachrichtenliste mit der Antwort des API-Dienstes
    """
    # Vorbereitung der Anfrage mit Parametern für die Antworterstellung
    data = {
        "messages": history,
        "max_tokens": -1,
        "temperature": 0.4,  # Deterministischer druch kleineren Wert
        "top_k": 40,
        "repeat_penalty": 1.1,
        "top_p": 0.95,
        "min_p": 0.05,
    }

    # API-Schlüssel in den Headers einfügen
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    # Anfrage an den Remote-Server senden
    response = requests.post(API_ENDPOINT, json=data, headers=headers)

    if response.status_code == 200:
        answer = response.json()['choices'][0]['message']['content']
        history.append({'role': 'assistant', 'content': answer})
    else:
        print("Error:", response.status_code, response.text)

    return history
