from flask import (
    Blueprint, render_template, g, request
)

import requests
from bookshelf.db import get_db
from bookshelf.auth import login_required

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
    if request.method == 'POST':
        isbn = request.form.get('ISBN')
        if isbn:
            response = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data')
    return render_template('library/add.html')


            

            

        
    return render_template('library/add.html')
