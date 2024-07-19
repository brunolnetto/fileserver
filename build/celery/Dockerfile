# Use a specific Python image as the base
FROM python:3.11

# Set the working directory in the container
WORKDIR /app

# Install any necessary system dependencies
RUN apt-get update && apt-get install -y build-essential libpq-dev

# Install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Define the command to run Celery
CMD ["sh", "/app/build/celery/entrypoint.sh"]
