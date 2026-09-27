from flask import Blueprint, request, redirect, url_for, flash
from app.services.comment_service import (
    create_comment,
    delete_comment
)

comment_bp = Blueprint("comment", __name__)


@comment_bp.route("/post/<int:post_id>/comment", methods=["POST"])
def add_comment(post_id):
    result = create_comment(post_id, request.form)

    if result.get("success"):
        flash(result.get("message", "Comment added successfully."), "success")
    else:
        flash(result.get("message", "Failed to add comment."), "danger")

    return redirect(url_for("post.post_details", post_id=post_id))


@comment_bp.route("/comment/<int:comment_id>", methods=["DELETE"])
def remove_comment(comment_id):
    result = delete_comment(comment_id)

    if result.get("success"):
        return {
            "success": True,
            "message": result.get("message", "Comment deleted successfully.")
        }, 200

    return {
        "success": False,
        "message": result.get("message", "Failed to delete comment.")
    }, 400