<img src="frontend/src/assets/logo_small.png" width="380" height="100">

## Folder structure:
```
Centralized-Platform
├───backend
│   ├───actions
│   │   ├───ansible
│   │   │   ├───inventory
│   │   │   └───project
│   │   └───migrations
│   ├───api
│   │   └───migrations
│   ├───backend
│   ├───inventory
│   │   ├───files
│   │   │   ├───changes
│   │   │   └───tasks
│   │   └───migrations
│   ├───static
│   └───websockets
│       └───migrations
└───frontend
    ├───node_modules
    ├───public
    └───src
        ├───assets
        ├───components
        ├───plugins
        ├───router
        └───views
```

## Requirements:
* Python 3.8 + pip 
* PostgreSQL 10 
* node.js 
* npm 
* Redis 
* Ansible 

## Deployement:
1. Install virtualenv
```
pip install virtualenv
```
2. Make virtual environment
```
virtualenv venv
```
3. Activate virtual environment 
```
source venv/bin/activate
```
4. Install dependencies Backend
```
pip install -r requirements.txt
```
5. create new database in PostgreSQL 
```
CREATE DATABASE <name>
```
6. create .env file and fill variables:
```
SQL_ENGINE=django.db.backends.postgresql_psycopg2
SQL_DATABASE=
SQL_USER=
SQL_PASSWORD=
SQL_HOST=
SQL_PORT=
DJANGO_ALLOWED_HOSTS=
DJANGO_KEY=
EMAIL_USER=
```
7. Install dependencies Frontend
```
npm install 
npm install -g n
n lts
```
8. Sincronise Django and PostgreSQL
```
python3 manage.py makemigrations
python3 manage.py migrate
```
9. Create administrator user
```
python3 manage.py createsuperuser
```

## Run:
- Backend 
```
python3 manage.py runserver
```
- Frontend
```
npm run serve
```
