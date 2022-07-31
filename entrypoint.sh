#!/bin/sh

# python manage.py makemigrations
python manage.py migrate

# Fixtures
python manage.py loaddata phase port service tool vulnerability # HallowPentest
python manage.py loaddata website # HallowWriteup

python manage.py collectstatic --no-input --clear

exec "$@"