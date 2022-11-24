from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from config import SECRET_KEY

app = Flask(__name__)
app.config.from_pyfile('config.py')
app.config['SECRET_KEY'] = SECRET_KEY
login_manager = LoginManager(app)

email = 'contato.salaobarbearia@gmail.com'
senha = 'obphdvlonygiaqsu'

app.config.update(
	DEBUG=True,
	#EMAIL SETTINGS
	MAIL_SERVER='smtp.gmail.com',
	MAIL_PORT=465,
	MAIL_USE_SSL=True,
	MAIL_USERNAME = email,
	MAIL_PASSWORD = senha
	)
    
mail = Mail(app)

db = SQLAlchemy(app)


from views import *

if __name__ == '__main__':
    app.run(debug=True)