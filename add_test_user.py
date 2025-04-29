from website import create_app, db
from website.models import User

app = create_app()

with app.app_context():
    test_user = User(username='admin')
    test_user.set_password('password')
    db.session.add(test_user)
    db.session.commit()
    print("Test user added.")
