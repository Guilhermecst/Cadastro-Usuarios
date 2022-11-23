from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = 'secreteKey'
login_manager = LoginManager(app)

db = SQLAlchemy(app)


from views import *

if __name__ == '__main__':
    app.run(debug=True)