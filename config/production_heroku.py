import os
import psycopg2
import urlparse

ADMINS = ['admin@test.com']
#DEBUG = False
DEBUG = True
SECRET_KEY = 'top secret!'


#if you are running this configuration locally, just export DATABASE_URL environment variable so you can connect to your local PostgreSQL database (or just insert the actual psql URL as you see in the other config files)
#But for Heroku deploy, this will suffice as the Heroku environment already sets DATABASE_URL to the psql url of the db istance, which is actually hosted on Amazon AWS. 
SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URL"]
