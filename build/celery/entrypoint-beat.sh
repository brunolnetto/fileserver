#!/bin/sh

set -e

echo "Generating migrations for django-celery-beat..."
python manage.py makemigrations django_celery_beat

echo "Applying django-celery-beat migrations..."
python manage.py migrate django_celery_beat

echo "Starting Celery Beat..."
celery -A fileserver beat --loglevel=info
