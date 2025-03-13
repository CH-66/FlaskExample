

from flask import Blueprint
bp = Blueprint('errors', __name__)

from app.errors import handlers

def init_app(app):
    app.register_blueprint(bp)