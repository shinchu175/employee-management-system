import os

from flask import Flask

from config import Config
from extensions import db


def create_app():

    app = Flask(__name__)

    app.config.from_object(Config)

    db.init_app(app)

    from models.employee import Employee
    from models.user import User

    from routes.auth import auth_bp
    from routes.admin import admin_bp
    from routes.employee import employee_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(admin_bp)
    app.register_blueprint(employee_bp)

    with app.app_context():

        db.create_all()

        # Create default admin account if no admin exists
        existing_admin = User.query.filter_by(
            role="admin"
        ).first()

        if not existing_admin:

            admin_username = os.getenv(
                "ADMIN_USERNAME"
            )

            admin_email = os.getenv(
                "ADMIN_EMAIL"
            )

            admin_password = os.getenv(
                "ADMIN_PASSWORD"
            )

            if (
                admin_username
                and admin_email
                and admin_password
            ):

                admin = User(
                    username=admin_username,
                    email=admin_email,
                    role="admin"
                )

                admin.set_password(
                    admin_password
                )

                db.session.add(admin)
                db.session.commit()

                print("Default admin account created.")

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)