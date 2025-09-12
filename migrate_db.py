#!/usr/bin/env python3
"""
Database migration script for adding dog profiles feature.
Run this script to update your database schema.
"""

from app import app, db
from sqlalchemy import text

def migrate_database():
    """Add new tables and columns for dog profiles feature"""

    with app.app_context():
        try:
            # Create Animal table
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS animal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    name VARCHAR(100) NOT NULL,
                    animal_type VARCHAR(50) NOT NULL,
                    breed VARCHAR(100) NOT NULL,
                    age INTEGER,
                    weight FLOAT,
                    special_needs TEXT,
                    temperament VARCHAR(50),
                    medical_conditions TEXT,
                    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES user (id)
                )
            """))

            # Create BookingAnimal association table
            db.session.execute(text("""
                CREATE TABLE IF NOT EXISTS booking_animal (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    booking_id INTEGER NOT NULL,
                    animal_id INTEGER NOT NULL,
                    FOREIGN KEY (booking_id) REFERENCES booking (id),
                    FOREIGN KEY (animal_id) REFERENCES animal (id)
                )
            """))

            # Add indexes for better performance
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_animal_user_id ON animal(user_id)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_booking_animal_booking_id ON booking_animal(booking_id)"))
            db.session.execute(text("CREATE INDEX IF NOT EXISTS idx_booking_animal_animal_id ON booking_animal(animal_id)"))

            db.session.commit()
            print("✅ Database migration completed successfully!")
            print("New features available:")
            print("- Animal profiles management (dogs, cats, birds, etc.)")
            print("- Animal selection in bookings")
            print("- Enhanced admin booking view")

        except Exception as e:
            db.session.rollback()
            print(f"❌ Migration failed: {e}")
            print("You may need to manually update your database schema.")

if __name__ == "__main__":
    migrate_database()