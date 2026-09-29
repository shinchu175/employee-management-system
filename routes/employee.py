from flask import Blueprint, render_template, session, redirect, url_for, request, flash
from models.user import User
from extensions import db


employee_bp = Blueprint(
    "employee",
    __name__,
    url_prefix="/employee"
)


# =========================
# EMPLOYEE LOGIN CHECK
# =========================

def employee_required():

    return (
        session.get("role") == "employee"
        and session.get("user_id") is not None
    )


# =========================
# EMPLOYEE DASHBOARD
# =========================

@employee_bp.route("/dashboard")
def dashboard():

    if not employee_required():
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user or not user.employee:
        session.clear()
        flash("Employee account not found.", "danger")
        return redirect(url_for("auth.login"))

    employee = user.employee

    return render_template(
        "employee/dashboard.html",
        employee=employee
    )


# =========================
# VIEW OWN PROFILE
# =========================

@employee_bp.route("/profile")
def profile():

    if not employee_required():
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user or not user.employee:
        session.clear()
        flash("Employee account not found.", "danger")
        return redirect(url_for("auth.login"))

    employee = user.employee

    return render_template(
        "employee/profile.html",
        employee=employee
    )


# =========================
# EDIT OWN PROFILE
# =========================

@employee_bp.route(
    "/profile/edit",
    methods=["GET", "POST"]
)
def edit_profile():

    if not employee_required():
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user or not user.employee:
        session.clear()
        flash("Employee account not found.", "danger")
        return redirect(url_for("auth.login"))

    employee = user.employee

    if request.method == "POST":

        # Employee can edit only these fields
        employee.phone = request.form.get("phone")
        employee.address = request.form.get("address")
        employee.city = request.form.get("city")

        db.session.commit()

        flash(
            "Profile updated successfully.",
            "success"
        )

        return redirect(
            url_for("employee.profile")
        )

    return render_template(
        "employee/edit_profile.html",
        employee=employee
    )


# =========================
# CHANGE PASSWORD
# =========================

@employee_bp.route(
    "/change-password",
    methods=["GET", "POST"]
)
def change_password():

    if not employee_required():
        return redirect(url_for("auth.login"))

    user = User.query.get(session["user_id"])

    if not user:
        session.clear()
        return redirect(url_for("auth.login"))

    if request.method == "POST":

        current_password = request.form.get(
            "current_password"
        )

        new_password = request.form.get(
            "new_password"
        )

        confirm_password = request.form.get(
            "confirm_password"
        )

        # Check current password
        if not user.check_password(
            current_password
        ):

            flash(
                "Current password is incorrect.",
                "danger"
            )

            return redirect(
                url_for("employee.change_password")
            )

        # Check new password
        if len(new_password) < 6:

            flash(
                "New password must be at least 6 characters.",
                "danger"
            )

            return redirect(
                url_for("employee.change_password")
            )

        # Check confirmation
        if new_password != confirm_password:

            flash(
                "New passwords do not match.",
                "danger"
            )

            return redirect(
                url_for("employee.change_password")
            )

        # Update password
        user.set_password(new_password)

        db.session.commit()

        flash(
            "Password changed successfully.",
            "success"
        )

        return redirect(
            url_for("employee.dashboard")
        )

    return render_template(
        "employee/change_password.html"
    )