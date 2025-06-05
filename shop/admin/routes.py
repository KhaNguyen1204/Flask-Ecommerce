from flask import render_template, session, request, redirect, url_for, flash
from shop import app, db, bcrypt, photos
import secrets
import os
from .forms import StaffRegistrationForm, LoginForm, ChangePasswordForm, RoleForm
from shop.products.models import AddProduct, Brand, Category
from .models import Staff
from shop.models import User, Role
from shop.decorators import role_required
from shop.customers.model import Customer, Order, OrderDetail
from shop.customers.forms import CustomerRegisterForm
from flask_login import current_user, logout_user, login_user

@app.route('/admin')
@role_required(['admin'])
def admin():
    products = AddProduct.query.all()
    return render_template('admin/index.html', title='Admin Page', products=products)

@app.route('/brands')
@role_required(['admin', 'sale', 'storekeeper'])
def brands():
    brands = Brand.query.order_by(Brand.id.desc()).all()
    return render_template('admin/brand.html', title='Brands Page', brands=brands)

@app.route('/categories')
@role_required(['admin', 'sale', 'storekeeper'])
def categories():
    categories = Category.query.order_by(Category.id.desc()).all()
    return render_template('admin/brand.html', title='Categories Page', categories=categories)

@app.route('/admin/register', methods=['GET', 'POST'])
def admin_register():
    """
    Đăng ký tài khoản admin. Nếu chưa có admin thì có thể tạo tài khoản admin đầu tiên
    không yêu cầu quyền. Nếu tạo tài khoản admin từ lần 2 thì phải có quyền admin.
    :return:
    """
    # Kiểm tra đã có admin hay chưa
    admin_role = Role.query.filter_by(name='admin').first()
    if admin_role:
        admin_exists = User.query.filter_by(role_id=admin_role.id).first()
    else:
        admin_exists = False
        admin_role = Role(name='admin')
        db.session.add(admin_role)
        db.session.commit()

    if admin_exists:
        # Nếu đã có admin mà chưa đăng nhập thì yêu cầu đăng nhập
        if not current_user.is_authenticated or current_user.role.name != 'admin':
            flash('You do not have permission to access this page.', 'danger')
            return redirect(url_for('login'))

    form = StaffRegistrationForm(request.form)
    # Không cần thiết lập choices cho role_id vì nó sẽ được gán tự động
    if request.method == 'POST':
        # Loại bỏ role_id khỏi xác thực biểu mẫu
        form.role_id.data = admin_role.id  # Gán role_id tự động
        if form.validate():
            # Kiểm tra email hay phone đã nhập chưa
            email = form.email.data
            phone = form.phone.data
            if not email or not phone:
                flash('Email and phone are required', 'danger')
                return redirect(url_for('admin_register'))

            # Kiểm tra email đã tồn tại chưa
            user = User.query.filter_by(email=form.email.data).first()
            if user:
                flash(f'Warning {form.email.data} has been registered already', 'danger')
                return redirect(url_for('admin_register'))

            # Kiểm tra phone đã được sử dụng chưa
            phone_user = User.query.filter_by(phone=form.phone.data).first()
            if phone_user:
                flash(f'Phone number {form.phone.data} is already registered', 'danger')
                return redirect(url_for('admin_register'))

            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            admin = Staff(
                username=form.username.data,
                email=form.email.data,
                phone=phone,
                password=hashed_password,
                position=form.position.data,
                role_id=admin_role.id  # Gán role_id trực tiếp
            )
            db.session.add(admin)
            db.session.commit()
            flash(f'Welcome {form.username.data}! Admin account created successfully.', 'success')
            return redirect(url_for('login'))
        else:
            # Hiển thị lỗi xác thực chi tiết
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f'Lỗi ở trường {field}: {error}', 'danger')

    return render_template('admin/register.html', form=form, title='Register Page')

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user)
            session['email'] = user.email
            session['role'] = user.role.name

            flash(f'Welcome {user.username}! You are logged in.', 'success')

            # Redirect based on role
            if user.role.name == 'admin':
                return redirect(url_for('admin'))
            elif user.role.name == 'storekeeper':
                return redirect(url_for('warehouse'))
            elif user.role.name == 'sale':
                return redirect(url_for('sales'))
            elif user.role.name == 'accountancy':
                return redirect(url_for('finance_management'))
            elif user.role.name == 'customer':
                return redirect(url_for('home'))
            else:
                flash('You do not have permission to access this page.', 'danger')
                return redirect(url_for('login'))
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')
    return render_template('login.html', form=form, title='Login Page')

@app.route('/change_password', methods=['GET', 'POST'])
def change_password():
    if 'email' not in session:
        flash('Please login to access this page.', 'danger')
        return redirect(url_for('login'))
    form = ChangePasswordForm(request.form)
    if request.method == 'POST' and form.validate():
        user = User.query.filter_by(email = session['email']).first()
        if user and bcrypt.check_password_hash(user.password, form.old_password.data):
            hashed_password = bcrypt.generate_password_hash(form.new_password.data)
            user.password = hashed_password
            db.session.commit()
            flash('Password are updated!', 'success')
            if user.role.name == 'admin':
                return redirect(url_for('admin'))
            elif user.role.name == 'storekeeper':
                return redirect(url_for('warehouse'))
            elif user.role.name == 'sale':
                return redirect(url_for('sales'))
            elif user.role.name == 'accountancy':
                return redirect(url_for('finance_management'))
        else:
            flash('Password is incorrect!', 'danger')

    return render_template('admin/change_password.html', form=form, title='Change Password Page')

@app.route('/logout')
def logout():
    session.pop('email', None)
    flash('You have been logged out.', 'success')
    return redirect(url_for('login'))

@app.route('/manager_roles')
@role_required(['admin'])
def roles():
    roles = Role.query.order_by(Role.id.desc()).all()
    return render_template('admin/roles.html', title='Roles Page', roles=roles)

@app.route('/addrole', methods=['GET', 'POST'])
@role_required(['admin'])
def add_role():
    form = RoleForm(request.form)
    form.submit.label.text = 'Add Role'
    if request.method == 'POST' and form.validate():
        # Check if role already exists
        role = Role.query.filter_by(name=form.name.data).first()
        if role:
            flash(f'Role {form.name.data} already exists!', 'danger')
            return redirect(url_for('roles'))

        # Create new role
        new_role = Role(
            name=form.name.data,
            description=form.description.data
        )
        db.session.add(new_role)
        db.session.commit()
        flash(f'Role {form.name.data} added successfully!', 'success')
        return redirect(url_for('roles'))
    else:
        return render_template('admin/add_role.html', form=form, title='Add Role Page')

@app.route('/updaterole/<int:id>', methods=['GET', 'POST'])
@role_required(['admin'])
def update_role(id):
    role = Role.query.get_or_404(id)
    form = RoleForm(request.form)
    form.submit.label.text = 'Update Role'

    # For GET requests, populate form with existing data
    if request.method == 'GET':
        form.name.data = role.name
        form.description.data = role.description

    if request.method == 'POST' and form.validate():
        # Check if role name already exists with another role
        existing_role = Role.query.filter_by(name=form.name.data).first()
        if existing_role and existing_role.id != id:
            flash(f'Role {form.name.data} already exists!', 'danger')
            return redirect(url_for('roles'))

        # Update role information
        role.name = form.name.data
        role.description = form.description.data

        db.session.commit()
        flash('Role updated successfully', 'success')
        return redirect(url_for('roles'))

    return render_template('admin/add_role.html', form=form, title='Update Role Page')

@app.route('/deleterole/<int:id>', methods=['GET', 'POST'])
@role_required(['admin'])
def delete_role(id):
    role = Role.query.get_or_404(id)
    # Check if the role is being used by any staff
    if Staff.query.filter_by(role_id=role.id).first():
        flash('Cannot delete this role as it is assigned to staff members.', 'danger')
        return redirect(url_for('roles'))

    db.session.delete(role)
    db.session.commit()
    flash('Role deleted successfully', 'success')
    return redirect(url_for('roles'))

@app.route('/manager_staffs')
@role_required(['admin'])
def staff():
    staffs = Staff.query.order_by(Staff.id.desc()).all()
    return render_template('admin/staff.html', staffs=staffs, title='Staff Page')
@app.route('/addstaff', methods=['GET', 'POST'])
@role_required(['admin'])
def add_staff():
    roles = Role.query.all()
    # Redundant session check removed as role_required decorator already handles this
    form = StaffRegistrationForm(request.form)
    form.submit.label.text = 'Add Staff'
    form.role_id.choices = [(role.id, role.name) for role in roles]
    if request.method == 'POST' and form.validate():
        # Check if staff with this email already exists
        staff = Staff.query.filter_by(email=form.email.data).first()
        if staff:
            flash('Staff already exists!', 'danger')
            return redirect(url_for('staff'))

        # Check if phone is already used
        phone_staff = Staff.query.filter_by(phone=form.phone.data).first()
        if phone_staff:
            flash(f'Phone number {form.phone.data} is already registered', 'danger')
            return render_template('admin/add_staff.html', form=form, title='Add Staff Member')

        # Create password hash
        hashed_password = bcrypt.generate_password_hash(form.password.data)

        # Create new staff member with proper fields
        staff = Staff(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hashed_password,
            position=form.position.data,
            role_id=form.role_id.data
        )

        db.session.add(staff)
        db.session.commit()
        flash(f'Staff member {form.username.data} added successfully!', 'success')
        return redirect(url_for('staff'))

    return render_template('admin/add_staff.html', form=form, title='Add Staff Member')


@app.route('/updatestaff/<int:id>', methods=['GET', 'POST'])
@role_required(['admin'])
def update_staff(id):
    staff = Staff.query.get_or_404(id)
    form = StaffRegistrationForm(request.form)
    form.submit.label.text = 'Update Staff'
    roles = Role.query.all()
    form.role_id.choices = [(role.id, role.name) for role in roles]
    # For GET requests, populate form with existing data
    if request.method == 'GET':
        form.username.data = staff.username
        form.email.data = staff.email
        form.phone.data = staff.phone
        form.position.data = staff.position
        form.role_id.data = staff.role_id

    if request.method == 'POST' and form.validate():
        # Check if email already exists with another staff
        existing_staff = Staff.query.filter_by(email=form.email.data).first()
        if existing_staff and existing_staff.id != id:
            flash(f'Email {form.email.data} already exists!', 'danger')
            return redirect(url_for('staff'))

        # Check if phone already exists with another staff
        phone_staff = Staff.query.filter_by(phone=form.phone.data).first()
        if phone_staff and phone_staff.id != id:
            flash(f'Phone {form.phone.data} already exists!', 'danger')
            return redirect(url_for('staff'))

        # Update staff information
        staff.username = form.username.data
        staff.email = form.email.data
        staff.phone = form.phone.data
        staff.position = form.position.data
        staff.role_id = form.role_id.data

        # Update password only if provided
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data)
            staff.password = hashed_password

        db.session.commit()
        flash('Staff member updated successfully', 'success')
        return redirect(url_for('staff'))

    return render_template('admin/add_staff.html', form=form, title='Update Staff Member')

@app.route('/deletestaff/<int:id>', methods=['POST'])
@role_required(['admin'])
def delete_staff(id):
    staff = Staff.query.get_or_404(id)
    user = User.query.get(staff.id)
    db.session.delete(staff)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Staff member deleted successfully', 'success')
    return redirect(url_for('staff'))

@app.route('/manager_customers', methods=['GET', 'POST'])
@role_required(['admin'])
def customers_manager():
    customers = User.query.filter_by(role_id=Role.query.filter_by(name='customer').first().id).all()
    return render_template('admin/customers.html', title='Customers Page', customers=customers)

@app.route('/add_customer', methods=['GET', 'POST'])
@role_required(['admin'])
def add_customer():
    form = CustomerRegisterForm()
    form.submit.label.text = 'Add Customer'
    if request.method == 'POST' and form.validate():
        # Check if user with this email already exists
        user_email = User.query.filter_by(email=form.email.data).first()
        if user_email:
            flash(f'Warning {form.email.data} has been registered already', 'danger')
            return redirect(url_for('customers_manager'))

        # Check if user with this phone already exists
        user_phone = User.query.filter_by(phone=form.phone.data).first()
        if user_phone:
            flash(f'Warning {form.phone.data} has been registered already', 'danger')
            return redirect(url_for('customers_manager'))

        # Hash password and create customer
        hash_password = bcrypt.generate_password_hash(form.password.data).decode('utf8')
        customer_role = Role.query.filter_by(name='customer').first()
        if not customer_role:
            customer_role = Role(name='customer')
            db.session.add(customer_role)
            db.session.commit()
        customer = Customer(
            username=form.username.data,
            email=form.email.data,
            phone=form.phone.data,
            password=hash_password,
            country=form.country.data,
            city=form.city.data,
            address=form.address.data,
            zipcode=form.zipcode.data,
            role_id=customer_role.id
        )

        if form.profile.data:
            image = photos.save(form.profile.data,
                                name=secrets.token_hex(10) + os.path.splitext(form.profile.data.filename)[1])
            customer.profile = image

        db.session.add(customer)
        db.session.commit()
        flash(f'Welcome {form.username.data}, Thanks for registering', 'success')
        return redirect(url_for('customers_manager'))

    return render_template('customers/register.html', form=form, title='Add Customer Page')

@app.route('/delete_customer/<int:id>', methods=['POST'])
@role_required(['admin'])
def delete_customer(id):
    customer = User.query.get_or_404(id)
    user = User.query.get(customer.id)
    db.session.delete(customer)
    if user:
        db.session.delete(user)
    db.session.commit()
    flash('Customer deleted successfully', 'success')
    return redirect(url_for('customers_manager'))

