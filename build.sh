#!/bin/bash
set -euo pipefail

export VERCEL=1
export PYTHONPATH="${PWD}/backend:${PWD}"

pip install -r requirements.txt

cd backend
python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
