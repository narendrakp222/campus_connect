from flask import Blueprint, request, redirect, url_for, flash, jsonify
from app.services.comment_service import (
    create_comment,
    delete_comment
)

comment_bp = Blueprint("comment", __name__)


@comment_bp.route("/post/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    data = request.get_json() if request.is_json else request.form
    result = create_comment(post_id, data)

    if request.is_json or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash(result.get("message", "Comment added successfully."), "success")
    else:
        flash(result.get("message", "Failed to add comment."), "danger")

    return redirect(url_for("post.post_details", post_id=post_id))


@comment_bp.route("/comment/<int:comment_id>", methods=["DELETE"])
@comment_bp.route("/comment/<int:comment_id>/delete", methods=["POST"])
def remove_comment(comment_id):
    result = delete_comment(comment_id)

    if request.is_json or request.method == "DELETE" or request.headers.get("X-Requested-With") == "XMLHttpRequest":
        status_code = 200 if result.get("success") else 400
        return jsonify(result), status_code

    if result.get("success"):
        flash("Comment deleted.", "success")
    else:
        flash(result.get("message", "Failed to delete comment."), "danger")

    post_id = result.get("post_id")
    if post_id:
        return redirect(url_for("post.post_details", post_id=post_id))
    return redirect(url_for("post.feed"))