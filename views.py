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


@app.route("/logout/")
def logout():
    session.pop("logged_in", None)
    flash("Goodbye!")
    return redirect(url_for('login'))


@app.route("/", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form[""] != app.config["USERNAME"] or request.form[""] != app.config["PASSWORD"]:
            error = "Invalid login credentials"
            return render_template('login.html', error=error)

        else:
            session["logged_in"] = True
            return redirect(url_for('main'))

    return render_template('login.html')
