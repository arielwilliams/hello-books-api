from flask import Blueprint, jsonify, abort, make_response, request
from app import db
from app.models.book import Book
from app.models.author import Author

# Blueprints for books and authors 
books_bp = Blueprint("books", __name__, url_prefix="/books")
authors_bp = Blueprint("authors_bp", __name__, url_prefix="/authors")

####### helper functions here #######
# helper function to validate any model
# currently being used to validate book model in read, update, and delete functions

def validate_model(cls, model_id):
    try:
        model_id = int(model_id)
    except:
        abort(make_response({"message":f"{cls.__name__} {model_id} invalid"}, 400))

    model = cls.query.get(model_id)

    if not model:
        abort(make_response({"message":f"{cls.__name__} {model_id} not found"}, 404))

    return model

###############################################################################

# Routes for book here 

# refactored function to create new book
@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book.from_dict(request_body)

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"), 201)


# refactored reads/gets all books to include query param title 
# uses helper function to_dict() from book.py
@books_bp.route("", methods=["GET"])
def read_all_books():
    title_query = request.args.get("title")
    if title_query:
        books = Book.query.filter_by(title=title_query)
    else:
        books = Book.query.all()

    books_response = []
    for book in books:
        books_response.append(book.to_dict())
    return jsonify(books_response), 200


# reads/gets specific existing book, if it does not exist returns 400 or 404
# uses helper function to_dict() from book.py
@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_model(Book, book_id)
    return book.to_dict(), 200 


# puts/updates specific existing book, if it does not exist returns 400 or 404
@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_model(Book, book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.description = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully updated"), 200)


# deletes specific existing book, if it does not exist returns 400 or 404
@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_model(Book, book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book.id} successfully deleted"), 200)

################################################################################
# Routes for author here 

@authors_bp.route("", methods=["POST"])
def create_author():
    request_body = request.get_json()
    new_author = Author(name=request_body["name"],)

    db.session.add(new_author)
    db.session.commit()

    return make_response(jsonify(f"Author {new_author.name} successfully created"), 201)

@authors_bp.route("", methods=["GET"])
def read_all_authors():
    
    authors = Author.query.all()

    authors_response = []
    for author in authors:
        authors_response.append(
            {
                "name": author.name
            }
        )
    return jsonify(authors_response)