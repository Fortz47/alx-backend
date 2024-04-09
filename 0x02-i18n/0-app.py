#!/usr/bin/env python3
from flask import Flask


app = Flash(__name__)

@app.route('/', strict_slashes=False)
def hello():
    """outputs welcome message"""
    return render_template('index.html')


if __name__ == "__main__":
    app.run()
