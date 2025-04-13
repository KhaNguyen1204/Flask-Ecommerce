from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os
from flask import current_app
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    """
    Chọn một số sản phâm từ các category để hiển thị ở thư mục home.html
    :return: home.html
    """
    featured_products = []

    categories = ['Smartphone', 'Laptop', 'Tablet', 'SmartWatch']
    for category in categories:
        file_path = os.path.join(current_app.root_path, 'static/json', f'products_{category.lower()}.json')
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                products = json.load(file)
                featured_products.extend(products[:2]) # Lấy 2 sản phẩm
        except FileNotFoundError:
            pass
    return render_template("home.html", products=featured_products, customer=current_user)


@views.route('/cart')
@login_required
def cart():
    return render_template("cart.html", customer=current_user)

@views.route('/search', methods=['GET', 'POST'])
def search():
    return '<h1>Tim kiem khong ra</h1>'

@views.route('/smartphone')
def smartphone():
    file_path = os.path.join(current_app.root_path, 'static/json', 'products_smartphone.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    return render_template("product_list.html", title='Smartphone', products=products, customer=current_user)


@views.route('/laptop')
def laptop():
    file_path = os.path.join(current_app.root_path, 'static/json', 'products_laptop.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    return render_template("product_list.html", title='Laptop', products=products, customer=current_user)


@views.route('/tablet')
def tablet():
    file_path = os.path.join(current_app.root_path, 'static/json', 'products_tablet.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    return render_template("product_list.html", title='Tablets', products=products, customer=current_user)

@views.route('/smartwatch')
def smartwatch():
    file_path = os.path.join(current_app.root_path, 'static/json', 'products_smartwatch.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    return render_template("product_list.html", title='Smart Watchs', products=products, customer=current_user)