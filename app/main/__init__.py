from flask import Blueprint

bp = Blueprint('main', __name__)

from app.main import routes

def init_app(app):
    app.register_blueprint(bp) 