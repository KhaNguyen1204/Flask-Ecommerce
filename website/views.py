from flask import Blueprint, render_template
from flask_login import login_required, current_user
import os
from flask import current_app
import json

views = Blueprint('views', __name__)

@views.route('/')
def home():
    return render_template("home.html", customer=current_user)


@views.route('/cart')
@login_required
def cart():
    return render_template("cart.html", customer=current_user)

@views.route('/search', methods=['GET', 'POST'])
def search():
    return '<h1>Tim kiem khong ra</h1>'

@views.route('/smartphone')
@views.route('/smartphone')
def smartphone():
    file_path = os.path.join(current_app.root_path, 'static', 'products_smartphone.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    return render_template("product_list.html", title='Smartphone', products=products, customer=current_user)


@views.route('/laptop', methods=['GET', 'POST'])
def laptop():
    file_path = os.path.join(current_app.root_path, 'static', 'products_laptop.json')
    with open(file_path, 'r', encoding='utf-8') as file:
        products = json.load(file)

    return render_template("product_list.html", title='Laptop', products=products, customer=current_user)


@views.route('/tablet', methods=['GET', 'POST'])
def tablet():
    return '<h1>List tablet</h1>'

@views.route('/smartwatch', methods=['GET', 'POST'])
def smartwatch():
    return '<h1>List dong ho thong minh</h1>'