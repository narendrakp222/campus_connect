import os
from flask import Flask, redirect, url_for, session, g
from app.database.db import db


def create_app():
    """
    Application Factory Function
    Creates and configures the Flask application instance.
    """
    # Root folder is 1 level up from 'app/' directory
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    template_folder = os.path.join(root_dir, "templates")
    static_folder = os.path.join(root_dir, "static")

    app = Flask(
        __name__,
        template_folder=template_folder,
        static_folder=static_folder
    )

    # Load configuration
    app.config.from_object("app.config.Config")

    # Ensure instance directory exists
    instance_path = os.path.join(root_dir, "instance")
    os.makedirs(instance_path, exist_ok=True)

    # Initialize extensions
    db.init_app(app)

    # Import models so SQLAlchemy can create the tables
    with app.app_context():
        from app.models.user import User
        from app.models.post import Post
        from app.models.comment import Comment
        from app.models.like import Like

        db.create_all()

    # Context processor to inject user into templates
    @app.context_processor
    def inject_user():
        from app.models.user import User
        user_id = session.get("user_id")
        current_user = None
        if user_id:
            current_user = User.query.get(user_id)
        return dict(current_user=current_user)

    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.post import post_bp
    from app.routes.comment import comment_bp
    from app.routes.profile import profile_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(post_bp)
    app.register_blueprint(comment_bp)
    app.register_blueprint(profile_bp)

    @app.route("/")
    def home():
        return redirect(url_for("post.feed"))

    return app