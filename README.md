# Centralized-Platform

REQUIREMENTS:
- Python 
- virtualenv 
- Django 
- postgresql
- python-dotenv 
- psycopg2
- djangorestframework
- django-cors-headers
- djangorestframework-jwt
- channels
- celery
- redis

- Node.js/npm
- Vue CLI
- router
- axios
- vuetify
- gsap
- vuex
- jspdf
- jspdf-autotable
- xlsx
- vue-tour


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
16. Add vue-router to frontend for routing: $ vue add router
17. Add axios to frontend for http requests: $ npm install axios --save
18. Add vuetify to frontend for styling: $ vue add vuetify
19. Add gsap to frontend for animations: $ npm install gsap
20. Add a middleware to allow the resources to be accessed on other domains thorugh CORS headers: (backend) $ python -m pip install django-cors-headers
21. Add JSON Web Token based Authorisation: (backend) $ pip install djangorestframework-jwt
22. Install vuex to manage app state: $ npm install vuex --save
23. Install jspdf and plugin to generate PDF files: $ npm install jspdf jspdf-autotable
24. Install xlsx to generate Excel files: $ npm install xlsx
25. Install channels to integrate websockets into django: (backend) $ python -m pip install -U channels
26. Install vue-tour: $ npm install vue-tour
27. Install celery: (backend) $ pip install celery
26. Install redis


if any problems run: sudo apt install libpq-dev python3-dev

- connect to postgres
- create superuser
