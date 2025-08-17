# Quick Start Guide - Pawan Dubey Portfolio

## 🚀 Quick Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Initialize database
python init_db.py

# 3. Run the app
python app.py
```

## 📍 Access Points
- **Website**: http://localhost:5000
- **Admin Panel**: http://localhost:5000/admin
- **Login**: http://localhost:5000/login

## 🔑 Default Login
- **Username**: admin
- **Password**: 1234

## 📁 Key Files
- `app.py` - Main application
- `models.py` - Database models
- `static/style.css` - Styling
- `templates/` - HTML pages

## 🎯 Quick Actions
- **Add Project**: Admin → Projects → Add New
- **Upload Images**: Admin → Media → Upload
- **Edit Content**: Admin → Content → Edit
- **Change Password**: Admin → Settings → Password

## 🛠️ Common Commands
```bash
# Reset database
python init_db.py

# Check logs
tail -f app.log

# Test locally
curl http://localhost:5000/api/projects
```

## 📞 Need Help?
Check the full README.md for detailed documentation.
