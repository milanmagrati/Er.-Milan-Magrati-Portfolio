#!/usr/bin/env bash
# Exit immediately if a command exits with a non-zero status
set -o errexit

echo "==> Upgrading pip..."
pip install --upgrade pip

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

# If manage.py is located inside project/, change directory into it
if [ -f "project/manage.py" ]; then
    cd project
fi

echo "==> Collecting static files..."
python manage.py collectstatic --no-input

echo "==> Applying database migrations..."
python manage.py migrate

echo "==> Seeding initial portfolio content and media..."
python manage.py seed_portfolio

echo "==> Build completed successfully!"
