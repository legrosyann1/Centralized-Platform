# Centralized-Platform

REQUIREMENTS:
- Python 
- virtualenv 
- Django 
- postgresql
- python-dotenv 
- psycopg2
- djangorestframework

- Node.js/npm
- Vue CLI


STEPS:
1. Install python
2. Install virtualenv: $ pip install virtualenv
3. Create virtual environment: $ virtualenv backend
4. Activate virtual environment: $ .\backend\Scripts\activate
5. Install django in virtual environment: (backend) $ pip install django
6. Start a new django project: (backend) $ django-admin startproject backend
    - All django related commands have to be executed in the virtual environment
    - (backend) $ python manage.py runserver
    - (backend) $ python manage.py makemigrations
    - (backend) $ python manage.py migrate // syncronises settings
    - (backend) $ python manage.py createsuperuser
    - (backend) $ python manage.py startapp inventory
7. Install Postgresql
8. Connect Django to Postgresql: ENGINE, NAME, USER, PASSWORD, HOST, PORT
9. Install python-dotenv in virtual environment: (backend) $ pip install python-dotenv
10. Create .env file and create new environment variables
11. Install psycopg2: (backend) $ pip install psycopg2
12. Install djangorestframework:  (backend) $ pip install djangorestframework
13. Install node.js/npm
14. Install vue command line: $ npm install -g @vue/cli
15. Create new project: $ vue create frontend

