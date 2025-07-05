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
        if response.status_code == 200:
            print(response["logID"])
            print(response["message"])
    except requests.exceptions.RequestException as e:
        print(e)

users = {
    "221501180@gmail.com": "12345",
    "viswa@gmail.com": "12345",
    "v@gmail.com" : "12345",
}
