#!/usr/bin/env bash
# Exit on error
set -o errexit

# Change to the app directory
cd app

# Modify this line as needed for your package manager (pip, poetry, etc.)
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate

# Initialize the database with any necessary data
python manage.py init-db