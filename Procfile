web: daphne testing_chat_app.asgi:application --port $PORT --bind 0.0.0.0 -v2
chatworker: python manage.py runworker --settings=testing_chat_app.settings -v2