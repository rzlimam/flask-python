from flask import Flask
from flask_mysqldb import MySQL

app = Flask(__name__, static_folder='./Flask/static')



app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'db_flask'

db = MySQL(app)

from views import *

if __name__ == '__main__':
    app.run(debug=True)
