#LOST 2 CAUSE BACKEND SETUP GUIDE

1. CLONE REPOSITORY
git clone https://github.com/yourusername/Lost-2-Cause.git
cd Lost-2-Cause

2. SETUP VIRTUAL ENVIRONMENT
python -m venv venv
venv\Scripts\activate  (Windows)
source venv/bin/activate  (Mac/Linux)

3. INSTALL DEPENDENCIES
pip install -r requirements.txt

4. CONFIGURE ENVIRONMENT
Create .env file with:
SECRET_KEY=your_random_secret_key_here
DATABASE_URL=sqlite:///site.db

5. INITIALIZE DATABASE
python init_db.py

6. RUN SERVER
python run.py

#API ENDPOINTS:
- POST /register {first_name, last_name, email, password, confirm_password}
- POST /login {email, password}
- GET /user (requires login)
- POST /logout

#SERVER RUNS ON: http://localhost:5000

#TROUBLESHOOTING:
- Delete instance/site.db and rerun init_db.py if database errors occur
- Ensure .env file exists if getting configuration errors
- Reactivate virtual environment if packages aren't found
