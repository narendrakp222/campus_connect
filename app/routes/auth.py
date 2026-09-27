from flask import Blueprint, render_template, request, redirect, url_for, flash
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
    result = login_user(request.form)

    if result.get("success"):
        flash(result.get("message", "Login successful"), "success")
        return redirect(url_for("post.feed"))

    flash(result.get("message", "Login failed"), "danger")
    return redirect(url_for("auth.login_page"))


@auth_bp.route("/register", methods=["GET"])
def register_page():
    return render_template("auth/register.html")


@auth_bp.route("/register", methods=["POST"])
def register():
    result = register_user(request.form)

    if result.get("success"):
        flash(result.get("message", "Registration successful"), "success")
        return redirect(url_for("auth.login_page"))

    flash(result.get("message", "Registration failed"), "danger")
    return redirect(url_for("auth.register_page"))


@auth_bp.route("/logout", methods=["GET"])
def logout():
    logout_user()

    flash("Logged out successfully", "success")
    return redirect(url_for("auth.login_page"))