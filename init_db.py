#!/usr/bin/env python3
"""
Database initialization script for Docker container
Run this from within the container to initialize the database
"""

import os
import sys

# Ensure we're in the right directory
os.chdir('/app')

# Add current directory to path so we can import app
sys.path.insert(0, '/app')

from app import app, db

def init_db():
    """Initialize the database"""
    with app.app_context():
        print("Creating database tables...")
        # Ensure data directory exists
        os.makedirs('/app/data', exist_ok=True)
        try:
            db.create_all()
            print("✅ Database tables created successfully!")
        except Exception as e:
            print(f"⚠️  Database tables might already exist: {e}")

        # Ensure admin user exists
        try:
            from app import ensure_admin_user
            ensure_admin_user()
            print("✅ Admin user setup complete!")
        except Exception as e:
            print(f"⚠️  Admin user setup issue: {e}")

if __name__ == "__main__":
    init_db()
