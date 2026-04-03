from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from app import db
from app.models import User, CompanyProfile, StudentProfile, PlacementDrive
from app.decorators import admin_required

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_companies = User.query.filter_by(role='company').count()
    total_drives = PlacementDrive.query.count()
    
    pending_companies = User.query.join(CompanyProfile).filter(User.role=='company', CompanyProfile.approval_status=='pending').all()
    pending_students = User.query.join(StudentProfile).filter(User.role=='student', StudentProfile.approval_status=='pending').all()
    pending_drives = PlacementDrive.query.filter_by(status='pending').all()
    
    return render_template('admin/dashboard.html', 
                           total_students=total_students,
                           total_companies=total_companies,
                           total_drives=total_drives,
                           pending_companies=pending_companies,
                           pending_students=pending_students,
                           pending_drives=pending_drives)

@admin_bp.route('/approve_company/<int:user_id>')
@login_required
@admin_required
def approve_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        user.is_active = True
        if user.company_profile:
            user.company_profile.approval_status = 'approved'
        db.session.commit()
        flash(f'Company {user.company_profile.company_name} approved!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject_company/<int:user_id>')
@login_required
@admin_required
def reject_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        if user.company_profile:
            user.company_profile.approval_status = 'rejected'
        db.session.commit()
        flash('Company registration rejected.', 'danger')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/approve_drive/<int:drive_id>')
@login_required
@admin_required
def approve_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'approved'
    db.session.commit()
    flash(f'Drive {drive.job_title} approved!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject_drive/<int:drive_id>')
@login_required
@admin_required
def reject_drive(drive_id):
    drive = PlacementDrive.query.get_or_404(drive_id)
    drive.status = 'rejected'
    db.session.commit()
    flash(f'Drive {drive.job_title} rejected!', 'danger')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/students')
@login_required
@admin_required
def list_students():
    students = StudentProfile.query.all()
    return render_template('admin/students.html', students=students)

@admin_bp.route('/approve_student/<int:user_id>')
@login_required
@admin_required
def approve_student(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'student':
        user.is_active = True
        if user.student_profile:
            user.student_profile.approval_status = 'approved'
        db.session.commit()
        flash(f'Student {user.student_profile.full_name} approved!', 'success')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/reject_student/<int:user_id>')
@login_required
@admin_required
def reject_student(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'student':
        if user.student_profile:
            user.student_profile.approval_status = 'rejected'
        db.session.commit()
        flash('Student registration rejected.', 'danger')
    return redirect(url_for('admin.dashboard'))

@admin_bp.route('/companies')
@login_required
@admin_required
def list_companies():
    companies = CompanyProfile.query.all()
    return render_template('admin/companies.html', companies=companies)

@admin_bp.route('/blacklist_student/<int:user_id>')
@login_required
@admin_required
def blacklist_student(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'student':
        user.is_active = False
        if user.student_profile:
            user.student_profile.approval_status = 'blacklisted'
        db.session.commit()
        flash(f'Student {user.student_profile.full_name} blacklisted!', 'danger')
    return redirect(url_for('admin.list_students'))

@admin_bp.route('/blacklist_company/<int:user_id>')
@login_required
@admin_required
def blacklist_company(user_id):
    user = User.query.get_or_404(user_id)
    if user.role == 'company':
        user.is_active = False
        if user.company_profile:
            user.company_profile.approval_status = 'blacklisted'
        db.session.commit()
        flash(f'Company {user.company_profile.company_name} blacklisted!', 'danger')
    return redirect(url_for('admin.list_companies'))

