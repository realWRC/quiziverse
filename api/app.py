#!/usr/bin/env python3
from config.config import app
from flask import jsonify

@app.route('/')
def index():
    """ Welcome Page
    """
    return jsonify({
        "message": "Welcome to quizziverse",
    })


if __name__ == "__main__":
    app.run(debug = True)
