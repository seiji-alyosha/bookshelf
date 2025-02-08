from flask import (
    Blueprint, render_template, g, request, redirect, url_for, flash, abort
)

from slugify import slugify
from bookshelf.db import get_db
from bookshelf.auth import login_required
from bookshelf.info import get_book_info, get_book_description
from bookshelf.author_name import get_author_name

bp = Blueprint('books',__name__)

'''
blueprint route functions
'''
@bp.route('/')
@login_required
def books():
   # to get the data from the py file that accesses the SQL database
   db = get_db()
   
   # lists all books in the library in descending order
   library = db.execute(
     'SELECT book.id, book.author, book.title, book.notes, date(book.added) as added'
     ' FROM book'
     ' ORDER BY book.id DESC'
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
      
      if not title or not author: 
         error = 'Please enter a title and author.'
         flash(error)
           
         return render_template('library/add')
       
      try: 
         if duplicate_check(title, author) == False:
               db.execute ( 
                  'INSERT INTO book (title, author, notes) VALUES (?, ?, ?)',
                  (title, author, notes),
               )
               db.commit()
               
               # to retrieve the id of the book added by the user
               book_id = db.execute (
                  'SELECT id FROM book WHERE title = ? AND author = ?', 
                  (title, author)
               ).fetchone()['id']

               db.close()

               # to handle cases where, for some reason, the id cannot be retrieved.
               if book_id is None:

                  error = 'Sorry, we could not access the book you just added. Please try viewing the book again.'
                  flash(error)

                  return render_template('library/add.html')

               # to redirect the user to the new book, given the retrieved id.
               return redirect(url_for('books.view_book', id=book_id, slug=slugify(title)))
         else:
               error = f'You already have <b>{title}</b> by <b>{author}</b> in your library.'
               flash(error)
      
      finally:
        db.close()
       
   return render_template('library/add.html')

@bp.route('/<int:id>/<slug>', methods=['GET', 'POST'])
@login_required
def view_book(id, slug):

   db = get_db()
   error = None

   try:
      # To run the delete function whenever the user clicks the delete button.
      # This should be the only instance where a post request is made in the view_book function.
      if request.method == 'POST':
         return delete_book(db, id)
      
      # if a user is viewing a book or clicks CANCEL when deleting a book, this function runs.
      # this is also an example of "early returns", which gives a default view for the function and also works as an else statement.
      content = db.execute (
         'SELECT * FROM book WHERE id = ?', 
         (id,)
      ).fetchone()

      # to tell the user the book with the id in the URL doesn't exist in the database.
      # This might not be necessary since the user will primarily select books from index.
      if not content:
         flash('This book is not in your library. Please try another selection.')

         # an early return to the books page if something goes wrong with viewing the book.
         return redirect(url_for('books.books'))


      # to recorrect the slug based on the id if the slug in the URL does not match the book id.
      if slug != slugify(content['title']):
         return redirect(url_for('books.view_book', id=id, slug=slugify(content['title'])))
         
      return render_template('library/book.html', book_info=content)
   
   finally:
      db.close()

@bp.route('/<int:id>/<slug>/edit', methods=['GET','POST'])
@login_required
def edit_book(id, slug):

   db = get_db()
   error = None

   try:
      if request.method == 'POST':
         title = request.form.get('title')
         author = request.form.get('author')
         notes = request.form.get('notes')

         # server side input validation of title and author
         if (not title or title.isspace()) and (not author or author.isspace()): 
            error = 'Looks like you forgot a title and an author. Please try again.'
            flash(error)
            return redirect(url_for('books.edit_book', id=id, slug=slug))
         elif not title or title.isspace():
            error = 'Looks like you forgot a title. Please try again.'
            flash(error)
            return redirect(url_for('books.edit_book', id=id, slug=slug))
         elif not author or author.isspace():
            error = 'Looks like you forgot an author. Please try again.'
            flash(error)
            return redirect(url_for('books.edit_book', id=id, slug=slug))

         return update_book(db, id, title, author, notes)
      
      content = db.execute (
         'SELECT * FROM book WHERE id = ?', 
         (id,)
      ).fetchone()

      # input validation if the book id doesn't exist in the database.
      if not content:
         abort(404, description='Sorry, we couldn\'t find the book you were looking for. Please try another selection.')

      # if the slug in the url doesn't match with the`` book title for the book id, it corrects the slug.
      if slug != slugify(content['title']):
         return redirect(url_for('books.edit_book', id=id, slug=slugify(content['title'])))

      return render_template('library/edit.html', book_info=content, slug=slugify(content['title']))
      
   finally:
      db.close()

'''
non-blueprint functions
'''
def duplicate_check(title, author):
    
   db = get_db()
    
   duplicate = db.execute (
      '''SELECT id FROM book 
      WHERE LOWER(title) = LOWER(?)
      AND LOWER(author) = LOWER(?)''',
      (title, author)
   ).fetchone()
   # returns true if there is a duplicate book. Used in add_book to check for duplicates.
   return duplicate is not None

# for deleting a book when viewing a book. Runs after the user clicks OK to delete a book.
def delete_book(db, id):
   try:
      db.execute('DELETE FROM book WHERE id = ?',
         (id,)
      )
      db.commit()
   except Exception as ex:
      db.rollback()
      raise ex
   return redirect(url_for('books.books'))

# for updating a book whenever the user clicks the save button in the edit page.
def update_book(db, id, title, author, notes):
   try:
      db.execute('UPDATE book SET title = ?, author = ?, notes = ? WHERE id = ?',
         (title, author, notes, id)
      )
      db.commit()
   except Exception as ex:
      db.rollback()
      raise ex
   return redirect(url_for('books.view_book', id=id, slug=title))












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