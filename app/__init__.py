# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_pyfile('config.py')
    
    db.init_app(app)

    with app.app_context():
        from . import routes
        from .scheduler import setup_scheduler
        db.create_all()
        setup_scheduler()

    return app
