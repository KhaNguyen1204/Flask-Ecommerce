from flask import redirect, render_template, url_for, request, flash, session, current_app
from website import app, db, photos
from .models import Brand, Category, AddProduct
from .forms import AddProducts
import secrets, os # Băm ảnh để không trùng lặp

@app.route('/addbrand', methods=['GET', 'POST'])
def addbrand():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        getbrand = request.form.get('brand')
        brand = Brand(name=getbrand)
        db.session.add(brand)
        db.session.commit()
        flash(f'Brand {getbrand} added successfully!', 'success')
        return redirect(url_for('addbrand'))

    return render_template('products/addbrand.html', brands='brands')

@app.route('/updatebrand/<int:id>', methods=['GET', 'POST'])
def updatebrand(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
    updatebrand = Brand.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatebrand.name = request.form.get('name')
        db.session.add(updatebrand)
        flash(f'Brand {updatebrand} updated successfully!', 'success')
        db.session.commit()
        return redirect(url_for('brands'))
    return render_template('products/updatebrand.html', title='Update Brand Page', updatebrand=updatebrand)

@app.route('/deletebrand/<int:id>', methods=['GET', 'POST'])
def deletebrand(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    brand = Brand.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(brand)
        db.session.commit()
    flash(f'Brand {brand.name} deleted successfully!', 'success')
    return redirect(url_for('brands'))

@app.route('/addcat', methods=['GET', 'POST'])
def addcategory():
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    if request.method == 'POST':
        get_category = request.form.get('category')
        category = Category(name=get_category)
        db.session.add(category)
        db.session.commit()
        flash(f'Category {get_category} added successfully!', 'success')
        return redirect(url_for('addcategory'))

    return render_template('products/addbrand.html', title='Add Category')

@app.route('/updatecat/<int:id>', methods=['GET', 'POST'])
def updatecat(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
    updatecat = Category.query.get_or_404(id)
    brand = request.form.get('brand')
    if request.method == 'POST':
        updatecat.name = request.form.get('name')
        db.session.add(updatebrand)
        flash(f'Category {updatecat} updated successfully!', 'success')
        db.session.commit()
        return redirect(url_for('categories'))
    return render_template('products/updatebrand.html', title='Update Category Page', updatecat=updatecat)

@app.route('/deletecat/<int:id>', methods=['GET', 'POST'])
def deletecat(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
        return redirect(url_for('login'))
    category = Category.query.get_or_404(id)
    if request.method == 'POST':
        db.session.delete(category)
        db.session.commit()
    flash(f'Category {category.name} deleted successfully!', 'success')
    return redirect(url_for('categories'))
@app.route('/addproduct', methods=['GET', 'POST'])
def addproduct():
    if 'email' not in session:
        flash('Please login first', 'danger')
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
        brand = request.form.get('brand') # Syntax bởi vì trong models AddProduct không có brand and category mà là liên kêt
        category = request.form.get('category')
        description = form.description.data
        image_1 = photos.save(request.files.get('image_1'), name=secrets.token_hex(10) + '.')
        image_2 = photos.save(request.files.get('image_2'), name=secrets.token_hex(10) + '.')
        image_3 = photos.save(request.files.get('image_3'), name=secrets.token_hex(10) + '.')
        addpro = AddProduct(name=name, price=price, discount=discount, stock=stock, colors=colors, brand_id=brand, category_id=category, description=description, image_1=image_1, image_2=image_2, image_3=image_3)
        db.session.add(addpro)
        db.session.commit()
        flash(f'Product {name} added successfully!', 'success')
        return redirect(url_for('admin'))

    return render_template('products/addproduct.html', title='Add Product', form=form, brands=brands, categories=categories)

@app.route('/updateproduct/<int:id>', methods=['GET', 'POST'])
def updateproduct(id):
    if 'email' not in session:
        flash('Please login first', 'danger')
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
        flash(f'Product {product} updated successfully!', 'success')
        db.session.commit()
        return redirect(url_for('admin'))

    form.name.data = product.name
    form.price.data = product.price
    form.description.data = product.description
    form.discount.data = product.discount
    form.stock.data = product.stock
    form.colors.data = product.colors

    return render_template('products/updateproduct.html', title='Update Product', form=form, brands=brands, categories=categories, product=product)