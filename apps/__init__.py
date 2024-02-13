import os

from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from importlib import import_module

db = SQLAlchemy()
login_manager = LoginManager()

def register_extensions(app):
    db.init_app(app)
    login_manager.init_app(app)

def register_blueprints(app):
    for module_name in ('authentication', 'home', 'assets', 'area', 'leases', ):
        module = import_module('apps.{}.routes'.format(module_name))
        app.register_blueprint(module.blueprint)

def configure_database(app):

    @app.before_request
    def initialize_database():
        try:
            db.create_all()
        except Exception as e:
            print('> Error: DBMS Exception: ' + str(e))
            # fallback to SQLite
            basedir = os.path.abspath(os.path.dirname(__file__))
            app.config['SQLALCHEMY_DATABASE_URI'] = SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'db.sqlite3')
            print('> Fallback to SQLite ')
            db.create_all()

    @app.teardown_request
    def shutdown_session(exception=None):
        db.session.remove()

def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    # Initialize Flask-Login
    login_manager.init_app(app)

    # Define the user_loader and request_loader functions
    from apps.authentication.models import Users
    @login_manager.user_loader
    def load_user(user_id):
        return Users.query.get(int(user_id))

    @login_manager.request_loader
    def load_user_from_request(request):
        auth_token = request.headers.get('Authorization')
        if auth_token:
            user = Users.verify_auth_token(auth_token)
            if user:
                return user
        return None

    register_extensions(app)
    register_blueprints(app)
    configure_database(app)
    return app
