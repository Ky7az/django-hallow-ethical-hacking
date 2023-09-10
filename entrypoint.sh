#!/bin/sh

# python3 manage.py makemigrations
python3 manage.py migrate

# Fixtures
python3 manage.py loaddata source # HallowWatch
python3 manage.py loaddata phase port service tool vulnerability action # HallowPentest
python3 manage.py loaddata website # HallowWriteup

exec "$@"