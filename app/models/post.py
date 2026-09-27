from datetime import datetime
from app.database.db import db


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(50), default="General")
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    comments = db.relationship("Comment", backref="post", lazy=True, cascade="all, delete-orphan", order_by="Comment.created_at.asc()")
    likes = db.relationship("Like", backref="post", lazy=True, cascade="all, delete-orphan")

    def format_time(self):
        now = datetime.utcnow()
        diff = now - self.created_at
        seconds = diff.total_seconds()
        if seconds < 60:
            return "Just now"
        elif seconds < 3600:
            minutes = int(seconds // 60)
            return f"{minutes}m ago"
        elif seconds < 86400:
            hours = int(seconds // 3600)
            return f"{hours}h ago"
        elif seconds < 604800:
            days = int(seconds // 86400)
            return f"{days}d ago"
        else:
            return self.created_at.strftime("%b %d, %Y")

    def to_dict(self, current_user_id=None):
        is_liked = False
        if current_user_id:
            is_liked = any(like.user_id == current_user_id for like in self.likes)

        return {
            "id": self.id,
            "content": self.content,
            "category": self.category or "General",
            "created_at": self.created_at.isoformat(),
            "formatted_time": self.format_time(),
            "user_id": self.user_id,
            "username": self.author.username if self.author else "Unknown",
            "author": {
                "id": self.author.id,
                "username": self.author.username,
                "full_name": self.author.full_name or self.author.username,
                "department": self.author.department,
                "avatar_color": self.author.avatar_color,
                "initial": (self.author.full_name or self.author.username)[0].upper()
            } if self.author else {"username": "Unknown", "initial": "U", "avatar_color": "#6366f1"},
            "likes": len(self.likes),
            "likes_count": len(self.likes),
            "is_liked": is_liked,
            "comments_count": len(self.comments),
            "comments": [c.to_dict() for c in self.comments],
        }

