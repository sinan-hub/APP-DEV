from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, EqualTo, Length, ValidationError, URL, Optional
from app.models import User

def prepend_http(url):
    if url and not url.startswith(('http://', 'https://')):
        return 'https://' + url
    return url

class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    role = SelectField('Role', choices=[('student', 'Student'), ('company', 'Company')], validators=[DataRequired()])
    
    # Specific fields for Company
    company_name = StringField('Company Name', validators=[Optional()])
    website = StringField('Website', validators=[Optional(), URL()], filters=[prepend_http])
    location = StringField('Location', validators=[Optional()])
    description = TextAreaField('Description', validators=[Optional()])
    hr_contact = StringField('HR Contact Name/Email', validators=[Optional()])

    # Specific fields for Student
    full_name = StringField('Full Name', validators=[Optional()])
    contact_number = StringField('Contact Number', validators=[Optional(), Length(max=10)])
    place_of_residence = StringField('Place of Residence', validators=[Optional(), Length(max=200)])
    
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')

class DriveForm(FlaskForm):
    job_title = StringField('Job Title', validators=[DataRequired(), Length(min=2, max=100)])
    job_description = TextAreaField('Job Description', validators=[DataRequired()])
    criteria = TextAreaField('Eligibility Criteria', validators=[DataRequired()])
    salary = StringField('Salary Package (e.g., 10 LPA)', validators=[DataRequired()])
    location = StringField('Job Location', validators=[DataRequired()])
    deadline = StringField('Application Deadline (YYYY-MM-DD)', validators=[DataRequired()]) # Simple string for now, could be DateField
    submit = SubmitField('Create Drive')

class StudentProfileForm(FlaskForm):
    full_name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    cgpa = StringField('CGPA', validators=[DataRequired()]) # FloatField can be tricky with some browsers/locales
    resume_link = StringField('Resume Link (Google Drive/Dropbox)', validators=[DataRequired(), URL()], filters=[prepend_http])
    skills = StringField('Skills (comma separated)', validators=[Optional()])
    contact_number = StringField('Contact Number', validators=[Optional(), Length(max=10)])
    place_of_residence = StringField('Place of Residence', validators=[Optional(), Length(max=200)])
    submit = SubmitField('Update Profile')
