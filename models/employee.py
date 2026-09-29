from datetime import datetime
from extensions import db


class Employee(db.Model):
    __tablename__ = "employees"

    id = db.Column(db.Integer, primary_key=True)

    employee_code = db.Column(
        db.String(20),
        unique=True,
        nullable=False
    )

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)

    email = db.Column(
        db.String(100),
        unique=True,
        nullable=False
    )

    phone = db.Column(db.String(15))

    department = db.Column(db.String(50))
    designation = db.Column(db.String(50))

    joining_date = db.Column(db.Date)

    salary = db.Column(db.Float)

    address = db.Column(db.String(255))
    city = db.Column(db.String(50))

    created_at = db.Column(
        db.DateTime,
        default=datetime.utcnow
    )

    user = db.relationship(
        "User",
        back_populates="employee",
        uselist=False
    )