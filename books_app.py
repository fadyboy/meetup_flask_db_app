from flask import Flask, request, render_template, url_for, redirect, session, \
                  flash, g
import sqlite3                  
import os

# for c9 users
host = os.getenv("IP", "0.0.0.0")
port = int(os.getenv("PORT", "8080"))

# configuration details
DATABASE = "books.db"
SECRET_KEY = "my_secret"

app = Flask(__name__)
app.config.from_object(__name__) # pulls in app configuration by looking for uppercase variables

# create function to connect to database
def connect_db():
    return sqlite3.connect(app.config["DATABASE"])
    
    
# create views/routes
@app.route("/")
def login():
    return render_template("login.html")
    
    
@app.route("/main")
def main():
    # create connection to db
    g.db = connect_db()
    # create a cursor to db
    conn = g.db.cursor()
    # execute a query against db
    conn.execute("SELECT * FROM books")
    books_data = conn.fetchall()
    
    # how do we want to display the data? In a list
    books = []
    # books data is a list of records that have same column items
    # i.e author, title, genre, price, best represented in a dictionary
    # iterate over books data and populate books list with data
    for book in books_data:
        books.append({"id":book[0],"author":book[1], "title":book[2], "genre":book[3], "price":book[4]})
        
    # close db connection
    g.db.close()
    
    # pass books data to our template for use
    return render_template("main.html", books=books)
    
    
# add route to add book
@app.route("/add", methods=["GET","POST"])
def add_book():
    msg = ""
    if request.method == "POST":
        author = request.form["author"]
        title = request.form["title"]
        genre = request.form["genre"]
        price = request.form["price"]
        
        g.db = connect_db()
        conn = g.db.cursor()
        conn.execute("INSERT INTO books (author, title, genre, price) VALUES(?, ?, ?, ?)", (author, title, genre, price))
        
        g.db.commit()
        g.db.close()
        msg = "Record successfully added!"
    
    return render_template('add_book.html', msg=msg)
    

@app.route("/edit", methods=["GET", "POST"])
def edit():
    # get query string arguments
    book_id = request.args.get("book_id")
    author = request.args.get("author")
    title = request.args.get("title")
    genre = request.args.get("genre")
    price = request.args.get("price")
    
    book = {
        "book_id":book_id,
        "author":author,
        "title":title,
        "genre":genre,
        "price":price
    }
    
    msg = ""
    
    if request.method == "POST":
        # get the data from form
        book_id = request.form["book_id"]
        author = request.form["author"]
        title = request.form["title"]
        genre = request.form["genre"]
        price = request.form["price"]
        
        # connect db and update record
        g.db = connect_db()
        conn = g.db.cursor()
        conn.execute("UPDATE books SET author=?, title=?, genre=?, price=? WHERE id=?", \
                     [author, title, genre, price, book_id])
        
        # update book variable with the latest changes
        book = {
        "book_id":book_id,
        "author":author,
        "title":title,
        "genre":genre,
        "price":price
            }
        
        g.db.commit()
        g.db.close()
        msg = "Changes successfully updated!"
    
    return render_template('edit.html', book_record=book, message=msg)
    
    
@app.route("/delete", methods=["GET", "POST"])
def delete():
    book_id = request.args.get("book_id")
    author = request.args.get("author")
    title = request.args.get("title")
    genre = request.args.get("genre")
    price = request.args.get("price")
    
    book = {
        "book_id":book_id,
        "author":author,
        "title":title,
        "genre":genre,
        "price":price
    }
    
    if request.method == "POST":
        book_id = request.form["book_id"]
        g.db = connect_db()
        conn = g.db.cursor()
        conn.execute("DELETE FROM books WHERE id=?", [book_id])
        g.db.commit()
        g.db.close()
        
        return redirect(url_for('main'))
    
    return render_template("delete.html", book_record=book)
    

    
    
if __name__ == "__main__":
    app.run(host=host, port=port, debug=True)
    
    

