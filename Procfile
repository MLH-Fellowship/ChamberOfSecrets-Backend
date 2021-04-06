release: cd backend && python3 manage.py makemigrations && python3 manage.py migrate
web: gunicorn gettingstarted.wsgi --preload --log-file -