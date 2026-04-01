from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

# Production configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///library.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ENGINE_OPTIONS'] = {
    'pool_pre_ping': True,
    'pool_recycle': 300,
}

# Security headers for production
@app.after_request
def add_security_headers(response):
    response.headers['X-Content-Type-Options'] = 'nosniff'
    response.headers['X-Frame-Options'] = 'DENY'
    response.headers['X-XSS-Protection'] = '1; mode=block'
    response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
    return response

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Initialize models
from models import init_models
User, Book, Borrow = init_models(db)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.before_request
def create_tables():
    if not hasattr(app, '_tables_created'):
        try:
            db.create_all()
            app._tables_created = True
            logger.info("Database tables created successfully")
        except Exception as e:
            logger.error(f"Error creating tables: {e}")


@app.route('/')
def index():
    try:
        books = Book.query.order_by(Book.title.asc()).all()
        borrows = {}
        if current_user.is_authenticated:
            user_borrows = Borrow.query.filter_by(user_id=current_user.id, returned=False).all()
            borrows = {b.book_id: b for b in user_borrows}
        return render_template('index.html', books=books, borrows=borrows)
    except Exception as e:
        logger.error(f"Error loading index page: {e}")
        flash('Error loading books. Please try again.', 'error')
        return render_template('index.html', books=[], borrows={})


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        try:
            name = request.form.get('name')
            email = request.form.get('email')
            password = request.form.get('password')
            role = request.form.get('role', 'User')

            if not name or not email or not password:
                flash('All fields are required.', 'error')
                return redirect(url_for('register'))

            if User.query.filter_by(email=email).first():
                flash('Email already registered.', 'error')
                return redirect(url_for('register'))

            hashed = generate_password_hash(password)
            user = User(name=name, email=email, password_hash=hashed, role=role)
            db.session.add(user)
            db.session.commit()
            flash('Registration successful. Please log in.', 'success')
            return redirect(url_for('login'))
        except Exception as e:
            logger.error(f"Error during registration: {e}")
            flash('Registration failed. Please try again.', 'error')
            return redirect(url_for('register'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        try:
            email = request.form.get('email')
            password = request.form.get('password')
            user = User.query.filter_by(email=email).first()
            if user and check_password_hash(user.password_hash, password):
                login_user(user)
                flash('Logged in successfully.', 'success')
                next_page = request.args.get('next')
                return redirect(next_page or url_for('index'))
            flash('Invalid credentials.', 'error')
        except Exception as e:
            logger.error(f"Error during login: {e}")
            flash('Login failed. Please try again.', 'error')
    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Logged out.', 'success')
    return redirect(url_for('index'))


def admin_required():
    if not current_user.is_authenticated or current_user.role != 'Admin':
        flash('Admin access required.', 'error')
        return False
    return True


@app.route('/admin')
@login_required
def admin_dashboard():
    if not admin_required():
        return redirect(url_for('index'))
    try:
        books = Book.query.order_by(Book.created_at.desc()).all()
        return render_template('admin/dashboard.html', books=books)
    except Exception as e:
        logger.error(f"Error loading admin dashboard: {e}")
        flash('Error loading dashboard.', 'error')
        return redirect(url_for('index'))


@app.route('/admin/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not admin_required():
        return redirect(url_for('index'))
    if request.method == 'POST':
        try:
            title = request.form.get('title')
            author = request.form.get('author')
            copies = request.form.get('copies', type=int)
            if not title or not author or copies is None:
                flash('All fields are required.', 'error')
                return redirect(url_for('add_book'))
            book = Book(title=title, author=author, total_copies=copies, available_copies=copies)
            db.session.add(book)
            db.session.commit()
            flash('Book added.', 'success')
            return redirect(url_for('admin_dashboard'))
        except Exception as e:
            logger.error(f"Error adding book: {e}")
            flash('Error adding book. Please try again.', 'error')
            return redirect(url_for('add_book'))
    return render_template('admin/add_book.html')


@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
    try:
        book = Book.query.get_or_404(book_id)
        if book.available_copies <= 0:
            flash('No copies available.', 'error')
            return redirect(url_for('index'))
        existing = Borrow.query.filter_by(user_id=current_user.id, book_id=book_id, returned=False).first()
        if existing:
            flash('You already borrowed this book.', 'error')
            return redirect(url_for('index'))
        borrow = Borrow(user_id=current_user.id, book_id=book_id)
        book.available_copies -= 1
        db.session.add(borrow)
        db.session.commit()
        flash('Book borrowed!', 'success')
    except Exception as e:
        logger.error(f"Error borrowing book: {e}")
        flash('Error borrowing book. Please try again.', 'error')
    return redirect(url_for('index'))


@app.route('/return/<int:book_id>', methods=['POST'])
@login_required
def return_book(book_id):
    try:
        borrow = Borrow.query.filter_by(user_id=current_user.id, book_id=book_id, returned=False).first()
        if not borrow:
            flash('No active borrow record found.', 'error')
            return redirect(url_for('index'))
        borrow.returned = True
        book = Book.query.get(book_id)
        if book:
            book.available_copies += 1
        db.session.commit()
        flash('Book returned. Thank you!', 'success')
    except Exception as e:
        logger.error(f"Error returning book: {e}")
        flash('Error returning book. Please try again.', 'error')
    return redirect(url_for('index'))


# Health check endpoint for deployment platforms
@app.route('/health')
def health_check():
    return {'status': 'healthy', 'message': 'Library Management System is running'}

# Error handlers
@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html'), 500

if __name__ == '__main__':
    # Use production settings when not in debug mode
    if os.environ.get('FLASK_ENV') == 'production':
        app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)), debug=False)
    else:
        app.run(host='0.0.0.0', port=5000, debug=True)
