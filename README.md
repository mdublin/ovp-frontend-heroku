To start gunicorn server locally you need to swap out the configuration in wsgi.py to "production" instead of "production_heroku".

Then run: 
$ gunicorn app.wsgi:application --log-level debug

(Leaving run.py file in case you want to use Flask server instead of Gunicorn)

For Heroku deployment, just make sure the wsgi.py is pointing to "production_heroku"

Some userful Heroku commands:

    Logging:

    heroku logs --tail

    Access the shell of your one-off dyno:

    heroku run bash


