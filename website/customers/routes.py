from flask import redirect, render_template, url_for, flash, request, session, current_app
from website import app, db, photos, search, bcrypt
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register
import os
import secrets
from flask_login import login_required, current_user, logout_user, login_user

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        hash_password = bcrypt.generate_password_hash(form.password.data)
        customer = Register(name=form.name.data, username=form.username.data, email=form.email.data,
                            password=hash_password, country=form.country.data, city=form.city.data,
                            contact=form.contact.data, address=form.address.data, zipcode=form.zipcode.data)
        db.session.add(customer)
        flash(f'Welcome {form.name.data}, Thanks for registering', 'success')
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('customers/register.html', form=form)

@app.route('/customer/login', methods=['GET', 'POST'])
def customer_login():
    form = CustomerLoginForm()
    if form.validate_on_submit():
        customer = Register.query.filter_by(email=form.email.data).first()
        if customer and bcrypt.check_password_hash(customer.password, form.password.data):
            login_user(customer)
            flash(f"Welcome {customer.name}", 'success')
            next = request.args.get('next')
            return redirect(next or url_for('home'))
        flash('Invalid email or password', 'danger')
        return redirect(url_for('customer_login'))

    return render_template('customers/login.html', form=form)

# @app.route('customer/logout')
# def customer_logout():
#     logout_user()
#     return redirect(url_for('customer_login'))