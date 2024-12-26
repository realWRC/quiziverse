#!/usr/bin/env python3
from config.config import app, login_manager
from flask import jsonify
from models.user import User


@login_manager.user_loader
def load_user(user_id):
    """ Flask login user loader
    """
    return User.getByID(user_id)


@app.route("/")
def index():
    """ Welcome Page
    """
    return jsonify({
        "message": "Welcome to quizziverse",
    })


@app.route("/register", methods=["POST"])
def register():
    """ Registration route
    """
    return jsonify({
        "message": "Successfully Registered"
    })


@app.route("/login", methods=["POST"])
def login():
    """ Login route
    """
    return jsonify({
        "message": "Successfully Logged in"
    })


@app.route("/logout", methods=["POST"])
def logout():
    """ Logout route
    """
    return jsonify({
        "message": "Successfully Logged out"
    })

if __name__ == "__main__":
    app.run(debug = True)
