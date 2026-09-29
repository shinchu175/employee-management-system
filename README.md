# Employee Management System

A role-based Employee Management System built using Flask, MySQL, SQLAlchemy, Bootstrap, and JavaScript.

## Features

### Admin
- Admin login
- Dashboard with total employee count
- Add employees
- Automatically create employee login credentials
- View all employees
- Search employees
- Sort employee records
- Pagination
- View complete employee details
- Edit employee details
- Delete employees
- Employee login account management
- Logout

### Employee
- Employee login
- View own profile
- Edit allowed profile information
- Change password
- Logout

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- MySQL
- PyMySQL
- HTML5
- CSS3
- Bootstrap 5
- JavaScript
- Werkzeug Password Hashing

## Project Structure

```text
employee_management_system/
│
├── app.py
├── config.py
├── extensions.py
├── create_admin.py
├── requirements.txt
├── .env.example
├── .gitignore
│
├── models/
│   ├── __init__.py
│   ├── user.py
│   └── employee.py
│
├── routes/
│   ├── __init__.py
│   ├── auth.py
│   ├── admin.py
│   └── employee.py
│
├── templates/
│   ├── base.html
│   ├── login.html
│   ├── admin/
│   └── employee/
│
└── static/
    ├── css/
    │   └── style.css
    └── js/
        └── script.js