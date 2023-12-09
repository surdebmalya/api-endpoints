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
        # Correct retrieval of all books from the database
        book_list = []
        for book in books:
            book_list.append({'id': book.id, 'title': book.title, 'author': book.author, 'published_date': book.published_date})
        return jsonify({'books': book_list})
    except Exception as e:
        # Proper error handling for database connection issues
        return jsonify({'error': str(e)}), 502

# Endpoint 2: Add a New Book
@app.route('/api/books', methods=['POST'])
def add_new_book():
    try:
        data = request.get_json()
        # Proper validation of the request payload
        if ('id' in list(data.keys())) and ('title' in list(data.keys())) and ('author' in list(data.keys())) and ('published_date' in list(data.keys())):
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
        else:
            return jsonify({'error': 'Payload error. In the payload you must have "id", "title", "title", "published_date"'}), 400
    except Exception as e:
        # Proper error handling for database connection issues
        return jsonify({'error': str(e)}), 502

# Endpoint 3: Update Book Details
@app.route('/api/books/<string:id>', methods=['PUT'])
def update_book_details(id):
    try:
        book = Book.query.get(id)
        
        # Correct identification and retrieval of the book from the database
        # Handling errors, such as updating a non-existent book
        if book is None:
            return jsonify({'error': 'Book not found'}), 404

        data = request.get_json()

        # Proper validation of the request payload
        if ('id' in list(data.keys())) or ('title' in list(data.keys())) or ('author' in list(data.keys())) or ('published_date' in list(data.keys())):
            try:
                newID = data['id']
            except:
                newID = book.id
            try:
                newTitle = data['title']
            except:
                newTitle = book.title
            try:
                newAuthor = data['author']
            except:
                newAuthor = book.author
            try:
                newDate = data['published_date']
            except:
                newDate = book.published_date
        else:
            return jsonify({'error': 'Payload error. In the payload you must have "id", "title", "author", "published_date"'}), 400

        # Updating the book details in the database with validity of the property (Checking primary key)
        try:
            book.id = data.get('id', newID)
            book.title = data.get('title', newTitle)
            book.author = data.get('author', newAuthor)
            book.published_date = data.get('published_date', newDate)

            db.session.commit()
            return jsonify({'message': 'Book updated successfully'})
        except:
            return jsonify({'error': 'Book ID should be unique for each book!'}), 409
    except Exception as e:
        # Proper error handling for database connection issues
        return jsonify({'error': str(e)}), 502

# Seed the database with mock data
@app.route('/seed', methods=['GET'])
def seed_database():
    try:
        books_data = [
            {'id': 'B1', 'title': 'Book 1', 'author': 'Author 1', 'published_date': '2023-01-01'},
            {'id': 'B2', 'title': 'Book 2', 'author': 'Author 2', 'published_date': '2023-02-01'},
            {'id': 'B3', 'title': 'Book 3', 'author': 'Author 3', 'published_date': '2023-03-01'},
        ]

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
