#!/usr/bin/env python3
"""A simple flask app Module"""
from flask import Flask, render_template, request
from flask_babel import Babel, _


app = Flask(__name__)
# babel = Babel(app)


class Config:
    """configuration for language"""
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


def get_locale():
    """determines best match from supported languages"""
    return request.accept_languages.best_match(app.config['LANGUAGES'])


babel = Babel(app, locale_selector=get_locale)    


@app.route('/', strict_slashes=False)
def hello() -> str:
    """outputs welcome message"""
    # get_locale()
    return render_template(
        '3-index.html',
        title=_("home_title"),
        header=_("home_header")
    )


if __name__ == "__main__":
    app.run()
