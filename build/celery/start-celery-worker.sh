#!/bin/sh

cd /app

# Start the Celery worker
echo "Starting Celery worker..."
celery -A fileserver.celery worker --loglevel=info