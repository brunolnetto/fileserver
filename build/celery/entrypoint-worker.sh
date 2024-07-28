#!/bin/sh

# Start the Celery worker
echo "Starting Celery worker..."
celery -A fileserver worker --loglevel=info --concurrency 1 -E