"""
bookshelf
a personal library

"""

#imports
import os
from flask import Flask, request, flash, session

#creating instance of the Flask object
bookshelf = Flask(__name__)
bookshelf.config['DEBUG'] = True

#login form function
def log_in_form():
     return 'login'
#user logging in function
def logging_in():
        if request.form['password'] == 'password' and request.form['password'] == 'username':
            session['logged_in'] = True
        else:
            flash('wrong password!')

#login screen
@bookshelf.route('/', methods = ['GET', 'POST'])
def login():
    if request.method == 'POST':
        return logging_in()
    else:
         return log_in_form()
    