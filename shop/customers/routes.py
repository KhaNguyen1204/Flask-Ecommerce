from flask import redirect, render_template, url_for, flash, request, session, current_app, make_response
from shop import app, db, photos, search, bcrypt
from .forms import CustomerRegisterForm, ReviewForm
from .model import Customer, Order, OrderDetail, Review
from shop.products.routes import brands, categories
from shop.models import Role, User
import os
import secrets
import pdfkit
from flask_login import login_required, current_user, logout_user, login_user
from shop.decorators import role_required
import logging

@app.route('/aboutus')
def about_us():
    return render_template('about_us.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/fqa')
def fqa():
    return render_template('fqa.html')

@app.route('/customer/register', methods=['GET', 'POST'])
def customer_register():
    form = CustomerRegisterForm()
    if form.validate_on_submit():
        # Check if user with this email already exists
        user_email = User.query.filter_by(email=form.email.data).first()
        if user_email:
            flash(f'Cảnh báo! {form.email.data} đã tồn tại!', 'danger')
            return redirect(url_for('login'))
        # Check if user with this phone already exists
        user_phone = User.query.filter_by(phone=form.phone.data).first()
        if user_phone:
            flash(f'Cảnh báo! {form.phone.data} đã tồn tại!', 'danger')
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
            role_id=customer_role.id
        )

        if form.profile.data:
            image = photos.save(form.profile.data,
                                name=secrets.token_hex(10) + os.path.splitext(form.profile.data.filename)[1])
            customer.profile = image

        db.session.add(customer)
        db.session.commit()
        flash(f'Chào mừng {form.username.data}, cảm ơn bạn đã đăng ký tài khoản!', 'success')
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
            flash(f'Đơn hàng {order.invoice} của bạn đã được gửi yêu cầu thành công!', 'success')
            return redirect(url_for('orders', invoice=invoice))
        except Exception as e:
            logging.error(f"Gặp lỗi trong quá trình gửi đơn hàng: {e}", exc_info=True)
            flash('Gặp lỗi trong quá trình gửi đơn hàng', 'danger')
            return redirect(url_for('getCart'))
    else:
        flash('Vui lòng đăng nhập để gửi đơn hàng', 'danger')
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
                                   invoice=invoice,
                                   brands=brands(),
                                   categories=categories())
        else:
            flash('Không tìm thấy đơn hàng', 'danger')
            return redirect(url_for('home'))
    else:
        return redirect(url_for('login'))

@app.route('/get_pdf/<invoice>', methods=['GET', 'POST'])
@role_required(['customer', 'sale', 'admin'])
@login_required
def get_pdf(invoice):
    # Allow: customer can only get their own order, staff/admin can get any order
    if current_user.role.name == 'customer':
        order = Order.query.filter_by(invoice=invoice, customer_id=current_user.id).first()
        customer = Customer.query.filter_by(id=current_user.id).first()
    else:
        order = Order.query.filter_by(invoice=invoice).first()
        customer = order.customer if order else None

    if not order:
        flash('Đơn hàng không tồn tại.', 'warning')
        return redirect(url_for('home'))

    if order.status == 'completed':
        rendered = render_template('customers/pdf.html',
                                  customer=customer,
                                  order=order,
                                  order_details=order.order_details,
                                  grand_total=order.grand_total,
                                  tax=order.tax,
                                  invoice=invoice)
        try:
            options = {'enable-local-file-access': None}
            pdf = pdfkit.from_string(rendered, False, options=options)
            response = make_response(pdf)
            response.headers['Content-Type'] = 'application/pdf'
            response.headers['Content-Disposition'] = f'attached; filename={invoice}.pdf'
            return response
        except OSError as e:
            flash('Lỗi khi tạo PDF. Vui lòng thử lại.', 'danger')
            return redirect(url_for('orders', invoice=invoice))
    else:
        flash('Bạn không thể xuất hóa đơn vì đơn hàng chưa hoàn thành.', 'warning')
        if current_user.role.name == 'admin' or current_user.role.name == 'sale':
            return redirect(request.referrer)
        return redirect(url_for('orders', invoice=invoice))

@app.route('/customer/profile')
@role_required(['customer'])
def customer_profile():
    if current_user.is_authenticated:
        customer = Customer.query.filter_by(id=current_user.id).first()
        if customer:
            return render_template('customers/profile.html', customer=customer)
        else:
            flash('Khách hàng không tồn tại!', 'danger')
            return redirect(url_for('home'))
    else:
        flash('Vui lòng đăng nhập để xem hồ sơ cá nhân!', 'danger')
        return redirect(url_for('login'))

@app.route('/customer/update', methods=['GET', 'POST'])
@role_required(['customer'])
def update_profile():
    customer_id = current_user.id
    customer = User.query.get_or_404(customer_id)
    # Khởi tạo form đúng cách để tránh validate sớm
    form = CustomerRegisterForm()
    form.submit.label.text = 'Cập nhật thông tin tài khoản'
    # Nếu là POST, xóa validator bắt buộc trước khi validate
    if request.method == 'POST':
        form.password.validators = []
        form.confirm.validators = []
    # Populate form with existing data for GET
    if request.method == 'GET':
        form.username.data = customer.username
        form.email.data = customer.email
        form.phone.data = customer.phone
        form.country.data = getattr(customer, 'country', '')
        form.city.data = getattr(customer, 'city', '')
        form.address.data = getattr(customer, 'address', '')
    if request.method == 'POST' and form.validate():
        # Kiểm tra email đã tồn tại chưa (trừ chính mình)
        user_email = User.query.filter_by(email=form.email.data).first()
        if user_email and user_email.id != customer.id:
            flash(f'Cảnh báo! Email {form.email.data} đã tồn tại!', 'danger')
            return redirect(url_for('update_profile'))
        # Kiểm tra phone đã tồn tại chưa (trừ chính mình)
        user_phone = User.query.filter_by(phone=form.phone.data).first()
        if user_phone and user_phone.id != customer.id:
            flash(f'Cảnh báo! Số điện thoại {form.phone.data} đã tồn tại', 'danger')
            return redirect(url_for('update_profile'))
        # Cập nhật thông tin
        customer.username = form.username.data
        customer.email = form.email.data
        customer.phone = form.phone.data
        if hasattr(customer, 'country'):
            customer.country = form.country.data
        if hasattr(customer, 'city'):
            customer.city = form.city.data
        if hasattr(customer, 'address'):
            customer.address = form.address.data
        # Cập nhật ảnh đại diện nếu có
        if form.profile.data:
            image = photos.save(form.profile.data,
                                name=secrets.token_hex(10) + os.path.splitext(form.profile.data.filename)[1])
            customer.profile = image
        db.session.commit()
        flash(f'Tài khoản {form.username.data} đã được cập nhật!', 'success')
        return redirect(url_for('customer_profile'))
    return render_template('customers/update_profile.html', form=form, customer=customer, title='Cập nhật thông tin tài khoản')

@app.route('/customer/histort_orders')
@role_required(['customer'])
def history_orders():
    if current_user.is_authenticated:
        customer_id = current_user.id
        customer = Customer.query.filter_by(id=customer_id).first()
        orders = Order.query.filter_by(customer_id=customer_id).all()

        if orders:
            return render_template('customers/history_orders.html', customer=customer, orders=orders)
        else:
            flash('Không có đơn hàng nào!', 'warning')
            return redirect(url_for('home'))
    else:
        flash('Vui lòng đăng nhập để xem danh sách đơn hàng', 'danger')
        return redirect(url_for('login'))

@app.route('/product/<int:product_id>/review', methods=['POST'])
@login_required
@role_required(['customer'])
def add_review(product_id):
    if current_user.is_authenticated:
        form = ReviewForm()
        if form.validate_on_submit():
            review_exist = Review.query.filter_by(customer_id=current_user.id, product_id=product_id).first()
            if review_exist:
                flash('Bạn đã đánh giá trước đó, hãy xóa đánh giá để tạo lại', 'danger')
                return redirect(url_for('single_page', id=product_id))

            review = Review(
                customer_id=current_user.id,
                product_id=product_id,
                rating=form.rating.data,
                comment=form.comment.data,
            )

            db.session.add(review)
            db.session.commit()
            flash('Cảm ơn bạn đã dánh giá sản phẩm', 'success')
            return redirect(url_for('single_page', id=product_id))
        else:
            flash('Nội dung bạn nhập chưa hợp lệ', 'danger')
            return redirect(url_for('single_page', id=product_id))
    else:
        flash('Hãy đăng nhập để đánh giá sản phẩm', 'danger')
        return redirect(url_for('single_page', id=product_id))

@app.route('/review/<int:review_id>/delete', methods=['GET', 'POST'])
@login_required
@role_required(['customer'])
def delete_review(review_id):
    review = Review.query.get_or_404(review_id)
    if review.customer_id != current_user.id:
        flash('Bạn không thể xóa đánh giá không phải của bạn', 'danger')
        return redirect(url_for('single_page', id=review.product_id))
    db.session.delete(review)
    db.session.commit()
    flash('Bạn đã xóa đánh giá thành công', 'success')
    return redirect(url_for('single_page', id=review.product_id))
