#!/usr/bin/env python3
"""
Database initialization script
Creates all tables based on models
"""

import os
import sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app, db

def init_database():
    """Initialize database with all tables"""
    with app.app_context():
        db.create_all()
        print("Database tables created successfully")

if __name__ == '__main__':
    init_database()
