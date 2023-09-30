from flask import jsonify, request, flash, Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from usermodel import app, User, bcrypt, db


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

    
if __name__ == '__main__':
    app.run(debug=True)