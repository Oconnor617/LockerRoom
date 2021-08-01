from application import db, app # Import the database stored iin the app directory
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin  # provides generic implementation so flaskLogin can work with all db
from application import login
import jwt
from time import time


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, nullable=True, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)
    registered_on = db.Column(db.DateTime, nullable=True)
    dl1rm = db.Column(db.Numeric(10, 2), default=100)
    bench1rm = db.Column(db.Numeric(10, 2), default=0)
    squat1rm = db.Column(db.Numeric(10, 2), default=0)
    press1rm = db.Column(db.Numeric(10, 2), default=0)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_reg_time(self):
        datetime_obj = datetime.datetime.today()
        self.registered_on = datetime_obj

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def set_dl(self, newDL):
        self.dl1rm = newDL

    def set_bench(self, newBench):
        self.bench1rm = newBench

    def set_squat(self, newSq):
        self.squaat1rm = newSq

    def set_dl(self, newPress):
        self.press1rm = newPress

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {'reset_password': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {}>'.format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post {}>'.format(self.body)

@login.user_loader
def load_user(id): # used by Flask-Login to load a user based on their session ID
    """used by flask login to load users as they navigate to new pages"""
    return User.query.get(int(id)) # Flask-Login uses String but db uses ints so convert