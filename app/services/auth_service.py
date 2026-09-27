
from flask import session


def register_user(form_data):
    """
    Handle user registration business logic.

    Args:
        form_data: request.form

    Returns:
        dict: success status and message
    """

    username = form_data.get("username", "").strip()
    email = form_data.get("email", "").strip()
    password = form_data.get("password", "").strip()

    if not username or not email or not password:
        return {
            "success": False,
            "message": "All fields are required."
        }

    # Database validation and user creation
    # will be implemented later

    return {
        "success": True,
        "message": "Registration successful."
    }


def login_user(form_data):
    """
    Handle user login business logic.

    Args:
        form_data: request.form

    Returns:
        dict: success status and message
    """

    email = form_data.get("email", "").strip()
    password = form_data.get("password", "").strip()

    if not email or not password:
        return {
            "success": False,
            "message": "Email and password are required."
        }

    # Database authentication
    # will be implemented later

    session["user_id"] = 1

    return {
        "success": True,
        "message": "Login successful."
    }


def logout_user():
    """
    Handle logout logic.
    """

    session.clear()

    return {
        "success": True,
        "message": "Logout successful."
    }