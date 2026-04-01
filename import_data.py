import csv
import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash

# Create Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = 'import-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Define models directly to avoid conflicts
from flask_login import UserMixin
from datetime import datetime

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

def import_books_from_csv(csv_file='books_dataset.csv'):
    """Import books from CSV file into the database"""
    
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if books already exist
        existing_books = Book.query.count()
        if existing_books > 0:
            print(f"Database already has {existing_books} books. Skipping import.")
            return
        
        # Read and import books from CSV
        books_imported = 0
        with open(csv_file, 'r', encoding='utf-8') as file:
            reader = csv.DictReader(file)
            for row in reader:
                book = Book(
                    title=row['title'],
                    author=row['author'],
                    total_copies=int(row['total_copies']),
                    available_copies=int(row['available_copies'])
                )
                db.session.add(book)
                books_imported += 1
                
                # Print progress
                if books_imported % 10 == 0:
                    print(f"Imported {books_imported} books...")
        
        # Commit all changes
        db.session.commit()
        print(f"Successfully imported {books_imported} books into the database!")

def create_sample_users():
    """Create sample users for demonstration"""
    
    with app.app_context():
        # Check if users already exist
        existing_users = User.query.count()
        if existing_users > 0:
            print(f"Database already has {existing_users} users. Skipping user creation.")
            return
        
        # Create sample users
        from werkzeug.security import generate_password_hash
        
        users = [
            {
                'name': 'Admin User',
                'email': 'admin@library.com',
                'password': 'admin123',
                'role': 'Admin'
            },
            {
                'name': 'John Student',
                'email': 'john@student.com',
                'password': 'student123',
                'role': 'User'
            },
            {
                'name': 'Jane Faculty',
                'email': 'jane@faculty.com',
                'password': 'faculty123',
                'role': 'User'
            }
        ]
        
        for user_data in users:
            user = User(
                name=user_data['name'],
                email=user_data['email'],
                password_hash=generate_password_hash(user_data['password']),
                role=user_data['role']
            )
            db.session.add(user)
        
        db.session.commit()
        print("Created sample users:")
        print("  Admin: admin@library.com / admin123")
        print("  Student: john@student.com / student123")
        print("  Faculty: jane@faculty.com / faculty123")

if __name__ == '__main__':
    print("Starting data import...")
    
    # Import books
    import_books_from_csv()
    
    # Create sample users
    create_sample_users()
    
    print("Data import completed!")
