from application import db#, app  # Import the database stored in the app directory
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
    dl1rm = db.Column(db.Numeric(10, 2), default=185)
    bench1rm = db.Column(db.Numeric(10, 2), default=135)
    squat1rm = db.Column(db.Numeric(10, 2), default=155)
    press1rm = db.Column(db.Numeric(10, 2), default=95)
    weight = db.Column(db.Numeric(10, 2), default=150)
    posts = db.relationship('Post', backref='author', lazy='dynamic')

    def set_reg_time(self):
        datetime_obj = datetime.today()
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
        self.squat1rm = newSq

    def set_ohp(self, newPress):
        self.press1rm = newPress

    def set_weight(self, newWeight):
        self.weight = newWeight

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

    def get_auth_token(self, expires_in=600): #Used to Generate an auth token for email 2fa. Token uses user ID
        return jwt.encode(
            {'auth': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256')

    @staticmethod
    def verify_auth_token(token): #used to verify and return the user who generated and clicked on the token
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['auth']
        except:
            return
        return User.query.get(id)

    def __repr__(self):
        return '<User {} Email: {} Confirmed: {}>'.format(self.username, self.email, self.confirmed)


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