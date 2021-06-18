from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_admin import Admin
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '2008de4bbf105d61f26a763f8ee8023b'
database = 'postgres://ikklvnabvallrb:1b8b1eb57f9495e6cd8d576ec6d2713425ac4ef97849b8b4ca9387e356197b71@ec2-34-192-58-41.compute-1.amazonaws.com:5432/d4ppsk1kj9brfe'
app.config['SQLALCHEMY_DATABASE_URI'] = database
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
admin = Admin(app, name='MESL', template_mode='bootstrap4')
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'
app.config['FLASK_ADMIN_SWATCH'] = 'Slate'

app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = 'regansomi@gmail.com'
app.config['MAIL_PASSWORD'] = 'reganzmuthom'
mail = Mail(app)


from main import routes
