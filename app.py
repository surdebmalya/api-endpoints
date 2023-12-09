from flask import Flask, request, jsonify
from db import db, Book

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
db.init_app(app)

# Endpoint 1: Retrieve All Books
@app.route('/api/books', methods=['GET'])
def get_all_books():
    try:
        books = Book.query.all()
        book_list = []
        for book in books:
            book_list.append({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date})
        return jsonify({'books': book_list})
    except Exception as e:
        return jsonify({'error': str(e)}), 502

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        data = request.get_json()
        # Proper validation of the request payload
        try:
            temp = data['id']
            temp = data['title']
            temp = data['author']
            temp = data['published_date']
        except:
            return jsonify({'error': 'Payload error. In the payload you must have "id", "title", "title", "published_date"'}), 400
        
        # Appropriate handling of errors, such as duplicate book entries
        requested_books = Book.query.filter_by(title=data['title'])
        for requested_book in requested_books:
            if requested_book is not None and requested_book.id==data['id'] and requested_book.title==data['title'] and requested_book.author==data['author'] and requested_book.published_date==data['published_date']:
                return jsonify({'error': 'Book already in the database'}), 409

        # Correct insertion of the new book into the database (Checking primary key) 
        try:
            new_book = Book(id=data['id'], title=data['title'], author=data['author'], published_date=data['published_date'])
            db.session.add(new_book)
            db.session.commit()
            return jsonify({'message': 'Book added successfully'})
        except:
            return jsonify({'error': 'Book ID should be unique for each book!'}), 409
        
    except Exception as e:
        return jsonify({'error': str(e)}), 502

# Endpoint 3: Update Book Details
@app.route('/api/books/<string:id>', methods=['PUT'])
def update_book_details(id):
    try:
        book = Book.query.get(id)
        if book is None:
            return jsonify({'error': 'Book not found'}), 404

        data = request.get_json()
        book.title = data.get('title', book.title)
        book.author = data.get('author', book.author)
        book.published_date = data.get('published_date', book.published_date)

        db.session.commit()
        return jsonify({'message': 'Book updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 502

# Seed the database with mock data
@app.route('/seed', methods=['GET'])
def seed_database():
    try:
        # books_data = [
        #     {'id': 'book1', 'title': 'Book 1', 'author': 'Author 1', 'published_date': '2023-01-01'},
        #     {'id': 'book2', 'title': 'Book 2', 'author': 'Author 2', 'published_date': '2023-02-01'},
        #     {'id': 'book3', 'title': 'Book 3', 'author': 'Author 3', 'published_date': '2023-03-01'},
        # ]

        books_data = [{'id': 'book4', 'title': 'Book 3', 'author': 'Author 4', 'published_date': '2023-03-01'}]

        # checking for the duplication of the book id
        try:
            for book_data in books_data:
                new_book = Book(id=book_data['id'], title=book_data['title'], author=book_data['author'], published_date=book_data['published_date'])
                db.session.add(new_book)

            db.session.commit()
        except:
            return jsonify({'error': 'Book ID should be unique for each book!'}), 409
        
        return jsonify({'message': 'Database successfully seeded with mock data'})
    except Exception as e:
        return jsonify({'error': str(e)}), 502

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
