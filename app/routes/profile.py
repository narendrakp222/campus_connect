from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.profile_service import (
    get_profile,
    update_profile
)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
def my_profile():
    """
    Display the currently logged-in user's profile.
    """

    profile_data = get_profile()

    return render_template(
        "profile/profile.html",
        profile=profile_data
    )


@profile_bp.route("/profile/<int:user_id>", methods=["GET"])
def user_profile(user_id):
    """
    Display another user's profile.
    """

    profile_data = get_profile(user_id)

    if not profile_data:
        flash("User not found.", "danger")
        return redirect(url_for("post.feed"))

    return render_template(
        "profile/profile.html",
        profile=profile_data
    )


@profile_bp.route("/profile/update", methods=["POST"])
def edit_profile():
    """
    Update profile information.
    """

    result = update_profile(request.form)

    if result.get("success"):
        flash(result.get("message", "Profile updated successfully."), "success")
    else:
        flash(result.get("message", "Failed to update profile."), "danger")

    return redirect(url_for("profile.my_profile"))