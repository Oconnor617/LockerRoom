### This module will be used to store the view funcitons associated with Authentication. Login, Register, Password Reset, etc.
from flask import render_template, request, flash, redirect, url_for, jsonify, make_response
from application import app, db
from application.models import Post, User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from application.auth.email import send_password_reset_email, send_auth_email
from flask_mail import Message
import datetime

from application.auth import bp # The auth Blueprint in this case

#############################################################################################
# Routes for user entrance/exit into app
#############################################################################################
# decorator so we know when to activate the login view function
@bp.route('/login', methods=['GET', 'POST'])
# the methods specify the HTTP request methods
def login():
    if current_user.is_authenticated:  # Auto redirect if they are already logged in
        return redirect(url_for('index'))
    if request.method == 'POST':
        # Get the data from the post
        username = request.form['username']
        password = request.form['password']
        print(username)
        print(password)
        # flash('from the server-side. Username ' + username + 'password: ' + password )
        # return render_template('login.html', title='Sign In')
        user = User.query.filter_by(username=username).first()
        if user is None or not user.check_password(password):
            flash('This is Server-side validation: Invalid username or password')
            return redirect(url_for('auth.login'))
        login_user(user)
        # following code is for handling redirects if someone who is not logged in tried to access protected pages
        next_page = request.args.get('next')
        if not next_page or url_parse(
                next_page).netloc != '':  # url_parse in case next is a URL to another site. We don't go there
            # next_page = url_for('index')
            next_page = url_for('main.user', username=current_user.username)
        return redirect(next_page)  # should be /user if no redirect
        ####

    else:
        return render_template('auth/login.html', title='Sign In')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))  # redirect them if they try to access this URL while logged in

    if request.method == 'POST':  # Form Submitted
        regName = request.form['regName']
        user_email = request.form['regEmail']
        pass1 = request.form['password']
        retype = request.form['retype']

        print(regName)
        print(user_email)
        print(pass1)

        taken_un = User.query.filter_by(username=regName).first()  # if this returns a value the name is taken
        taken_email = User.query.filter_by(email=user_email).first()  # if this returns a value the email is taken
        if taken_un is not None:
            flash("This is Server-side Validation: That username is taken. Please choose another one")
            return redirect(url_for('auth.register'))
        if taken_email is not None:
            flash("This is Server-side Validation: That email is taken. Please use another one")
            return redirect(url_for('auth.register'))
        else:  # Everything must be okay let's register this new user
            user = User(username=regName, email=user_email)  # create a new user in the db
            user.set_password(pass1)  # Javascript on front-end should have already confirmed pass1 == retype
            # use the set_pw method because it will store a hashed password and we never see the plain-text password
            user.set_reg_time()
            db.session.add(user)
            db.session.commit()  # user added!
            flash('From the Sever: Thanks for registering please use your new credentials to login')
            return redirect(url_for('auth.login'))

    else:
        return render_template('auth/registration.html')  # It's a GET request. No form Submitted


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('main.index')) #Back to the home page
