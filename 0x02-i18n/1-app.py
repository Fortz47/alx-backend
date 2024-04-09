#!/usr/bin/env python3
"""A simple flask app Module"""
from flask import Flask, render_template
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """configuration for language"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


@app.route('/', strict_slashes=False)
def hello() -> str:
    """outputs welcome message"""
    return render_template('1-index.html')


if __name__ == "__main__":
    app.run()
