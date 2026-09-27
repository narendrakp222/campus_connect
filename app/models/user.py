from datetime import datetime
from app.database.db import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(250), nullable=False)
    full_name = db.Column(db.String(120), default="")
    bio = db.Column(db.Text, default="")
    department = db.Column(db.String(100), default="Computer Science")
    grad_year = db.Column(db.String(20), default="2026")
    avatar_color = db.Column(db.String(30), default="#6366f1")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    posts = db.relationship("Post", backref="author", lazy=True, cascade="all, delete-orphan")
    comments = db.relationship("Comment", backref="author", lazy=True, cascade="all, delete-orphan")
    likes = db.relationship("Like", backref="user", lazy=True, cascade="all, delete-orphan")

    def to_dict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "full_name": self.full_name or self.username,
            "bio": self.bio,
            "department": self.department,
            "grad_year": self.grad_year,
            "avatar_color": self.avatar_color,
            "created_at": self.created_at.strftime("%B %Y") if self.created_at else "",
            "posts_count": len(self.posts),
            "likes_count": sum(len(p.likes) for p in self.posts)
        }

