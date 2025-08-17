from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_session import Session
from flask_mail import Mail, Message
from models import db, Project, AboutMe, Contact, ProjectImage, ProjectVideo, ProjectFile, User, Testimonial
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'secret_key_here'
app.config['SESSION_TYPE'] = 'filesystem'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portfolio.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = 'static/uploads'
Session(app)
db.init_app(app)

# Ensure upload folder exists
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

# Flask-Mail configuration
mail = Mail(app)

# Database authentication - users are now stored in User table

# Homepage
@app.route('/')
def index():
    about = AboutMe.query.first()
    contact = Contact.query.first()
    running_projects = Project.query.filter_by(status='running').all()
    completed_projects = Project.query.filter_by(status='completed').all()
    home_images = ProjectImage.query.filter(ProjectImage.project_id == None).all()
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return render_template(
        'index.html',
        about=about,
        contact=contact,
        running_projects=running_projects,
        completed_projects=completed_projects,
        home_images=home_images,
        testimonials=testimonials
    )

@app.route('/index2')
def index2():
    about = AboutMe.query.first()
    contact = Contact.query.first()
    running_projects = Project.query.filter_by(status='running').all()
    completed_projects = Project.query.filter_by(status='completed').all()
    home_images = ProjectImage.query.filter(ProjectImage.project_id == None).all()
    return render_template(
        'index2.html',
        about=about,
        contact=contact,
        running_projects=running_projects,
        completed_projects=completed_projects,
        home_images=home_images
    )

# Login Page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        login_id = request.form['loginId']
        password = request.form['password']
        
        # Use database authentication instead of hardcoded users
        user = User.query.filter_by(username=login_id).first()
        
        if user and user.check_password(password):
            session['user'] = user.username
            return redirect('/admin')
        else:
            flash("Invalid login credentials.")
            return redirect('/login')
    return render_template('login.html')

# Admin Page (Protected)
@app.route('/admin')
def admin():
    if 'user' not in session:
        return redirect('/login')
    return render_template('admin.html')

# Logout Route
@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/login')

# Review Page
@app.route('/review')
def review():
    return render_template('review.html')

# Password Reset Page
@app.route('/password', methods=['GET', 'POST'])
def password():
    if request.method == 'POST':
        mobile = request.form['mobile']
        otp = request.form['otp']
        new_password = request.form['newPassword']
        confirm_password = request.form['confirmPassword']

        # Use database to find user by mobile
        user = User.query.filter_by(mobile=mobile).first()

        if user and new_password == confirm_password:
            user.set_password(new_password)
            db.session.commit()
            flash('Password changed successfully!')
            return redirect('/login')
        else:
            flash('Invalid mobile or passwords do not match.')
            return redirect('/password')
    return render_template('password.html')

# --- PROJECT MANAGEMENT API ENDPOINTS ---
@app.route('/api/projects', methods=['GET', 'POST'])
def api_projects():
    if request.method == 'GET':
        status = request.args.get('status')
        if status:
            projects = Project.query.filter_by(status=status).all()
        else:
            projects = Project.query.all()
        
        return jsonify([{
            'id': p.id,
            'title': p.title,
            'address': p.address,
            'description': p.description,
            'info': p.info,
            'status': p.status,
            'map_url': project.map_url,
            'images': [{'id': img.id, 'name': img.image_name} for img in p.images],
            'videos': [{'id': vid.id, 'name': vid.video_name} for vid in p.videos],
            'files': [{'id': f.id, 'name': f.file_name} for f in p.files],
            'thumbnail_image_id': p.thumbnail_image_id
        } for p in projects])

    elif request.method == 'POST':
        try:
            data = request.form
            project = Project(
                title=data.get('title', ''),
                address=data.get('address', ''),
                description=data.get('description', ''),
                info=data.get('info', ''),
                status=data.get('status', 'running'),
                map_url=data.get('map_url', '')
            )
            db.session.add(project)
            db.session.commit()

            # Handle thumbnail image
            if 'thumbnail' in request.files:
                file = request.files['thumbnail']
                if file and file.filename:
                    img = ProjectImage(
                        project_id=project.id,
                        image_data=file.read(),
                        image_mimetype=file.mimetype,
                        image_name=secure_filename(file.filename)
                    )
                    db.session.add(img)
                    db.session.commit()
                    project.thumbnail_image_id = img.id
                    db.session.commit()

            # Handle multiple images
            if 'images' in request.files:
                for file in request.files.getlist('images'):
                    if file and file.filename:
                        img = ProjectImage(
                            project_id=project.id,
                            image_data=file.read(),
                            image_mimetype=file.mimetype,
                            image_name=secure_filename(file.filename)
                        )
                        db.session.add(img)
                db.session.commit()

            # Handle videos
            if 'videos' in request.files:
                for file in request.files.getlist('videos'):
                    if file and file.filename:
                        vid = ProjectVideo(
                            project_id=project.id,
                            video_data=file.read(),
                            video_mimetype=file.mimetype,
                            video_name=secure_filename(file.filename)
                        )
                        db.session.add(vid)
                db.session.commit()

            # Handle files
            if 'files' in request.files:
                for file in request.files.getlist('files'):
                    if file and file.filename:
                        pf = ProjectFile(
                            project_id=project.id,
                            file_data=file.read(),
                            file_mimetype=file.mimetype,
                            file_name=secure_filename(file.filename)
                        )
                        db.session.add(pf)
                db.session.commit()

            return jsonify({'message': 'Project created successfully', 'id': project.id})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error creating project: {str(e)}'}), 500

@app.route('/api/projects/<int:project_id>', methods=['GET', 'PUT', 'DELETE'])
def api_project_detail(project_id):
    project = Project.query.get_or_404(project_id)
    
    if request.method == 'GET':
        return jsonify({
            'id': project.id,
            'title': project.title,
            'address': project.address,
            'description': project.description,
            'info': project.info,
            'status': project.status,
            'map_url': project.map_url,
            'images': [{'id': img.id, 'name': img.image_name} for img in project.images],
            'videos': [{'id': vid.id, 'name': vid.video_name} for vid in project.videos],
            'files': [{'id': f.id, 'name': f.file_name} for f in project.files],
            'thumbnail_image_id': project.thumbnail_image_id
        })
    
    elif request.method == 'PUT':
        try:
            data = request.form
            project.title = data.get('title', project.title)
            project.address = data.get('address', project.address)
            project.description = data.get('description', project.description)
            project.info = data.get('info', project.info)
            project.map_url = data.get('map_url', project.map_url)
            db.session.commit()
            
            # Handle file updates
            # Similar to POST method for handling files
            # ... (implementation similar to POST)
            
            return jsonify({'message': 'Project updated successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error updating project: {str(e)}'}), 500
    
    elif request.method == 'DELETE':
        try:
            # Delete associated files
            ProjectImage.query.filter_by(project_id=project_id).delete()
            ProjectVideo.query.filter_by(project_id=project_id).delete()
            ProjectFile.query.filter_by(project_id=project_id).delete()
            
            db.session.delete(project)
            db.session.commit()
            return jsonify({'message': 'Project deleted successfully'})
        except Exception as e:
            db.session.rollback()
            return jsonify({'message': f'Error deleting project: {str(e)}'}), 500

@app.route('/api/projects/<status>')
def api_projects_by_status(status):
    if status not in ['running', 'completed']:
        return jsonify({'message': 'Invalid status'}), 400
    
    projects = Project.query.filter_by(status=status).all()
    return jsonify([{
        'id': p.id,
        'title': p.title,
        'address': p.address,
        'description': p.description,
        'info': p.info,
        'map_url': p.map_url,
        'images': [{'id': img.id, 'name': img.image_name} for img in p.images],
        'videos': [{'id': vid.id, 'name': vid.video_name} for vid in p.videos],
        'files': [{'id': f.id, 'name': f.file_name} for f in p.files]
    } for p in projects])

# File upload endpoints
@app.route('/api/upload/<media_type>/<int:project_id>', methods=['POST'])
def upload_media(media_type, project_id):
    if media_type not in ['image', 'video', 'file']:
        return jsonify({'message': 'Invalid media type'}), 400
    
    project = Project.query.get_or_404(project_id)
    
    try:
        if media_type == 'image':
            files = request.files.getlist('file')
            for file in files:
                if file and file.filename:
                    img = ProjectImage(
                        project_id=project_id,
                        image_data=file.read(),
                        image_mimetype=file.mimetype,
                        image_name=secure_filename(file.filename)
                    )
                    db.session.add(img)
        
        elif media_type == 'video':
            files = request.files.getlist('file')
            for file in files:
                if file and file.filename:
                    vid = ProjectVideo(
                        project_id=project_id,
                        video_data=file.read(),
                        video_mimetype=file.mimetype,
                        video_name=secure_filename(file.filename)
                    )
                    db.session.add(vid)
        
        elif media_type == 'file':
            files = request.files.getlist('file')
            for file in files:
                if file and file.filename:
                    pf = ProjectFile(
                        project_id=project_id,
                        file_data=file.read(),
                        file_mimetype=file.mimetype,
                        file_name=secure_filename(file.filename)
                    )
                    db.session.add(pf)
        
        db.session.commit()
        return jsonify({'message': f'{media_type.capitalize()}s uploaded successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error uploading {media_type}: {str(e)}'}), 500

# --- ABOUT ME SECTION ---
@app.route('/api/about', methods=['GET', 'PUT'])
def api_about():
    about = AboutMe.query.first()
    if request.method == 'GET':
        if not about:
            return jsonify({})
        return jsonify({
            'name': about.name,
            'title': about.title,
            'description': about.description
        })
    elif request.method == 'PUT':
        data = request.json
        if not about:
            about = AboutMe()
            db.session.add(about)
        about.name = data.get('name', about.name)
        about.title = data.get('title', about.title)
        about.description = data.get('description', about.description)
        db.session.commit()
        return jsonify({'message': 'About updated'})

@app.route('/api/about/image', methods=['POST'])
def update_about_image():
    about = AboutMe.query.first()
    if not about:
        about = AboutMe()
        db.session.add(about)
    file = request.files['image']
    if file:
        about.image_data = file.read()
        about.image_mimetype = file.mimetype
        about.image_name = file.filename
        db.session.commit()
        return jsonify({'message': 'Image updated'})
    return jsonify({'message': 'No image uploaded'}), 400

# --- CONTACT SECTION ---
@app.route('/api/contact', methods=['GET', 'PUT'])
def api_contact():
    contact = Contact.query.first()
    if request.method == 'GET':
        if not contact:
            return jsonify({})
        return jsonify({
            'phone1': contact.phone1,
            'phone2': contact.phone2,
            'email': contact.email,
            'office_address': contact.office_address
        })
    elif request.method == 'PUT':
        data = request.json
        if not contact:
            contact = Contact()
            db.session.add(contact)
        contact.phone1 = data.get('phone1', contact.phone1)
        contact.phone2 = data.get('phone2', contact.phone2)
        contact.email = data.get('email', contact.email)
        contact.office_address = data.get('office_address', contact.office_address)
        db.session.commit()
        return jsonify({'message': 'Contact updated'})

# Serve About Image
@app.route('/media/about/image')
def serve_about_image():
    about = AboutMe.query.first()
    if about and about.image_data:
        return app.response_class(about.image_data, mimetype=about.image_mimetype)
    return '', 404

# Serve Project Images
@app.route('/media/project/image/<int:image_id>')
def serve_project_image(image_id):
    img = ProjectImage.query.get_or_404(image_id)
    return app.response_class(img.image_data, mimetype=img.image_mimetype)

# Serve Project Videos
@app.route('/media/project/video/<int:video_id>')
def serve_project_video(video_id):
    vid = ProjectVideo.query.get_or_404(video_id)
    return app.response_class(vid.video_data, mimetype=vid.video_mimetype)

# Serve Project Files
@app.route('/media/project/file/<int:file_id>')
def serve_project_file(file_id):
    file = ProjectFile.query.get_or_404(file_id)
    return app.response_class(file.file_data, mimetype=file.file_mimetype,
                             headers={"Content-Disposition": f"attachment;filename={file.file_name}"})

@app.route('/api/about/image', methods=['GET'])
def get_about_image():
    about = AboutMe.query.first()
    if about and about.image_data:
        return app.response_class(about.image_data, mimetype=about.image_mimetype)
    return '', 404

@app.route('/api/admin/password', methods=['POST'])
def change_admin_password():
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    data = request.get_json()
    new_password = data.get('new_password')
    username = session['user']
    if not new_password:
        return jsonify({'message': 'No password provided'}), 400
    
    # Update password in database
    user = User.query.filter_by(username=username).first()
    if user:
        user.set_password(new_password)
        db.session.commit()
        return jsonify({'message': 'Password changed!'})
    else:
        return jsonify({'message': 'User not found'}), 404

# --- USER PROFILE MANAGEMENT ---
@app.route('/api/user/profile', methods=['GET'])
def get_user_profile():
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    username = session['user']
    user = User.query.filter_by(username=username).first()
    if not user:
        return jsonify({'message': 'User not found'}), 404
    
    return jsonify({
        'username': user.username,
        'mobile': user.mobile
    })

@app.route('/api/user/username', methods=['PUT'])
def update_username():
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    data = request.get_json()
    new_username = data.get('username', '').strip()
    
    if not new_username:
        return jsonify({'message': 'Username cannot be empty'}), 400
    
    if len(new_username) < 3:
        return jsonify({'message': 'Username must be at least 3 characters'}), 400
    
    # Check if username already exists
    existing_user = User.query.filter_by(username=new_username).first()
    if existing_user and existing_user.username != session['user']:
        return jsonify({'message': 'Username already taken'}), 400
    
    # Update username
    user = User.query.filter_by(username=session['user']).first()
    if user:
        old_username = user.username
        user.username = new_username
        db.session.commit()
        
        # Update session with new username
        session['user'] = new_username
        
        return jsonify({'message': 'Username updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

@app.route('/api/user/mobile', methods=['PUT'])
def update_mobile():
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    data = request.get_json()
    new_mobile = data.get('mobile', '').strip()
    
    # Validate mobile number (basic validation for 10 digits)
    if new_mobile and not new_mobile.isdigit():
        return jsonify({'message': 'Mobile number must contain only digits'}), 400
    
    if new_mobile and len(new_mobile) != 10:
        return jsonify({'message': 'Mobile number must be 10 digits'}), 400
    
    # Update mobile number
    user = User.query.filter_by(username=session['user']).first()
    if user:
        user.mobile = new_mobile or None
        db.session.commit()
        return jsonify({'message': 'Mobile number updated successfully'})
    else:
        return jsonify({'message': 'User not found'}), 404

from flask import request, jsonify
from models import Testimonial

@app.route('/api/testimonials', methods=['POST'])
def submit_testimonial():
    data = request.get_json()
    name = data.get('name')
    address = data.get('address')
    star_rating = data.get('star_rating')
    text_review = data.get('text_review')

    if not all([name, address, star_rating, text_review]):
        return jsonify({'message': 'All fields are required'}), 400

    try:
        star_rating = int(star_rating)
        if star_rating < 1 or star_rating > 5:
            return jsonify({'message': 'Star rating must be between 1 and 5'}), 400
    except ValueError:
        return jsonify({'message': 'Invalid star rating'}), 400

    testimonial = Testimonial(
        name=name,
        address=address,
        star_rating=star_rating,
        text_review=text_review,
        is_approved=True  # Auto-approve testimonials
    )
    db.session.add(testimonial)
    db.session.commit()

    return jsonify({'message': 'Testimonial submitted successfully'})

@app.route('/api/testimonials', methods=['GET'])
def get_testimonials():
    """Get all testimonials for display on the website"""
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'address': t.address,
        'star_rating': t.star_rating,
        'text_review': t.text_review,
        'created_at': t.created_at.isoformat()
    } for t in testimonials])

@app.route('/api/admin/testimonials', methods=['GET'])
def get_all_testimonials_admin():
    """Get all testimonials for admin management"""
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    testimonials = Testimonial.query.order_by(Testimonial.created_at.desc()).all()
    return jsonify([{
        'id': t.id,
        'name': t.name,
        'address': t.address,
        'star_rating': t.star_rating,
        'text_review': t.text_review,
        'created_at': t.created_at.isoformat(),
        'is_approved': t.is_approved
    } for t in testimonials])

@app.route('/api/admin/testimonials/<int:testimonial_id>/approve', methods=['PUT'])
def approve_testimonial(testimonial_id):
    """Approve a testimonial"""
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    testimonial.is_approved = True
    db.session.commit()
    return jsonify({'message': 'Testimonial approved successfully'})

@app.route('/api/admin/testimonials/<int:testimonial_id>/reject', methods=['PUT'])
def reject_testimonial(testimonial_id):
    """Reject a testimonial"""
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    testimonial.is_approved = False
    db.session.commit()
    return jsonify({'message': 'Testimonial rejected successfully'})

@app.route('/api/admin/testimonials/<int:testimonial_id>', methods=['DELETE'])
def delete_testimonial(testimonial_id):
    """Delete a testimonial"""
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    testimonial = Testimonial.query.get_or_404(testimonial_id)
    db.session.delete(testimonial)
    db.session.commit()
    return jsonify({'message': 'Testimonial deleted successfully'})

# --- MEDIA DELETION ENDPOINTS ---
@app.route('/api/delete/<media_type>/<int:media_id>', methods=['DELETE'])
def delete_media(media_type, media_id):
    """Delete media files (images, videos, files)"""
    if 'user' not in session:
        return jsonify({'message': 'Not logged in'}), 401
    
    try:
        if media_type == 'image':
            media = ProjectImage.query.get_or_404(media_id)
        elif media_type == 'video':
            media = ProjectVideo.query.get_or_404(media_id)
        elif media_type == 'file':
            media = ProjectFile.query.get_or_404(media_id)
        else:
            return jsonify({'message': 'Invalid media type'}), 400
        
        db.session.delete(media)
        db.session.commit()
        return jsonify({'message': f'{media_type.capitalize()} deleted successfully'})
    
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': f'Error deleting {media_type}: {str(e)}'}), 500

# Vercel handler function
def handler(request):
    return app

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # This will create portfolio.db and tables
    app.run(debug=True)
