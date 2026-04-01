from flask import Flask, render_template, redirect, url_for, request, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key')
# Use SQLite for easier demo
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///library.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
        db.create_all()
        app._tables_created = True


@app.route('/')
def index():
    books = Book.query.order_by(Book.title.asc()).all()
    borrows = {}
    if current_user.is_authenticated:
        user_borrows = Borrow.query.filter_by(user_id=current_user.id, returned=False).all()
        borrows = {b.book_id: b for b in user_borrows}
    return render_template('index.html', books=books, borrows=borrows)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
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

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password_hash, password):
            login_user(user)
            flash('Logged in successfully.', 'success')
            next_page = request.args.get('next')
            return redirect(next_page or url_for('index'))
        flash('Invalid credentials.', 'error')
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
    books = Book.query.order_by(Book.created_at.desc()).all()
    return render_template('admin/dashboard.html', books=books)


@app.route('/admin/books/add', methods=['GET', 'POST'])
@login_required
def add_book():
    if not admin_required():
        return redirect(url_for('index'))
    if request.method == 'POST':
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
    return render_template('admin/add_book.html')


@app.route('/borrow/<int:book_id>', methods=['POST'])
@login_required
def borrow_book(book_id):
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
    return redirect(url_for('index'))


@app.route('/return/<int:book_id>', methods=['POST'])
@login_required
def return_book(book_id):
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
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
