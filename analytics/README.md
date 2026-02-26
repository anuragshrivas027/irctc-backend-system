# IRCTC Mini Backend System

## Project Overview

This project is a simplified IRCTC backend system built using Django REST Framework.  
It supports user authentication, train management, seat booking, search logging, and analytics.

The system uses two databases:
- MySQL for transactional data (users, trains, bookings)
- MongoDB for logging and analytics (train search history and aggregation)

This project demonstrates clean API design, role-based access control, and separation of transactional and analytical workloads.

---

## Tech Stack

Backend:
- Django
- Django REST Framework (DRF)

Databases:
- MySQL (Transactional Data)
- MongoDB (Search Logs & Analytics)

Authentication:
- JWT (djangorestframework-simplejwt)

API Documentation:
- Swagger (drf-yasg)

Environment Configuration:
- python-dotenv (.env based configuration)

---

## Features Implemented

### 1. User Authentication

POST /api/register/  
POST /api/login/

- Users can register and log in.
- Login returns JWT access and refresh tokens.
- All protected endpoints require:

Authorization: Bearer <access_token>

Role-based access:
- Admin users can create trains and access analytics.
- Normal users can search and book trains.

---

### 2. Train Management (Admin Only)

POST /api/trains/create/

Admin can:
- Create trains
- Set train number (unique)
- Define source and destination
- Set departure and arrival times
- Set total seats and available seats

Train number is unique to prevent duplicates.

---

### 3. Train Search

GET /api/trains/search/?source=&destination=

- Users can search trains between two stations.
- Search is case-insensitive.
- Each search request is logged in MongoDB.
- Logged data includes:
  - user_id
  - source
  - destination
  - execution time
  - timestamp

---

### 4. Booking System

POST /api/bookings/create/

- Users select train ID and number of seats.
- System checks seat availability.
- If seats are available:
  - Seats are deducted.
  - Booking record is created.
- If seats are not available:
  - Request is rejected with error message.

Atomic transactions are used to prevent overbooking and race conditions.

---

### 5. My Bookings

GET /api/bookings/my/

- Returns only the bookings of the currently logged-in user.
- Ensures user-level data isolation.

---

### 6. Analytics (Admin Only)

GET /api/analytics/top-routes/

- Uses MongoDB aggregation pipeline.
- Groups search logs by source and destination.
- Returns top 5 most searched routes.
- Demonstrates NoSQL aggregation capability.

---

## Project Structure

irctc_backend/
│
├── config/               # Django project settings
├── users/                # Authentication app
├── trains/               # Train management
├── bookings/             # Booking logic
├── analytics/            # MongoDB aggregation
├── config/utils/         # MongoDB connection utility
│
├── manage.py
├── requirements.txt
├── .env.example
├── README.md

---

## Setup Instructions

1. Clone the repository

git clone <repository_url>  
cd irctc_backend  

2. Create virtual environment

python -m venv venv  
venv\Scripts\activate  

3. Install dependencies

pip install -r requirements.txt  

4. Create .env file

SECRET_KEY=your_secret_key  
DB_NAME=irctc_db  
DB_USER=root  
DB_PASSWORD=your_mysql_password  
DB_HOST=127.0.0.1  
DB_PORT=3306  

Ensure MySQL and MongoDB services are running.

5. Apply migrations

python manage.py migrate  

6. Create admin user

python manage.py createsuperuser  

7. Run server

python manage.py runserver  

---

## API Documentation

Swagger UI is available at:

http://127.0.0.1:8000/swagger/

Swagger provides:
- Interactive API testing
- Request and response schema
- Authentication testing with JWT

---

## Security Practices

- No hardcoded passwords in settings.py
- All sensitive data stored in .env
- .env excluded using .gitignore
- JWT-based authentication
- Role-based permission control
- Atomic transactions for booking safety

---

## Key Technical Highlights

- Dual database architecture (MySQL + MongoDB)
- Transaction-safe seat booking
- Role-based access control
- MongoDB aggregation pipeline for analytics
- Clean modular Django app structure
- Environment-based configuration

---

Sample Test Credentials

Admin:
username: admin
password: 12345

User:
username: testuser
password: ****

---

## Conclusion

This project demonstrates backend architecture design, authentication and authorization handling, database modeling, transaction management, logging strategy, and analytics implementation using both relational and NoSQL databases.

The system is fully functional and ready for demonstration or evaluation.