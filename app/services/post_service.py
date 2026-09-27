def create_post(form_data):
    """
    Handle post creation business logic.

    Args:
        form_data: request.form

    Returns:
        dict
    """

    content = form_data.get("content", "").strip()

    if not content:
        return {
            "success": False,
            "message": "Post content cannot be empty."
        }

    # Database save logic will be added later

    return {
        "success": True,
        "message": "Post created successfully."
    }


def get_feed():
    """
    Return all posts for feed.

    Returns:
        list
    """

    # Database query will be added later

    return [
        {
            "id": 1,
            "username": "Narendra",
            "content": "Welcome to CampusConnect!",
            "likes": 0,
            "comments": 0
        }
    ]


def get_post(post_id):
    """
    Return a single post.

    Args:
        post_id: int

    Returns:
        dict | None
    """

    # Database query will be added later

    dummy_post = {
        "id": post_id,
        "username": "Narendra",
        "content": "Sample post content.",
        "likes": 0,
        "comments": []
    }

    return dummy_post


def delete_post(post_id):
    """
    Delete a post.

    Args:
        post_id: int

    Returns:
        dict
    """

    # Database delete logic will be added later

    return {
        "success": True,
        "message": f"Post {post_id} deleted successfully."
    }