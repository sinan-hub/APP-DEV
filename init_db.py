from app import create_app, db
from app.models import User

app = create_app()

with app.app_context():
    db.create_all()
    
    # Check if admin exists
    if not User.query.filter_by(role='admin').first():
        admin = User(
            username='admin',
            email='admin@institute.edu',
            role='admin',
            is_active=True
        )
        admin.set_password('admin123')
        db.session.add(admin)
        db.session.commit()
        print("Database initialized and Admin user created.")
    else:
        print("Database already initialized.")
