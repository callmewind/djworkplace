release: pip install psycopg2-binary gunicorn && python manage.py migrate --noinput
web: gunicorn billdev.wsgi
