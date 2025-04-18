from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import Customer
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from .utilities import logout_required

auth = Blueprint('auth', __name__)

@auth.route('/signup', methods=['GET', 'POST'])
@logout_required
def sign_up():
    if request.method=='POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        customer = Customer.query.filter_by(email=email).first()
        if customer:
            flash('Email already exists.', category='error')
        elif len(email) <= 10:
            flash('Email must be greater than 10 characters.', category='error')
        elif len(username) <= 6:
            flash('Username must be greater than 6 characters.', category='error')
        elif len(password1) < 8:
            flash('Password must be at least 8 characters long.', category='error')
        elif password1 != password2:
            flash('Password do not match.', category='error')
        elif Customer.query.filter_by(email=email).first():
            flash('Email already exists.',category='error')
        else:
            new_customer = Customer(email=email, username=username, password=password2)
            db.session.add(new_customer)
            db.session.commit()
            flash('Account created.', category='success')
            login_user(new_customer, remember='True')
            return redirect(url_for('views.home'))
    return render_template("signup.html", user=current_user)


@auth.route('/login', methods=['GET', 'POST'])
@logout_required
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        customer = Customer.query.filter_by(email=email).first()
        if customer:
            if check_password_hash(customer.password, password):
                flash('Login successfully.', category='success')
                login_user(customer, remember='True')
                return redirect(url_for('views.home'))
            else:
                flash('Password incorrect.', category='error')
        else:
            flash('Email does not exist.', category='error')
    return render_template("login.html", customer=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('views.home'))



