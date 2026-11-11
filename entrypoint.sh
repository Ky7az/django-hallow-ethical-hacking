#!/bin/sh
set -e

# Only one service (django) runs migrations and fixtures, to avoid races.
if [ "$RUN_MIGRATIONS" = "1" ]; then
    # python3 manage.py makemigrations
    python3 manage.py migrate --no-input

    # Fixtures
    python3 manage.py loaddata source # HallowWatch
    python3 manage.py loaddata phase port service tool vulnerability action # HallowPentest
    python3 manage.py loaddata website # HallowWriteup
fi

exec "$@"
