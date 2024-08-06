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
    book_response = None
    if request.method == 'POST':
        isbn = request.form.get('ISBN')
        if isbn:
            #check the url to see if it loads the correct information. next step is to print out actual book information.
            #check chat gpt
            response = requests.get(f'https://openlibrary.org/api/books?bibkeys=ISBN:{isbn}&format=json&jscmd=data')
            if response.status_code == 200:
                book_response = response.json()
    return render_template('library/add.html', ISBN=book_response)


            

            

        
    return render_template('library/add.html')
