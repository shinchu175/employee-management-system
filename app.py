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

    return app


app = create_app()


if __name__ == "__main__":
    app.run(debug=True)