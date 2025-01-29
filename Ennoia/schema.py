# In your __init__.py or a commands.py file
import click
from flask.cli import with_appcontext
from bookshelf.db import get_db


@click.command('update-schema')
@with_appcontext
def update_schema_command():
    """Update the database schema."""
    db = get_db()

    db.execute('CREATE TABLE book_backup AS SELECT * FROM book;')

    # Drop and recreate table
    db.execute('DROP TABLE IF EXISTS book;')

    # This is where the actual schema gets changed. Currently, this is meant to update the schemas timestamp.
    db.execute('''CREATE TABLE book (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        author TEXT NOT NULL,
        title TEXT NOT NULL,
        notes TEXT,
        added DATETIME DEFAULT CURRENT_TIMESTAMP
    );''')
    
    # Restore data with proper timestamp format
    db.execute('''INSERT INTO book (id, author, title, notes, added)
        SELECT 
            id,
            author,
            title,
            notes,
            CASE 
                WHEN added LIKE '% %' THEN added 
                ELSE added || ' 00:00:00'
            END
        FROM book_backup;''')
    
    # Optional: drop backup table
    db.execute('DROP TABLE book_backup;')
    
    db.commit()
    
    click.echo('Updated schema.')

# Register the command
def init_app(bookshelf):
    bookshelf.cli.add_command(update_schema_command)