from flask import Flask, request, jsonify
import requests
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

LOGGING_URL = os.getenv("LOGGING_URL")
ACCESS_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJNYXBDbGFpbXMiOnsiYXVkIjoiaHR0cDovLzIwLjI0NC41Ni4xNDQvZXZhbHVhdGlvbi1zZXJ2aWNlIiwiZW1haWwiOiIyMjE1MDExODBAcmFqYWxha3NobWkuZWR1LmluIiwiZXhwIjoxNzUxNjk3MTg5LCJpYXQiOjE3NTE2OTYyODksImlzcyI6IkFmZm9yZCBNZWRpY2FsIFRlY2hub2xvZ2llcyBQcml2YXRlIExpbWl0ZWQiLCJqdGkiOiIzNzU3MWIxOC00ODUxLTQ5MTEtYjc3MC1mZTY1MDhkMTE3ZWIiLCJsb2NhbGUiOiJlbi1JTiIsIm5hbWUiOiJ2aXN3YSB2aWpheWFrdW1hciIsInN1YiI6ImM2MDE5OWZjLTk1OTYtNGJkMy05OGYxLWZjZGIzMTc3MWIzMiJ9LCJlbWFpbCI6IjIyMTUwMTE4MEByYWphbGFrc2htaS5lZHUuaW4iLCJuYW1lIjoidmlzd2EgdmlqYXlha3VtYXIiLCJyb2xsTm8iOiIyMjE1MDExODAiLCJhY2Nlc3NDb2RlIjoiY1d5YVhXIiwiY2xpZW50SUQiOiJjNjAxOTlmYy05NTk2LTRiZDMtOThmMS1mY2RiMzE3NzFiMzIiLCJjbGllbnRTZWNyZXQiOiJCQ2twRGpqY1RmRXJ5TXhXIn0.MAuJYH-ehBFeB9xL5gxpdvNeOG9-70qtuYbzzaC_8VI"

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
