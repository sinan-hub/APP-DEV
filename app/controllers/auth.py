from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from app import db
from app.models import User, CompanyProfile, StudentProfile
from app.forms import LoginForm, RegistrationForm

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin.dashboard')) # Placeholder
        elif current_user.role == 'company':
            return redirect(url_for('company.dashboard')) # Placeholder
        elif current_user.role == 'student':
            return redirect(url_for('student.dashboard')) # Placeholder
        
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and user.check_password(form.password.data):
            if not user.is_active:
               flash('Your account is waiting for approval.', 'warning')
               return redirect(url_for('auth.login'))
               
            login_user(user)
            flash('Login successful!', 'success')
            
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
                
            if user.role == 'admin':
                return redirect(url_for('admin.dashboard')) # Placeholder
            elif user.role == 'company':
                return redirect(url_for('company.dashboard')) # Placeholder
            elif user.role == 'student':
                return redirect(url_for('student.dashboard')) # Placeholder
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('auth.login'))
        
    form = RegistrationForm()
    if form.validate_on_submit():
        if form.role.data == 'company':
            user = User(username=form.username.data, email=form.email.data, role='company', is_active=False) # Company needs approval
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            company = CompanyProfile(
                user_id=user.id,
                company_name=form.company_name.data,
                website=form.website.data,
                location=form.location.data,
                description=form.description.data,
                hr_contact=form.hr_contact.data,
                approval_status='pending'
            )
            db.session.add(company)
            db.session.commit()
            
            flash('Company account created! Please wait for admin approval.', 'info')
            return redirect(url_for('auth.login'))
            
        elif form.role.data == 'student':
            user = User(username=form.username.data, email=form.email.data, role='student', is_active=False) # Student needs approval
            user.set_password(form.password.data)
            db.session.add(user)
            db.session.commit()
            
            student = StudentProfile(
                user_id=user.id,
                full_name=form.full_name.data,
                contact_number=form.contact_number.data,
                place_of_residence=form.place_of_residence.data,
                approval_status='pending'
            )
            db.session.add(student)
            db.session.commit()
            
            flash('Student account created! Please wait for admin approval.', 'info')
            return redirect(url_for('auth.login'))
            
    return render_template('auth/register.html', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))
