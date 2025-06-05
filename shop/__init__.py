from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
from flask_msearch import Search
from flask_login import LoginManager, login_manager
from flask_migrate import Migrate

# Thư mục hiện tại
basedir = os.path.abspath(os.path.dirname(__file__))
# Khởi tạo Flask app
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pak123!!!@localhost/shopdb'
app.config['SECRET_KEY'] = 'fkshfkhwoe8ww0590fmw050'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images/products')
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

# Cấu hình Flask-Migrate
migrate = Migrate(app, db)
with app.app_context():
    if db.engine.url.drivername == 'mysql':
        migrate.init_app(app, db, render_as_batch=True)
    else:
        migrate.init_app(app, db)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.needs_refresh_message_category = 'danger'
login_manager.login_message = 'Please login to access this page'

from shop.admin import routes
from shop.products import routes
from shop.carts import carts
from shop.customers import routes
from shop.sale import routes
from shop.warehouse import routes
from shop.accounting import routes