import os
import psycopg2
import urlparse

ADMINS = ['admin@test.com']
#DEBUG = False
DEBUG = True
SECRET_KEY = 'top secret!'


SQLALCHEMY_DATABASE_URI = "postgresql://mdublin1@localhost:5432/VideoDashBoard"


