# Centralized-Platform

Requirements:
1. Python 3.8 + pip 
2. PostgreSQL 10 
3. node.js 
4. npm 
4. Redis 
5. Ansible 
6. virtualenv

Deployement:
1. Make virtual environment -> virtualenv <name>
2. Activate virtual environment -> source <name>/bin/activate
3. pip install -r requirements.txt
4. create new database in PostgreSQL -> CREATE DATABASE <name>
5. create .env file and fill variables:
    SQL_ENGINE=django.db.backends.postgresql_psycopg2
    SQL_DATABASE=
    SQL_USER=
    SQL_PASSWORD=
    SQL_HOST=
    SQL_PORT=
    DJANGO_ALLOWED_HOSTS=
    DJANGO_KEY=
    EMAIL_USER=
6. npm install 
7. npm install -g n
8. n lts
7. python3 manage.py makemigrations
8. python3 manage.py migrate
9. python3 manage.py createsuperuser

Run:
- Backend: python3 manage.py runserver
- Frontend: npm run serve