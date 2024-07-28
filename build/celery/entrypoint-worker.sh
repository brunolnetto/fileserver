#!/bin/sh

until cd /app/backend
do
    echo "Waiting for server volume..."
done

# Start the Celery worker
echo "Starting Celery worker..."
celery -A fileserver worker --loglevel=info --concurrency 1 -E