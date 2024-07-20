from flask import (
    Blueprint, render_template, g
)
from bookshelf.db import get_db
from bookshelf.auth import login_required

bp = Blueprint('books',__name__)

@bp.route('/')
def books():
    #to get the data from the py file that accesses the SQL database
    db = get_db()
    #? 
    library = db.execute(
        'SELECT book.id, book.author, book.title, book.info, book.added'
        ' FROM book'
        ' ORDER BY added DESC'
    ).fetchall()
    return render_template('library/index.html', list=library)

