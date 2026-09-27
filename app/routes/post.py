from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.services.post_service import (
    create_post,
    get_feed,
    get_post,
    delete_post
)

post_bp = Blueprint("post", __name__)


@post_bp.route("/feed", methods=["GET"])
def feed():
    posts = get_feed()

    return render_template(
        "post/feed.html",
        posts=posts
    )


@post_bp.route("/post/<int:post_id>", methods=["GET"])
def post_details(post_id):
    post = get_post(post_id)

    if not post:
        flash("Post not found.", "danger")
        return redirect(url_for("post.feed"))

    return render_template(
        "post/post_details.html",
        post=post
    )


@post_bp.route("/create-post", methods=["POST"])
def create_new_post():
    result = create_post(request.form)

    if result.get("success"):
        flash(result.get("message", "Post created successfully."), "success")
    else:
        flash(result.get("message", "Failed to create post."), "danger")

    return redirect(url_for("post.feed"))


@post_bp.route("/post/<int:post_id>", methods=["DELETE"])
def remove_post(post_id):
    result = delete_post(post_id)

    if result.get("success"):
        return {
            "success": True,
            "message": result.get("message", "Post deleted successfully.")
        }, 200

    return {
        "success": False,
        "message": result.get("message", "Failed to delete post.")
    }, 400