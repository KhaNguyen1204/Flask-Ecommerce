from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_uploads import UploadSet, IMAGES, configure_uploads
import os
from flask_migrate import Migrate


# Thư mục hiện tại
basedir = os.path.abspath(os.path.dirname(__file__))
# Khởi tạo Flask app
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:Pak123!!!@localhost/shop'
app.config['SECRET_KEY'] = 'fkshfkhwoe8ww0590fmw050'
app.config['UPLOADED_PHOTOS_DEST'] = os.path.join(basedir, 'static/images')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16MB Limit


photos = UploadSet('photos', IMAGES)
configure_uploads(app, photos)

db = SQLAlchemy(app)
bcrypt = Bcrypt(app) # Bâm app
migrate = Migrate(app, db)


from website.admin import routes
from website.products import routes