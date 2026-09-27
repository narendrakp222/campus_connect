from flask import session
from app.database.db import db
from app.models.post import Post
from app.models.user import User
from app.models.like import Like


def create_post(form_data):
    """
    Handle post creation business logic.

    Args:
        form_data: request.form or dict

    Returns:
        dict
    """
    content = form_data.get("content", "").strip()
    category = form_data.get("category", "General").strip()
    user_id = session.get("user_id")

    if not content:
        return {
            "success": False,
            "message": "Post content cannot be empty."
        }

    if not user_id:
        return {
            "success": False,
            "message": "You must be logged in to create a post."
        }

    user = User.query.get(user_id)
    if not user:
        return {
            "success": False,
            "message": "User session is invalid. Please log in again."
        }

    post = Post(content=content, category=category, user_id=user.id)
    db.session.add(post)
    db.session.commit()

    return {
        "success": True,
        "message": "Post published successfully.",
        "post": post.to_dict(current_user_id=user_id)
    }


def get_feed(category=None, user_id_filter=None):
    """
    Return posts for feed, newest first. Optional category and user filtering.

    Returns:
        list of dicts
    """
    current_user_id = session.get("user_id")
    query = Post.query.order_by(Post.created_at.desc())

    if category and category.lower() != "all":
        query = query.filter(Post.category == category)

    if user_id_filter:
        query = query.filter(Post.user_id == user_id_filter)

    posts = query.all()
    return [p.to_dict(current_user_id=current_user_id) for p in posts]


def get_post(post_id):
    """
    Return a single post detail with comments and like status.
    """
    current_user_id = session.get("user_id")
    post = Post.query.get(post_id)
    return post.to_dict(current_user_id=current_user_id) if post else None


def toggle_like(post_id):
    """
    Toggle like/unlike for a post by current logged-in user.
    """
    user_id = session.get("user_id")
    if not user_id:
        return {
            "success": False,
            "message": "You must be logged in to like posts."
        }

    post = Post.query.get(post_id)
    if not post:
        return {
            "success": False,
            "message": "Post not found."
        }

    existing_like = Like.query.filter_by(user_id=user_id, post_id=post_id).first()

    if existing_like:
        db.session.delete(existing_like)
        db.session.commit()
        is_liked = False
        message = "Post unliked."
    else:
        new_like = Like(user_id=user_id, post_id=post_id)
        db.session.add(new_like)
        db.session.commit()
        is_liked = True
        message = "Post liked."

    likes_count = len(post.likes)
    return {
        "success": True,
        "message": message,
        "is_liked": is_liked,
        "likes_count": likes_count,
        "post_id": post_id
    }


def delete_post(post_id):
    """
    Delete a post if authorized.
    """
    user_id = session.get("user_id")
    if not user_id:
        return {
            "success": False,
            "message": "Authentication required."
        }

    post = Post.query.get(post_id)
    if not post:
        return {
            "success": False,
            "message": "Post not found."
        }

    if post.user_id != user_id:
        return {
            "success": False,
            "message": "You can only delete your own posts."
        }

    db.session.delete(post)
    db.session.commit()

    return {
        "success": True,
        "message": "Post deleted successfully.",
        "post_id": post_id
    }

