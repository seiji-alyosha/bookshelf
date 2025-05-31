import click
from flask.cli import with_appcontext
from bookshelf.db import get_db

#this is for managing the database, like changing table values, adding new columns, etc.

#this function adds a user_id column to the book table in the database. I needed to do this because any user was able to access the same books. This way, each user can only access their own books
@click.command('add-user-id-column')
@with_appcontext
def add_user_id_column():
    """Add user_id column to book table."""
    db = get_db()
    try:
        db.execute('ALTER TABLE book ADD COLUMN user_id INTEGER')
        db.commit()
        click.echo('Added user_id column.')
    except Exception as e:
        click.echo(f'Column might already exist: {e}')

def init_app(bookshelf):
    bookshelf.cli.add_command(add_user_id_column)


@click.command('add-1-to-user-id')
@with_appcontext
def add_1_to_user_id():
    """Add 1 to user_id for all books."""
    db = get_db()
    try:
        db.execute('UPDATE book SET user_id = 1')
        db.commit()
        click.echo('Added 1 to user_id for all books.')
    except Exception as e:
        click.echo(f'Error updating user_id: {e}')


def init_app(bookshelf):
    bookshelf.cli.add_command(add_user_id_column)
    bookshelf.cli.add_command(add_1_to_user_id)