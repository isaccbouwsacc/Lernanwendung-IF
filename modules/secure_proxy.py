from flask import Flask, request, jsonify
import requests
import secrets
import os

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
        headers={key: value for key, value in request.headers if key != "Authorization"},
        data=request.get_data(),
        cookies=request.cookies,
        allow_redirects=False
    )

    return response.content, response.status_code, response.headers.items()


if __name__ == '__main__':
    print(f"Secure proxy running with API key: {API_KEY}")
    app.run(host="0.0.0.0", port=8080)
