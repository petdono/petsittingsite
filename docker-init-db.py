#!/usr/bin/env python3
"""
Docker database initialization script
"""

from app import app, db

def init_db():
    """Initialize the database"""
    with app.app_context():
        print("Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")

        # Ensure admin user exists
        try:
            from app import ensure_admin_user
            ensure_admin_user()
            print("✅ Admin user setup complete!")
        except Exception as e:
            print(f"⚠️  Admin user setup issue: {e}")

if __name__ == "__main__":
    init_db()