import requests
import secrets
import threading
from pyngrok import ngrok
from flask import Flask, request, jsonify

app = Flask(__name__)


# Generiert einen zufälligen API-Schlüssel
def generate_api_key():
    """
    Erzeugt einen zufälligen API-Schlüssel

    in: Keine
    out: Zufälliger Hex-String als API-Schlüssel
    """
    return secrets.token_hex(16)  # 32-stelliger Hex-String


API_KEY = generate_api_key()


@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    """
    Proxy-Funktion, die Anfragen an den lokalen LLM-Server weiterleitet

    in:
        path - Der Pfad der Anfrage
    out:
        Antwort vom lokalen LLM-Server oder Fehlermeldung
    """
    # Überprüft den API-Schlüssel
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 403

    # Leitet die Anfrage an den lokalen LLM-Server weiter, falls API-Schlüssel gültig
    response = requests.request(
        method=request.method,
        url=f"http://127.0.0.1:1234/{path}",
        headers={key: value for key, value in request.headers.items() if key != "Authorization"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    return response.content, response.status_code, response.headers.items()


def start_ngrok():
    """
    Startet einen ngrok-Tunnel, um den Proxy über das Internet zugänglich zu machen

    in: Keine
    out: Keine direkte Rückgabe, gibt die öffentliche URL in der Konsole aus
    """
    # hier ngrok-authtoken einsetzen
    ngrok_auth_token = "2uaTFNpu8CsRqM1SxSreDJTmaD0_5WyUAXe2QEGjCMhiRCzGJ"
    ngrok.set_auth_token(ngrok_auth_token)

    # startet einen "HTTP-Tunnel" auf port 8080
    public_url = ngrok.connect(8080)
    print(f"ngrok tunnel (use as API endpoint) is running at:\n\n{public_url}\n")


if __name__ == '__main__':
    """
    Haupteinstiegspunkt des Programms

    Startet den Proxy-Server und den ngrok-Tunnel
    """
    print(f"Secure proxy running with API key:\n\n{API_KEY}\n")

    # ngork-Tunnel separat starten
    threading.Thread(target=start_ngrok, daemon=True).start()

    # Flask-Server starten
    app.run(host="0.0.0.0", port=8080)
