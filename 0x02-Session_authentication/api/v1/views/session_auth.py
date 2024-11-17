#!/usr/bin/env python3
"""Module: session_auth"""
from api.v1.views import app_views
from flask import request, jsonify


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def session_login():
    print('control in method')
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    from models.user import User

    users = User.search({'email': email})
    if not users:
        return jsonify({"error": "no user found for this email"}), 404

    user = next(
        (user for user in users if user.is_valid_password(password)),
        None)
    if not user:
        return jsonify({"error": "wrong password"}), 401

    from api.v1.app import auth
    from os import getenv
    session = auth.create_session(user.id)

    out = jsonify(user.to_json())
    out.set_cookie(getenv('SESSION_NAME'), session)
    return out
