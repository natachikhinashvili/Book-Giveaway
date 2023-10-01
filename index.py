from flask import jsonify, request, flash, Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from usermodel import app, User, bcrypt, db, Book


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/login', methods=['GET'])
def auth():
    user_email = request.args.get('email')
    user_password = request.args.get('password')

    user = User.query.filter_by(email=user_email).first()

    if user and bcrypt.check_password_hash(user.password, user_password):
        return jsonify({"message": "Authentication successful"})
    else:
        return jsonify({"message": "Authentication failed"}), 401
    
@app.route('/register', methods=['POST'])
def register():
    if request.method == 'POST':
        user_email = request.form.get('email')
        user_password = request.form.get('password')

        existing_user = User.query.filter_by(email=user_email).first()
        if existing_user:
            return jsonify({"message": "User already exists"}), 400

        hashed_password = bcrypt.generate_password_hash(user_password).decode('utf-8')
        new_user = User(email=user_email, password=hashed_password)

        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Registration successful"}), 201
    
@app.route('/add_book', methods=['POST'])
def add_book():
    if request.method == 'POST':
        title = request.form.get('title')
        author = request.form.get('author')
        genre = request.form.get('genre')
        user_id = request.form.get('user_id')

        user = User.query.get(user_id)
        if user is None:
            return jsonify({"message": "User not found"}), 404

        new_book = Book(title=title, author=author, genre=genre, user_id=user_id)

        db.session.add(new_book)
        db.session.commit()

        return jsonify({"message": "Book added successfully"}), 201
@app.route('/books', methods=['GET'])
def books():
    if request.method == 'GET':
        books = Book.query.all()

        book_list = []
        for book in books:
            book_data = {
                'id': book.id,
                'title': book.title,
                'author': book.author,
                'genre': book.genre,
                'user_id': book.user_id
            }
            book_list.append(book_data)

        return jsonify({'books': book_list})
    
@app.route('/add_interest', methods=['POST'])
def add_interest():
    if request.method == 'POST':
        book_id = request.form.get('book_id')
        recepient = request.form.get('recepient')

        book = Book.query.get(book_id)
        if book is None:
            return jsonify({"message": "Book not found"}), 404

        if book.title not in recepient.interests:
            recepient.interests.append(book.title)

        book.user_id = recepient.id
        db.session.commit()
        return jsonify({"message": "Ownership changed successfully"}), 200

@app.route('/request_interest', methods=['POST'])
def request_interest():
    if request.method == 'POST':
        client_user_id = request.form.get('client_user_id')
        book_title = request.form.get('book_title')

        client_user = User.query.get(client_user_id)
        if client_user is None:
            return jsonify({"message": "Client user not found"}), 404
        
        url = 'http://localhost:5000/add_interest'
        book = Book.query.filter_by(title=book_title).first()
        recepient = Book.query.filter_by(id=client_user_id).first()
        request.post(url, data={"book_id": book.id, "recepient": recepient})
        
        return jsonify({"message": "Request sent to owner"}), 200

if __name__ == '__main__':
    app.run(debug=True)