# Use a lightweight Python image
FROM python:3.9-slim

# Environment variables
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y libpq-dev gcc curl \
    && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy project files
COPY . /app/

# Collect static files (optional, ignore errors if none)
RUN python manage.py collectstatic --noinput || true

# ✅ Apply Django migrations automatically
RUN python manage.py makemigrations --noinput && python manage.py migrate --noinput

# Expose Django/Gunicorn port
EXPOSE 8000

# Start Gunicorn server
CMD ["gunicorn", "sms_project.wsgi:application", "--bind", "0.0.0.0:8000", "--workers", "2", "--timeout", "120"]
