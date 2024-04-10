#!/usr/bin/env python3
""" A simple flask app Module """
from flask import Flask, render_template, request
from flask_babel import Babel


app = Flask(__name__)
babel = Babel(app)


class Config:
    """ configuration for babel instance """
    LANGUAGES = ["en", "fr"]
    BABEL_DEFAULT_LOCALE = "en"
    BABEL_DEFAULT_TIMEZONE = "UTC"


app.config.from_object(Config)


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
    return render_template('4-index.html')


if __name__ == "__main__":
    app.run()
