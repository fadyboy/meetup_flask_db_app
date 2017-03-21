import sqlite3

with sqlite3.connect("books.db") as connection:
    conn = connection.cursor()
    conn.execute("CREATE TABLE IF NOT EXISTS books(author TEXT, title TEXT, genre TEXT, price REAL)")
    
    books_data = [
            ("Steven King", "It", "Horror", 5.99),
            ("Dan Brown", "The Davinci Code", "Thriller", 4.99),
            ("Alexander Dumas", "The Count of Monte Cristo", "Adventure", 10.99),
            ("James H. Chase", "This way for a shroud", "Action", 3.50)
        ]
        
    conn.executemany("INSERT INTO books VALUES(?, ?, ?, ?)", books_data)
    conn.execute("SELECT * FROM books")
    book = conn.fetchone()
    print(book)