# code below handles development AND test modes
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

db = SQLAlchemy()
migrate = Migrate()
load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__)

    if not test_config:
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
            "SQLALCHEMY_DATABASE_URI")
    else:
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
        app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
            "SQLALCHEMY_TEST_DATABASE_URI")

    # Import models here
    from app.models.book import Book
    from app.models.author import Author

    db.init_app(app)
    migrate.init_app(app, db)

    # Register Blueprints here
    from .routes import books_bp
    app.register_blueprint(books_bp)

    from .routes import authors_bp
    app.register_blueprint(authors_bp)

    return app



# ######### WORKING BEFORE AUTHOR #########
# def create_app(test_config=None):
#     app = Flask(__name__)

#     if not test_config:
#         app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#         app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
#             "SQLALCHEMY_DATABASE_URI")
#     else:
#         app.config["TESTING"] = True
#         app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
#         app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get(
#             "SQLALCHEMY_TEST_DATABASE_URI")

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # Register Blueprints here
#     from app.models.book import Book

#     from .routes import books_bp
#     app.register_blueprint(books_bp)

#     return app







# # code below only handles development mode
# from flask import Flask
# from flask_sqlalchemy import SQLAlchemy
# from flask_migrate import Migrate

# db = SQLAlchemy()
# migrate = Migrate()


# def create_app(test_config=None):
#     app = Flask(__name__)

#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://postgres:postgres@localhost:5432/hello_books_development'

#     db.init_app(app)
#     migrate.init_app(app, db)

#     # line below ensures Book model will be available to the app when we update database
#     from app.models.book import Book
#     from .routes import books_bp

#     app.register_blueprint(books_bp)

#     return app