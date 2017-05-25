import sqlite3

with sqlite3.connect("books.db") as connection:
	conn = connection.cursor()

	# alter existing books table by renaming it
	conn.execute("ALTER TABLE books RENAME TO book_old")

	# create new books table with primary key constraint
	conn.execute("CREATE TABLE books(id INTEGER PRIMARY KEY AUTOINCREMENT, author TEXT, title TEXT, genre TEXT, price REAL)")

	# fetch data from old books table
	conn.execute("SELECT * FROM book_old")
	old_books_data = conn.fetchall()
	print(old_books_data)
	

	# insert all records from old books table into new books table
	for book in old_books_data:
	    conn.execute("INSERT INTO books (author, title, genre, price) VALUES (?, ?, ?, ?)", [book[0], book[1], book[2], book[3]])

	# check records successfully transferred
	conn.execute("SELECT * FROM books")

	books_data = conn.fetchall()
	print("Books record - ", books_data)

	# delete books_old table
	conn.execute("DROP TABLE book_old")