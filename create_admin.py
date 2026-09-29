from app import app, db
from models.user import User


with app.app_context():

    existing_admin = User.query.filter_by(role="admin").first()

    if existing_admin:
        print("Admin account already exists.")
    else:

        admin = User(
            username="admin",
            email="admin@example.com",
            role="admin"
        )

        admin.set_password("Admin@123")

        db.session.add(admin)
        db.session.commit()

        print("Admin account created successfully!")
        print("Username: admin")
        print("Password: Admin@123")