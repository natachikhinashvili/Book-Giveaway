from flask import Flask
from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://app_user:app_password@localhost/bookapi'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False) 
    interests = db.Column(db.JSON) 
    books = db.relationship('Book', backref='owner', lazy=True)

    def __init__(self, email, password, interests=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')
        self.interests = interests

    def __repr__(self):
        return f"User(email='{self.email}', interests='{self.interests}')"

class Book(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=True) 
    genre = db.Column(db.String(255), nullable=True) 
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __init__(self, title, user_id):
        self.title = title
        self.user_id = user_id

    def __repr__(self):
        return f"Book(title='{self.title}')"