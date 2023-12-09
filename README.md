# Building Three API Endpoints with Database Interaction
Language used for backend development: Python (flask framework)

### API Codes used
- 200: OK
- 400: Bad request / Invalid argument (invalid request payload)
- 404: Not found
- 409: Conflict response status code indicates a request conflict with the current state of the target resource
- 502: Bad gateway

### Directory setting
```
project
    |- app.py
    |- db.py
    |- instance
    |   |- library.db
    |- problem_description.txt
    |- README.md
    |- images
        |- database_image.png
```

### Database structure
![Database architecture](images\database_image.png)

### Running the Application
Install Flask:
```
pip install Flask
```
Install Flask SQLAlchemy:
```
pip install Flask-SQLAlchemy
```
Run the application:
```
python app.py
```
The application will start running on `http://127.0.0.1:5000/`

### System Architecture To-do lists
```
GET /api/books
    |- Error handling for database connection issues [✓]
    |- Retrieval of all books from the database [✓]

POST /api/books
    |- Error handling for database connection issues [✓]
    |- Proper validation of the request payload [✓]
    |- Appropriate handling of errors, such as duplicate book entries [✓]
    |- Correct insertion of the new book into the database (Checking primary key) [✓]

PUT /api/books/<string:id>
    |- Error handling for database connection issues [✓]
    |- Correct identification and retrieval of the book from the database [✓]
    |- Handling errors, such as updating a non-existent book [✓]
    |- Proper validation of the request payload [✓]
    |- Updating the book details in the database with validity of the property (Checking primary key) [✓]

GET /seed
    |- Assumption: The payload structure will be followed
    |- Checking for the duplication of the book id
    |- Error handling for database connection issues
```

### Seeding the Database with Mock Data
To seed the database with mock data, I have added a separate route in the `app.py` file.

To to seed the database with mock data just send a request to `http://127.0.0.1:5000/seed`

### 