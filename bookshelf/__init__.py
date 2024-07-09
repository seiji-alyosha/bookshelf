"""
bookshelf
a personal library

"""
import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev',
        #stores the database in the instance folder
        DATABASE=os.path.join(app.instance_path, 'bookshelf.sqlite'),
    )

    if test_config is None:
        #to update the secret key for deployment
        app.config.from_pyfile('config.py', silent=True)

    else:
        #configurations for testing
        app.config.update(test_config)

    #makes the instance folder if not present.
    #needed because Flask does not make one automatically.
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route('/')
    def hello():
        return 'Testing the application factory.'
    
    return app
