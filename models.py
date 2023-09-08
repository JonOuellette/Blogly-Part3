"""Models for Blogly."""
import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

DEFAULT_IMAGE_URL = "https://www.freeiconspng.com/uploads/icon-user-blue-symbol-people-person-generic--public-domain--21.png"

class User(db.Model):
    """Site user"""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    first_name = db.Column(db.String(25), nullable = False )
    last_name = db.Column(db.String(30), nullable= False)
    image_url = db.Column(db.Text, nullable = False, default = DEFAULT_IMAGE_URL)

    posts = db.relationship("Post", backref="user", cascade="all, delete-orphan")


class Post(db.Model):
    """BLog post"""
    __tablename__ = "posts"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(
        db.DateTime,
        nullable=False,
        default=datetime.datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

class PostTag(db.Model):
    """Tag on a post"""

    __tablename__ = "posts_tags"

    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'), primary_key=True)
    tag_id = db.Column(db.Integer, db.ForeignKey('tags.id'), primary_key=True)

class Tag(db.Model):
    """Tag that can be added to posts."""

    __tablename__ = 'tags'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text, nullable=False, unique=True)

    posts = db.relationship(
        'Post',
        secondary="posts_tags",
        # cascade="all,delete",
        backref="tags",
    )

def connect_db(app):
    """Connects database to Flask app"""
    db.app = app
    db.init_app(app)