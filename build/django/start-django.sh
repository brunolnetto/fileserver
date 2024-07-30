#!/bin/sh

# Check if the /app/backend directory exists
if [ ! -d /app ]; then
  echo "/app directory not found. Exiting."
  exit 1
fi

cd /app

# Wait for the database to be ready and then generate database migrations
echo "Generating database migrations..."
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
exec gunicorn fileserver.wsgi:application --bind 0.0.0.0:8000 --workers 4 --threads 4
