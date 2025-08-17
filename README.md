# Pawan Dubey's Portfolio - Real Estate Developer Website

A comprehensive portfolio website showcasing real estate projects and services for DNS Homes Pvt. Ltd., built with Flask and featuring a modern, responsive design.

## 🏗️ Project Overview

This is a professional portfolio website for Pawan Dubey, a real estate developer and Diamond Diplomat at DNS Homes Pvt. Ltd. The platform showcases running and completed real estate projects, provides detailed project information, and offers a complete admin panel for content management.

## ✨ Features

### 🏠 Frontend Features
- **Responsive Design**: Mobile-first responsive layout
- **Project Showcase**: Interactive display of running and completed projects
- **Image Galleries**: Lightbox-style image galleries for each project
- **Video Integration**: Embedded project videos and walkthroughs
- **Document Downloads**: PDF files and project documents
- **Contact Forms**: Integrated contact and inquiry forms
- **Testimonials**: Customer review system with approval workflow
- **Interactive Maps**: Google Maps integration for project locations

### 🔐 Admin Panel
- **Secure Authentication**: Database-driven user authentication
- **Project Management**: CRUD operations for projects, images, videos, and files
- **Content Management**: Dynamic content updates for About Me and Contact sections
- **User Management**: Admin user creation and password management
- **Testimonial Moderation**: Review and approval system for customer testimonials
- **Media Management**: Upload and manage project media files

### 📊 Technical Features
- **RESTful API**: Complete API for all CRUD operations
- **File Upload System**: Secure file upload with validation
- **Database Storage**: Binary storage for images, videos, and documents
- **Session Management**: Flask session-based authentication
- **Responsive Images**: Optimized image serving for different devices

## 🛠️ Technology Stack

### Backend
- **Flask**: Python web framework
- **SQLAlchemy**: ORM for database operations
- **Flask-Session**: Server-side session management
- **Flask-Mail**: Email integration (configured)
- **Werkzeug**: Security utilities for password hashing

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with Flexbox and Grid
- **JavaScript**: Interactive features and AJAX
- **Boxicons**: Icon library
- **Google Fonts**: Typography

### Database
- **SQLite**: Development database
- **Large Binary Storage**: For media files
- **Relational Design**: Normalized database structure

## 📁 Project Structure

```
e:/Pawan dubey's portfolio/
├── app.py                 # Main Flask application
├── models.py              # Database models
├── config.py              # Configuration settings
├── init_db.py            # Database initialization
├── migrate_users.py      # User migration script
├── instance/
│   └── portfolio.db      # SQLite database
├── static/
│   ├── css/
│   │   └── style.css     # Main stylesheet
│   ├── js/
│   │   └── script.js     # JavaScript functionality
│   ├── images/           # Image assets
│   ├── uploads/          # User uploaded files
│   └── dns details/      # Company documents
├── templates/
│   ├── index.html        # Homepage
│   ├── login.html        # Login page
│   ├── admin.html        # Admin dashboard
│   ├── password.html     # Password reset
│   ├── review.html       # Review system
│   └── *.html            # Additional templates
└── flask_session/        # Session files
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.7+
- pip (Python package manager)

### Installation Steps

1. **Clone the repository**
```bash
git clone [repository-url]
cd pawan-dubey-portfolio
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Initialize the database**
```bash
python init_db.py
```

5. **Run the application**
```bash
python app.py
```

6. **Access the website**
- Frontend: http://localhost:5000
- Admin Panel: http://localhost:5000/admin
- Login: http://localhost:5000/login

### Default Admin Credentials
- Username: admin
- Password: admin123
- *Change these credentials after first login*

## 🔧 Configuration

### Environment Variables
Create a `.env` file with:
```env
SECRET_KEY=your-secret-key-here
DATABASE_URL=sqlite:///portfolio.db
UPLOAD_FOLDER=static/uploads
```

### Email Configuration
Update the mail settings in `app.py`:
```python
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = 'your-email@gmail.com'
app.config['MAIL_PASSWORD'] = 'your-app-password'
```

## 📊 Database Schema

### Core Tables
- **projects**: Real estate projects
- **project_images**: Project images (binary storage)
- **project_videos**: Project videos (binary storage)
- **project_files**: Project documents (binary storage)
- **about_me**: Personal information
- **contact**: Contact details
- **users**: Admin users
- **testimonials**: Customer reviews

## 🎯 API Endpoints

### Projects
- `GET /api/projects` - List all projects
- `POST /api/projects` - Create new project
- `GET /api/projects/<id>` - Get project details
- `PUT /api/projects/<id>` - Update project
- `DELETE /api/projects/<id>` - Delete project

### Media Management
- `POST /api/upload/<type>/<project_id>` - Upload media files
- `DELETE /api/delete/<type>/<id>` - Delete media files

### Admin Functions
- `GET /api/admin/testimonials` - Manage testimonials
- `PUT /api/admin/testimonials/<id>/approve` - Approve testimonial
- `POST /api/admin/password` - Change admin password

## 🎨 Customization

### Adding New Projects
1. Login to admin panel
2. Navigate to Projects section
3. Click "Add New Project"
4. Fill project details and upload media
5. Save project

### Updating Content
- **About Me**: Admin panel → About Section
- **Contact Info**: Admin panel → Contact Section
- **Homepage Images**: Admin panel → Media Management

### Styling
- Main colors: Defined in `static/style.css`
- Fonts: Google Fonts integration
- Responsive breakpoints: Mobile, tablet, desktop

## 📱 Responsive Design

The website is fully responsive with breakpoints at:
- **Mobile**: < 768px
- **Tablet**: 768px - 1024px
- **Desktop**: > 1024px

## 🔒 Security Features

- Password hashing with Werkzeug
- Session-based authentication
- CSRF protection
- File upload validation
- SQL injection prevention through SQLAlchemy

## 🚀 Deployment

### Production Deployment
1. **Environment Setup**
```bash
export FLASK_ENV=production
export SECRET_KEY=your-production-secret
```

2. **Database Migration**
For production, consider migrating to PostgreSQL:
```python
# Update SQLALCHEMY_DATABASE_URI
postgresql://user:password@localhost/dbname
```

3. **Web Server**
Use Gunicorn with Nginx:
```bash
gunicorn app:app
```

### Docker Deployment
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create a Pull Request

## 📞 Support

For support or questions:
- Email: info@dnshomes.in
- Phone: +91-XXXXXXXXXX
- Website: https://dnshomes.in

## 📄 License

This project is proprietary software developed for DNS Homes Pvt. Ltd. All rights reserved.

## 🙏 Acknowledgments

- DNS Homes Pvt. Ltd. for the project opportunity
- Flask community for excellent documentation
- Contributors and testers

---

**Built by Nirman kumar for Pawan dubey**
