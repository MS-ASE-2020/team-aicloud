#!/bin/bash

chmod +x backend/static

python manage.py runserver
# gunicorn backend.wsgi:application --bind 0.0.0.0:8000 --workers 2