release: python manage.py migrate --noinput
web: uwsgi --http-socket :80 --wsgi-file djworkplace/wsgi.py --master --processes 2 --threads 2
