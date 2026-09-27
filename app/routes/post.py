from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, session
from app.services.post_service import (
    create_post,
    get_feed,
    get_post,
    delete_post,
    toggle_like
)

post_bp = Blueprint("post", __name__)


@post_bp.route("/post/create", methods=["GET"])
def create_page():
    if not session.get("user_id"):
        flash("Please log in to create a post.", "warning")
        return redirect(url_for("auth.login_page"))
    return render_template("post/create_post.html")


@post_bp.route("/feed", methods=["GET"])
def feed():
    category = request.args.get("category", "All")
    posts = get_feed(category=category)

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        return jsonify({"posts": posts, "category": category})

    return render_template(
        "post/feed.html",
        posts=posts,
        active_category=category
    )


@post_bp.route("/post/<int:post_id>", methods=["GET"])
def post_details(post_id):
    post = get_post(post_id)

    if not post:
        flash("Post not found.", "danger")
        return redirect(url_for("post.feed"))

    if request.is_json:
        return jsonify(post)

    return render_template(
        "post/post_details.html",
        post=post
    )


@post_bp.route("/create-post", methods=["POST"])
@post_bp.route("/post/create", methods=["POST"])
def create_new_post():
    data = request.get_json() if request.is_json else request.form
    result = create_post(data)

    if request.is_json:
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash(result.get("message", "Post created successfully."), "success")
    else:
        flash(result.get("message", "Failed to create post."), "danger")

    return redirect(url_for("post.feed"))


@post_bp.route("/post/<int:post_id>/like", methods=["POST"])
def like_post(post_id):
    result = toggle_like(post_id)

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if not result.get("success"):
        flash(result.get("message"), "danger")

    return redirect(request.referrer or url_for("post.feed"))


@post_bp.route("/post/<int:post_id>", methods=["DELETE"])
@post_bp.route("/post/<int:post_id>/delete", methods=["POST"])
def remove_post(post_id):
    result = delete_post(post_id)

    if request.is_json or request.method == "DELETE" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash("Post deleted successfully.", "success")
    else:
        flash(result.get("message", "Failed to delete post."), "danger")

    return redirect(url_for("post.feed"))