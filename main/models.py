from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from main import db, login_manager, app, admin
from flask_login import UserMixin
from flask import session
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


@login_manager.user_loader
def load_user(user_id):
    if session['account_type'] == 'Employer':
        return Employers.query.get(int(user_id))
    elif session['account_type'] == 'User':
        return User.query.get(int(user_id))
    else:
        return None


class User(db.Model, UserMixin):

    __tablename__ = 'user'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    id_number = db.Column(db.Integer, unique=True, nullable=False)
    birth = db.Column(db.Integer, nullable=False)
    gender = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(100), unique=True, nullable=False)
    location = db.Column(db.String(100), nullable=False)
    profession = db.Column(db.String(100), nullable=False)
    employer = db.Column(db.String(100), nullable=False)
    qualification = db.Column(db.String(50), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='user')
    image_file = db.Column(db.String(20), nullable=False, default='default.jpeg')
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    # def __repr__(self):
        # return f"{self.name}, {self.location}, {self.profession}"

    def get_reset_token(self, expires_sec=1800):
        s = Serializer(app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']
        except:
            return None
        return User.query.get(user_id)


class Employers(db.Model, UserMixin):
    __tablename__ = 'employers'
    id = db.Column(db.Integer, primary_key=True)
    employer_Name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    kra_pin = db.Column(db.String(13), unique=True, nullable=False)
    business_registration_number = db.Column(db.String(100), unique=True, nullable=False)
    postal_address = db.Column(db.String(100), unique=True, nullable=False)
    town = db.Column(db.String(100), nullable=False)
    county = db.Column(db.String(100), nullable=False)
    physical_address = db.Column(db.String(100), nullable=False)
    mobile = db.Column(db.String(15), unique=True, nullable=False)
    website = db.Column(db.String(100), unique=True, nullable=False)
    economic_activity = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(100), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.employer_Name}, {self.email}, {self.business_registration_number}, {self.date_created}"


class Subscriptions(db.Model):

    __tablename__ = 'subscriptions'

    id = db.Column(db.Integer, primary_key=True)
    subscription = db.Column(db.String(20), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    id_number = db.Column(db.Integer, nullable=False)
    subscription_date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.subscription}, {self.amount}, {self.subscription_date}"


class MyModelView(ModelView):
    column_exclude_list = ['password', 'image_file']
    can_delete = False # disable model deletion
    can_create = False
    column_searchable_list = ('name', 'id_number', 'profession', 'location')
    page_size = 50

    def is_accessible(self):
        # Use the role column to determine who accesses the page
        return current_user.is_authenticated and current_user.role == 'admin'


class SubModelView(ModelView):
    can_delete = False  # disable model deletion
    can_create = False
    can_edit = False
    can_export = True
    column_searchable_list = ('subscription', 'id_number')
    page_size = 50

    def is_accessible(self):
        # Use the role column to determine who accesses the page
        return current_user.is_authenticated and current_user.role == 'admin'


admin.add_view(MyModelView(User, db.session))
admin.add_view(SubModelView(Subscriptions, db.session))



