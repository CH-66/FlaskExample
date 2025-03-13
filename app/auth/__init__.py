from .routes import auth

def init_app(app):
    app.register_blueprint(auth, url_prefix='/auth')
