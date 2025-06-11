from flask import redirect, render_template, url_for, request, flash, session, current_app
from shop import app, db, photos, search
from .models import Brand, Category, AddProduct
from .forms import AddProducts
import secrets, os  # Băm ảnh để không trùng lặp
from shop.models import User, Role
from shop.customers.forms import ReviewForm
from shop.customers.model import Review
from ..decorators import role_required


def brands():
    brands = Brand.query.join(AddProduct, (Brand.id == AddProduct.brand_id)).all()
    return brands


def categories():
    categories = Category.query.join(AddProduct, (AddProduct.category_id == Category.id)).all()
    return categories

@app.route('/')
def home():
    # Hiển thi nút đăng kí admin nếu chưa có admin đầu tiên
    admin_role = Role.query.filter_by(name='admin').first()
    admin_exists = False
    if admin_role:
        admin_exists = User.query.filter_by(role_id=admin_role.id).first() is not None
    show_admin_register = not admin_exists

    page = request.args.get('page', 1, type=int)
    products = AddProduct.query.filter(AddProduct.stock > 0).paginate(page=page, per_page=4)
    return render_template('products/index.html', products=products, brands=brands(), categories=categories(),
                           show_admin_register=show_admin_register)

@app.route('/result')
def result():
    # Hiển thi nút đăng kí admin nếu chưa có admin đầu tiên
    admin_role = Role.query.filter_by(name='admin').first()
    admin_exists = False
    if admin_role:
        admin_exists = User.query.filter_by(role_id=admin_role.id).first() is not None
    show_admin_register = not admin_exists

    searchword = request.args.get('q')
    products = AddProduct.query.msearch(searchword, fields=['name', 'description'], limit=6)
    return render_template('products/result.html', products=products, brands=brands(), categories=categories(),
                           show_admin_register=show_admin_register)


@app.route('/product/<int:id>')
def single_page(id):
    # Hiển thi nút đăng kí admin nếu chưa có admin đầu tiên
    admin_role = Role.query.filter_by(name='admin').first()
    admin_exists = False
    if admin_role:
        admin_exists = User.query.filter_by(role_id=admin_role.id).first() is not None
    show_admin_register = not admin_exists

    product = AddProduct.query.get_or_404(id)
    reviews = Review.query.filter_by(product_id=product.id).order_by(Review.created_at.desc()).all()
    review_form = ReviewForm()
    return render_template('products/single_page.html', product=product, brands=brands(), categories=categories(),
                           show_admin_register=show_admin_register, reviews=reviews, review_form=review_form)


@app.route('/brand/<int:id>')
def get_brand(id):
    # Hiển thi nút đăng kí admin nếu chưa có admin đầu tiên
    admin_role = Role.query.filter_by(name='admin').first()
    admin_exists = False
    if admin_role:
        admin_exists = User.query.filter_by(role_id=admin_role.id).first() is not None
    show_admin_register = not admin_exists

    page = request.args.get('page', 1, type=int)
    get_b = Brand.query.filter_by(id=id).first_or_404()
    brand = AddProduct.query.filter_by(brand_id=get_b.id).paginate(page=page, per_page=4)
    return render_template('products/index.html', brand=brand, brands=brands(), categories=categories(), get_b=get_b,
                           show_admin_register=show_admin_register)


@app.route('/categories/<int:id>')
def get_categories(id):
    # Hiển thi nút đăng kí admin nếu chưa có admin đầu tiên
    admin_role = Role.query.filter_by(name='admin').first()
    admin_exists = False
    if admin_role:
        admin_exists = User.query.filter_by(role_id=admin_role.id).first() is not None
    show_admin_register = not admin_exists

    page = request.args.get('page', 1, type=int)
    get_cat = Category.query.filter_by(id=id).first_or_404()
    get_cat_prod = AddProduct.query.filter_by(category=get_cat).paginate(page=page, per_page=4)
    return render_template('products/index.html', get_cat_prod=get_cat_prod, brands=brands(), categories=categories(),
                           get_cat=get_cat, show_admin_register=show_admin_register)


@app.route('/addbrand', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def addbrand():
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'Thương hiệu {getbrand} được thêm thành công!', 'success')
        return redirect(url_for('brands'))

    return render_template('products/addbrand.html', brands='brands')


@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def updatebrand(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = request.form.get('name')
        db.session.add(updatebrand)
        flash(f'Thương hiệu {updatebrand} được cập nhật thành công!', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Cập nhật thương hiệu', updatebrand=updatebrand)


@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def deletebrand(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
    flash(f'Thương hiệu  {brand.name} đã xóa thành công!', 'success')
    return redirect(url_for('brands'))

@app.route('/addcat', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def addcategory():
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        get_category = request.form.get('category')
        category = Category(name=get_category)
        db.session.add(category)
        db.session.commit()
        flash(f'Danh mục {get_category} được thêm thành công!', 'success')
        return redirect(url_for('categories'))

    return render_template('products/addbrand.html', title='Add Category')


@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def updatecat(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    updatecat = Category.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatecat.name = request.form.get('name')
        db.session.add(updatebrand)
        flash(f'Danh mục {updatecat} được cập nhật thành công!', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title='Cập nhật danh mục', updatecat=updatecat)

@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def deletecat(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
    flash(f'Danh mục {category.name} được xóa thành công!', 'success')
    return redirect(url_for('categories'))

@app.route('/addproduct', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def addproduct():
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    form = AddProducts(request.form)
    if request.method == 'POST':
        name = form.name.data
        price = form.price.data
        discount = form.discount.data
        stock = form.stock.data
        colors = form.colors.data
        brand = request.form.get(
            'brand')  # Syntax bởi vì trong models AddProduct không có brand and category mà là liên kêt
        category = request.form.get('category')
        description = form.description.data
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        addpro = AddProduct(name=name, price=price, discount=discount, stock=stock, colors=colors, brand_id=brand,
                            category_id=category, description=description, image_1=image_1, image_2=image_2,
                            image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'Sản phẩm {name} được thêm thành công!', 'success')
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', title='Thêm sản phẩm', form=form, brands=brands,
                           categories=categories)


@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
@role_required(['admin', 'sale'])
def updateproduct(id):
    if 'email' not in session:
        flash('Vui lòng đăng nhập để truy cập trang!', 'danger')
        return redirect(url_for('login'))
    brands = Brand.query.all()
    categories = Category.query.all()
    product = AddProduct.query.get_or_404(id)
    brand = request.form.get('brand')
    category = request.form.get('category')
    form = AddProducts(request.form)
    if request.method == 'POST':
        product.name = form.name.data
        product.price = form.price.data
        product.discount = form.discount.data
        product.stock = form.stock.data
        product.brand_id = brand
        product.category_id = category
        product.color = form.colors.data
        product.description = form.description.data
        if request.files.get('image_1'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_2'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')

        if request.files.get('image_3'):
            try:
                os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
                product.image_1 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
            except:
                product.image_1 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')

        db.session.add(product)
        flash(f'Sản phẩm {product.name} được cập nhật thành công!', 'success')
        db.session.commit()
        return redirect(request.referrer)

    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.description
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors

    return render_template('products/updateproduct.html', title='Cập nhật thành công', form=form, brands=brands,
                           categories=categories, product=product)

@app.route('/deleteproduct/<int:id>', methods=['POST'])
@role_required(['admin', 'sale'])
def deleteproduct(id):
    product = AddProduct.query.get_or_404(id)
    if request.method == 'POST':
        try:
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_1))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_2))
            os.unlink(os.path.join(current_app.root_path, 'static/images/' + product.image_3))
        except Exception as e:
            print(e)
        db.session.delete(product)
        db.session.commit()
        flash(f'Sản phẩm {product.name} đã được xóa thành công!', 'success')
        return redirect(url_for('admin'))
    flash(f'Không thể xóa sản phẩm {product.name}!', 'danger')
    return redirect(url_for('admin'))

