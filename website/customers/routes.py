from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from website import app, db, photos, search, bcrypt
from .forms import CustomerRegisterForm
from .model import Customer, Order, OrderDetail
from website.models import Role, User
import os
import secrets
import pdfkit
from flask_login import login_required, current_user, logout_user, login_user
from website.decorators import role_required
import logging


@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        # Check if user with this email already exists
        user_email = User.query.filter_by(email=form.email.data).first()
        if user_email:
            flash(f'Warning {form.email.data} has been registered already', 'danger')
            return redirect(url_for('login'))
        # Check if user with this phone already exists
        user_phone = User.query.filter_by(phone=form.phone.data).first()
        if user_phone:
            flash(f'Warning {form.phone.data} has been registered already', 'danger')
            return redirect(url_for('login'))
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
        return redirect(url_for('login'))
    return render_template('customers/register.html', form=form)

@app.route('/customer/logout')
def customer_logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/getorder')
@role_required(['customer'])
@login_required
def get_order():
    if current_user.is_authenticated:
        customer_id = current_user.id
        invoice = secrets.token_hex(5)
        try:
            # Tạo đơn hàng mới
            order = Order(invoice=invoice, customer_id=customer_id)

            # Tính toán các giá trị tổng
            subtotal = 0
            for _key, product in session.get('ShopCart', {}).items():
                # Check if product_id/id exists or can be derived from the key
                if 'id' not in product and _key.isdigit():
                    product['id'] = int(_key)  # Use the dictionary key as id if possible

                # Validate product keys
                required_keys = ['name', 'price', 'quantity']  # Make 'id' optional
                if not all(key in product for key in required_keys):
                    logging.error(f"Missing essential keys in product: {product}")
                    flash('Invalid product data in cart', 'danger')
                    return redirect(url_for('getCart'))

                # Set default values for missing keys
                product_id = int(product.get('id', 0))  # Default to 0 if missing
                product_price = float(product['price'])
                product_quantity = int(product['quantity'])
                product_discount = float(product.get('discount', 0))  # Default to 0 if no discount

                # Tính giá trị sau khi giảm giá cho mỗi sản phẩm
                discount_amount = (product_discount / 100) * product_price * product_quantity
                product_subtotal = product_price * product_quantity - discount_amount
                subtotal += product_subtotal

                # Tạo chi tiết đơn hàng
                order_detail = OrderDetail(
                    product_id=product_id,
                    product_name=product['name'],
                    price=product_price,
                    quantity=product_quantity,
                    discount=product_discount,
                    subtotal=product_subtotal
                )
                order.order_details.append(order_detail)

            # Tính thuế và tổng cộng
            tax_rate = 0.06  # 6%
            tax = subtotal * tax_rate
            grand_total = subtotal + tax

            # Cập nhật thông tin tổng hợp vào đơn hàng
            order.subtotal = subtotal
            order.tax = tax
            order.grand_total = grand_total

            # Lưu đơn hàng và chi tiết đơn hàng vào database
            db.session.add(order)
            db.session.commit()

            # Xóa giỏ hàng sau khi đã đặt hàng thành công
            session.pop('ShopCart')
            flash(f'Your order {order.invoice} has been sent successfully', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            logging.error(f"Error occurred while processing order: {e}", exc_info=True)
            flash('Error occurred while processing your order', 'danger')
            return redirect(url_for('getCart'))
    else:
        flash('Please login to place an order', 'danger')
        return redirect(url_for('login'))


@app.route('/orders/<invoice>')
@role_required(['customer'])
@login_required
def orders(invoice):
    if current_user.is_authenticated:
        customer_id = current_user.id
        customer = Customer.query.filter_by(id=customer_id).first()
        order = Order.query.filter_by(invoice=invoice, customer_id=customer_id).first()

        if order:
            # Sử dụng giá trị đã tính sẵn từ model mới
            return render_template('customers/orders.html',
                                   customer=customer,
                                   order=order,
                                   order_details=order.order_details,
                                   grand_total=order.grand_total,
                                   tax=order.tax,
                                   invoice=invoice)
        else:
            flash('No orders found', 'danger')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))


@app.route('/getpdf/<invoice>', methods=['POST'])
@role_required(['customer'])
@login_required
def get_pdf(invoice):
    if current_user.is_authenticated:
        customer_id = current_user.id
        if request.method == 'POST':
            customer = Customer.query.filter_by(id=customer_id).first()
            order = Order.query.filter_by(invoice=invoice, customer_id=customer_id).first()

            if order:
                rendered = render_template('customers/pdf.html',
                                          customer=customer,
                                          order=order,
                                          order_details=order.order_details,
                                          grand_total=order.grand_total,
                                          tax=order.tax,
                                          invoice=invoice)
                try:
                    options = {
                        'enable-local-file-access': None
                    }
                    pdf = pdfkit.from_string(rendered, False, options=options)
                    response = make_response(pdf)
                    response.headers['Content-Type'] = 'application/pdf'
                    response.headers['Content-Disposition'] = f'attached; filename={invoice}.pdf'
                    return response
                except OSError as e:
                    print({'error': str(e)})
                    flash('Lỗi khi tạo PDF. Vui lòng thử lại.', 'danger')
                    return redirect(url_for('orders', invoice=invoice))
            else:
                flash('Order not found.', 'warning')
                return redirect(url_for('home'))
    return redirect(url_for('login'))
