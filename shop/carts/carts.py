from flask import redirect, render_template, url_for, flash, request, session, current_app
from shop import db, app
from shop.products.models import AddProduct
from shop.products.routes import brands, categories
import json

def MergeDict(dict1, dict2):
    if isinstance(dict1, list) and isinstance(dict2, list):
        return dict1 + dict2
    elif isinstance(dict1, dict) and isinstance(dict2, dict):
        return dict(list(dict1.items()) + list(dict2.items()))
    return False


@app.route('/addcart', methods=['POST'])
def AddCart():
    try:
        product_id = request.form.get('product_id')
        quantity = request.form.get('quantity')
        colors = request.form.get('colors')
        product = AddProduct.query.filter_by(id=product_id).first()

        if product_id and quantity and colors and request.method == 'POST':
            # Convert quantity to integer
            quantity = int(quantity)

            DictItem = {
                product_id: {
                    'id': product.id,
                    'name': product.name,
                    'price': product.price,
                    'quantity': quantity,
                    'colors': colors,
                    'discount': product.discount,
                    'image': product.image_1,
                    'color': product.colors
                }
            }

            if 'ShopCart' in session:
                if str(product_id) in session['ShopCart']:
                    session.modified = True
                    session['ShopCart'][str(product_id)]['quantity'] += quantity
                else:
                    # Add a new product to the cart
                    session['ShopCart'] = MergeDict(session['ShopCart'], DictItem)
            else:
                # Create a new cart if it doesn't exist
                session['ShopCart'] = DictItem

            flash("Product added to cart successfully", 'success')
            return redirect(request.referrer)
    except Exception as e:
        print(e)
        flash("Error adding product to cart", 'danger')
    finally:
        return redirect(request.referrer)

@app.route('/carts')
def getCart():
    if 'ShopCart' not in session or len(session['ShopCart']) <= 0:
        return redirect(url_for('home'))
    subtotal = 0
    grandtotal = 0
    for key, product in session['ShopCart'].items():
        discount = (product['discount']/100) * float(product['price'])
        subtotal += float(product['price']) * int(product['quantity'])
        subtotal -= discount
        tax =  ("%.2f" % (.06 * float(subtotal)))
        grandtotal = float("%.2f" % (1.06 * subtotal))
    return render_template('products/carts.html', tax=tax, grandtotal=grandtotal, brands=brands(), categories=categories())

@app.route('/updatecart/<int:code>', methods=['POST'])
def updateCart(code):
    if 'ShopCart' not in session or len(session['ShopCart']) <= 0:
        return redirect(url_for('home'))
    if request.method == 'POST':
        quantity = request.form.get('quantity')
        color = request.form.get('colors')
        try:
            session.modified = True
            for key, item in session['ShopCart'].items():
                if int(key) == code:
                    item['quantity'] = int(quantity)
                    item['colors'] = color
                    flash('Cart updated successfully', 'success')
                    return redirect(url_for('getCart'))
        except Exception as e:
            print(e)
            return redirect(url_for('getCart'))

@app.route('/deleteitem/<int:code>')
def deleteItem(code):
    if 'ShopCart' not in session or len(session['ShopCart']) <= 0:
        return redirect(url_for('home'))
    try:
        session.modified = True
        for key, item in session['ShopCart'].items():
            if int(key) == code:
                session['ShopCart'].pop(key, None)
                flash('Product removed from cart', 'success')
                return redirect(url_for('getCart'))
    except Exception as e:
        print(e)
        return redirect(url_for('getCart'))

@app.route('/clearcart')
def clearCart():
    try:
        session.pop('ShopCart', None)
        return redirect(url_for('home'))
    except Exception as e:
        print(e)