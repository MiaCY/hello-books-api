from pydoc import describe
from app import db
from app.models.book import Book
from flask import Blueprint, jsonify, abort, make_response, request


# class Book:
#     def __init__(self, id, title, description):
#         self.id = id
#         self.title = title
#         self.description = description

# books = [
#     Book(1, "Fictional Book Title", "A fantacy novel set in an imaginary world."),
#     Book(2, "Fictional Book Title", "A fantacy novel set in an imaginary world."),
#     Book(3, "Fictional Book Title", "A fantacy novel set in an imaginary world.")
# ]

# @books_bp.route("", methods=["GET"])
# def handle_books():
#     books_response = []
#     for book in books:
#         books_response.append({
#             "id": book.id,
#             "title": book.title,
#             "description": book.description
#         })
#     return jsonify(books_response)

# def validate_book(book_id):
#     try:
#         book_id = int(book_id)
#     except:
#         abort(make_response({"message": f"book {book_id} invalid"}, 400))
    
#     for book in books:
#         if book.id == book_id:
#             return book
    
#     abort(make_response({"message": f"book {book_id} not found"}, 404))

# @books_bp.route("/<book_id>", methods = ["GET"])
# def handle_book(book_id):   
#     book = validate_book(book_id)
    
#     return dict(
#         id = book.id,
#         title = book.title,
#         description = book.description
#     )

books_bp = Blueprint("books", __name__, url_prefix = "/books")

@books_bp.route("", methods=["POST"])
def create_book():
    request_body = request.get_json()
    new_book = Book(
        title = request_body["title"],
        description = request_body["description"]
    )

    db.session.add(new_book)
    db.session.commit()

    return make_response(jsonify(f"Book {new_book.title} successfully created"),201)

@books_bp.route("", methods=["GET"])
def read_all_books():
    book_response = []
    books = Book.query.all()
    for book in books:
        book_response.append(
            {
                "id": book.id,
                "title": book.title,
                "description": book.description
            }
        )
    return jsonify(book_response)

def validate_book(book_id):
    try:
        book_id = int(book_id)
    except:
        abort(make_response({"message": f"book {book_id} invalid"}, 400))

    book = Book.query.get(book_id)

    if not book:
        abort(make_response({"message": f"book {book_id} not found"}, 404))

    return book

@books_bp.route("/<book_id>", methods=["GET"])
def read_one_book(book_id):
    book = validate_book(book_id)
    return dict(
        id = book.id,
        title = book.title,
        description = book.description
    )

@books_bp.route("/<book_id>", methods=["PUT"])
def update_book(book_id):
    book = validate_book(book_id)

    request_body = request.get_json()

    book.title = request_body["title"]
    book.desciprtion = request_body["description"]

    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully updated"))

@books_bp.route("/<book_id>", methods=["DELETE"])
def delete_book(book_id):
    book = validate_book(book_id)

    db.session.delete(book)
    db.session.commit()

    return make_response(jsonify(f"Book #{book_id} successfully deleted"))