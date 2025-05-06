from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
from flask_msearch import Search
from flask_login import LoginManager, login_manager

# Thư mục hiện tại
basedir = os.path.abspath(os.path.dirname(__file__))
# Khởi tạo Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pak123!!!@localhost/shopdb'
app.config['SECRET_KEY'] = 'fkshfkhwoe8ww0590fmw050'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB Limit

# Cấu hình search
# app.config['MSEARCH_BACKEND'] = 'whoosh'
# app.config['MSEARCH_INDEX_NAME'] = 'msearch'

photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # Bâm app
search = Search(db=db)
search.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'customer_login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = 'Please login to access this page'

from website.admin import routes
from website.products import routes
from website.carts import carts
from website.customers import routes