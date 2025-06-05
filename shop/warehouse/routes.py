from .models import Warehouse, InboundReceipt, InboundReceiptDetail, OutboundReceipt, OutboundReceiptDetail
from .forms import InboundReceiptForm, OutboundReceiptForm, WarehouseForm
from shop import app, db
from shop.decorators import role_required
from flask import render_template, redirect, url_for, flash, request, session
from shop.products.models import AddProduct, Brand, Category
from flask_login import login_required, current_user
from shop.admin.models import Staff
from ..models import Role


@app.route('/warehouse')
@role_required(['admin', 'storekeeper'])
def warehouse():
    products = AddProduct.query.all()
    brands = Brand.query.all()
    categories = Category.query.all()
    for product in products:
        if product.stock <= 10:
            flash(f'Sản phẩm {product.name} sắp hết hàng', 'warning')
    return render_template('warehouse/warehouse.html', title='Warehouse Dashboard', products=products, brands=brands, categories=categories)


@app.route('/manager_warehouse')
@role_required(['admin', 'storekeeper'])
def manager_warehouse():
    warehouses = Warehouse.query.all()
    return render_template('warehouse/warehouse_detail.html', title='Warehouse Management', warehouses=warehouses)


@app.route('/warehouse_add', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def warehouse_add():
    form = WarehouseForm()
    # Chọn người quản lý kho từ danh sách storekeepers
    role = Role.query.filter_by(name='storekeeper').first()
    storekeepers = Staff.query.filter_by(role_id=role.id).all()
    form.manager_id.choices = [(sk.id, sk.username) for sk in storekeepers]

    if request.method == 'POST' and form.validate_on_submit():
        warehouse = Warehouse(
            name=form.name.data,
            location=form.location.data,
            capacity=form.capacity.data,
            description=form.description.data,
            status=form.status.data,
            manager_id=form.manager_id.data,
        )
        db.session.add(warehouse)
        db.session.commit()
        flash('Kho được thêm thành công', 'success')
        return redirect(url_for('warehouse'))
    return render_template('warehouse/warehouse_add.html', title='Add Warehouse', form=form)


@app.route('/warehouse_edit/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def warehouse_edit(id):
    role = Role.query.filter_by(name='storekeeper').first()
    storekeepers = Staff.query.filter_by(role_id=role.id).all()
    warehouse = Warehouse.query.get_or_404(id)

    form = WarehouseForm()
    if request.method == 'GET':
        form.name.data = warehouse.name
        form.location.data = warehouse.location
        form.capacity.data = warehouse.capacity
        form.description.data = warehouse.description
        form.status.data = warehouse.status
        form.manager_id.data = warehouse.manager_id

    form.manager_id.choices = [(sk.id, sk.username) for sk in storekeepers]
    if form.validate_on_submit():
        warehouse.name = form.name.data
        warehouse.location = form.location.data
        warehouse.capacity = form.capacity.data
        warehouse.description = form.description.data
        warehouse.manager_id = form.manager_id.data
        db.session.commit()
        flash(f'Cập nhật kho {warehouse.name} thành công', 'success')
        return redirect(url_for('warehouse'))

    return render_template('warehouse/warehouse_add.html', title='Edit Warehouse', form=form, warehouse=warehouse,
                           is_edit=True)


@app.route('/warehouse_delete/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def warehouse_delete(id):
    warehouse = Warehouse.query.get_or_404(id)
    db.session.delete(warehouse)
    db.session.commit()
    flash('Warehouse deleted successfully', 'success')
    return redirect(url_for('warehouse'))


@app.route('/inbound_receipt')
@role_required(['admin', 'storekeeper'])
def inbound_receipt():
    receipts = InboundReceipt.query.all()
    return render_template('warehouse/inbound_receipt.html', title='Inbound Receipts', receipts=receipts)

@app.route('/adjust_stock/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def adjust_stock(id):
    product = AddProduct.query.get_or_404(id)
    adjustment_type = request.form.get('adjustment_type')
    adjustment_quantity = int(request.form.get('adjustment_quantity', 0))
    adjustment_reason = request.form.get('adjustment_reason')

    current_stock = product.stock

    if adjustment_type == 'add':
        product.stock += adjustment_quantity
    elif adjustment_type == 'subtract':
        if product.stock < adjustment_quantity:
            flash(f'Không đủ số lượng để trừ. Hiện tại: {product.stock}', 'danger')
            return redirect(url_for('warehouse'))
        product.stock -= adjustment_quantity
    elif adjustment_type == 'set':
        product.stock = adjustment_quantity

    # Lưu lịch sử điều chỉnh nếu cần

    db.session.commit()
    flash(f'Đã điều chỉnh số lượng sản phẩm {product.name} từ {current_stock} thành {product.stock} vì {adjustment_reason}.' , 'success')
    return redirect(url_for('warehouse'))

@app.route('/inbound_receipt_add', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def inbound_receipt_add():
    form = InboundReceiptForm()
    warehouses = Warehouse.query.filter_by(status='active').all()
    form.warehouse_id.choices = [(w.id, w.name) for w in warehouses]

    products = AddProduct.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        receipt = InboundReceipt(
            receipt_number=form.receipt_number.data,
            receipt_date=form.receipt_date.data,
            supplier=form.supplier.data,
            notes=form.notes.data,
            warehouse_id=form.warehouse_id.data,
            created_by=current_user.id,
            status='pending',
            total_amount=request.form.get('total_amount', 0)
        )
        db.session.add(receipt)
        db.session.flush()  # Lấy ID của receipt mới tạo

        # Lấy dữ liêu chi tiết từ form
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        pricse = request.form.getlist('price[]')
        subtotals = request.form.getlist('subtotal[]')

        # Tạo các chi tiết phiêu nhập
        for i in range(len(product_ids)):
            if product_ids[i]:
                detail = InboundReceiptDetail(
                    inbound_receipt_id=receipt.id,
                    product_id=product_ids[i],
                    quantity=quantities[i],
                    price=pricse[i],
                    subtotal=subtotals[i]
                )
                db.session.add(detail)

        db.session.commit()
        flash('Phiếu nhập kho đã được tạo thành công', 'success')
        return redirect(url_for('inbound_receipt'))

    return render_template('warehouse/inbound_receipt_add.html', title='Add Inbound Receipt', form=form, products=products)

@app.route('/inbound_receipt_detail/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def inbound_receipt_detail(id):
    receipt = InboundReceipt.query.get_or_404(id)
    products = AddProduct.query.all()
    return render_template('warehouse/inbound_receipt_detail.html', title='Inbound Receipt Detail', receipt=receipt, products=products, receipt_details=receipt.receipt_details)

@app.route('/inbound_receipt_edit/<int:id>', methods=['GET','POST'])
@role_required(['admin', 'storekeeper'])
def inbound_receipt_edit(id):
    receipt = InboundReceipt.query.get_or_404(id)

    # Chỉ cho phép chỉnh sửa phiếu nhập kho đang xử lý
    if receipt.status != 'pending':
        flash('Phiếu nhập kho này không thể chỉnh sửa', 'danger')
        return redirect(url_for('inbound_receipt'))

    form = InboundReceiptForm(obj=receipt)
    wasehouses = Warehouse.query.filter_by(status='active').all()
    form.warehouse_id.choices = [(w.id, w.name) for w in wasehouses]
    products = AddProduct.query.all()

    if request.method == "GET":
        form.receipt_number.data = receipt.receipt_number
        form.receipt_date.data = receipt.receipt_date
        form.supplier.data = receipt.supplier
        form.notes.data = receipt.notes
        form.warehouse_id.data = receipt.warehouse_id

        return render_template('warehouse/inbound_receipt_edit.html', title='Edit Inbound Receipt', form=form, receipt=receipt, products=products, receipt_details=receipt.receipt_details)

    if request.method == 'POST' and form.validate_on_submit():
        receipt.receipt_number = form.receipt_number.data
        receipt.receipt_date = form.receipt_date.data
        receipt.supplier = form.supplier.data
        receipt.notes = form.notes.data
        receipt.warehouse_id = form.warehouse_id.data
        receipt.total_amount = request.form.get('total_amount', 0)

        # Xóa các chi tiết cũ
        for detail in receipt.receipt_details:
            db.session.delete(detail)

        # Lấy dữ liệu chi tiết từ form
        products_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')
        subtotals = request.form.getlist('subtotal[]')

        # Tạo các chi tiết mới
        for i in range(len(products_ids)):
            if products_ids[i]:
                detail = InboundReceiptDetail(
                    inbound_receipt_id=receipt.id,
                    product_id=products_ids[i],
                    quantity=quantities[i],
                    price=prices[i],
                    subtotal=subtotals[i]
                )
                db.session.add(detail)

        db.session.commit()
        flash('Phiếu nhập kho đã được cập nhật thành công', 'success')
        return redirect(url_for('inbound_receipt'))

    return render_template('warehouse/inbound_receipt_edit.html', title='Edit Inbound Receipt', form=form, receipt=receipt, receipt_details=receipt.receipt_details, products=products)

@app.route('/inbound_receipt_delete/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def inbound_receipt_delete(id):
    receipt = InboundReceipt.query.get_or_404(id)

    # Chỉ cho phép xóa phiếu nhập kho đang xử lý
    if receipt.status != 'pending':
        flash('Phiếu nhập kho này không thể xóa', 'danger')
        return redirect(url_for('inbound_receipt'))

    db.session.delete(receipt)
    db.session.commit()
    flash('Phiếu nhập kho đã được xóa thành công', 'success')
    return redirect(url_for('inbound_receipt'))

@app.route('/inbound_receipt_complete/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def inbound_receipt_complete(id):
    receipt = InboundReceipt.query.get_or_404(id)
    if receipt.status != 'pending':
        flash('Phiếu nhập kho này không thể xác nhận hoàn thành', 'danger')
        return redirect(url_for('inbound_receipt'))

    # Cập nhật số lượng sản phẩm trong kho
    for detail in receipt.receipt_details:
        product = AddProduct.query.get(detail.product_id)
        if product:
            product.stock += detail.quantity
        else:
            flash("Sản phẩm không tồn tại", 'danger')

    # Cập nhật trạng thái phiếu nhập kho
    receipt.status = 'completed'
    db.session.commit()
    flash('Phiếu nhập kho đã được xác nhận hoàn thành và cập nhật số lượng sản phẩm', 'success')

    return redirect(url_for('inbound_receipt'))

@app.route('/inbound_receipt_cancel/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def inbound_receipt_cancel(id):
    receipt = InboundReceipt.query.get_or_404(id)

    # Chỉ cho phép hủy phiếu nhập kho đang xử lý
    if receipt.status != 'pending':
        flash('Phiếu nhập kho này không thể hủy', 'danger')
        return redirect(url_for('inbound_receipt'))

    receipt.status = 'cancelled'
    db.session.commit()
    flash('Phiếu nhập kho đã được hủy thành công', 'success')
    return redirect(url_for('inbound_receipt'))

@app.route('/outbound_receipt')
@role_required(['admin', 'storekeeper'])
def outbound_receipt():
    receipts = OutboundReceipt.query.all()
    return render_template('warehouse/outbound_receipt.html', title='Outbound Receipts', receipts=receipts)

@app.route('/outbound_receipt_add', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def outbound_receipt_add():
    form = OutboundReceiptForm()
    warehouses = Warehouse.query.filter_by(status='active').all()
    form.warehouse_id.choices = [(w.id, w.name) for w in warehouses]

    products = AddProduct.query.all()
    if request.method == 'POST' and form.validate_on_submit():
        receipt = OutboundReceipt(
            receipt_number=form.receipt_number.data,
            receipt_date=form.receipt_date.data,
            recipient=form.recipient.data,
            notes=form.notes.data,
            warehouse_id=form.warehouse_id.data,
            created_by=current_user.id,
            status='pending',
            total_amount=request.form.get('total_amount', 0)
        )
        db.session.add(receipt)
        db.session.flush()  # Lấy ID của receipt mới tạo

        # Lấy dữ liệu chi tiết từ form
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')
        subtotals = request.form.getlist('subtotal[]')
        # Tạo các chi tiết phiếu xuất
        for i in range(len(product_ids)):
            if product_ids[i]:
                detail = OutboundReceiptDetail(
                    outbound_receipt_id=receipt.id,
                    product_id=product_ids[i],
                    quantity=quantities[i],
                    price=prices[i],
                    subtotal=subtotals[i]
                )
                db.session.add(detail)
        db.session.commit()
        flash('Phiếu xuất kho đã được tạo thành công', 'success')
        return redirect(url_for('outbound_receipt'))
    return render_template('warehouse/outbound_receipt_add.html', title='Add Outbound Receipt', form=form, products=products)

@app.route('/outbound_receipt_detail/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def outbound_receipt_detail(id):
    receipt = OutboundReceipt.query.get_or_404(id)
    products = AddProduct.query.all()
    return render_template('warehouse/outbound_receipt_detail.html', title='Outbound Receipt Detail', receipt=receipt, products=products, receipt_details=receipt.receipt_details)

@app.route('/outbound_receipt_edit/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'storekeeper'])
def outbound_receipt_edit(id):
    receipt = OutboundReceipt.query.get_or_404(id)

    # Chỉ cho phép chỉnh sửa phiếu xuất kho đang xử lý
    if receipt.status != 'pending':
        flash('Phiếu xuất kho này không thể chỉnh sửa', 'danger')
        return redirect(url_for('outbound_receipt'))

    form = OutboundReceiptForm(obj=receipt)
    warehouses = Warehouse.query.filter_by(status='active').all()
    form.warehouse_id.choices = [(w.id, w.name) for w in warehouses]
    products = AddProduct.query.all()

    if request.method == "GET":
        form.receipt_number.data = receipt.receipt_number
        form.receipt_date.data = receipt.receipt_date
        form.recipient.data = receipt.recipient
        form.notes.data = receipt.notes
        form.warehouse_id.data = receipt.warehouse_id

        return render_template('warehouse/outbound_receipt_edit.html', title='Edit Outbound Receipt', form=form, receipt=receipt, products=products, receipt_details=receipt.receipt_details)

    if request.method == 'POST' and form.validate_on_submit():
        receipt.receipt_number = form.receipt_number.data
        receipt.receipt_date = form.receipt_date.data
        receipt.recipient = form.recipient.data
        receipt.notes = form.notes.data
        receipt.warehouse_id = form.warehouse_id.data
        receipt.total_amount = request.form.get('total_amount', 0)

        # Xóa các chi tiết cũ
        for detail in receipt.receipt_details:
            db.session.delete(detail)

        # Lấy dữ liệu chi tiết từ form
        product_ids = request.form.getlist('product_id[]')
        quantities = request.form.getlist('quantity[]')
        prices = request.form.getlist('price[]')
        subtotals = request.form.getlist('subtotal[]')

        # Tạo các chi tiết mới
        for i in range(len(product_ids)):
            if product_ids[i]:
                detail = OutboundReceiptDetail(
                    outbound_receipt_id=receipt.id,
                    product_id=product_ids[i],
                    quantity=quantities[i],
                    price=prices[i],
                    subtotal=subtotals[i]
                )
                db.session.add(detail)

        db.session.commit()
        flash('Phiếu xuất kho đã được cập nhật thành công', 'success')
        return redirect(url_for('outbound_receipt'))
    return render_template('warehouse/outbound_receipt_edit.html', title='Edit Outbound Receipt', form=form, receipt=receipt, receipt_details=receipt.receipt_details, products=products)

@app.route('/outbound_receipt_delete/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def outbound_receipt_delete(id):
    receipt = OutboundReceipt.query.get_or_404(id)

    # Chỉ cho phép xóa phiếu xuất kho đang xử lý
    if receipt.status != 'pending':
        flash('Phiếu xuất kho này không thể xóa', 'danger')
        return redirect(url_for('outbound_receipt'))

    db.session.delete(receipt)
    db.session.commit()
    flash('Phiếu xuất kho đã được xóa thành công', 'success')
    return redirect(url_for('outbound_receipt'))

@app.route('/outbound_receipt_complete/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def outbound_receipt_complete(id):
    receipt = OutboundReceipt.query.get_or_404(id)
    if receipt.status != 'pending':
        flash('Phiếu xuất kho này không thể xác nhận hoàn thành', 'danger')
        return redirect(url_for('outbound_receipt'))

    # Cập nhật số lượng sản phẩm trong kho
    for detail in receipt.receipt_details:
        product = AddProduct.query.get(detail.product_id)
        if product:
            if product.stock < detail.quantity:
                flash(f'Sản phẩm {product.name} không đủ số lượng để xuất kho', 'danger')
                return redirect(url_for('outbound_receipt'))
            product.stock -= detail.quantity
        else:
            flash("Sản phẩm không tồn tại", 'danger')
    # Cập nhật trạng thái phiếu xuất kho
    receipt.status = 'completed'
    db.session.commit()
    flash('Phiếu xuất kho đã được xác nhận hoàn thành và cập nhật số lượng sản phẩm', 'success')
    return redirect(url_for('outbound_receipt'))

@app.route('/outbound_receipt_cancel/<int:id>', methods=['POST'])
@role_required(['admin', 'storekeeper'])
def outbound_receipt_cancel(id):
    receipt = OutboundReceipt.query.get_or_404(id)

    # Chỉ cho phép hủy phiếu xuất kho đang xử lý
    if receipt.status != 'pending':
        flash('Phiếu xuất kho này không thể hủy', 'danger')
        return redirect(url_for('outbound_receipt'))

    receipt.status = 'cancelled'
    db.session.commit()
    flash('Phiếu xuất kho đã được hủy thành công', 'success')
    return redirect(url_for('outbound_receipt'))
