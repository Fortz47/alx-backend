#!/usr/bin/env python3
""" A simple flask app Module """
from flask import (
        Flask,
        render_template,
        request,
        g
    )
from flask_babel import Babel, format_datetime
from typing import Optional, Dict
from pytz import timezone
import pytz.exceptions
from datetime import datetime


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
    """ rank and return first supported language """
    language_options = [
        request.args.get('locale', '').strip(),
        g.user.get('locale') if g.user else None,
        request.accept_languages.best_match(app.config['LANGUAGES']),
        app.config['BABEL_DEFAULT_LOCALE']
    ]
    for lang in language_options:
        if lang in app.config['LANGUAGES']:
            return lang


@babel.timezoneselector
def get_timezone() -> str:
    """retrieve timezone"""
    timezone_options = [
        request.args.get('timezone', '').strip(),
        g.user.get('timezone') if g.user else None,
    ]

    tz = app.config['BABEL_DEFAULT_TIMEZONE']  # 'UTC'
    for tzone in timezone_options:
        try:
            tz = timezone(tzone)
            tz = tz.zone
            break
        except pytz.exceptions.UnknownTimeZoneError:
            pass
    return tz


# babel = Babel(
#        app,
#        locale_selector=get_locale,
#        timezone_selector=get_timezone
#    )


@app.route('/', strict_slashes=False)
def hello() -> str:
    """ outputs welcome message with rendered template """
    return render_template('index.html')


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
    setattr(g, 'current_time', format_datetime(datetime.now()))


if __name__ == "__main__":
    app.run()
