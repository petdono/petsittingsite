# Use Python 3.# Install Python dependencies in batches
RUN pip install --no-cache-dir Flask==2.3.3 Werkzeug==2.3.7
RUN pip install --no-cache-dir Flask-SQLAlchemy==3.0.5 Flask-Login==0.6.2
RUN pip install --no-cache-dir SQLAlchemy==2.0.23
RUN pip install --no-cache-dir python-dotenv==1.0.0 gunicorn==21.2.0
RUN pip install --no-cache-dir email-validator==2.1.0pip install --no-cache-dir Flask-SQLAlchemy==3.1.1 Flask-Login==0.7.0full image (more dependencies pre-installed)
FROM python:3.13

# Set working directory
WORKDIR /app

# Clear pip cache to ensure fresh installs
RUN pip cache purge
RUN apt-get update && apt-get install -y \
    gcc \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies in batches
RUN pip install --no-cache-dir Flask==3.1.2 Werkzeug==3.1.3
RUN pip install --no-cache-dir Flask-SQLAlchemy==3.0.5 Flask-Login==0.6.2
RUN pip install --no-cache-dir SQLAlchemy==2.0.43
RUN pip install --no-cache-dir python-dotenv==1.0.0 gunicorn==21.2.0
RUN pip install --no-cache-dir email-validator==2.2.0

# Copy application code
COPY . .

# Create non-root user
RUN useradd --create-home --shell /bin/bash app \
    && chown -R app:app /app
USER app

# Expose port
EXPOSE 5000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Run with gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "3", "--timeout", "120", "app:app"]
