from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# 1. DNS Details Table
'''class DNSDetails(db.Model):
    __tablename__ = 'dns_details'
    id = db.Column(db.Integer, primary_key=True)
    file_name = db.Column(db.String(255))
    file_url = db.Column(db.String(500))
    bank_name = db.Column(db.String(255))
    account_number = db.Column(db.String(100))
    ifsc_code = db.Column(db.String(50))
    account_holder_name = db.Column(db.String(255))'''

# 2. Project Table (Running or Completed)
class Project(db.Model):
    __tablename__ = 'projects'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    thumbnail_image_id = db.Column(db.Integer, db.ForeignKey('project_images.id'), nullable=True)
    address = db.Column(db.String(200))
    map_url = db.Column(db.String(200))
    description = db.Column(db.Text)
    info = db.Column(db.Text)
    status = db.Column(db.String(20))  # 'running' or 'completed'

    # Relationships
    images = db.relationship(
        'ProjectImage',
        backref='project',
        lazy=True,
        foreign_keys='ProjectImage.project_id'
    )
    videos = db.relationship(
        'ProjectVideo',
        backref='project',
        lazy=True,
        foreign_keys='ProjectVideo.project_id'
    )
    files = db.relationship(
        'ProjectFile',
        backref='project',
        lazy=True,
        foreign_keys='ProjectFile.project_id'
    )
    thumbnail_image = db.relationship(
        'ProjectImage',
        foreign_keys=[thumbnail_image_id],
        uselist=False
    )

# 2.1 Project Images Table
class ProjectImage(db.Model):
    __tablename__ = 'project_images'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    image_data = db.Column(db.LargeBinary)
    image_mimetype = db.Column(db.String(50))
    image_name = db.Column(db.String(100))

# 2.2 Project Videos Table
class ProjectVideo(db.Model):
    __tablename__ = 'project_videos'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    video_data = db.Column(db.LargeBinary)
    video_mimetype = db.Column(db.String(50))
    video_name = db.Column(db.String(100))

# 2.3 Project PDF Files Table
class ProjectFile(db.Model):
    __tablename__ = 'project_files'
    id = db.Column(db.Integer, primary_key=True)
    project_id = db.Column(db.Integer, db.ForeignKey('projects.id'), nullable=False)
    file_data = db.Column(db.LargeBinary)
    file_mimetype = db.Column(db.String(50))
    file_name = db.Column(db.String(100))

# 3. About Me Table
class AboutMe(db.Model):
    __tablename__ = 'about_me'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    title = db.Column(db.String(100))
    description = db.Column(db.Text)
    image_data = db.Column(db.LargeBinary)
    image_mimetype = db.Column(db.String(50))
    image_name = db.Column(db.String(100))

# 4. Contact Table
class Contact(db.Model):
    __tablename__ = 'contact'
    id = db.Column(db.Integer, primary_key=True)
    phone1 = db.Column(db.String(20))
    phone2 = db.Column(db.String(20))
    email = db.Column(db.String(100))
    office_address = db.Column(db.String(200))

# 5. User Table for Authentication
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    mobile = db.Column(db.String(20))
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

    def set_password(self, password):
        """Hash and set password"""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Check if provided password matches hash"""
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Convert user to dictionary (excluding password)"""
        return {
            'id': self.id,
            'username': self.username,
            'mobile': self.mobile,
            'is_admin': self.is_admin,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

# 6. Testimonials Table
class Testimonial(db.Model):
    __tablename__ = 'testimonials'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    star_rating = db.Column(db.Integer, nullable=False)
    text_review = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())
    is_approved = db.Column(db.Boolean, default=False)
