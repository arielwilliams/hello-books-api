from flask import Flask


def create_app(test_config=None):
    app = Flask(__name__)

    # Register Blueprints here
    # Blueprint for hello_word_bp
    from .routes import hello_world_bp
    app.register_blueprint(hello_world_bp)
    # Blueprint for books_bp
    from .routes import books_bp
    app.register_blueprint(books_bp)

    return app

