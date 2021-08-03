"""
Created June 16, 2021
@author: oconn
"""
from flask import render_template, request, flash, redirect, url_for, jsonify
from application import app, db, mail
from application.models import User
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse
from application.email import send_password_reset_email, send_auth_email
from flask_mail import Message
import datetime


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Get the data from the post
        message = request.form['message']
        print(message)
        flash("Message Recieved. We will get back to you soon "
              "")
        return render_template('index.html')

    else:  # It is a GET Request
        return render_template('index.html')


#############################################################################################
# Routes for user entrance/exit into app
#############################################################################################
# decorator so we know when to activate the login view function
@app.route('/login', methods=['GET', 'POST'])
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
            return redirect(url_for('login'))
        login_user(user)
        # following code is for handling redirects if someone who is not logged in tried to access protected pages
        next_page = request.args.get('next')
        if not next_page or url_parse(
                next_page).netloc != '':  # url_parse in case next is a URL to another site. We don't go there
            # next_page = url_for('index')
            next_page = url_for('user', username=current_user.username)
        return redirect(next_page)  # should be /user if no redirect
        ####

    else:
        return render_template('login.html', title='Sign In')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))  # redirect them if they try to access this URL while logged in

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
            return redirect(url_for('register'))
        if taken_email is not None:
            flash("This is Server-side Validation: That email is taken. Please use another one")
            return redirect(url_for('register'))
        else:  # Everything must be okay let's register this new user
            user = User(username=regName, email=user_email)  # create a new user in the db
            user.set_password(pass1)  # Javascript on front-end should have already confirmed pass1 == retype
            # use the set_pw method because it will store a hashed password and we never see the plain-text password
            user.set_reg_time()
            db.session.add(user)
            db.session.commit()  # user added!
            flash('From the Sever: Thanks for registering please use your new credentials to login')
            return redirect(url_for('login'))

    else:
        return render_template('registration.html')  # It's a GET request. No form Submitted


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


#############################################################################################
# Routes for user pages - profile page and message board
#############################################################################################


@app.route('/user/<username>')  # each user page will have a unique URL
@login_required  # You must be logged in as that user to access that specific user page URL
# Flask-Login ensures that a user must be logged in to access. It will redirect to /login
def user(username):
    user = User.query.filter_by(username=username).first_or_404()  # search the db for the UN passed in
    # The above will send a 404 back to the client browser if no user is found
    return render_template('user.html', user=user)


#############################################################################################
# Routes for updating DB - profile page and message board
#############################################################################################

@app.route('/update_dl/<username>', methods=['GET', 'POST'])
@login_required  # You must be logged in as a user to update a 1rm
def update_dl(username):
    user = User.query.filter_by(username=username).first_or_404()  # make sure we get the user who passed the data
    if request.method == 'POST':
        new_dl = request.form['new_dl']
        if new_dl == '':
            flash('More Server-Side Validation. Please enter a Number')
            return redirect(url_for('user', username=user.username))
        user.set_dl(new_dl) # update the DB
        db.session.add(user)
        db.session.commit()
        flash("Your Deadlift Max has been updated")
        # return render_template('user.html', user=user)
        return redirect(url_for('user', username=user.username))
    else:  # Must be a GET
        return render_template('user.html', user=user)


@app.route('/update_ohp/<username>', methods=['GET', 'POST'])
@login_required  # You must be logged in as a user to update a 1rm
def update_ohp(username):
    user = User.query.filter_by(username=username).first_or_404()  # make sure we get the user who passed the data
    if request.method == 'POST':
        new_ohp = request.form['new_ohp']
        if new_ohp == '':
            flash('More Server-Side Validation. Please enter a Number')
            return redirect(url_for('user', username=user.username))
        user.set_ohp(new_ohp) # update the DB
        db.session.add(user)
        db.session.commit()
        flash("Your Press Max has been updated")
        # return render_template('user.html', user=user)
        return redirect(url_for('user', username=user.username))
    else:  # Must be a GET
        return render_template('user.html', user=user)


@app.route('/update_squat/<username>', methods=['GET', 'POST'])
@login_required  # You must be logged in as a user to update a 1rm
def update_squat(username):
    user = User.query.filter_by(username=username).first_or_404()  # make sure we get the user who passed the data
    if request.method == 'POST':
        new_squat = request.form['new_squat']
        if new_squat == '':
            flash('More Server-Side Validation. Please enter a Number')
            return redirect(url_for('user', username=user.username))
        user.set_squat(new_squat) # update the DB
        db.session.add(user)
        db.session.commit()
        flash("Your Squat Max has been updated")
        # return render_template('user.html', user=user)
        return redirect(url_for('user', username=user.username))
    else:  # Must be a GET
        return render_template('user.html', user=user)


@app.route('/update_bench/<username>', methods=['GET', 'POST'])
@login_required  # You must be logged in as a user to update a 1rm
def update_bench(username):
    user = User.query.filter_by(username=username).first_or_404()  # make sure we get the user who passed the data
    if request.method == 'POST':
        new_bench = request.form['new_bench']
        if new_bench == '':
            flash('More Server-Side Validation. Please enter a Number')
            return redirect(url_for('user', username=user.username))
        user.set_bench(new_bench) # update the DB
        db.session.add(user)
        db.session.commit()
        flash("Your Press Max has been updated")
        # return render_template('user.html', user=user)
        return redirect(url_for('user', username=user.username))
    else:  # Must be a GET
        return render_template('user.html', user=user)


@app.route('/update_weight/<username>', methods=['GET', 'POST'])
@login_required  # You must be logged in as a user to update a 1rm
def update_weight(username):
    user = User.query.filter_by(username=username).first_or_404()  # make sure we get the user who passed the data
    if request.method == 'POST':
        new_weight = request.form['enter-weight']
        if new_weight == '':
            flash('More Server-Side Validation. Please enter a Number')
            return redirect(url_for('user', username=user.username))
        user.set_weight(new_weight) # update the DB
        db.session.add(user)
        db.session.commit()
        flash("Your weight has been updated")
        # return render_template('user.html', user=user)
        return redirect(url_for('user', username=user.username))
    else:  # Must be a GET
        return render_template('user.html', user=user)

#@app.route('check_un', methods=['GET', 'POST'])
#def check_un(): #I am not sure if this needs perameters or not
#    # GET Request
#    if request.method == 'GET':
#        message = {'here': 'Returning GET'}
#        return jsonify(message) #serialize and add JSPN headers
#    if request.method == 'POST':
