# 🐱 Pet Sitting Website

A comprehensive web application for pet sitting services built with Flask, featuring user authentication, booking management, animal profiles, and an admin panel.

## ✨ Features

- **User Authentication**: Secure login/registration system
- **Animal Profiles**: Manage detailed profiles for all pet types (dogs, cats, birds, etc.)
- **Booking System**: Easy booking with animal selection and pricing
- **Admin Panel**: Complete booking management with status updates and notes
- **Responsive Design**: Modern dark theme with Bootstrap 5
- **Database**: SQLite with SQLAlchemy ORM
- **Security**: Password hashing, session management, and CSRF protection

## 🚀 Quick Start

### Prerequisites
- Python 3.8 or higher
- Git

### Installation

1. **Clone the repository**
   ```bash
   git clone <your-repo-url>
   cd petsittingsite
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows:
   venv\Scripts\activate
   # macOS/Linux:
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup environment**
   ```bash
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Initialize database**
   ```bash
   python deploy.py init-db
   ```

6. **Run the application**
   ```bash
   python deploy.py dev
   ```

7. **Open in browser**
   ```
   http://localhost:5000
   ```

## 📁 Project Structure

```
petsittingsite/
├── app.py                 # Main Flask application
├── deploy.py             # Deployment script
├── migrate_db.py         # Database migration utilities
├── requirements.txt      # Python dependencies
├── .env.example          # Environment variables template
├── Procfile             # Heroku deployment configuration
├── runtime.txt          # Python version for Heroku
├── DEPLOYMENT.md        # Comprehensive deployment guide
├── .gitignore           # Git ignore rules
├── static/
│   ├── style.css        # Custom CSS styling
│   └── ...              # Static assets
└── templates/
    ├── base.html        # Base template
    ├── home.html        # Homepage
    ├── book.html        # Booking form
    ├── admin_bookings.html  # Admin booking management
    ├── my_bookings.html     # User booking history
    ├── my_animals.html      # Animal profile management
    └── ...               # Other templates
```

## 🛠️ Development Commands

```bash
# Initialize database
python deploy.py init-db

# Run development server
python deploy.py dev

# Run production server
python deploy.py prod

# Manual database migration
python migrate_db.py
```

## 🌐 Deployment

See [DEPLOYMENT.md](DEPLOYMENT.md) for comprehensive deployment instructions including:

- **Heroku** (easiest option)
- **DigitalOcean App Platform**
- **AWS EC2**
- **Docker deployment**
- **Local production setup**

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key (required)
- `FLASK_ENV`: Environment (development/production)
- `SQLALCHEMY_DATABASE_URI`: Database connection string
- `BASE_HOURLY_RATE`: Default hourly rate for services

### Database
- **Development**: SQLite (users.db)
- **Production**: PostgreSQL recommended

## 📊 Features Overview

### For Users
- Register/login with secure authentication
- Create and manage animal profiles
- Book pet sitting services with animal selection
- View booking history and status
- Cancel bookings (non-completed only)

### For Admins
- View all bookings with filtering
- Update booking status (pending → approved → in progress → completed)
- Add admin notes to bookings
- Delete bookings (with confirmation)
- View detailed animal information via clickable pet names

### Animal Management
- Support for all pet types (dogs, cats, birds, etc.)
- Detailed profiles with breed, age, special needs
- Medical information and behavior notes
- Photo uploads (future enhancement)

## 🛡️ Security Features

- **Password Hashing**: Werkzeug security for password storage
- **Session Management**: Flask-Login for user sessions
- **CSRF Protection**: Built-in Flask-WTF protection
- **Input Validation**: Form validation and sanitization
- **SQL Injection Prevention**: SQLAlchemy ORM protection

## 🎨 Design

- **Dark Theme**: Modern dark color scheme
- **Responsive**: Mobile-friendly Bootstrap 5
- **Interactive**: Modal dialogs, status badges, hover effects
- **Accessible**: High contrast ratios and semantic HTML

## 📝 API Endpoints

- `GET /` - Homepage
- `GET/POST /login` - User login
- `GET/POST /register` - User registration
- `GET /logout` - User logout
- `GET/POST /book` - Create booking
- `GET /my-bookings` - User bookings
- `GET /admin/bookings` - Admin booking management
- `POST /update-booking/<id>` - Update booking status
- `POST /delete-booking/<id>` - Delete booking
- `GET/POST /my-animals` - Animal profile management
- `GET /view-animal/<id>` - View animal details

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📄 License

This project is open source. Please check the license file for details.

## 🆘 Support

For issues or questions:
1. Check the [DEPLOYMENT.md](DEPLOYMENT.md) for common problems
2. Review the code comments for implementation details
3. Create an issue in the repository

---

**Happy coding! 🐕🐱🐦**