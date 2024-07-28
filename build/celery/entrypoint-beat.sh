#!/bin/sh

# Make migrations for django-celery-beat
echo "Generating migrations for django-celery-beat..."
python manage.py makemigrations django_celery_beat

# Apply migrations for django-celery-beat
echo "Applying django-celery-beat migrations..."
python manage.py migrate django_celery_beat

# Start the Celery Beat service
echo "Starting Celery Beat..."
celery -A fileserver beat --loglevel=info
