# 🚀 Pet Sitting Website - Deployment Guide

## 📋 Prerequisites

- Python 3.8 or higher
- Git
- A server/cloud platform (Heroku, AWS, DigitalOcean, etc.)

## 🛠️ Local Development Setup

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd petsittingsite
```

### 2. Create Virtual Environment
```bash
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Environment Configuration
```bash
cp .env.example .env
# Edit .env with your actual values
```

### 5. Initialize Database
```bash
python deploy.py init-db
```

### 6. Run Development Server
```bash
python deploy.py dev
# Or directly:
python app.py
```

## 🌐 Production Deployment Options

### Option 1: Heroku (Easiest)

#### 1. Install Heroku CLI
```bash
# Download from: https://devcenter.heroku.com/articles/heroku-cli
```

#### 2. Create Heroku App
```bash
heroku create your-app-name
```

#### 3. Configure Environment Variables
```bash
heroku config:set SECRET_KEY=your-super-secret-key-here
heroku config:set FLASK_ENV=production
```

#### 4. Deploy
```bash
git push heroku main
```

#### 5. Initialize Database
```bash
heroku run python deploy.py init-db
```

### Option 2: DigitalOcean App Platform

#### 1. Create App Spec (app.yaml)
```yaml
name: pet-sitting-site
services:
- name: web
  source_dir: /
  github:
    repo: your-username/your-repo
    branch: main
  run_command: gunicorn --bind 0.0.0.0:$PORT --workers 2 app:app
  environment_slug: python
  instance_count: 1
  instance_size_slug: basic-xxs
  envs:
  - key: SECRET_KEY
    value: your-super-secret-key-here
  - key: FLASK_ENV
    value: production
```

#### 2. Deploy via DigitalOcean Dashboard
- Go to DigitalOcean App Platform
- Connect your GitHub repository
- Use the app.yaml configuration

### Option 3: AWS EC2

#### 1. Launch EC2 Instance
```bash
# Choose Ubuntu 20.04 LTS
# t2.micro for development, t2.small+ for production
```

#### 2. Connect and Setup
```bash
ssh -i your-key.pem ubuntu@your-instance-ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Python and pip
sudo apt install python3 python3-pip python3-venv -y

# Install nginx
sudo apt install nginx -y
```

#### 3. Setup Application
```bash
# Clone your repository
git clone your-repo-url
cd petsittingsite

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
pip install gunicorn

# Setup environment
cp .env.example .env
nano .env  # Edit with your values

# Initialize database
python deploy.py init-db
```

#### 4. Configure Nginx
```bash
sudo nano /etc/nginx/sites-available/petsitting
```

Add this configuration:
```nginx
server {
    listen 80;
    server_name your-domain.com;

    location = /favicon.ico { access_log off; log_not_found off; }

    location / {
        include proxy_params;
        proxy_pass http://unix:/home/ubuntu/petsittingsite/petsitting.sock;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/petsitting /etc/nginx/sites-enabled
sudo nginx -t
sudo systemctl restart nginx
```

#### 5. Create Systemd Service
```bash
sudo nano /etc/systemd/system/petsitting.service
```

Add this content:
```ini
[Unit]
Description=Pet Sitting Website
After=network.target

[Service]
User=ubuntu
Group=www-data
WorkingDirectory=/home/ubuntu/petsittingsite
Environment="PATH=/home/ubuntu/petsittingsite/venv/bin"
ExecStart=/home/ubuntu/petsittingsite/venv/bin/gunicorn --workers 3 --bind unix:petsitting.sock -m 007 app:app

[Install]
WantedBy=multi-user.target
```

```bash
# Start and enable service
sudo systemctl start petsitting
sudo systemctl enable petsitting
```

### Option 4: Docker Deployment

#### 1. Create Dockerfile
```dockerfile
FROM python:3.9-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

EXPOSE 8000

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "3", "app:app"]
```

#### 2. Create docker-compose.yml
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "8000:8000"
    environment:
      - SECRET_KEY=your-secret-key
      - FLASK_ENV=production
    volumes:
      - ./users.db:/app/users.db
```

#### 3. Deploy
```bash
docker-compose up -d
```

## 🔧 Configuration

### Environment Variables
- `SECRET_KEY`: A long, random string for session security
- `FLASK_ENV`: Set to 'production' for production deployment
- `SQLALCHEMY_DATABASE_URI`: Database connection string

### Database Migration
For production, consider using PostgreSQL instead of SQLite:
```bash
# Install PostgreSQL
sudo apt install postgresql postgresql-contrib -y

# Create database and user
sudo -u postgres psql
CREATE DATABASE petsitting_db;
CREATE USER petsitting_user WITH PASSWORD 'your-password';
GRANT ALL PRIVILEGES ON DATABASE petsitting_db TO petsitting_user;
\q
```

Update your `.env`:
```
SQLALCHEMY_DATABASE_URI=postgresql://petsitting_user:your-password@localhost:5432/petsitting_db
```

## 🚀 Quick Start Commands

```bash
# Development
python deploy.py dev

# Production with gunicorn
python deploy.py prod

# Initialize database
python deploy.py init-db

# Manual gunicorn start
gunicorn --bind 0.0.0.0:8000 --workers 3 app:app
```

## 🔒 Security Checklist

- [ ] Change SECRET_KEY to a long, random string
- [ ] Use HTTPS in production
- [ ] Set FLASK_ENV=production
- [ ] Use strong passwords for database
- [ ] Keep dependencies updated
- [ ] Use environment variables for sensitive data
- [ ] Configure firewall properly
- [ ] Regular backups of database

## 📊 Monitoring

Consider adding:
- Application logs
- Database backups
- Health check endpoints
- Error monitoring (Sentry, etc.)
- Performance monitoring

## 🆘 Troubleshooting

### Common Issues:
1. **Port already in use**: Change port in deployment command
2. **Database connection failed**: Check database credentials
3. **Static files not loading**: Check file permissions
4. **Memory issues**: Reduce gunicorn workers or increase server size

### Logs:
```bash
# View application logs
journalctl -u petsitting -f

# View nginx logs
sudo tail -f /var/log/nginx/error.log
```