
from flask import Blueprint, jsonify, abort, make_response

class Book:
    def __init__(self, id, title, description):
        self.id = id
        self.title = title
        self.description = description

books = [
    Book(1, "Fictional Book", "A fantasy novel set in an imaginary world."),
    Book(2, "Wheel of Time", "A fantasy novel set in an imaginary world."),
    Book(3, "Fictional Book Title", "A fantasy novel set in an imaginary world.")
]

books_bp = Blueprint("books_bp", __name__, url_prefix="/books")

# func gets all books as a list of dicts where each book is a dict
@books_bp.route("", methods=["GET"])
def handle_books():
    books_response = []
    for book in books:
        books_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return jsonify(books_response)

###### Note: refactored version below #######
# # Does all 3 of these things: grabs 1 book dict, 
# # handles non-existent book w/ 404, & string that can't be transformed
# # into an int w/ 400
# # if if check evaluates to False, func returns None     
# @books_bp.route("/<book_id>", methods=["GET"])
# def handle_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         return {"message":f"book {book_id} invalid"}, 400
    
#     # book_id = int(book_id)
#     for book in books:
#         if book.id == book_id:
#             return jsonify({
#                 "id": book.id,
#                 "title": book.title,
#                 "description": book.description,
#             })
        
#     return {"message":f"book {book_id} not found"}, 404


### Refactored function from above by using helper function ###

# helper function for error handling logic that will be used later
# validate_book helper func: 1. handles non-existing book, 2. handles invalid book_id
def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message":f"book {book_id} invalid"}, 400))

    for book in books:
        if book.id == book_id:
            return book

    abort(make_response({"message":f"book {book_id} not found"}, 404))

# Refactored handle_book(book_id) func 
@books_bp.route("/<book_id>", methods=["GET"])
def handle_book(book_id):
    book = validate_book(book_id)

    return {
        "id": book.id,
        "title": book.title,
        "description": book.description,
    }
