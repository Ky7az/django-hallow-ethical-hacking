#!/bin/sh

# python manage.py makemigrations
python manage.py migrate
python manage.py loaddata phase port service tool vulnerability
python manage.py collectstatic --no-input --clear

exec "$@"