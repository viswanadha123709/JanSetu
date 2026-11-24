#!/usr/bin/env bash
# Exit on error
set -o errexit

echo "Installing production dependencies..."
pip install -r requirements.txt

echo "Collecting static assets..."
python manage.py collectstatic --no-input

echo "Running database migrations..."
python manage.py migrate

echo "Seeding master schemes and policies..."
python manage.py shell -c "from apps.schemes.seed_data import populate_seed_data; populate_seed_data()"

echo "Build process completed successfully!"
