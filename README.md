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

## � Docker Deployment (Recommended)

### Quick Docker Setup

1. **Ensure Docker is installed** on your system

2. **Clone and setup**:
   ```bash
   git clone <your-repo-url>
   cd petsittingsite
   cp .env.example .env
   # Edit .env with your configuration
   ```

3. **Deploy with Docker**:
   ```bash
   # Using the deployment script (Linux/Mac):
   ./docker-deploy.sh

   # Or manually:
   docker-compose build
   docker-compose up -d
   ```

4. **Initialize database**:
   ```bash
   docker-compose exec web python deploy.py init-db
   ```

5. **Access your application**:
   - **Local**: http://localhost
   - **Health check**: http://localhost/health

### Docker Commands

```bash
# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Rebuild after changes
docker-compose build --no-cache
docker-compose up -d

# Access container shell
docker-compose exec web bash
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