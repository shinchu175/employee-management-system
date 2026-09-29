from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.employee import Employee
from models.user import User
from extensions import db
from datetime import datetime
import secrets
from sqlalchemy import or_


admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


def admin_required():
    return session.get("role") == "admin"


# =========================
# ADMIN DASHBOARD
# =========================

@admin_bp.route("/dashboard")
def dashboard():

    if not admin_required():
        return redirect(url_for("auth.login"))

    total_employees = Employee.query.count()

    return render_template(
        "admin/dashboard.html",
        total_employees=total_employees
    )


# =========================
# ADD EMPLOYEE
# =========================

@admin_bp.route("/employees/add", methods=["GET", "POST"])
def add_employee():

    if not admin_required():
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        employee_code = request.form.get("employee_code")
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        department = request.form.get("department")
        designation = request.form.get("designation")
        joining_date = request.form.get("joining_date")
        salary = request.form.get("salary")
        address = request.form.get("address")
        city = request.form.get("city")

        # Check duplicate employee code
        if Employee.query.filter_by(
            employee_code=employee_code
        ).first():

            flash(
                "Employee code already exists.",
                "danger"
            )

            return redirect(
                url_for("admin.add_employee")
            )

        # Check duplicate employee email
        if Employee.query.filter_by(
            email=email
        ).first():

            flash(
                "Employee email already exists.",
                "danger"
            )

            return redirect(
                url_for("admin.add_employee")
            )

        # Create employee
        employee = Employee(

            employee_code=employee_code,

            first_name=first_name,

            last_name=last_name,

            email=email,

            phone=phone,

            department=department,

            designation=designation,

            joining_date=datetime.strptime(
                joining_date,
                "%Y-%m-%d"
            ).date() if joining_date else None,

            salary=float(salary) if salary else None,

            address=address,

            city=city
        )

        db.session.add(employee)

        # Get employee ID
        db.session.flush()

        # Automatically create username
        username = employee_code.lower()

        # Generate temporary password
        temporary_password = secrets.token_urlsafe(8)

        # Create employee login
        user = User(

            username=username,

            email=email,

            role="employee",

            employee_id=employee.id
        )

        user.set_password(temporary_password)

        db.session.add(user)

        db.session.commit()

        flash(
            f"Employee created! "
            f"Login: {username} | "
            f"Temporary password: {temporary_password}",
            "success"
        )

        return redirect(
            url_for("admin.employees")
        )

    return render_template(
        "admin/add_employee.html"
    )


# =========================
# VIEW ALL EMPLOYEES
# =========================
@admin_bp.route("/employees")
def employees():

    if not admin_required():
        return redirect(url_for("auth.login"))

    search = request.args.get("search", "").strip()

    sort = request.args.get("sort", "id")
    order = request.args.get("order", "desc")

    page = request.args.get("page", 1, type=int)

    query = Employee.query

    # Search
    if search:
        query = query.filter(
            or_(
                Employee.first_name.ilike(f"%{search}%"),
                Employee.last_name.ilike(f"%{search}%"),
                Employee.employee_code.ilike(f"%{search}%"),
                Employee.email.ilike(f"%{search}%")
            )
        )

    # Sorting
    sort_columns = {
        "id": Employee.id,
        "code": Employee.employee_code,
        "name": Employee.first_name,
        "email": Employee.email,
        "department": Employee.department,
        "designation": Employee.designation
    }

    sort_column = sort_columns.get(
        sort,
        Employee.id
    )

    if order == "asc":
        query = query.order_by(sort_column.asc())
    else:
        query = query.order_by(sort_column.desc())

    # Pagination
    employees = query.paginate(
        page=page,
        per_page=5,
        error_out=False
    )

    return render_template(
        "admin/employees.html",
        employees=employees,
        search=search,
        sort=sort,
        order=order
    )

# =========================
# VIEW ONE EMPLOYEE
# =========================

@admin_bp.route("/employees/<int:employee_id>")
def view_employee(employee_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    employee = Employee.query.get_or_404(
        employee_id
    )

    return render_template(
        "admin/view_employee.html",

        employee=employee
    )


# =========================
# EDIT EMPLOYEE
# =========================

@admin_bp.route(
    "/employees/<int:employee_id>/edit",
    methods=["GET", "POST"]
)
def edit_employee(employee_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    employee = Employee.query.get_or_404(
        employee_id
    )

    if request.method == "POST":

        new_email = request.form.get("email")

        # Check if another employee already uses this email
        existing_employee = Employee.query.filter(
            Employee.email == new_email,
            Employee.id != employee.id
        ).first()

        if existing_employee:

            flash(
                "Another employee already uses this email.",
                "danger"
            )

            return redirect(
                url_for(
                    "admin.edit_employee",
                    employee_id=employee.id
                )
            )

        employee.first_name = request.form.get(
            "first_name"
        )

        employee.last_name = request.form.get(
            "last_name"
        )

        employee.email = new_email

        employee.phone = request.form.get(
            "phone"
        )

        employee.department = request.form.get(
            "department"
        )

        employee.designation = request.form.get(
            "designation"
        )

        employee.address = request.form.get(
            "address"
        )

        employee.city = request.form.get(
            "city"
        )

        # Joining date
        joining_date = request.form.get(
            "joining_date"
        )

        if joining_date:

            employee.joining_date = datetime.strptime(
                joining_date,
                "%Y-%m-%d"
            ).date()

        # Salary
        salary = request.form.get(
            "salary"
        )

        if salary:

            employee.salary = float(
                salary
            )

        # Update login email also
        user = User.query.filter_by(
            employee_id=employee.id
        ).first()

        if user:

            user.email = new_email

        db.session.commit()

        flash(
            "Employee updated successfully.",
            "success"
        )

        return redirect(
            url_for(
                "admin.view_employee",
                employee_id=employee.id
            )
        )

    return render_template(
        "admin/edit_employee.html",

        employee=employee
    )


# =========================
# DELETE EMPLOYEE
# =========================

@admin_bp.route(
    "/employees/<int:employee_id>/delete",
    methods=["POST"]
)
def delete_employee(employee_id):

    if not admin_required():
        return redirect(url_for("auth.login"))

    employee = Employee.query.get_or_404(
        employee_id
    )

    # Find employee login
    user = User.query.filter_by(
        employee_id=employee.id
    ).first()

    # Delete login first
    if user:

        db.session.delete(user)

    # Delete employee
    db.session.delete(employee)

    db.session.commit()

    flash(
        "Employee deleted successfully.",
        "success"
    )

    return redirect(
        url_for("admin.employees")
    )