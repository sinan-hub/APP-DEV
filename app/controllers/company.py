from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import PlacementDrive, Application, StudentProfile
from app.forms import DriveForm
from app.decorators import company_required
from datetime import datetime

company_bp = Blueprint('company', __name__, url_prefix='/company')

@company_bp.route('/dashboard')
@login_required
@company_required
def dashboard():
    drives = PlacementDrive.query.filter_by(company_id=current_user.company_profile.id).all()
    return render_template('company/dashboard.html', drives=drives)

@company_bp.route('/create_drive', methods=['GET', 'POST'])
@login_required
@company_required
def create_drive():
    form = DriveForm()
    if form.validate_on_submit():
        try:
            deadline_date = datetime.strptime(form.deadline.data, '%Y-%m-%d')
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return render_template('company/create_drive.html', form=form)

        drive = PlacementDrive(
            company_id=current_user.company_profile.id,
            job_title=form.job_title.data,
            job_description=form.job_description.data,
            criteria=form.criteria.data,
            salary=form.salary.data,
            location=form.location.data,
            deadline=deadline_date,
            status='pending' # Default status
        )
        db.session.add(drive)
        db.session.commit()
        flash('Placement Drive Created! Pending Admin Approval.', 'success')
        return redirect(url_for('company.dashboard'))
    return render_template('company/create_drive.html', form=form)

@company_bp.route('/drive/<int:drive_id>/applications')
@login_required
@company_required
def view_applications(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    # Ensure company owns this drive
    if drive.company_id != current_user.company_profile.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('company.dashboard'))
    
    applications = Application.query.filter_by(drive_id=drive.id).all()
    return render_template('company/applications.html', drive=drive, applications=applications)

@company_bp.route('/application/<int:app_id>/update/<string:status>')
@login_required
@company_required
def update_application_status(app_id, status):
    application = Application.query.get_or_404(app_id)
    # Ensure company owns the drive for this application
    if application.drive.company_id != current_user.company_profile.id:
        flash('Unauthorized access.', 'danger')
        return redirect(url_for('company.dashboard'))
        
    if status in ['shortlisted', 'selected', 'rejected']:
        application.status = status
        db.session.commit()
        flash(f'Student status updated to {status}.', 'success')
    else:
        flash('Invalid status.', 'danger')
        
    return redirect(url_for('company.view_applications', drive_id=application.drive.id))
