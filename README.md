# 🐱 Pet Sitting Website

A simple Flask web application for pet sitting services built with AI. Was used for a while in production but it's pretty much orphaned now.

## Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Initialize Database
```bash
python init_db.py
```

### 3. Run the Application
```bash
python run.py
```

### 4. Access the Website
Open your browser and go to: http://localhost:5000

## � Docker Deployment

### Quick Docker Setup

1. **Build and run**:
   ```bash
   docker-compose up --build
   ```

2. **Initialize database** (in another terminal):
   ```bash
   docker-compose exec web python docker-init-db.py
   ```

3. **Access the application**:
   - **Local**: http://localhost:5000
   - **Health check**: http://localhost:5000/health

### Docker Commands

```bash
# Start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild after changes
docker-compose up --build

# Initialize database
docker-compose exec web python docker-init-db.py
```

### Development with Docker

For development with live reload:
```bash
# Use the override file for development
docker-compose -f docker-compose.yml -f docker-compose.override.yml up --build
```

## �📁 Project Structure
```
petsittingsite/
├── app.py              # Main Flask application
├── run.py              # Simple run script
├── init_db.py          # Database initialization
├── requirements.txt    # Python dependencies
├── templates/          # HTML templates
├── static/            # CSS, JS, images
└── users.db           # SQLite database (created automatically)
```

## 🛠️ Development

- **Debug Mode**: Enabled by default
- **Database**: SQLite (users.db)
- **Port**: 5000
- **Admin User**: Created automatically on first run

## 🔧 Troubleshooting

If you get database errors:
```bash
# Delete the database and recreate
rm users.db
python init_db.py
```

## 📝 Features

- User registration and login
- Pet sitting booking system
- Admin panel for managing bookings
- Responsive design with Bootstrap
- SQLite database for data storage
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
