"""
bookshelf
a personal library

"""
import os
from flask import Flask

def create_app(test_config=None):
    bookshelf = Flask(__name__, instance_relative_config=True)
    bookshelf.config.from_mapping(
        SECRET_KEY='dev',
        #stores the database in the instance folder
        DATABASE=os.path.join(bookshelf.instance_path, 'bookshelf.sqlite'),
    )

    if test_config is None:
        #to update the secret key for deployment
        bookshelf.config.from_pyfile('config.py', silent=True)

    else:
        #configurations for testing
        bookshelf.config.update(test_config)

    #makes the instance folder if not present.
    #needed because Flask does not make one automatically.
    try:
        os.makedirs(bookshelf.instance_path)
    except OSError:
        pass

    @bookshelf.route('/')
    def hello():
        return 'Testing the application factory.'
    
    #to initialize the database with bookshelf
    from . import db
    db.init_app(bookshelf)

    #registers blueprints with bookshelf
    from . import auth
    from . import books
    bookshelf.register_blueprint(auth.bp)
    bookshelf.register_blueprint(books.bp)
    app.add_url_rule('/', endpoint='index')

    
    return bookshelf
