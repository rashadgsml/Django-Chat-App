release: python manage.py migrate
web: gunicorn --bind :8000 --workers 3 --threads 2 testing_chat_app.wsgi:application
websocket: daphne -b 0.0.0.0 -p 5000 testing_chat_app.asgi:application
worker: python manage.py runworker channels --settings=testing_chat_app.settings -v2