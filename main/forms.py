from flask_wtf import FlaskForm
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError
from password_strength import PasswordPolicy, PasswordStats
from main.models import User, Employers

style = {'class': 'button', 'style': 'width:50%; background-color: #283891; color: #ffffff; border-radius: 20px;'}
style_remember = {'style': 'width:2px; margin:2px;'}
style_sub = {'style': 'width:100%; height:45px; border: 1px solid #5F5FB0'}
style_register = {'class': 'button', 'style': 'width:50%; background-color: #283891; color: #ffffff; border-radius: 20px; padding: 10px; border: 1px solid #5F5FB0;'}
style_update = {'class': 'button', 'style': 'width:auto; background-color: #BADCD4; border-radius: 5px; padding: 5px 10px; border: 1px solid #5F5FB0; float: center;'}
style_checkout = {'class': 'button', 'style': 'width:auto; background-color: #BADCD4; border-radius: 5px; padding: 10px; border: 1px solid #5F5FB0; margin-top: 20px; '}
style_payment = {'class': 'button', 'style': 'width:30%; background-color: #283891; color: #ffffff; border-radius: 5px; padding: 10px; border: 1px solid #5F5FB0;'}


class Registration(FlaskForm):
    options = ['-- Profession --', 'Seamanship', 'Navigation', 'Marine Seals', 'Deep Sea Divers', 'Search and Rescue (SAR)', 'Nuclear Biological Chemical',
                'Defence', 'Marine and Electrical Engineers', 'Shipwrights', 'Disaster Preparedness and Management Consultants', 'Marine Commandos',
                'Logisticians', 'ICT Experts', 'Armourers', 'Medical Fraternity', 'Paratroopers', 'Watch Keeping']
    qualify = ['-- Level of Qualification --', 'PhD', 'Masters', 'Degree', 'Diploma', 'Technician', 'Artisan']
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=20)], render_kw={"placeholder": "Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    id_number = IntegerField('Id_no', validators=[DataRequired()])
    birth = IntegerField('YoB', validators=[DataRequired()])
    gender = SelectField('Gender', validators=[DataRequired()], choices=['-- Gender --', 'Male', 'Female', 'Other'])
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Mobile"})
    location = StringField('Current location', validators=[DataRequired()])
    profession = SelectField('Profession', validators=[DataRequired()], choices=options)
    prev_employer = StringField('Employer', validators=[DataRequired()])
    qualification = SelectField('Qualification', validators=[DataRequired()], choices=qualify)
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register', render_kw=style_register)

    # Verification whether username exist in Db
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        employer = Employers.query.filter_by(email=email.data).first()
        if user or employer:
            raise ValidationError('Email already exists')

    # Verification whether username exist in Db
    def validate_id(self, id_number):
        user = User.query.filter_by(id_number=id_number.data).first()
        if user:
            raise ValidationError('ID Number already exists! Please confirm.')

    # Check password strength
    def validate_password(self, password):
        policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1, special=1, strength=0.30)
        password = password.data
        stats = PasswordStats(password)
        checkpolicy = policy.test(password)
        if stats.strength() < 0.30:
            raise ValidationError('Password too weak! Avoid consecutive characters and easily guessed numbers!')


class EmployerRegistration(FlaskForm):
    options = ['- County -', 'Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita Taveta', 'Garissa', 'Wajir',
               'Mandera', 'Marsabit', 'Isiolo', 'Meru', 'Tharaka Nithi', 'Embu', 'Kitui', 'Machakos', 'Makueni'
               'Nyandarua', 'Nyeri', 'Kirinyaga', 'Muranga', 'Kiambu', 'Turkana', 'West Pokot', 'Samburu',
               'Trans Nzoia', 'Uasin Gishu', 'Elgeyo Marakwet', 'Nandi', 'Baringo', 'Laikipia', 'Nakuru', 'Narok',
               'Kericho', 'Bomet', 'Kakamega', 'Vihiga', 'Bungoma', 'Busia', 'Siaya', 'Kisumu', 'Homa Bay', 'Migori',
               'Kisii', 'Nyamira', 'Nairobi']
    employer = StringField('employerName', validators=[DataRequired(), Length(min=3, max=20)],
                           render_kw={"placeholder": "Employer Name"})
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    kra = StringField('KRA Pin', validators=[DataRequired()])
    registration = StringField('Business Registration', validators=[DataRequired()])
    postal_address = StringField('Postal Address', validators=[DataRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Postal Address"})
    town = StringField('Town', validators=[DataRequired()])
    county = SelectField('County', validators=[DataRequired()], choices=options)
    physical_address = StringField('Physical Address', validators=[DataRequired()])
    mobile = StringField('Office Line', validators=[DataRequired(), Length(min=3, max=20)])
    website = StringField('Website', validators=[DataRequired(), Length(min=3, max=100)])
    economic_activity = StringField('Economic Activity', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8, max=200)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Register', render_kw=style_register)

    # Verification whether username exist in Db
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        employer = Employers.query.filter_by(email=email.data).first()
        if user or employer:
            raise ValidationError('Email already exists! Please try another.')

    def validate_kra(self, kra):
        user = User.query.filter_by(kra=kra.data).first()
        if user:
            raise ValidationError('KRA pin already exists! Please confirm.')

    # Check employer password strength
    def validate_password(self, password):
        policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1, special=1, strength=0.30)
        password = password.data
        stats = PasswordStats(password)
        if stats.strength() < 0.30:
            raise ValidationError('Password too weak! Avoid consecutive characters and easily guessed numbers!')


class Login(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=200)], render_kw={"placeholder": "Password"})
    remember = BooleanField('Remember me', render_kw=style_remember)
    submit = SubmitField('Continue', render_kw=style)


# Request for a password reset
class Request_reset_form(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    submit = SubmitField('Request Password Reset', render_kw=style_checkout)

    # Check whether the email address is already in the database
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        employer = Employers.query.filter_by(email=email.data).first()
        if user is None or employer is None:
            raise ValidationError('Email does not exist! Register or confirm email')


# Reset password
class Reset_password(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired(), Length(min=5, max=200)], render_kw={"placeholder": "Password"})
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')], render_kw={"placeholder": "Confirm Password"})
    submit = SubmitField('Reset', render_kw=style_register)

    def validate_password(self, password):
        policy = PasswordPolicy.from_names(length=8, uppercase=1, numbers=1,special=1, strength=0.66)
        password = password.data
        stats = PasswordStats(password)
        checkpolicy = policy.test(password)
        if stats.strength() < 0.30:
            raise ValidationError('Password too weak! Avoid consecutive characters and easily guessed numbers!')


class Update(FlaskForm):
    qualify = ['-- Level of Qualification --', 'PhD', 'Masters', 'Degree', 'Diploma', 'Technician', 'Artisan']
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Mobile"})
    location = StringField('Current location', validators=[DataRequired()])
    prev_employer = StringField('Employer', validators=[DataRequired()])
    qualification = SelectField('Qualification', validators=[DataRequired()], choices=qualify)
    submit = SubmitField('Update', render_kw=style_update)

    # Verification whether email exist in Db
    def validate_email(self, email):
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')


class ClientUpdate(FlaskForm):
    options = ['- County -', 'Mombasa', 'Kwale', 'Kilifi', 'Tana River', 'Lamu', 'Taita Taveta', 'Garissa', 'Wajir',
               'Mandera', 'Marsabit', 'Isiolo', 'Meru', 'Tharaka Nithi', 'Embu', 'Kitui', 'Machakos', 'Makueni'
               'Nyandarua', 'Nyeri', 'Kirinyaga', 'Muranga', 'Kiambu', 'Turkana', 'West Pokot', 'Samburu',
               'Trans Nzoia', 'Uasin Gishu', 'Elgeyo Marakwet', 'Nandi', 'Baringo', 'Laikipia', 'Nakuru', 'Narok',
               'Kericho', 'Bomet', 'Kakamega', 'Vihiga', 'Bungoma', 'Busia', 'Siaya', 'Kisumu', 'Homa Bay', 'Migori',
               'Kisii', 'Nyamira', 'Nairobi']
    email = StringField('Email', validators=[DataRequired(), Email()], render_kw={"placeholder": "Email"})
    postal_address = StringField('Postal Address', validators=[DataRequired(), Length(min=0, max=20)], render_kw={"placeholder": "Postal Address"})
    town = StringField('Town', validators=[DataRequired()])
    county = SelectField('County', validators=[DataRequired()], choices=options)
    physical_address = StringField('Physical Address', validators=[DataRequired()])
    mobile = StringField('Office Line', validators=[DataRequired(), Length(min=3, max=20)])
    website = StringField('Website', validators=[DataRequired(), Length(min=3, max=100)])
    submit = SubmitField('Update', render_kw=style_update)

    # Verification whether email exist in Db
    def validate_email(self, email):
        if email.data != current_user.email:
            user = Employers.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError('Email already exists')

    # Verification whether website exist in Db
    def validate_website(self, website):
        if website.data != current_user.website:
            user = Employers.query.filter_by(website=website.data).first()
            if user:
                raise ValidationError('Website already exists')


class Payment(FlaskForm):
    subs = ['Platinum', 'Gold', 'Silver', 'Bronze', 'Ordinary']
    cards = ['Visa', 'Mastercard', 'Amex', 'Discover', 'Other']
    subscription = SelectField('Subscription', validators=[DataRequired()], choices=subs, render_kw=style_sub)
    card = SelectField('Card', validators=[DataRequired()], choices=cards, render_kw=style_sub)
    first_name = StringField('First Name', validators=[DataRequired()])
    last_name = StringField('Last Name', validators=[DataRequired()])
    card_number = IntegerField('Card Number', validators=[DataRequired()])
    expiration_month = IntegerField('Expiration Month', validators=[DataRequired()])
    expiration_year = IntegerField('Expiration Year', validators=[DataRequired()])
    card_cvv = IntegerField('CVV', validators=[DataRequired()])
    submit = SubmitField('Pay Now', render_kw=style_payment)


class Mobile(FlaskForm):
    subs = ['Platinum', 'Gold', 'Silver', 'Bronze', 'Ordinary']
    subscription = SelectField('Subscription', validators=[DataRequired()], choices=subs, render_kw=style_sub)
    mobile = StringField('Mobile', validators=[DataRequired(), Length(min=0, max=20)],
                         render_kw={"placeholder": "Mobile. e.g (254700000000)"})
    submit = SubmitField('Pay Now', render_kw=style_payment)
