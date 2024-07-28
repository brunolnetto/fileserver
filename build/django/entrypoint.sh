#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# Generate database migrations
until python manage.py makemigrations
do
    echo "Generating database migrations..."
    sleep 2
done

# Apply database migrations
until python manage.py migrate
do
    echo "Applying database migrations..."
    sleep 2
done

# Collect static files
echo "Generating static files..."
python manage.py collectstatic --noinput

# Start the development server
echo "Starting server..."
gunicorn backend.wsgi --bind 0.0.0.0:8000 --workers 4 --threads 4