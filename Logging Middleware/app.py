from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LOGGING_URL = os.getenv("LOGGING_URL")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
def log(stack, level, package, message):
    headers = {
        "Authorization": f"Bearer {ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "stack": stack,
        "level": level,
        "package": package,
        "message": message
    }

    try:
        response = requests.post(LOGGING_URL, headers=headers, json=payload)
        if response.status_code == 200 or response.status_code == 201:
            return response.json()
    except requests.exceptions.RequestException as e:
        print(e)

users = {
    "221501180@gmail.com": "12345",
    "viswa@gmail.com": "12345",
    "v@gmail.com" : "12345",
}

@app.route('/login', methods=['POST'])
def login():
    data = request.json or {}
    email = data.get("email")
    password = data.get("password")

    if not email or not password:
        res = log("backend", "error", "handler", "Login failed: Missing email or password")
        return jsonify(error="Email and password are required", response_from_server = res), 400

    if email in users and users[email] == password:
        res = log("backend", "info", "controller", f"Login successful for {email}")
        return jsonify(message="Login successful", email=email, response_from_server = res)
    else:
        res = log("backend", "warn", "handler", f"Login failed for {email}")
        return jsonify(error="Invalid credentials", response_from_server = res), 401

if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
