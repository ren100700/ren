import redis
from flask import Flask
from flask_script import Manager
from flask_session import Session

from app.house_views import house_blue
from app.models import db
from app.order_views import order_blue
from app.user_views import blue

app = Flask(__name__)

app.register_blueprint(blueprint=blue,url_prefix='/user')
app.register_blueprint(blueprint=house_blue,url_prefix='/house')
app.register_blueprint(blueprint=order_blue,url_prefix='/order')

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:123456@localhost:3306/flaskxm'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_REDIS'] = redis.Redis(host='127.0.0.1', port='6379')


app.config['SECRET_KEY'] = 'secret_key'

session = Session()
session.init_app(app=app)

db.init_app(app)

manage = Manager(app)

if __name__ == '__main__':

	manage.run()