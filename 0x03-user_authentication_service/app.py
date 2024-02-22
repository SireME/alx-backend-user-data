#!/usr/bin/env python3
"""
This module contains a basic flask application
"""

from flask import Flask, jsonify, request
from auth import Auth
AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def welcome() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users():
    email = request.form.get('email')
    password = request.form.get('password')
    try:
        user = AUTH.register_user(email, password)
        if user:
            r = {'email': email, "message": "user created"}
            return jsonify(r)
    except ValueError:
        r = {"message": "email already registered"}
        return jsonify(r), 400


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
