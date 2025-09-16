from website import create_app, db 
from website.models import User

app = create_app()

with app.app_context():
    max_user = db. session .query(db. func . max(User. user_id)). scalar()
    next_user_id = 1 if max_user is None else max_user + 1

    test_user = User(user_id =next_user_id ,username = 'admin')
    test_user. set_password('password')
    db.session.add(test_user)
    db.session.commit()
    print(f"Test user added: user_id={next_user_id}, username='admin', password='password'")