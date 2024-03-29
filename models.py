"""SQLAlchemy models for Warbler."""

from datetime import datetime

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy

bcrypt = Bcrypt()
db = SQLAlchemy()


class List(db.Model):
    """Mapping user list to movie."""

    __tablename__ = 'lists' 

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='cascade'))
    movie_id = db.Column(db.String(15), db.ForeignKey('movies.id', ondelete='cascade'), unique=True)

    def __repr__(self):
        return f"<List: {self.username}, {self.movie_id}>"
    
    movie = db.relationship('Movie')

class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.Text, nullable=False, unique=True)
    image_url = db.Column(db.Text, default="/static/images/default-pic.png")
    password = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<User: {self.username}>"

    @classmethod
    def signup(cls, username, image_url, password):
        """Sign up user.

        Hashes password and adds user to system.
        """

        hashed_pwd = bcrypt.generate_password_hash(password).decode('UTF-8')

        user = User(username=username, image_url=image_url, password=hashed_pwd)
        db.session.add(user)

        return user

    @classmethod
    def authenticate(cls, username, password):
        """Find user with `username` and `password`.

        This is a class method (call it on the class, not an individual user.)
        It searches for a user whose password hash matches this password
        and, if it finds such a user, returns that user object.

        If can't find matching user (or if password is wrong), returns False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False
    
    list = db.relationship('List')


class Studio(db.Model):

    __tablename__ = "studios"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, default="NONE")


class Movie(db.Model):

    __tablename__ = "movies"

    id = db.Column(db.String(15), primary_key=True)


class Actor(db.Model):

    __tablename__ = "actors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


class Director(db.Model):

    __tablename__ = "directors"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False)


def connect_db(app):
    """Connect this database to provided Flask app.
    You should call this in your Flask app.
    """

    db.app = app
    db.init_app(app)
