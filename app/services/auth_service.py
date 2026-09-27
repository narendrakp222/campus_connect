
import random
from flask import session
from werkzeug.security import generate_password_hash, check_password_hash
from app.database.db import db
from app.models.user import User

AVATAR_COLORS = [
    "#6366f1", "#8b5cf6", "#ec4899", "#f43f5e", 
    "#10b981", "#06b6d4", "#3b82f6", "#f59e0b"
]


def register_user(form_data):
    """
    Handle user registration business logic.

    Args:
        form_data: request.form or dict

    Returns:
        dict: success status, message, and optional user object
    """
    username = form_data.get("username", "").strip()
    email = form_data.get("email", "").strip().lower()
    password = form_data.get("password", "").strip()
    full_name = form_data.get("full_name", "").strip() or username
    department = form_data.get("department", "").strip() or "Computer Science"

    if not username or not email or not password:
        return {
            "success": False,
            "message": "Username, email, and password are required."
        }

    if len(password) < 6:
        return {
            "success": False,
            "message": "Password must be at least 6 characters long."
        }

    if User.query.filter(User.username.ilike(username)).first():
        return {
            "success": False,
            "message": "Username is already taken."
        }

    if User.query.filter(User.email.ilike(email)).first():
        return {
            "success": False,
            "message": "Email is already registered."
        }

    avatar_color = random.choice(AVATAR_COLORS)

    user = User(
        username=username,
        email=email,
        full_name=full_name,
        department=department,
        avatar_color=avatar_color,
        password_hash=generate_password_hash(password)
    )
    db.session.add(user)
    db.session.commit()

    session["user_id"] = user.id

    return {
        "success": True,
        "message": "Account created successfully!",
        "user": user.to_dict()
    }


def login_user(form_data):
    """
    Handle user login business logic.

    Args:
        form_data: request.form or dict

    Returns:
        dict: success status and message
    """
    identifier = form_data.get("username", "").strip() or form_data.get("email", "").strip()
    password = form_data.get("password", "").strip()

    if not identifier or not password:
        return {
            "success": False,
            "message": "Username/Email and password are required."
        }

    user = User.query.filter(
        (User.email.ilike(identifier)) | (User.username.ilike(identifier))
    ).first()

    if not user or not check_password_hash(user.password_hash, password):
        return {
            "success": False,
            "message": "Invalid username/email or password."
        }

    session["user_id"] = user.id

    return {
        "success": True,
        "message": f"Welcome back, {user.full_name or user.username}!",
        "user": user.to_dict()
    }


def logout_user():
    """
    Handle logout logic.
    """
    session.clear()
    return {
        "success": True,
        "message": "Logged out successfully."
    }