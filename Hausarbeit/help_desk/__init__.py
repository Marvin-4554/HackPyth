from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeSerializer
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

app = Flask(__name__)
limiter = Limiter(
    get_remote_address,
    app=app,
    #default_limits=["200 per day", "50 per hour"],
    storage_uri="memory://",
)

SECRET_KEY = 'password1'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://help_user:pass123@localhost/help_desk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = SECRET_KEY

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SESSION_COOKIE_HTTPONLY'] = False

s = URLSafeSerializer(app.config['SECRET_KEY'])

db = SQLAlchemy(app)

from help_desk import routes