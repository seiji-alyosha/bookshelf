from functools import wraps
from werkzeug.security import check_password_hash, generate_password_hash
from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from bookshelf.db import get_db
#to create a blueprint for authentication views
bp = Blueprint('auth', __name__, url_prefix='/auth')

def login_required(view):
    #a decorator that ensures each view is accessed by a logged in user. I have no clue what the kwargs is for.
    @wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
    
        return view(**kwargs)
    
    return wrapped_view

@bp.before_app_request
def load_user():
    #to get the session id from the logged in user
    user_id = session.get('user_id')

    #in case the url is accessed without logging in ?
    if user_id is None:
        g.user = None

    #keeps the users session id as long as they are logged in ?
    else:
        g.user = (
            get_db().execute('SELECT * FROM user WHERE id = ?', (user_id,)).fetchone()
        )

@bp.route('/create', methods=('GET','POST'))
def create():
    #to create a username and password, the user will have to submit a form. in this case, the method will be POST. 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        #setting up the database whenever user adds information
        db = get_db()
        error = None

        #to handle users forgetting to add usernames or passwords.
        if not username:
            error = 'Whoops! Looks like you forgot to add a username. Please try again.'
        elif not password:
            error = 'Whoops! Looks like you forgot to add a password. Please try again.'

        #validating the username and password
        if error is None:
            try:
                #to add the username and password into the user database table. 
                #this function fills the ? with the values in the variables defined in create().
                #execute() prevents from SQL injection attack.
                db.execute(
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                #because data was modified, it is considered pending. 
                #this completes the pending transaction of data.
                db.commit()
            #this error is raised when the username is already taken, apparently.
            #why is this error risen? and why is there not an exception for a taken password?
            except db.IntegrityError:
                error = f'Sorry, {username} is already taken. Please try another.'
            #once the user successfully creates an account, they are redirected to the login screen.
            else:
                return redirect(url_for('auth.login'))
        #this allows the user to see the error messages if they occur.
        flash(error)
    return render_template('auth/create.html', is_create=True)

@bp.route('/login', methods=('GET','POST'))
def login():
    #to login, the user still sends data to the server. this makes it a POST method.
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None

        #to handle users forgetting to add usernames or passwords.
        #try making this a try block
        if not username:
            error = 'Whoops! Looks like you forgot to add a username. Please try again.'
        elif not password:
            error = 'Whoops! Looks like you forgot to add a password. Please try again.'

        #used to validate the users input. 
        #gets data based on the users input.
        user = db.execute(
            'SELECT * FROM user WHERE username = ?',
            (username,)
        ).fetchone()

        #can this be a try block? why and why not?
        if user is None:
            error = 'Sorry, we did not recognize that username.'
        elif not check_password_hash(user["password"], password):
            error = 'Sorry, we did not recognize that password for that username.'
        
        if error is None:
            #clears the session of any data.
            session.clear()
            #stores the session's id as the user's id.
            #this allows the users data to be available throughout all views.
            session['user_id'] = user['id']
            #to direct successfully logged in users to the index page.
            return redirect(url_for('index'))
        #this allows the user to see the error messages if they occur.
        flash(error)
    return render_template('auth/login.html', is_login=True)   
        
@bp.route('/logout')
def logout():
    #to clears the users session and send them to the login window.
    session.clear()
    return redirect(url_for('auth.login'))

