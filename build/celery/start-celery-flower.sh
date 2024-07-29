#!/bin/bash

set -o errexit
set -o nounset

worker_ready() {
    celery -A fileserver inspect ping
}

until worker_ready; do
  >&2 echo 'Celery workers not available'
  sleep 1
done
>&2 echo 'Celery workers are available'

celery -A fileserver  \
    --broker="${CELERY_BROKER_URL}" \
    flower
