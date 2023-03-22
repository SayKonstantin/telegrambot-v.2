#!/bin/sh

if [ "$DATABASE" = "postgres" ]
then
    echo "Waiting for postgres..."

    while ! nc -z $DBHOST $PORT; do
      sleep 0.5
    done

    echo "PostgreSQL started"
fi

python django_app.py makemigrations
python django_app.py migrate

exec "$@"