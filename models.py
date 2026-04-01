from flask_login import UserMixin
from datetime import datetime


def init_models(db):
    class User(UserMixin, db.Model):
        id = db.Column(db.Integer, primary_key=True)
        name = db.Column(db.String(120), nullable=False)
        email = db.Column(db.String(120), unique=True, nullable=False)
        password_hash = db.Column(db.String(255), nullable=False)
        role = db.Column(db.String(20), default='User')
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

        def get_id(self):
            return str(self.id)

    class Book(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        title = db.Column(db.String(200), nullable=False)
        author = db.Column(db.String(200), nullable=False)
        total_copies = db.Column(db.Integer, nullable=False, default=1)
        available_copies = db.Column(db.Integer, nullable=False, default=1)
        created_at = db.Column(db.DateTime, default=datetime.utcnow)

    class Borrow(db.Model):
        id = db.Column(db.Integer, primary_key=True)
        user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
        book_id = db.Column(db.Integer, db.ForeignKey('book.id'), nullable=False)
        borrowed_at = db.Column(db.DateTime, default=datetime.utcnow)
        returned = db.Column(db.Boolean, default=False)

        user = db.relationship('User', backref=db.backref('borrows', lazy=True))
        book = db.relationship('Book', backref=db.backref('borrows', lazy=True))

    return User, Book, Borrow
