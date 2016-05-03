import os
import psycopg2
import urlparse

ADMINS = ['admin@test.com']
#DEBUG = False
DEBUG = True
SECRET_KEY = 'top secret!'
#SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(
#    os.path.dirname(__file__), '../data.sqlite3')

#SQLALCHEMY_DATABASE_URI = "postgresql://mdublin1@localhost:5432/VideoDashBoard"

url = urlparse.urlparse(os.environ["DATABASE_URL"])
SQLALCHEMY_DATABASE_URI = url


'''import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

conn = pyscopg2.connect(
        database=url.path[1:],
        user=url.username,
        password=url.password,
        port=url.port
)'''



