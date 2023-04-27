# from flask import Flask


# def create_app(test_config=None):
#     app = Flask(__name__)

#     # Register Blueprints here
#     from .routes import books_bp
#     app.register_blueprint(books_bp)

#     return app

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

db = SQLAlchemy()
migrate = Migrate()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

    db.init_app(app)
    migrate.init_app(app, db)

    # line below ensures Book model will be available to the app when we update database
    from app.models.book import Book
    from .routes import books_bp

    app.register_blueprint(books_bp)

    return app