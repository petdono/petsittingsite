# Portainer Deployment Guide

4. **Choose deployment method**:

   **Option A: Git Repository (Recommended)**
   - **Repository URL**: `https://github.com/petdono/petsittingsite.git`
   - **Repository reference**: `main`
   - **Compose path**: `docker-compose.yml`

   **Option B: Web Editor with Custom Compose**
   - Choose "Web editor"
   - Copy the contents of `docker-compose.portainer.yml`
   - This file is optimized for Portainer deployment

5. **Environment Variables** (add these in Portainer):
   ```
   SECRET_KEY=your-super-secret-key-here-change-this
   FLASK_ENV=production
   SQLALCHEMY_DATABASE_URI=sqlite:///app/users.db
   BASE_HOURLY_RATE=15.0
   ```

6. **Deploy the Stack**te

## 🚀 Quick Portainer Setup

### 1. Install Portainer (if not already installed)

```bash
# Create Portainer volume
docker volume create portainer_data

# Run Portainer
docker run -d \
  -p 8000:8000 \
  -p 9443:9443 \
  --name portainer \
  --restart=always \
  -v /var/run/docker.sock:/var/run/docker.sock \
  -v portainer_data:/data \
  portainer/portainer-ce:latest
```

### 2. Access Portainer
- **URL**: https://localhost:9443 (or your server IP)
- **First time**: Create admin account

## 📦 Deploy Your Pet Sitting Site

### Method 1: Git Repository Deployment (Recommended)

1. **Go to Portainer Dashboard**
2. **Navigate to**: Stacks → Add Stack
3. **Fill in details**:
   - **Name**: `pet-sitting-site`
   - **Repository URL**: `https://github.com/petdono/petsittingsite.git`
   - **Repository reference**: `main` (or your default branch)
   - **Compose path**: `docker-compose.yml`

4. **Environment Variables**:
   ```
   SECRET_KEY=dev-key-change-later
   FLASK_ENV=production
   SQLALCHEMY_DATABASE_URI=sqlite:///app/users.db
   BASE_HOURLY_RATE=15.0
   ```

5. **Advanced Options**:
   - Enable "Enable GitOps updates" if you want auto-updates
   - Set update interval (e.g., every 5 minutes)

6. **Deploy the Stack**

### Method 2: Manual Docker Compose (Alternative)

1. **Go to Portainer Dashboard**
2. **Navigate to**: Stacks → Add Stack
3. **Choose**: "Web editor"
4. **Copy and paste** the contents of `docker-compose.portainer.yml`:

```yaml
version: '3.8'

services:
  web:
    build: https://github.com/petdono/petsittingsite.git
    ports:
      - "5000:5000"
    environment:
      - SECRET_KEY=dev-key-change-later
      - FLASK_ENV=production
      - SQLALCHEMY_DATABASE_URI=sqlite:///app/users.db
      - BASE_HOURLY_RATE=15.0
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:5000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
```

## 🔧 Post-Deployment Setup

### Initialize Database
```bash
# In Portainer, go to Containers
# Click on your web container
# Go to Console
# Run: python init_db.py
```

### Test Database Connection
```bash
# Test if database is working
python test_db.py
```

### Access Your Application
- **Portainer**: https://your-server-ip:9443
- **Pet Sitting Site**: http://your-server-ip:5000
- **Health Check**: http://your-server-ip:5000/health

## 🔄 Updates and Maintenance

### Automatic Updates (GitOps)
1. **Enable GitOps** in your stack settings
2. **Set update interval** (e.g., every 5 minutes)
3. **Portainer will automatically pull** and redeploy when you push to GitHub

### Manual Updates
1. **Go to Stacks** in Portainer
2. **Click your stack**
3. **Click "Pull and redeploy"**

## 🛠️ Troubleshooting

### Check Logs
1. **Go to Containers** in Portainer
2. **Click on your container**
3. **Go to "Logs" tab**

### Access Container Shell
1. **Go to Containers** in Portainer
2. **Click on your container**
3. **Go to "Console" tab**
4. **Run commands** like `ls -la`, `python --version`, etc.

### Common Issues

1. **Build fails**:
   - Check repository URL is correct
   - Ensure Dockerfile exists in root directory
   - Check build logs for errors

2. **Port conflicts**:
   - Change ports in docker-compose.yml if 80/8000 are in use

3. **Database issues**:
   - Check volume permissions
   - Run database initialization manually

## 🔒 Security Considerations

1. **Change default SECRET_KEY** to a long, random string
2. **Use HTTPS** in production (configure SSL certificates)
3. **Set up firewall rules** to restrict access
4. **Regular backups** of the database volume

## 📊 Monitoring

### Health Checks
- **Application**: http://your-domain:5000/health
- **Container status**: Check in Portainer dashboard
- **Resource usage**: Monitor in Portainer

### Logs
- **Application logs**: Available in container logs
- **Access logs**: Available in nginx container logs
- **Portainer logs**: Check Portainer container logs

Your pet sitting website is now ready for Portainer deployment! 🎉