#!/usr/bin/env python3
"""
This module contains a basic flask application
"""

from flask import Flask, jsonify, request, abort
from flask import redirect
from auth import Auth
AUTH = Auth()

app = Flask(__name__)


@app.route('/')
def welcome() -> str:
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'])
def users() -> str:
    """
    register user in database from form data
    """
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


@app.route('/sessions', methods=['POST'])
def login() -> str:
    """
    authenticate and login user
    """
    email = request.form.get('email')
    password = request.form.get('password')
    if not AUTH.valid_login(email, password):
        abort(401)

    session_id = AUTH.create_session(email)
    msg = {"email": email, "message": "logged in"}
    response = jsonify(msg)
    response.set_cookie("session_id", session_id)
    return response


@app.route('/sessions', methods=['DELETE'])
def logout() -> str:
    """
    method yo logout user and send appropriate response
    """
    session_id = request.cookies.get('session_id')
    # if user with session id exists, delete session
    user = AUTH.get_user_from_session_id(session_id)
    if not user:
        abort(403)
    id = user.id
    AUTH.destroy_session(id)
    return redirect('/')


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
