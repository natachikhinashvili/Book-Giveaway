from flask import jsonify, request, flash, Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from usermodel import app, User, bcrypt


@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/auth', methods=['GET'])
def auth():
    user_email = request.args.get('email')
    user_password = request.args.get('password')

    user = User.query.filter_by(email=user_email).first()

    if user and bcrypt.check_password_hash(user.password, user_password):
        return jsonify({"message": "Authentication successful"})
    else:
        return jsonify({"message": "Authentication failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)