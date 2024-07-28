#!/bin/sh

# Check if the /app/backend directory exists
if [ ! -d /app/backend ]; then
  echo "/app/backend directory not found. Exiting."
  exit 1
fi

cd /app/backend

# Wait for the database to be ready and then generate database migrations
echo "Waiting for database to be ready..."
until python manage.py makemigrations; do
  echo "Failed to generate migrations. Retrying..."
  sleep 2
done

# Apply database migrations
echo "Applying database migrations..."
until python manage.py migrate; do
  echo "Failed to apply migrations. Retrying..."
  sleep 2
done

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --noinput

# Start the server
echo "Starting server..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
