import sqlite3
from functools import wraps
from flask import Flask, render_template, redirect, flash, request, url_for, session

# config settings
app = Flask(__name__)
app.config.from_object('_config')


def connect_db():
    return sqlite3.connect(app.config['DATABASE_PATH'])


def login_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if 'logged_in' in session:
            return func(*args, **kwargs)

        else:
            flash("You need to be logged in!")
            return redirect(url_for('login'))

    return wrapper
