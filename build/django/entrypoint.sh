#!/bin/sh

# Collect static files
echo "Generating static files..."
python manage.py collectstatic --noinput

# Generate database migrations
echo "Generating database migrations..."
python manage.py makemigrations fileserver

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate fileserver

# Start the development server
echo "Starting server..."
python manage.py runserver 0.0.0.0:8000