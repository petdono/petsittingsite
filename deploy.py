#!/usr/bin/env python3
"""
Production deployment script for Pet Sitting Website
Run with: python deploy.py
"""

import os
import sys
from app import app, db

def create_database():
    """Create database tables"""
    with app.app_context():
        db.create_all()
        print("✅ Database tables created successfully!")

def run_development():
    """Run in development mode"""
    print("🚀 Starting development server...")
    app.run(debug=True, host='0.0.0.0', port=5000)

def run_production():
    """Run in production mode with gunicorn"""
    print("🚀 Starting production server with gunicorn...")
    os.system("gunicorn --bind 0.0.0.0:8000 --workers 3 app:app")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        command = sys.argv[1]

        if command == "init-db":
            create_database()
        elif command == "dev":
            run_development()
        elif command == "prod":
            run_production()
        else:
            print("Usage: python deploy.py [init-db|dev|prod]")
    else:
        print("🐱 Pet Sitting Website Deployment Script")
        print("Usage:")
        print("  python deploy.py init-db    # Initialize database")
        print("  python deploy.py dev       # Run development server")
        print("  python deploy.py prod      # Run production server")
        print("\nFor production deployment, use:")
        print("  gunicorn --bind 0.0.0.0:8000 --workers 3 app:app")