# configuration details for flask app
import os

# grab the directory where script is located
basedir = os.path.abspath(os.path.dirname(__file__))

DATABASE = "books.db"
USERNAME = 'admin'
PASSWORD = 'admin'
WTF_CSRF_ENABLED = True
SECRET_KEY = 'my_password'

# full path for database
DATABASE_PATH = os.path.join(basedir, DATABASE)



