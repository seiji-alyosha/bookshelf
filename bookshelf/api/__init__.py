from flask import Blueprint
from . import auth, books

bp = Blueprint('api',__name__, url_prefix='/api')