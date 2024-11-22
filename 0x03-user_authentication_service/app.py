#!/usr/bin/env python3
"""Module: app"""

from flask import Flask, jsonify, request, abort
from auth import Auth


app = Flask(__name__)
auth = Auth()


@app.route('/', strict_slashes=False)
def home():
    """Home Route"""""
    return jsonify({"message": "Bienvenue"})


@app.route('/users', methods=['POST'], strict_slashes=False)
def register_user():
    """Register new user"""
    email = request.form.get('email')
    password = request.form.get('password')

    try:
        auth.register_user(email, password)
        return jsonify({'email': email, 'message': 'user created'})
    except ValueError:
        return jsonify({'message': 'email already registered'}), 400


@app.route('/sessions', methods=['POST'], strict_slashes=False)
def login():
    """Authenticate user"""
    email = request.form.get('email')
    password = request.form.get('password')

    if not auth.valid_login(email, password):
        abort(401)

    response = jsonify({'email': email, 'message': 'logged in'})
    response.set_cookie('session_id', auth.create_session(email))
    return response


if __name__ == '__main__':
    app.run(debug=True)
