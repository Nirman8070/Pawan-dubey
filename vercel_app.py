import os
from flask import Flask
from werkzeug.middleware.proxy_fix import ProxyFix

# Create Flask app
app = Flask(__name__)

# Configuration for Vercel
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SESSION_TYPE'] = 'filesystem'
app.config['UPLOAD_FOLDER'] = '/tmp/uploads'

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Import models and routes
from models import db, Project, AboutMe, Contact, ProjectImage, ProjectVideo, ProjectFile, User, Testimonial
from app import *

# Initialize extensions
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail

db.init_app(app)
Session(app)
mail = Mail(app)

# Create tables on first request
with app.app_context():
    db.create_all()

# Vercel handler
def handler(request):
    return app

# For local development
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
