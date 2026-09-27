from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from app.services.auth_service import (
    register_user,
    login_user,
    logout_user
)

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET"])
def login_page():
    return render_template("auth/login.html")


@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json() if request.is_json else request.form
    result = login_user(data)

    if request.is_json:
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash(result.get("message", "Welcome back!"), "success")
        return redirect(url_for("post.feed"))

    flash(result.get("message", "Login failed"), "danger")
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("auth/register.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json() if request.is_json else request.form
    result = register_user(data)

    if request.is_json:
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash(result.get("message", "Registration successful!"), "success")
        return redirect(url_for("post.feed"))

    flash(result.get("message", "Registration failed"), "danger")
    return redirect(url_for("auth.register_page"))


@auth_bp.route("/logout", methods=["GET", "POST"])
def logout():
    result = logout_user()

    if request.is_json:
        return jsonify(result), 200

    flash("Logged out successfully.", "info")
    return redirect(url_for("auth.login_page"))