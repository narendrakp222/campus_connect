from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.services.profile_service import (
    get_profile,
    update_profile
)

profile_bp = Blueprint("profile", __name__)


@profile_bp.route("/profile", methods=["GET"])
def my_profile():
    user_id = session.get("user_id")
    if not user_id:
        flash("Please log in to view your profile.", "warning")
        return redirect(url_for("auth.login_page"))

    profile_data = get_profile(user_id)
    if not profile_data:
        flash("Profile not found.", "danger")
        return redirect(url_for("post.feed"))

    if request.is_json:
        return jsonify(profile_data)

    return render_template(
        "profile/profile.html",
        profile=profile_data
    )


@profile_bp.route("/profile/<int:user_id>", methods=["GET"])
def user_profile(user_id):
    profile_data = get_profile(user_id)

    if not profile_data:
        flash("User profile not found.", "danger")
        return redirect(url_for("post.feed"))

    if request.is_json:
        return jsonify(profile_data)

    return render_template(
        "profile/profile.html",
        profile=profile_data
    )


@profile_bp.route("/profile/update", methods=["POST"])
def edit_profile():
    data = request.get_json() if request.is_json else request.form
    result = update_profile(data)

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash(result.get("message", "Profile updated successfully."), "success")
    else:
        flash(result.get("message", "Failed to update profile."), "danger")

    return redirect(url_for("profile.my_profile"))