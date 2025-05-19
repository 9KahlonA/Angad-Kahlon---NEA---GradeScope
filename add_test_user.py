from website import create_app, db 
from website.models import User # Import the User model from models.py

app = create_app()

with app.app_context():
    # Determine the next available user_id
    max_user = db.session.query(db.func.max(User.user_id)).scalar()  # Use user_id instead of id
    next_user_id = 1 if max_user is None else max_user + 1

    # Create a test user
    test_user = User(user_id=next_user_id, username='admin')  # Use user_id instead of id
    test_user.set_password('password')  # Replace 'password' with your desired password
    db.session.add(test_user)
    db.session.commit()
    print(f"Test user added: user_id={next_user_id}, username='admin', password='password'")