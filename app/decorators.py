from functools import wraps
from flask import abort
from flask_login import current_user

# Check if user is admin
def admin_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)  # not logged in
        if current_user.role != 'admin':
            abort(403)  # not an admin
        return func(*args, **kwargs)  # run the original function
    return wrapper

# Check if user is company
def company_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)  # not logged in
        if current_user.role != 'company':
            abort(403)  # not a company
        if not current_user.is_active:
            abort(403, description="Account not approved yet.")  # company not approved
        return func(*args, **kwargs)
    return wrapper

# Check if user is student
def student_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(403)  # not logged in
        if current_user.role != 'student':
            abort(403)  # not a student
        return func(*args, **kwargs)
    return wrapper
