#!/usr/bin/env python3
"""
Route module for the API
"""
from os import getenv
from api.v1.views import app_views
from flask import Flask, jsonify, abort, request
from flask_cors import (CORS, cross_origin)
import os


app = Flask(__name__)
app.register_blueprint(app_views)
CORS(app, resources={r"/api/v1/*": {"origins": "*"}})
auth = os.getenv("AUTH_TYPE")

if auth == "basic_auth":
    from api.v1.auth.basic_auth import BasicAuth
    auth = BasicAuth()
elif auth == "session_auth":
    from api.v1.auth.session_auth import SessionAuth
    auth = SessionAuth()
else:
    from api.v1.auth.auth import Auth
    auth = Auth()


@app.errorhandler(404)
def not_found(error) -> str:
    """ Not found handler
    """
    return jsonify({"error": "Not found"}), 404


@app.errorhandler(401)
def unauthorized(error) -> str:
    """
    unauthorized
    """
    return jsonify({"error": "Unauthorized"}), 401


@app.errorhandler(403)
def forbidden(error) -> str:
    """
    authenticated but not allowed to accees resource
    """
    return jsonify({"error": "Forbidden"}), 403


@app.before_request
def filter_request():
    """
    A filter function to check authentication and
    authorization before processing each request.

    This function checks if authentication is required for
      the requested path and ensures the user is
        authenticated and authorized.

    If authentication is not required or the user
      is authenticated and authorized, the request proceeds.
    Otherwise, appropriate HTTP error
    responses (401 or 403) are returned.

    :return: None
    """

    if auth is None:
        return

    excluded_paths = [
        '/api/v1/status/',
        '/api/v1/unauthorized/',
        '/api/v1/forbidden/'
    ]

    path = request.path

    # Check if authentication is required for the requested path
    if not auth.require_auth(path, excluded_paths):
        return

    # Check if the request contains authorization headers
    if auth.authorization_header(request) is None:
        print(request.headers)  # Optionally log the request headers
        abort(401)  # Unauthorized

    # Check if the user associated with the request is valid
    if auth.current_user(request) is None:
        abort(403)  # Forbidden

    # add current user to request
    current_user = auth.current_user(request)
    request.current_user = current_user


if __name__ == "__main__":
    host = getenv("API_HOST", "0.0.0.0")
    port = getenv("API_PORT", "5000")
    app.run(host=host, port=port)
