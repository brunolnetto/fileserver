# Source: https://testdriven.io/courses/django-celery/docker/
FROM python:3.11-slim-buster

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

RUN apt-get update \
  # dependencies for building Python packages
  && apt-get install -y build-essential \
  # psycopg2 dependencies
  && apt-get install -y libpq-dev \
  # Translations dependencies
  && apt-get install -y gettext \
  # Additional dependencies
  && apt-get install -y git \
  # cleaning up unused files
  && apt-get purge -y --auto-remove -o APT::AutoRemove::RecommendsImportant=false \
  && rm -rf /var/lib/apt/lists/*


# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

# Requirements are installed here to ensure they will be cached.
COPY ./requirements.txt /requirements.txt
RUN pip install -r /requirements.txt

COPY ./build/django/entrypoint-django.sh /entrypoint-django.sh
RUN sed -i 's/\r$//g' /entrypoint-django.sh
RUN chmod +x /entrypoint-django.sh

COPY ./build/django/start-django.sh /start-django.sh
RUN sed -i 's/\r$//g' /start-django.sh
RUN chmod +x /start-django.sh

COPY ./build/celery/start-celery-worker.sh /start-celery-worker.sh
RUN sed -i 's/\r$//g' /start-celery-worker.sh
RUN chmod +x /start-celery-worker.sh

COPY ./build/celery/start-celery-beat.sh /start-celery-beat.sh
RUN sed -i 's/\r$//g' /start-celery-beat.sh
RUN chmod +x /start-celery-beat.sh

COPY ./build/celery/start-flower.sh /start-flower.sh
RUN sed -i 's/\r$//g' /start-flower.sh
RUN chmod +x /start-flower.sh
