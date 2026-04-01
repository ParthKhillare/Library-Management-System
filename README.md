# Library Management System 📚

A complete, production-ready Library Management System built with Flask and MySQL/SQLite. Perfect for libraries, schools, and educational institutions! 

## ✨ Features

- **🔐 User Authentication**: Secure registration, login, logout with role-based access
- **👥 Role Management**: Admin and User roles with different permissions
- **📚 Book Management**: Add, view, and manage books with copy tracking
- **📖 Borrow/Return System**: Complete book borrowing and returning workflow
- **🎨 Modern UI**: Clean, responsive design with Jinja2 templates
- **💾 Database Support**: MySQL for production, SQLite for development
- **📊 Sample Data**: Pre-loaded with 50+ books from various genres
- **🐳 Docker Ready**: Full containerization support
- **🚀 Production Ready**: Environment variables, health checks, and deployment scripts

## 🏗️ Project Structure

```
Library-Management-System/
├── app.py                 # Main Flask application (MySQL version)
├── app_sqlite.py          # Flask application (SQLite version)
├── models.py              # SQLAlchemy models
├── requirements.txt       # Python dependencies
├── import_data.py         # Data import script
├── generate_dataset.py    # Sample data generator
├── books_dataset.csv      # Sample books data
├── Dockerfile             # Docker configuration
├── docker-compose.yml     # Docker Compose setup
├── deploy.sh / deploy.bat # Deployment scripts
├── .env.example           # Environment template
├── .gitignore             # Git ignore file
├── static/
│   └── style.css         # Modern CSS styling
└── templates/
    ├── base.html         # Base template
    ├── index.html        # Book listing
    ├── login.html        # User login
    ├── register.html     # User registration
    └── admin/
        ├── dashboard.html # Admin dashboard
        └── add_book.html  # Add book form
```

## 🛠️ Tech Stack

- **Backend**: Flask, Flask-SQLAlchemy, Flask-Login
- **Database**: MySQL (production), SQLite (development)
- **Authentication**: Werkzeug password hashing
- **Frontend**: Jinja2 templates, modern CSS
- **Deployment**: Docker, Docker Compose
- **Python**: 3.11+

## 🚀 Quick Start

### Option 1: Local Development (SQLite)

1. **Clone and setup**:
   ```bash
   git clone <repository-url>
   cd Library-Management-System
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   # or
   venv\Scripts\Activate.ps1  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Import sample data**:
   ```bash
   python import_data.py
   ```

5. **Run the application**:
   ```bash
   python app_sqlite.py
   ```

6. **Open** http://localhost:5000

### Option 2: Docker Deployment (Production)

1. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with your settings
   ```

2. **Deploy with script**:
   ```bash
   # Linux/Mac
   chmod +x deploy.sh
   ./deploy.sh
   
   # Windows
   deploy.bat
   ```

3. **Access** http://localhost:5000

### Option 3: Manual Docker

1. **Build and run**:
   ```bash
   docker-compose build
   docker-compose up -d
   ```

2. **Import data**:
   ```bash
   docker-compose run --rm web python import_data.py
   ```

## 👤 Default Users

After importing data, you can login with:

- **Admin**: `admin@library.com` / `admin123`
- **Student**: `john@student.com` / `student123`  
- **Faculty**: `jane@faculty.com` / `faculty123`

## 📊 Sample Data

The system comes pre-loaded with:
- **50+ Books** across various genres (Fiction, Science, Biography, etc.)
- **Classic Literature** and modern titles
- **Realistic copy counts** and availability
- **Sample users** for testing

## 🔧 Configuration

### Environment Variables

```bash
# Required
SECRET_KEY=your-very-secure-secret-key
DATABASE_URL=sqlite:///library.db  # or mysql+pymysql://...

# Optional
FLASK_ENV=production
DEBUG=False
PORT=5000
HOST=0.0.0.0
```

### MySQL Setup (Optional)

1. **Create database**:
   ```sql
   CREATE DATABASE library_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
   ```

2. **Update .env**:
   ```bash
   DATABASE_URL=mysql+pymysql://user:password@localhost/library_db
   ```

3. **Run MySQL version**:
   ```bash
   python app.py
   ```

## 🐳 Docker Deployment

### Production with SQLite
```bash
docker-compose up -d
```

### Production with MySQL
Uncomment the MySQL section in `docker-compose.yml` and configure the environment variables.

### Health Checks
The Docker container includes health checks that monitor the application status.

## 📱 Features in Detail

### Admin Features
- ✅ Add new books to the library
- ✅ View all books and their availability
- ✅ Track borrowed books
- ✅ Manage user access

### User Features  
- ✅ Register new accounts
- ✅ Browse available books
- ✅ Borrow available books
- ✅ Return borrowed books
- ✅ View borrowing history

### System Features
- ✅ Automatic availability tracking
- ✅ Duplicate book prevention
- ✅ Secure password storage
- ✅ Session management
- ✅ Error handling and validation

## 🔒 Security Features

- **Password Hashing**: Uses Werkzeug's secure password hashing
- **Session Management**: Flask-Login handles secure sessions
- **Role-Based Access**: Admin-only routes protected
- **CSRF Protection**: Built-in Flask CSRF protection
- **Input Validation**: Form validation and sanitization

## 📈 Performance & Monitoring

- **Health Checks**: Docker health monitoring
- **Error Logging**: Comprehensive error handling
- **Database Optimization**: Efficient queries with SQLAlchemy
- **Static File Caching**: Optimized CSS delivery

## 🔄 Future Enhancements

- **Book Search & Filtering**: Advanced search capabilities
- **Due Dates & Fines**: Automated due date tracking
- **User Profiles**: Enhanced user management
- **Email Notifications**: Borrowing reminders
- **REST API**: Mobile app support
- **Analytics**: Usage statistics and reports
- **Multi-language Support**: Internationalization

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🆘 Troubleshooting

### Common Issues

**Q: Database connection errors**
A: Check your DATABASE_URL in .env file and ensure MySQL/SQLite is accessible.

**Q: Docker build fails**
A: Ensure Docker is running and you have sufficient disk space.

**Q: Port 5000 is in use**
A: Change the port mapping in docker-compose.yml or app configuration.

**Q: Sample data not importing**
A: Run `python import_data.py` manually to check for errors.

### Getting Help

- Check the logs: `docker-compose logs -f`
- Review environment variables in .env
- Ensure all dependencies are installed
- Verify database connectivity

## 📞 Support

For issues and questions:
- Create an issue on GitHub
- Check the troubleshooting section
- Review the documentation

---

**Happy Library Management! 📚✨**
