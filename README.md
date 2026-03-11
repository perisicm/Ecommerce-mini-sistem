# Ecommerce Mini System (Demo Application)

This is a demo full stack web application for selling online development courses built with the Flask framework.

The project was created for learning and portfolio purposes. It demonstrates authentication, role-based access control, cart management, and an admin dashboard, but it is not intended for production use.

---

## Features

- User registration and login system
- Secure password hashing
- Session-based shopping cart
- Course purchasing simulation
- User budget tracking
- Admin panel with role-based access
- Add and delete courses (admin only)
- Dashboard statistics:
  - Total users
  - Total courses
  - Total revenue
  - Top 3 users by spending
- Form validation with custom error messages
- Responsive UI built with Bootstrap 5

---

## Technologies Used

- Python
- Flask
- Flask-SQLAlchemy
- Flask-Login
- Flask-WTF
- SQLite
- Bootstrap 5
- HTML
- CSS

---

## Project Structure

## Installation and Setup
Follow these steps to run the project locally.

### 1. Clone the repository

bash
git clone https://github.com/perisicm/Ecommerce-mini-sistem.git
cd Ecommerce-mini-sistem

### 2. Create virtual environment

bash
python -m venv venv

Activate the environment:

Windows
bash
venv\Scripts\activate
Linux / Mac
bash
source venv/bin/activate

### 3. Install dependencies

bash
pip install -r requirements.txt

### 4. Create database

Run migrations to create the database and tables:
bash
flask db upgrade

### 5. Run the application

bash
python app.py

### 6. Open in browser

Open the following address in your browser:
http://127.0.0.1:5000
