from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import PlacementDrive, Application, StudentProfile
from app.forms import StudentProfileForm
from app.decorators import student_required
from datetime import datetime

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
@student_required
def dashboard():
    # Show drives that are approved and deadline not passed
    available_drives = PlacementDrive.query.filter(
        PlacementDrive.status == 'approved',
        PlacementDrive.deadline >= datetime.utcnow()
    ).all()
    
    # Get IDs of drives already applied to
    applied_drive_ids = [app.drive_id for app in current_user.student_profile.applications]
    
    my_applications = current_user.student_profile.applications
    
    return render_template('student/dashboard.html', 
                           drives=available_drives, 
                           applied_drive_ids=applied_drive_ids,
                           my_applications=my_applications)

@student_bp.route('/apply/<int:drive_id>')
@login_required
@student_required
def apply_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    
    # Check if profile is complete (e.g. resume link exists)
    if not current_user.student_profile.resume_link:
        flash('Please complete your profile and add a resume link before applying.', 'warning')
        return redirect(url_for('student.profile'))

    # Check if already applied
    existing_application = Application.query.filter_by(student_id=current_user.student_profile.id, drive_id=drive.id).first()
    if existing_application:
        flash('You have already applied for this drive.', 'warning')
        return redirect(url_for('student.dashboard'))
        
    application = Application(
        student_id=current_user.student_profile.id,
        drive_id=drive.id
    )
    db.session.add(application)
    db.session.commit()
    flash(f'Successfully applied for {drive.job_title} at {drive.company.company_name}!', 'success')
    return redirect(url_for('student.dashboard'))

@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
@student_required
def profile():
    form = StudentProfileForm()
    if form.validate_on_submit():
        current_user.student_profile.full_name = form.full_name.data
        current_user.student_profile.cgpa = float(form.cgpa.data)
        current_user.student_profile.resume_link = form.resume_link.data
        current_user.student_profile.skills = form.skills.data
        current_user.student_profile.contact_number = form.contact_number.data
        if current_user.student_profile.contact_number:
            if len(current_user.student_profile.contact_number) !=10:
                flash('Contact number must be 10 digits', 'error')
                return redirect(url_for('student.profile'))
        db.session.commit()
        flash('Profile updated successfully!', 'success')
        return redirect(url_for('student.profile'))
    elif request.method == 'GET':
        form.full_name.data = current_user.student_profile.full_name
        form.cgpa.data = current_user.student_profile.cgpa
        form.resume_link.data = current_user.student_profile.resume_link
        form.skills.data = current_user.student_profile.skills
        
    return render_template('student/profile.html', form=form)

