from flask import Blueprint, render_template
from flask_login import login_required, current_user

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

@views.route('/smartphone', methods=['GET', 'POST'])
def smartphone():
    return '<h1>List dien thoai</h1>'

@views.route('/laptop', methods=['GET', 'POST'])
def laptop():
    return '<h1>List laptop</h1>'

@views.route('/tablet', methods=['GET', 'POST'])
def tablet():
    return '<h1>List tablet</h1>'

@views.route('/smartwatch', methods=['GET', 'POST'])
def smartwatch():
    return '<h1>List dong ho thong minh</h1>'

@views.route('/watch', methods=['GET', 'POST'])
def watch():
    return '<h1>List watch</h1>'
