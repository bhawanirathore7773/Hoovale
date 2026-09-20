#!/usr/bin/env bash
set -e

echo "==> Installing dependencies"
pip install -r requirements.txt

echo "==> Applying checked-in database migrations"
# Production deployments must apply the migrations committed to Git.
# Do not generate new migration files during the Render build.
python manage.py migrate --noinput

echo "==> Collecting static files"
python manage.py collectstatic --noinput

echo "==> Creating/checking Django admin user"
python create_admin.py

echo "==> Build completed successfully"
