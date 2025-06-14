# Lost 2 Cause Backend

## Setup
1. Clone repo
2. Create virtual environment: `python -m venv venv`
3. Activate: `source venv/bin/activate` (Linux/Mac) or `venv\Scripts\activate` (Windows)
4. Install requirements: `pip install -r requirements.txt`
5. Initialize DB: `python init_db.py`
6. Run: `python run.py`


# API Documentation

## Authentication
- `POST /register` - Register new user
- `POST /login` - Login user
- `POST /logout` - Logout user
- `GET /user` - Get current user

