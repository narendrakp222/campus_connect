from flask import session
from app.database.db import db
from app.models.user import User
from app.models.post import Post


def get_profile(user_id=None):
    """
    Return profile data for the logged-in user,
    or another user when user_id is given.
    """
    current_user_id = session.get("user_id")

    if user_id is None:
        user_id = current_user_id

    if not user_id:
        return None

    user = User.query.get(user_id)
    if not user:
        return None

    data = user.to_dict()
    # Fetch user posts
    user_posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    data["posts"] = [p.to_dict(current_user_id=current_user_id) for p in user_posts]
    data["is_self"] = (user.id == current_user_id)

    return data


def update_profile(form_data):
    """
    Update the logged-in user's profile.

    Args:
        form_data: request.form or dict

    Returns:
        dict
    """
    user_id = session.get("user_id")

    if not user_id:
        return {
            "success": False,
            "message": "You must be logged in to update your profile."
        }

    user = User.query.get(user_id)
    if not user:
        return {
            "success": False,
            "message": "User not found."
        }

    full_name = form_data.get("full_name", "").strip()
    bio = form_data.get("bio", "").strip()
    department = form_data.get("department", "").strip()
    grad_year = form_data.get("grad_year", "").strip()

    if full_name:
        user.full_name = full_name
    if bio is not None:
        user.bio = bio
    if department:
        user.department = department
    if grad_year:
        user.grad_year = grad_year

    db.session.commit()

    return {
        "success": True,
        "message": "Profile updated successfully.",
        "profile": user.to_dict()
    }

