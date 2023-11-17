web: gunicorn --bind :8000 --workers 3 --threads 2 config.wsgi:application
websocketdaphne: daphne -b 0.0.0.0 -p 5000 config.asgi:application
