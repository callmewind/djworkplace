release: python manage.py migrate --noinput
web: uwsgi --http-socket :$PORT --wsgi-file djworkplace/wsgi.py --master --processes 2 --threads 2 --die-on-term
