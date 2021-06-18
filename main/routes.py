from flask import url_for, render_template, flash, redirect, request, session
from main import app, db, bcrypt, mail, admin
from main.forms import (Registration, Login, Request_reset_form, Reset_password, Payment,
                        Mobile, EmployerRegistration, Update, ClientUpdate)
from main.models import User, Subscriptions, Employers
from flask_admin import BaseView, expose
from flask_login import login_user, current_user, logout_user, login_required
from flask_mail import Message
from rave_python import Rave, RaveExceptions, Misc


class Dashboard(BaseView):
    @expose('/')
    def index(self):
        users = User.query.all()
        subs = Subscriptions.query.all()
        total_users = []
        platinum = []
        gold = []
        silver = []
        bronze = []
        ordinary = []
        for u in users:
            total_users.append(u.name)
        for s in subs:
            if s.subscription == 'Platinum':
                platinum.append(s)
            elif s.subscription == 'Gold':
                gold.append(s)
            elif s.subscription == 'Silver':
                silver.append(s)
            elif s.subscription == 'Bronze':
                bronze.append(s)
            elif s.subscription == 'Ordinary':
                ordinary.append(s)
        p = len(platinum)
        g = len(gold)
        s = len(silver)
        b = len(bronze)
        o = len(ordinary)
        no_users = len(total_users)
        if current_user.role == 'admin':
            return self.render('dashboard.html', no_users=no_users, p=p, g=g, s=s, b=b, o=o)
        else:
            flash(f"{current_user.name} can't view dashboard! Admin Only", 'danger')
        return redirect(url_for('portal'))


admin.add_view(Dashboard(name='Dashboard'))


# Flutterwave card payment function
def flutter_payments(form, amount):
    # Payload with pin
    rave = Rave("FLWPUBK_TEST-6552fcf87bea2389633d971496e4fa4c-X", "FLWSECK_TEST-518b44bafe055e63d34dc38ca652de63-X", usingEnv=False)
    payload = {
            "cardno": str(form.card_number.data),
            "cvv": str(form.card_cvv.data),
            "currency": "KES",
            "expirymonth": str(form.expiration_month.data),
            "expiryyear": str(form.expiration_year.data),
            "amount": amount,
            "email": str(current_user.email),
            "phonenumber": str(User.mobile),
            "firstname": str(form.first_name.data),
            "lastname": str(form.last_name.data),
            "IP": "355426087298442"}

    try:
        res = rave.Card.charge(payload)

        if res["suggestedAuth"]:
            arg = Misc.getTypeOfArgsRequired(res["suggestedAuth"])

            if arg == "pin":
                Misc.updatePayload(res["suggestedAuth"], payload, pin="3310")
            if arg == "address":
                Misc.updatePayload(res["suggestedAuth"], payload, address={"billingzip": "07205", "billingcity": "Hillside",
                                                                           "billingaddress": "470 Mundet PI",
                                                                           "billingstate": "NJ", "billingcountry": "US"})

            res = rave.Card.charge(payload)

        if res["validationRequired"]:
            rave.Card.validate(res["flwRef"], "12345")

        res = rave.Card.verify(res["txRef"])
        return str(res["transactionComplete"])

    except RaveExceptions.CardChargeError as e:
        flash(e.err["errMsg"], 'danger')

    except RaveExceptions.TransactionValidationError as e:
        flash(e.err, 'danger')

    except RaveExceptions.TransactionVerificationError as e:
        flash(e.err["errMsg"], 'danger')


# Fluttewave Mpesa payment
def fluttermobile(form, amount):
    rave = Rave("FLWPUBK_TEST-6552fcf87bea2389633d971496e4fa4c-X", "FLWSECK_TEST-518b44bafe055e63d34dc38ca652de63-X", usingEnv=False)

    # mobile payload
    payload = {
        "amount": amount,
        "phonenumber": str(form.mobile.data),
        "email": str(current_user.email),
        "IP": "40.14.290",
        "narration": "funds payment",
    }

    try:
        res = rave.Mpesa.charge(payload)
        res = rave.Mpesa.verify(res["txRef"])
        return res['chargemessage']

    except RaveExceptions.TransactionChargeError as e:
        flash(e.err["errMsg"], 'danger')

    except RaveExceptions.TransactionVerificationError as e:
        flash(e.err["errMsg"], 'danger')


# Sign-up email
def send_signup_email(user):
    msg = Message('Marine Escort (MESL) Signup', sender='regansomi@gmail.com', recipients=[user])
    msg.body = ''' Thank You for joining Marine Escorts. Please subscribe to our packages to enjoy all our
    services.'''
    mail.send(msg)


# Home
@app.route('/')
@app.route('/home')
def home():
    if current_user.is_authenticated:
        experts = User.query.filter_by(email=current_user.email).first()
        return render_template('index.html', experts=experts)
    else:
        return render_template('index.html')


# About
@app.route('/about')
def about():
    return render_template('about.html')


# Resource page
@app.route('/resources')
def resource():
    return render_template('resource.html')


# Resource page
@app.route('/news')
def news():
    return render_template('news.html')


# Resource page
@app.route('/contact')
def contact():
    return render_template('contact.html')


# Client Login
@app.route('/client-login', methods=['POST', 'GET'])
def client_login():
    form = Login()
    if current_user.is_authenticated:
        session['account_type'] = 'Employer'
        return redirect(url_for('client_portal'))
    if form.validate_on_submit():
        user = Employers.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in as {current_user.employer_Name}!', 'success')
            session['account_type'] = 'Employer'
            return redirect(next_page) if next_page else redirect(url_for('client_portal'))
        else:
            flash(f'Invalid password or email', 'danger')
    return render_template('login.html', form=form)


# Expert Login
@app.route('/login', methods=['POST', 'GET'])
def login():
    form = Login()
    if current_user.is_authenticated:
        session['account_type'] = 'User'
        return redirect(url_for('expert_portal'))
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f'Logged in as {current_user.name}!', 'success')
            session['account_type'] = 'User'
            return redirect(next_page) if next_page else redirect(url_for('expert_portal'))
        else:
            flash(f'Invalid password or email', 'danger')
    return render_template('login.html', form=form)


# Employer registration.
@app.route('/client-signup', methods=['POST', 'GET'])
def client_register():
    if current_user.is_authenticated:
        return redirect(url_for('portal'))
    form = EmployerRegistration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        employer = Employers(employer_Name=form.employer.data,
                             email=form.email.data,
                             kra_pin=form.kra.data,
                             business_registration_number=form.registration.data,
                             postal_address=form.postal_address.data,
                             town=form.town.data,
                             county=form.county.data,
                             physical_address=form.physical_address.data,
                             mobile=form.mobile.data,
                             website=form.website.data,
                             economic_activity=form.economic_activity.data,
                             password=hashed_password,
                             )
        db.session.add(employer)
        db.session.commit()
        flash(f'Account created for {form.employer.data}! Now log in.', 'success')
        return redirect(url_for('client_login'))
    return render_template('employer-register.html', form=form)


# Registration
@app.route('/signup', methods=['POST', 'GET'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('expert_portal'))
    form = Registration()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(name=form.name.data,
                    email=form.email.data,
                    id_number=form.id_number.data,
                    birth=form.birth.data,
                    gender=form.gender.data,
                    mobile=form.mobile.data,
                    location=form.location.data,
                    profession=form.profession.data,
                    employer=form.prev_employer.data,
                    qualification=form.qualification.data,
                    password=hashed_password,
                    )
        db.session.add(user)
        db.session.commit()
        flash(f'Account created for {form.name.data}! Now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)


# Logout
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


# Client Portal
@app.route('/portal', methods=['POST', 'GET'])
@login_required
def client_portal():
    client = Employers.query.filter_by(email=current_user.email).first()
    users = User.query.all()
    return render_template('portal.html', client=client, users=users)


# Expert Portal
@app.route('/expert-portal', methods=['POST', 'GET'])
@login_required
def expert_portal():
    experts = User.query.filter_by(email=current_user.email).first()
    return render_template('expert_portal.html', experts=experts)


@app.route('/expert-profile-update', methods=['POST', 'GET'])
@login_required
def update_expert_profile():
    form = Update()
    experts = User.query.filter_by(email=current_user.email).first()
    if experts:
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.mobile = form.mobile.data
            current_user.location = form.location.data
            current_user.employer = form.prev_employer.data
            current_user.qualification = form.qualification.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('expert_portal'))
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.mobile.data = current_user.mobile
            form.location.data = current_user.location
            form.prev_employer.data = current_user.employer
            form.qualification.data = current_user.qualification
    else:
        flash('Must be logged in as expert to update expert account', 'danger')
    return render_template('expert_account_update.html', form=form, experts=experts)


@app.route('/client-profile-update', methods=['POST', 'GET'])
@login_required
def update_client_profile():
    form = ClientUpdate()
    clients = Employers.query.filter_by(email=current_user.email).first()
    if clients:
        if form.validate_on_submit():
            current_user.email = form.email.data
            current_user.postal_address = form.postal_address.data
            current_user.town = form.town.data
            current_user.county = form.county.data
            current_user.physical_address = form.physical_address.data
            current_user.mobile = form.mobile.data
            current_user.website = form.website.data
            db.session.commit()
            flash('Your account has been updated', 'success')
            return redirect(url_for('portal'))
        elif request.method == 'GET':
            form.email.data = current_user.email
            form.postal_address.data = current_user.postal_address
            form.town.data = current_user.town
            form.county.data = current_user.county
            form.physical_address.data = current_user.physical_address
            form.mobile.data = current_user.mobile
            form.website.data = current_user.website
    else:
        flash('Must be logged in as client to update client account', 'danger')
    return render_template('client_account_update.html', form=form, clients=clients)


# Manage subscriptions
def manage_subscriptions(form):
    if form.subscription.data == 'Platinum':
        return 5000
    elif form.subscription.data == 'Gold':
        return 4000
    elif form.subscription.data == 'Silver':
        return 3000
    elif form.subscription.data == 'Bronze':
        return 2000
    elif form.subscription.data == 'Ordinary':
        return 1000


# Payment
@app.route('/payment', methods=['POST', 'GET'])
@login_required
def payment():
    form = Payment()
    if form.validate_on_submit():
        subscribe = Subscriptions(
            subscription=form.subscription.data,
            amount=manage_subscriptions(form),
            id_number=current_user.id_number
        )
        db.session.add(subscribe)
        db.session.commit()
        if flutter_payments(form, manage_subscriptions(form)) == 'True':
            flash('Transaction Successful!', 'success')
            return redirect(url_for('portal'))
        else:
            flash('Transaction was not successful! Please try again.', 'danger')

    return render_template('payment.html', form=form)


# Mpesa
# Payment
@app.route('/mobile', methods=['POST', 'GET'])
@login_required
def mobile():
    form = Mobile()
    if form.validate_on_submit():
        subscribe = Subscriptions(
            subscription=form.subscription.data,
            amount=manage_subscriptions(form),
            id_number=current_user.id_number
        )
        db.session.add(subscribe)
        db.session.commit()
        if fluttermobile(form, manage_subscriptions(form)) == 'Successful':
            flash('Transaction Successful!', 'success')
            return redirect(url_for('portal'))
        else:
            flash('Transaction was not successful! Please try again.', 'danger')

    return render_template('mobilepayment.html', form=form)


# Send password reset email
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset', sender='regansomi@gmail.com', recipients=[user.email])
    msg.body = f''' To reset your password, visit the following link:
{url_for('reset_password', token=token, _external=True)}
If you did not make this request please ignore this email. No changes will be made in your account.
'''
    mail.send(msg)


# Request password reset
@app.route('/reset_form', methods=['POST', 'GET'])
def reset_form():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = Request_reset_form()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        send_reset_email(user)
        flash('We have sent you an email on how to reset your password.', 'info')
        return redirect(url_for('login'))
    return render_template('request_reset.html', form=form)


# password reset
@app.route('/reset_password/<token>', methods=['POST', 'GET'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('Token Invalid or Expired.', 'warning')
        return redirect(url_for('reset_form'))
    form = Reset_password()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user.password = hashed_password
        db.session.commit()
        flash(f'Password has been updated! Now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

