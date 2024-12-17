from flask import (
    Blueprint, render_template, g, request, redirect, url_for, flash
)

import requests
from bookshelf.db import get_db
from bookshelf.auth import login_required
from bookshelf.info import get_book_info, get_book_description
from bookshelf.author_name import get_author_name

bp = Blueprint('books',__name__)

@bp.route('/')
@login_required
def books():
    #to get the data from the py file that accesses the SQL database
    db = get_db()
    #? 
    library = db.execute(
        'SELECT book.id, book.author, book.title, book.notes, date(book.added) as added'
        ' FROM book'
        ' ORDER BY added DESC'
    ).fetchall()
    return render_template('library/index.html', list=library)

@bp.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    if request.method == 'POST':
       title = request.form.get('title')
       author = request.form.get('author')
       notes = request.form.get('notes')

       db = get_db()
       error = None
       
       db.execute( 
            'INSERT INTO book (title, author, notes) VALUES (?, ?, ?)',
            (title, author, notes),
        )
       db.commit()

    return render_template('library/add.html')

@bp.route('/<string:title>', methods=['GET', 'POST'])
@login_required
def view_book(title):

    db = get_db()
    error = None

    if request.method == 'POST':
        db.execute('DELETE FROM book WHERE title = ?',
            (title,)
        )
        db.commit()
        db.close()

        return redirect(url_for('books.books'))
    
    content = db.execute (
        'SELECT * FROM book WHERE title = ?', 
        (title,)
    ).fetchone()

    return render_template('library/book.html', book_info=content)


@bp.route('/<string:title>/edit', methods=['GET','POST'])
@login_required
def edit_book(title):

    db = get_db()
    error = None

    if request.method == 'POST':
       new_title = request.form.get('title')
       author = request.form.get('author')
       notes = request.form.get('notes')
       
       db.execute('UPDATE book SET title = ?, author = ?, notes = ? WHERE title = ?',
                    (new_title, author, notes, title))
       db.commit()
       db.close()

       return redirect(url_for('books.view_book', title=new_title))
    
    content = db.execute (
        'SELECT * FROM book WHERE title = ?', 
        (title,)
    ).fetchone()

    return render_template('library/edit.html', book_info=content)















    '''
    SAVING FOR LATER
    isbn = request.form.get('ISBN')
    if isbn:
        #check the url to see if it loads the correct information. next step is to print out actual book information.
        #check chat gpt
        book_info = get_book_info(isbn)
        works_key = book_info.get('works','this book does not have a works_key :()')
        author_key = book_info.get('authors')

        tad = dict (
            title = book_info.get('title'),
            author = get_author_name(author_key),
            description = get_book_description(works_key)
        )
    '''