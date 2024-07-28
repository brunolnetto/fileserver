FROM python:3.11

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Create a non-root user and group
RUN groupadd app && useradd -g app appuser

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code  

COPY . .

# Set correct ownership for scripts and application code
RUN chown -R appuser:app /app

# Switch to the appuser
USER appuser

# Entrypoint scripts
COPY build/celery/entrypoint-worker.sh /app/build/celery/
COPY build/celery/entrypoint-beat.sh /app/build/celery/
COPY build/django/entrypoint.sh /app/build/django/

