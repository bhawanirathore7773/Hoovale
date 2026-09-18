#!/usr/bin/env bash
set -e

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Synchronizing model migrations"
# Generate any missing migrations from the current models before applying them.
# This is intentionally kept in the Render build so the deployed PostgreSQL
# schema cannot lag behind the checked-in Django models.
python manage.py makemigrations --noinput

echo "==> Applying database migrations"
python manage.py migrate --noinput

echo "==> Collecting static files"
python manage.py collectstatic --noinput

echo "==> Creating/checking Django admin user"
python create_admin.py

echo "==> Build completed successfully"
