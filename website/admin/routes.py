from flask import render_template, session, request, redirect, url_for, flash
from website import app, db, bcrypt
from .form import RegistrationForm, LoginForm
from website.products.models import AddProduct, Brand, Category
from .models import Admin

@app.route('/admin')
def admin():
    if 'email' not in session:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('login'))
    products = AddProduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/admin/brands')
def brands():
    if 'email' not in session:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brands Page', brands=brands)

@app.route('/admin/categories')
def categories():
    if 'email' not in session:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('login'))
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Categories Page', categories=categories)

@app.route('/admin/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm(request.form)
    if request.method == 'POST' and form.validate():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        user = Admin(username=form.username.data, email=form.email.data,
                     password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Welcome {form.username.data}! Thank you for registering.', 'success')
        return redirect(url_for('admin'))
    return render_template('admin/register.html', form=form, title='Register Page')

@app.route('/admin/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = Admin.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            session['email'] = form.email.data
            flash(f'Welcome {user.username}! You are logged in.', 'success')
            return redirect(request.args.get('next') or url_for('admin'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
            return redirect(url_for('login'))
    return render_template('admin/login.html', form=form, title='Login Page')
