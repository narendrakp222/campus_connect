# from app.database.db import db

# class User(db.Model):
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(db.String(80), unique=True, nullable=False)
#     email = db.Column(db.String(120), unique=True, nullable=False)
#     password_hash = db.Column(db.String(200), nullable=False)


from datetime import datetime

from app.database.db import db


class User(db.Model):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    posts = db.relationship(
        "Post", backref="author", lazy=True, cascade="all, delete-orphan"
    )
    comments = db.relationship(
        "Comment", backref="author", lazy=True, cascade="all, delete-orphan"
    )
    likes = db.relationship(
        "Like", backref="user", lazy=True, cascade="all, delete-orphan"
    )
