# Temp file to create db
import sqlite3

connection = sqlite3.connect("books.db")
conn = connection.cursor()

conn.execute("CREATE TABLE IF NOT EXISTS books(Id INTEGER PRIMARY KEY AUTOINCREMENT, Author TEXT, Title TEXT, Genre TEXT,\
              Price REAL)")
books_data = [
    ("Judith Kranz", "I'll Take Manhattan", "Drama", 8.99),
    ("Steven King", "Carrie", "Horror", 7.99),
    ("Sandra Brown", "Richochet", "Drama", 9.99),
    ("Dan Brown", "The Da Vinci Code", "Thriller", 12.49)
]

conn.executemany("INSERT INTO books (Author, Title, Genre, Price) VALUES(?, ?, ?, ?)", books_data)
connection.commit()
connection.close()
