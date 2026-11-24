# Production Dockerfile for JanSetu
FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies for PyMuPDF & SQLite
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

RUN python manage.py collectstatic --no-input
RUN python manage.py migrate
RUN python manage.py shell -c "from apps.schemes.seed_data import populate_seed_data; populate_seed_data()"

EXPOSE 8000

CMD ["gunicorn", "jansetu.wsgi:application", "--bind", "0.0.0.0:8000"]
