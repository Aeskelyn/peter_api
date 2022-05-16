# Setting up XPO MGMT API

1. Make sure that you've python 3 installed.
2. Clone repo
3. Create python virtual enviroment, ex. `python -m venv venv`
4. Activate your venv:
    - Windows CMD: `venv\Scripts\activate`
    - Windows PS: `venv\Scripts\activate.ps1`
    - Unix: `venv\Scripts\activate`
5. Install all required dependencies `pip install -r requirements.txt`
6. Create your database `python manage.py migrate`
7. Create your superuser _system_ for system operations on database and your _admin_ account `python manage.py createsuperuser --username [username]`
8. Run server `python manage.py runserver` 
