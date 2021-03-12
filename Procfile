release: python manage.py migrate
web: daphne testing_chat_app.asgi:application --port $PORT --bind 0.0.0.0 -v2
worker: python manage.py runworker channels --settings=testing_chat_app.settings -v2