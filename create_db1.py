import sqlite3

with sqlite3.connect("books.db") as connection:
    conn = connection.cursor()
    conn.execute("DROP TABLE books")
    conn.execute("CREATE TABLE IF NOT EXISTS books(author TEXT, title TEXT, genre TEXT, price REAL)")
    books_data = [
            ("Steven King", "IT", "Horror", 7.99),
            ("Dan Brown", "The Davinci Code", "Thriller", 8.99),
            ("Alexander Dumas", "The Count of Monte Cristo", "Adventure", 10.99),
            ("James H. Chase", "Shogun", "Action", 3.55)
        ]
    conn.executemany("INSERT INTO books VALUES(?, ?, ?, ?)", books_data)
    
    conn.execute("SELECT * FROM books")
    data = conn.fetchall()
    print(data)
    
    
    