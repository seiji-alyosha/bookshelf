#imports 
from functools import wraps
from werkzeug.security import check_password_hash
from flask import (
    Blueprint, g, request, jsonify
)

#bookshelf function imports
from bookshelf.db import get_db

#api blueprint
bp = Blueprint('api', __name__, url_prefix='/api/v1')

#api authentication functions
def api_auth_required(view):
   
   #to set up the decorataror for API authentication (used before each API route)
   @wraps(view)
   def wrapped_view(**kwargs):
      #checks if the request has authorization headers
      if request.authorization is None:
         return jsonify({"error": "Authorization required"}), 401

      #sets the username and password from the request authorization
      username = request.authorization.username
      password = request.authorization.password

      #setting up the database
      db= get_db()

      #gathering the user information from the database based on the username from the request
      user = db.execute(
         'SELECT * FROM user WHERE username = ?',
         (username,)
      ).fetchone()

      #checking if username and password from the request exists in the database exists in the database
      if user is None:
         return jsonify({"error": "Invalid credentials"}), 401
      elif not check_password_hash(user["password"], password):
         return jsonify({"error": "Invalid credentials"}), 401
      
      #if the user is authenticated, set the user in the global context
      g.user = user
      return view(**kwargs)
   
   return wrapped_view
   

#api route functions
@bp.route('/books', methods=['GET'])
#to check if the user is authenticated before accessing the API route
@api_auth_required
def api_books():
   db= get_db()
   #to get all books from SQL database
   library = db.execute(
       'SELECT * FROM book WHERE user_id = ? ORDER BY id DESC',
       (g.user['id'],)
   ).fetchall()

   #to get all books in a language that can be converted to JSON
   book_list = [dict(book) for book in library]

   #returns the list of books in JSON format
   return jsonify(book_list)

@bp.route('/books/<int:id>', methods=['GET'])
@api_auth_required
#to check if the user is authenticated before accessing the API route
def api_view_book(id):

   db = get_db()
   
   #to get a book from the SQL database based on the book id
   book = db.execute(
       'SELECT * FROM book WHERE id = ? AND user_id = ?',
       (id, g.user['id'])
   ).fetchone()

   if book is None:
      #if the book does not exist, return a 404 error
      return jsonify({"error": "Book not found"}), 404

   #to get a book into a language that can be converted to JSON
   book_info = dict(book)

   #returns the book information in JSON format
   return jsonify(book_info)