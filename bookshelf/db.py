import sqlite3

import click
from flask import current_app, g

#to set up the database if the request does not have one
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

#to run the function that sets up the database.
def init_db():
    db = get_db()

    #no idea what this does.
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

#a function that allows users to initialize the database through the command line.
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

#to register the databse with the application
def init_app(bookshelf):
    bookshelf.teardown_appcontext(close_db)
    bookshelf.cli.add_command(init_db_command)