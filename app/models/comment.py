from datetime import datetime
from app.database.db import db


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

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
        else:
            return self.created_at.strftime("%b %d, %Y")

    def to_dict(self):
        author_name = self.author.full_name or self.author.username if self.author else "Anonymous"
        username = self.author.username if self.author else "unknown"
        avatar_color = self.author.avatar_color if self.author else "#6366f1"
        initial = author_name[0].upper() if author_name else "A"

        return {
            "id": self.id,
            "content": self.content,
            "created_at": self.created_at.isoformat(),
            "formatted_time": self.format_time(),
            "post_id": self.post_id,
            "user_id": self.user_id,
            "username": username,
            "author_name": author_name,
            "avatar_color": avatar_color,
            "initial": initial
        }


