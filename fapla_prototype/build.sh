#!/usr/bin/env bash
# exit on error
set -o errexit

cd fapla_prototype

pip install -r requirements.txt

python manage.py migrate

python manage.py collectstatic --no-input