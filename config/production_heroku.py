import os
import psycopg2
import urlparse

ADMINS = ['admin@test.com']
#DEBUG = False
DEBUG = True
SECRET_KEY = 'top secret!'

SQLALCHEMY_DATABASE_URI = "postgres://gkjrtbegisyndh:lF5JgQxWOvSMCBooTBUizlYFKK@ec2-107-20-174-127.compute-1.amazonaws.com:5432/dh9lfn7o0f3hv"



urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = pyscopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        port=url.port
)

#SQLALCHEMY_DATABASE_URI = url


