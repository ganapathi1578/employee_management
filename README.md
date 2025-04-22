# 🧑‍💼 Employee Management System

A simple Django-based web application to manage employee records — including creating, updating, deleting, and viewing employee details.

---

## 🚀 Features

- 🔍 View all employee records
- ➕ Add new employees
- 📝 Update employee information
- ❌ Delete employee records
- 💾 Uses SQLite for backend database
- 🌐 Built with Django, HTML, CSS, and JavaScript

---

## 🛠️ Tech Stack

- **Backend**: Python, Django
- **Frontend**: HTML, CSS, JavaScript
- **Database**: SQLite
- **Platform**: Web

---

## 🧩 Installation Guide

Follow these steps to run the project locally:

```bash
# 1. Clone the repository
git clone https://github.com/ganapathi1578/employee_management.git

# 2. Navigate into the project directory
cd employee_management

# 3. Create a virtual environment (optional but recommended)
python -m venv env

# 4. Activate the virtual environment
#    On macOS/Linux:
source env/bin/activate
#    On Windows:
# env\Scripts\activate

# 5. Install required dependencies
pip install -r requirements.txt

# 6. Apply migrations to set up the database
python manage.py migrate

# 7. Run the development server
python manage.py runserver

# 8. Open the application in your browser
#    Visit: http://127.0.0.1:8000/
