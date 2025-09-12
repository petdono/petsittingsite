# 🚀 GitHub Setup & Docker Deployment Guide

## 📋 Prerequisites

- Git installed on your system
- Docker and Docker Compose installed
- A GitHub account

## 🔧 Step 1: GitHub Repository Setup

### Option A: Create New Repository on GitHub

1. **Go to GitHub.com** and sign in
2. **Click "New repository"**
3. **Repository name**: `pet-sitting-site` or your preferred name
4. **Description**: "A comprehensive pet sitting website built with Flask"
5. **Choose Public or Private**
6. **Don't initialize** with README (we already have one)
7. **Click "Create repository"**

### Option B: Use Existing Repository

If you already have a repository, skip to Step 2.

## 📁 Step 2: Local Git Setup

### Initialize Git (if not already done)

```bash
cd /path/to/your/petsittingsite
git init
```

### Add Remote Repository

```bash
# Replace with your actual GitHub repository URL
git remote add origin https://github.com/YOUR_USERNAME/pet-sitting-site.git
```

### Configure Git (First time only)

```bash
git config --global user.name "Your Name"
git config --global user.email "your.email@example.com"
```

## 📤 Step 3: Push to GitHub

### Add Files to Git

```bash
# Add all files
git add .

# Or add specific files
git add README.md docker-compose.yml Dockerfile .env.example
```

### Commit Changes

```bash
git commit -m "Initial commit: Pet sitting website with Docker support"
```

### Push to GitHub

```bash
# Push to main branch
git branch -M main
git push -u origin main
```

## 🐳 Step 4: Docker Deployment

### Local Docker Setup

1. **Navigate to your project directory**:
   ```bash
   cd /path/to/your/petsittingsite
   ```

2. **Copy environment file**:
   ```bash
   cp .env.example .env
   ```

3. **Edit environment variables**:
   ```bash
   nano .env  # or use your preferred editor
   ```
   Make sure to set a secure SECRET_KEY!

4. **Deploy with Docker**:
   ```bash
   # Quick deployment (Linux/Mac)
   ./docker-deploy.sh

   # Manual deployment
   docker-compose build
   docker-compose up -d
   ```

5. **Initialize database**:
   ```bash
   docker-compose exec web python deploy.py init-db
   ```

6. **Access your application**:
   - **Website**: http://localhost
   - **Health check**: http://localhost/health

### Docker Management Commands

```bash
# View running containers
docker-compose ps

# View logs
docker-compose logs -f

# Stop application
docker-compose down

# Restart after changes
docker-compose restart

# Rebuild completely
docker-compose build --no-cache
docker-compose up -d

# Access container shell
docker-compose exec web bash
```

## 🌐 Step 5: Production Deployment

### Option A: Deploy to VPS/Server

1. **Server Setup**:
   ```bash
   # On your server
   git clone https://github.com/YOUR_USERNAME/pet-sitting-site.git
   cd pet-sitting-site
   cp .env.example .env
   # Edit .env with production values
   ```

2. **Deploy on Server**:
   ```bash
   docker-compose build
   docker-compose up -d
   docker-compose exec web python deploy.py init-db
   ```

3. **Configure Domain** (optional):
   - Point your domain to the server IP
   - Update nginx configuration if needed

### Option B: Cloud Platforms

#### DigitalOcean App Platform
1. **Connect GitHub repository** to DigitalOcean App Platform
2. **Use the app.yaml** configuration provided
3. **Set environment variables** in the dashboard
4. **Deploy automatically** on git push

#### Railway
1. **Connect GitHub repository**
2. **Railway auto-detects** the Dockerfile
3. **Set environment variables**
4. **Deploy**

#### Render
1. **Connect GitHub repository**
2. **Choose "Docker"** as runtime
3. **Set environment variables**
4. **Deploy**

## 🔐 Step 6: Environment Variables Setup

### For Local Development (.env)
```bash
SECRET_KEY=your-super-secret-key-here
FLASK_ENV=development
SQLALCHEMY_DATABASE_URI=sqlite:///users.db
BASE_HOURLY_RATE=15.0
```

### For Production
```bash
SECRET_KEY=generate-a-very-long-random-string
FLASK_ENV=production
SQLALCHEMY_DATABASE_URI=sqlite:///app/users.db
BASE_HOURLY_RATE=15.0
```

### Generate Secure Secret Key
```bash
# Python command to generate secure key
python -c "import secrets; print(secrets.token_hex(32))"
```

## 🚀 Step 7: GitHub Actions (Optional)

### Setup Automated Deployment

1. **Go to your GitHub repository**
2. **Click "Settings" → "Secrets and variables" → "Actions"**
3. **Add these secrets**:
   - `DOCKER_USERNAME`: Your Docker Hub username
   - `DOCKER_PASSWORD`: Your Docker Hub password
   - `SERVER_HOST`: Your server IP (for VPS deployment)
   - `SERVER_USERNAME`: Server username
   - `SERVER_SSH_KEY`: SSH private key

4. **The workflow file** (`.github/workflows/docker-deploy.yml`) is already configured
5. **Push changes** to trigger automated deployment

## 📊 Step 8: Monitoring & Maintenance

### Health Checks
- **Application health**: http://your-domain/health
- **Docker containers**: `docker-compose ps`
- **Logs**: `docker-compose logs -f`

### Database Backups
```bash
# Backup SQLite database
docker-compose exec web cp users.db users.db.backup

# Download backup
docker cp $(docker-compose ps -q web):/app/users.db.backup ./backup.db
```

### Updates
```bash
# Pull latest changes
git pull origin main

# Rebuild and restart
docker-compose build --no-cache
docker-compose up -d

# Update database if needed
docker-compose exec web python migrate_db.py
```

## 🆘 Troubleshooting

### Common Issues

1. **Port already in use**:
   ```bash
   # Change port in docker-compose.yml
   ports:
     - "8001:8000"  # Change 8000 to available port
   ```

2. **Database connection failed**:
   - Check `.env` file configuration
   - Ensure database file permissions

3. **Static files not loading**:
   ```bash
   docker-compose exec web ls -la static/
   ```

4. **Container won't start**:
   ```bash
   docker-compose logs web
   ```

### Useful Commands

```bash
# Clean up Docker
docker system prune -a

# View container resource usage
docker stats

# Debug container
docker-compose exec web bash

# Check application logs
docker-compose logs -f web
```

## 🎉 Success!

Your pet sitting website is now:
- ✅ **Containerized** with Docker
- ✅ **Version controlled** with Git
- ✅ **Hosted** on GitHub
- ✅ **Production ready** with nginx reverse proxy
- ✅ **Monitored** with health checks
- ✅ **Scalable** and maintainable

**Access your application at**: http://localhost (or your domain)

Happy deploying! 🚀