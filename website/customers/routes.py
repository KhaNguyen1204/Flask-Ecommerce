from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from website import app, db, photos, search, bcrypt
from .forms import CustomerRegisterForm, CustomerLoginForm
from .model import Register, CustomerOrder
import os
import secrets
import pdfkit
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

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/getorder')
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            order = CustomerOrder(invoice=invoice, customer_id=customer_id, orders=session['ShopCart'])
            db.session.add(order)
            db.session.commit()
            session.pop('ShopCart')
            flash(f'Your order {order.invoice} has been sent success', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            print(e)
            flash('Error occurred while processing your order', 'danger')
            return redirect(url_for('getCart'))

@app.route('/orders/<invoice>')
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        grand_total = 0
        sub_total = 0
        customer_id = current_user.id
        customer = Register.query.filter_by(id=customer_id).first()
        orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
        for _key, product in orders.orders.items():
            discount = (product['discount'] / 100) * float(product['price'])
            sub_total += float(product['price']) * int(product['quantity'])
            sub_total -= discount
            tax = ("%.2f" % (.6 *float(sub_total)))
            grand_total += float("%.2f" % (1.06 * sub_total))
    else:
        return redirect(url_for('customer_login'))
    return render_template('customers/orders.html', customer=customer, orders=orders, grand_total=grand_total,sub_total=sub_total, tax=tax, invoice=invoice)

import pdfkit

@app.route('/getpdf/<invoice>', methods=['POST'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        grand_total = 0
        sub_total = 0
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Register.query.filter_by(id=customer_id).first()
            orders = CustomerOrder.query.filter_by(customer_id=customer_id).order_by(CustomerOrder.id.desc()).first()
            for _key, product in orders.orders.items():
                discount = (product['discount'] / 100) * float(product['price'])
                sub_total += float(product['price']) * int(product['quantity'])
                sub_total -= discount
                tax = ("%.2f" % (.6 * float(sub_total)))
                grand_total += float("%.2f" % (1.06 * sub_total))
            rendered = render_template('customers/pdf.html', customer=customer, orders=orders, grand_total=grand_total, tax=tax, invoice=invoice)
            try:
                options = {
                    'enable-local-file-access': None
                }
                pdf = pdfkit.from_string(rendered, False, options=options)
                response = make_response(pdf)
                response.headers['Content-Type'] = 'application/pdf'
                response.headers['Content-Disposition'] = f'atteched; filename={invoice}.pdf'
                return response
            except OSError as e:
                print({'error': str(e)})
                flash('Lỗi khi tạo PDF. Vui lòng thử lại.', 'danger')
                return redirect(url_for('orders', invoice=invoice))
    return redirect(url_for('customer_login'))
