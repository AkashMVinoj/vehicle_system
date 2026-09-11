# 🚗 Vehicle Inventory & Booking REST API

A production-style Backend REST API for managing vehicle inventory and handling automated customer bookings with real-time validation and dynamic pricing computation.

Built for **Django Developer Machine Test**.

---

## 🎯 Objective

Build a complete Vehicle Inventory & Booking REST API using Django REST Framework that demonstrates strong backend development skills, proper API structuring, data validation, and the ability to implement business logic within a real-world application scenario.

---

## 🌟 Key Features

- **Vehicle Management:** Full CRUD operations for managing vehicles.
- **Advanced Filtering:** Filter vehicles dynamically by `brand`, `fuel_type`, and `is_available`.
- **Automatic Pricing Engine:** Dynamically calculates `total_amount = (end_date - start_date) * price_per_day`.
- **Double-Booking Protection:** Advanced temporal ORM query prevents overlapping date reservations for the same vehicle.
- **Strict Validation Rules:**
  - Phone number must contain **exactly 10 digits**.
  - Start date cannot be in the past.
  - End date must be strictly after the start date.
- **Automatic Status Updates:** Sets `is_available = False` automatically upon successful reservation.
- **Interactive API Docs:** Built-in Swagger UI (`/api/docs/`) & ReDoc using `drf-spectacular`.

---

## 🛠️ Tech Stack

- **Language:** Python 3.10+
- **Framework:** Django 4.2+ & Django REST Framework (DRF)
- **Database:** PostgreSQL (Production) / SQLite (Local Development)
- **Documentation:** `drf-spectacular` (OpenAPI 3.0)
- **Filtering:** `django-filter`
- **WSGI Server:** Gunicorn

---

## 🚀 Local Project Setup

Follow these steps to set up and run the project locally.

### 1. Clone the Repository
```bash
git clone <your-github-repository-url>
cd vehicle_system

2. Set Up Virtual Environment
Bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python -m venv venv
source venv/bin/activate

3. Install Dependencies
pip install -r requirements.txt

5. Run Database Migrations
python manage.py makemigrations
python manage.py migrate

6. Create Superuser (Django Admin)

python manage.py createsuperuser

7. Run Local Development Server
python manage.py runserver


GOOGLE DRIVE LINK 

https://drive.google.com/file/d/13Ue4e_1AmT2w22Q0XgNFRiB2yavo5lUU/view?usp=drive_link 