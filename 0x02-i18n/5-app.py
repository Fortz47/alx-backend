#!/usr/bin/env python3
""" A simple flask app Module """
from flask import Flask, render_template, request, g
from flask_babel import Babel
from typing import Optional, Dict


app = Flask(__name__)
babel = Babel(app)


class Config:
    """ configuration for babel instance """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)
users = {
    1: {"name": "Balou", "locale": "fr", "timezone": "Europe/Paris"},
    2: {"name": "Beyonce", "locale": "en", "timezone": "US/Central"},
    3: {"name": "Spock", "locale": "kg", "timezone": "Vulcan"},
    4: {"name": "Teletubby", "locale": None, "timezone": "Europe/London"},
}


@babel.localeselector
def get_locale() -> str:
    """ determines best match from supported languages """
    locale = request.args.get('locale')
    if locale and locale in app.config['LANGUAGES']:
        return locale
    else:
        return request.accept_languages.best_match(app.config['LANGUAGES'])


# babel = Babel(app, locale_selector=get_locale)


@app.route('/', strict_slashes=False)
def hello() -> str:
    """ outputs welcome message with rendered template """
    return render_template('5-index.html')


def get_user() -> Optional[Dict]:
    """retrievs a user from users if exists else None"""
    user_id = request.args.get('login_as')
    try:
        user_id = int(user_id)
    except Exception:
        return None
    return users.get(user_id)


@app.before_request
def before_request() -> None:
    """
    function to execute before others, set user as global on flask.g.user
    """
    user = get_user()
    g.user = user


if __name__ == "__main__":
    app.run()
