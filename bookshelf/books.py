from flask import (
    Blueprint, render_template, g, request
)

import requests
from bookshelf.db import get_db
from bookshelf.auth import login_required
from bookshelf.info import get_book_info, get_book_description

bp = Blueprint('books',__name__)

@bp.route('/')
@login_required
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

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    tad = None
    book_info = None
    if request.method == 'POST':
        isbn = request.form.get('ISBN')
        if isbn:
            #check the url to see if it loads the correct information. next step is to print out actual book information.
            #check chat gpt
            book_info = get_book_info(isbn)
            works_key = book_info.get('works','this book does not have a works_key :()')

            tad = dict (
                title = book_info.get('title'),
                author = book_info.get('author'),
                description = get_book_description(works_key)
            )
      
    return render_template('library/add.html', book=tad)