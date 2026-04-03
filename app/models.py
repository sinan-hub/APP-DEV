from datetime import datetime
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(120), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    role = db.Column(db.String(20), nullable=False)  # 'admin', 'company', 'student'
    is_active = db.Column(db.Boolean, default=True) # Used for approval logic (default True for student, False for company)

    # Relationships
    company_profile = db.relationship('CompanyProfile', backref='user', uselist=False)
    student_profile = db.relationship('StudentProfile', backref='user', uselist=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return f'<User {self.username}>'

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class CompanyProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    company_name = db.Column(db.String(100), nullable=False)
    website = db.Column(db.String(200))
    location = db.Column(db.String(100))
    description = db.Column(db.Text)
    hr_contact = db.Column(db.String(100))
    approval_status = db.Column(db.String(20), default='pending')
    # Drives relationship
    drives = db.relationship('PlacementDrive', backref='company', lazy='dynamic')

class StudentProfile(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    full_name = db.Column(db.String(100), nullable=False)
    cgpa = db.Column(db.Float)
    resume_link = db.Column(db.String(200)) # URL to resume
    skills = db.Column(db.String(200))
    contact_number = db.Column(db.String(10))
    place_of_residence = db.Column(db.String(200))
    approval_status = db.Column(db.String(20), default='pending')
    # Applications relationship
    applications = db.relationship('Application', backref='student', lazy='dynamic')

class PlacementDrive(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('company_profile.id'), nullable=False)
    job_title = db.Column(db.String(100), nullable=False)
    job_description = db.Column(db.Text, nullable=False)
    criteria = db.Column(db.Text) # Eligibility criteria
    salary = db.Column(db.String(50))
    location = db.Column(db.String(100))
    status = db.Column(db.String(20), default='pending') # 'pending', 'approved', 'rejected'
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    deadline = db.Column(db.DateTime)
    
    # Applications for this drive
    applications = db.relationship('Application', backref='drive', lazy='dynamic')

class Application(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student_profile.id'), nullable=False)
    drive_id = db.Column(db.Integer, db.ForeignKey('placement_drive.id'), nullable=False)
    date_applied = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='applied') # 'applied', 'shortlisted', 'selected', 'rejected'
