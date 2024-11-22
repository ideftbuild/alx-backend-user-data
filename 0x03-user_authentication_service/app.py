#!/usr/bin/env python3
"""Module: app"""

from flask import Flask, jsonify


app = Flask(__name__)


@app.route('/', strict_slashes=False)
def home():
    """Home Route"""""
    return jsonify({"message": "Bienvenue"})


if __name__ == '__main__':
    app.run()
