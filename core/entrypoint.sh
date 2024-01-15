#!/bin/sh

python manage.py migrate

python manage.py collectstatic --noinput

nohup python manage.py run_bot &

uwsgi --ini /app/traffic_light.uwsgi.ini