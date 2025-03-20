from openai import OpenAI

# Initialisierung des LM Studio Clients
client = OpenAI(base_url="http://127.0.0.1:1234/v1", api_key="lm-studio")
MODEL = "gemma-3-12b-it"


def respond(history):
    """
    Sendet eine Anfrage an das lokale Sprachmodell und gibt die Antwort zurück

    in:
        history - Liste von Nachrichten im Format [{"role": "...", "content": "..."}]
    out:
        history - Aktualisierte Nachrichtenliste mit der Antwort des Modells
    """
    response = client.chat.completions.create(
        model=MODEL,
        messages=history,
        max_tokens=-1,
        temperature=0.5
    )

    # Extrahiert den Inhalt aus der Antwort
    answer = response.choices[0].message.content
    history.append({'role': 'assistant', 'content': answer})

    return history
