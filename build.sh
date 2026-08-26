#!/bin/bash
set -e

pip install -r requirements.txt

export PYTHONPATH="${PWD}/backend"
cd backend

python manage.py collectstatic --noinput --clear
python manage.py migrate --noinput
