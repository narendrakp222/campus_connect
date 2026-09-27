def create_comment(post_id, form_data):
    """
    Handle comment creation business logic.

    Args:
        post_id (int): ID of the post being commented on
        form_data: request.form

    Returns:
        dict
    """

    comment_text = form_data.get("comment", "").strip()

    if not comment_text:
        return {
            "success": False,
            "message": "Comment cannot be empty."
        }

    # Database save logic will be added later

    return {
        "success": True,
        "message": "Comment added successfully.",
        "post_id": post_id
    }


def delete_comment(comment_id):
    """
    Handle comment deletion business logic.

    Args:
        comment_id (int): ID of the comment

    Returns:
        dict
    """

    # Database delete logic will be added later

    return {
        "success": True,
        "message": f"Comment {comment_id} deleted successfully."
    }