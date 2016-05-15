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

Also, if you want to work on the same repository that is for the same Heroku app, you need to connect the repository copies on your other machines to the same app via: 

$ heroku git:remote -a yourappname

The other way to get the actual repository that's used for the app is to git clone it from the Heroku dashboard, but that won't actually be connected to your github repository version unless you create a new github repository, push it, etc. 



For local dev, sometimes port gets stuck -- to find offending port:
    $ lsof -n -i4TCP:8000 | grep LISTEN


