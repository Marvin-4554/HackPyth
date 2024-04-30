from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://help_user:pass123@localhost/help_desk'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'f1c50cdf58a5ac7024799454'

s = URLSafeTimedSerializer(app.config['SECRET_KEY'])

db = SQLAlchemy(app)

from help_desk import routes