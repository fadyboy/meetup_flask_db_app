from flask import Flask, request, render_template, redirect, session, flash, \
                  url_for, g
# g is used to manage the application context e.g connections to db
# session is used to manage user session and store user info in secure way
import sqlite3
import os

host = os.getenv("IP", "0.0.0.0")
port = int(os.getenv("PORT", "8080"))

# Configuration details
DATABASE = "books.db"
USERNAME = "admin"
PASSWORD = "admin"
SECRET_KEY = "very_secret_password"

app = Flask(__name__) # create a flask app in this module
app.config.from_object(__name__) # get all config details from this module

# create connection to db
def connect_db():
    return sqlite3.connect(app.config["DATABASE"])
    
# create routes for login and main pages
@app.route("/", methods=["GET", "POST"])
def login():
    error = None
    status_code = 200
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] or \
            request.form["password"] != app.config["PASSWORD"]:
                error = "Invalid credentials, please login with a valid username and password"
                status_code = 401
        else:
            session["logged_in"] = True
            return redirect(url_for('main'))
    return render_template("login.html", error=error), status_code
    
    
@app.route("/main")
def main():
    books = [] # books have author, title, genre, price fields; our data is a list of books
    # create connection to db
    g.db = connect_db()
    conn = g.db.cursor()
    conn.execute("SELECT * FROM books")
    books_data = conn.fetchall()
    for book in books_data:
        books.append({"author":book[0], "title":book[1], "genre":book[2], "price":book[3]})
        
    # remember to close connection to db
    g.db.close()
        
    return render_template("main.html", books=books)
    
    
@app.route("/logout")
def logout():
    # kill/pop current session
    session.pop("logged_in", None)
    flash("You are now logged out")
    
    return redirect(url_for('login'))
    
    
    
if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
