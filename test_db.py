#!/usr/bin/env python3
"""
Simple database test script
"""

import os
import sys

# Ensure we're in the right directory
os.chdir('/app')

# Add current directory to path
sys.path.insert(0, '/app')

from app import app, db

def test_db():
    """Test database connection and creation"""
    print("Testing database connection...")

    with app.app_context():
        try:
            # Ensure data directory exists
            os.makedirs('/app/data', exist_ok=True)
            print("✅ Data directory exists")

            # Test database connection
            db.engine.execute('SELECT 1')
            print("✅ Database connection successful")

            # Create tables
            db.create_all()
            print("✅ Database tables created")

            return True
        except Exception as e:
            print(f"❌ Database error: {e}")
            return False

if __name__ == "__main__":
    success = test_db()
    sys.exit(0 if success else 1)