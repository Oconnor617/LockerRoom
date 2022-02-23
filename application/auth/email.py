"""
Created on Aug 1, 2021
@author: oconn
Issues:
"""
from flask_mail import Message
from application import app, mail
from flask import render_template
from application.email import send_email

def send_password_reset_email(user):
    token = user.get_reset_password_token()
    send_email('[The LockerRoom] Reset Your Password',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/reset_password.txt',
                                         user=user, token=token),
               html_body=render_template('email/reset_password.html',
                                         user=user, token=token))

def send_auth_email(user):
    token = user.get_auth_token()
    send_email('[The LockerRoom] Account Confirmation Link',
               sender=app.config['ADMINS'][0],
               recipients=[user.email],
               text_body=render_template('email/auth.txt',
                                         user=user, token=token),
               html_body=render_template('email/auth.html',
                                         user=user, token=token))