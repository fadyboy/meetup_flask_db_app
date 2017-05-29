import sqlite3
from functools import wraps
from flask import Flask, render_template, redirect, flash, request, url_for, session, g

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
    return redirect(url_for('main'))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form["username"] != app.config["USERNAME"] or request.form["password"] != app.config["PASSWORD"]:
            error = "Invalid login credentials"
            return render_template('login.html', error=error)

        else:
            session["logged_in"] = True
            session['username'] = request.form['username']
            return redirect(url_for('main'))

    return render_template('login.html')


@app.route("/")
def main():
    g.db = connect_db()
    conn = g.db.cursor()
    conn.execute("SELECT * FROM books")
    books_data = conn.fetchall()

    books = [] # empty dictionary to store books_data
    for book in books_data:
        books.append({"Book_id":book[0], "Author":book[1], "Title":book[2], "Genre":book[3], "Price":book[4]})

    return render_template('main.html', books=books)



@app.route('/add', methods=["GET", "POST"])
def add():
    msg = "" # initialize msg variable to empty string
    if request.method == "POST":
        # get book details from form
        author = request.form["author"]
        title = request.form["title"]
        genre = request.form["genre"]
        price = request.form["price"]

        # connect to db and add book
        g.db = connect_db()
        conn = g.db.cursor()
        conn.execute("INSERT INTO books (Author, Title, Genre, Price) VALUES(?, ?, ?, ?)", (author, title, genre, price))
        g.db.commit()
        g.db.close()
        msg = "Book record successfully added!"



    return render_template('add.html', message=msg)



@app.route('/edit')
def edit():
    pass



@app.route('/delete')
def delete():
    pass



