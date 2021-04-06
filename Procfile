release: python manage.py makemigrations && python manage.py migrate
web: gunicorn gettingstarted.wsgi --preload --log-file -