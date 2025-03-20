import requests
import secrets
import threading
from pyngrok import ngrok
from flask import Flask, request, jsonify


app = Flask(__name__)


# Generate a random API key
def generate_api_key():
    return secrets.token_hex(16)  # 32 character hex string


API_KEY = generate_api_key()


@app.route('/<path:path>', methods=['GET', 'POST'])
def proxy(path):
    auth = request.headers.get("Authorization")
    if auth != f"Bearer {API_KEY}":
        return jsonify({"error": "Unauthorized"}), 403

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
    # Set your ngrok authtoken here
    ngrok_auth_token = "2uaTFNpu8CsRqM1SxSreDJTmaD0_5WyUAXe2QEGjCMhiRCzGJ"  # Replace with your actual token
    ngrok.set_auth_token(ngrok_auth_token)

    # Start an HTTP tunnel on port 8080
    public_url = ngrok.connect(8080)
    print(f"ngrok tunnel (use as API endpoint) is running at:\n\n{public_url}\n")


if __name__ == '__main__':
    print(f"Secure proxy running with API key:\n\n{API_KEY}\n")

    # Start ngrok in a separate thread
    threading.Thread(target=start_ngrok, daemon=True).start()

    # Start Flask app
    app.run(host="0.0.0.0", port=8080)
