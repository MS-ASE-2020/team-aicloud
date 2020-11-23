#!/bin/bash

chmod +x backend/static

/wait.sh -t 120 mysql:3306

# python manage.py runserver
python manage.py migrate
echo "from account.models import User; User.objects.create_superuser('admin', '', 'admin')" | python manage.py shell
gunicorn rishi.wsgi:application --bind 0.0.0.0:8000 --workers 2