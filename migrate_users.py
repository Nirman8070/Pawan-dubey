#!/usr/bin/env python3
"""
Migration script to populate initial admin user in database
Run this script once to migrate from hardcoded users to database
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db
from models import User

def migrate_users():
    """Migrate hardcoded users to database"""
    with app.app_context():
        # Check if admin user already exists
        admin_user = User.query.filter_by(username='admin').first()
        
        if not admin_user:
            # Create admin user with current hardcoded credentials
            admin_user = User(
                username='admin',
                mobile='8102138070',
                is_admin=True
            )
            admin_user.set_password('1234')
            db.session.add(admin_user)
            db.session.commit()
            print("✓ Admin user created successfully")
        else:
            print("✓ Admin user already exists")
        
        # List all users
        users = User.query.all()
        print(f"Total users in database: {len(users)}")
        for user in users:
            print(f"  - {user.username} (admin: {user.is_admin})")

if __name__ == '__main__':
    migrate_users()
