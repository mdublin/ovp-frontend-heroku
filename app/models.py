from werkzeug.security import generate_password_hash, check_password_hash

# from . import db == importing the db=SQLAlchemy() instance created in the __init__.py in this same directory
from . import db, lm
from flask.ext.login import UserMixin


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(200), index=True, unique=True)
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(200))


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def register(username, email, password):
        user = User(username=username, email=email)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()

    def __repr__(self):
        return '<User {0}>'.format(self.username)

# loads user from database
@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


# Some notes of how SQLAlchemy is working in this app, which is kind of magical so it warrants some explicit break:
# because we are note, anywhere, executing models.py directly, how does this model class actuall get mapped to the SQLite database?

# 1. You create a Flask-SQLAlchemy instance (the db variable which is created in the __init__.py file in the app package as db = SQLAlchemy()). This class looks up the configuration in your Flask app instance, and that is how it knows where the database is.

# 2. Then you import all your models, which are defined as subclasses of db.Model as here, where the class User model is inheriting from db.Model class.

# 3. You then call db.create_all() which is executed in run.py, which uses introspection to find all the known subclasses of db.Model, and then for each one of them that does not have a corresponding table in the database, translates its properties into a create table SQL statement and runs it (this is the magical aspect, wherein the classes defined here in models.py get mapped to the SQLite database).

# A lot of people make the mistake of omitting #2, for example, and that makes db.create_all() do nothing, or create only some of the tables but not all.

# Note in #3 that create_all only creates a table if the table does not exist already. If you change a model and run create_db() again, it will not upgrade an existing table, you will need to remove the old tables by calling db.drop_all(), then you can make new tables with the updated models, and of course you will lose all your data.

# Also, just for the sake of correctness, we are mixing Flask-SQLAlchemy and SQLAlchemy as if they were the same thing. The Flask extension is a thin wrapper on top of SQLAlchemy. The db instance is a Flask-SQLAlchemy construct. There is an equivalent thing when you use SQLAlchemy directly, but it is implemented differently. The db.Model class comes from Flask-SQLAlchemy as well, but it builds on top of a base model class provided by SQLAlchemy. Having the query object as a property of the model (as in User.query), is an improvementsfrom the Flask extension. SQLAlchemy does have the same query object, but it is not attached to the model.
