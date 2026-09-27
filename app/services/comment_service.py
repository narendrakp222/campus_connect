from flask import session
from app.database.db import db
from app.models.comment import Comment
from app.models.post import Post


def create_comment(post_id, form_data):
    """
    Handle comment creation business logic.

    Args:
        post_id (int): ID of the post being commented on
        form_data: request.form or dict

    Returns:
        dict
    """
    comment_text = (form_data.get("comment", "") or form_data.get("content", "")).strip()
    user_id = session.get("user_id")

    if not comment_text:
        return {
            "success": False,
            "message": "Comment text cannot be empty."
        }

    if not user_id:
        return {
            "success": False,
            "message": "You must be logged in to comment."
        }

    post = Post.query.get(post_id)
    if not post:
        return {
            "success": False,
            "message": "Post not found."
        }

    comment = Comment(
        content=comment_text,
        post_id=post.id,
        user_id=user_id
    )
    db.session.add(comment)
    db.session.commit()

    return {
        "success": True,
        "message": "Comment added successfully.",
        "comment": comment.to_dict(),
        "comments_count": len(post.comments),
        "post_id": post_id
    }


def delete_comment(comment_id):
    """
    Handle comment deletion business logic.

    Args:
        comment_id (int): ID of the comment

    Returns:
        dict
    """
    user_id = session.get("user_id")
    if not user_id:
        return {
            "success": False,
            "message": "Authentication required."
        }

    comment = Comment.query.get(comment_id)
    if not comment:
        return {
            "success": False,
            "message": "Comment not found."
        }

    if comment.user_id != user_id:
        return {
            "success": False,
            "message": "You can only delete your own comments."
        }

    post_id = comment.post_id
    db.session.delete(comment)
    db.session.commit()

    post = Post.query.get(post_id)
    comments_count = len(post.comments) if post else 0

    return {
        "success": True,
        "message": "Comment deleted successfully.",
        "comment_id": comment_id,
        "post_id": post_id,
        "comments_count": comments_count
    }

