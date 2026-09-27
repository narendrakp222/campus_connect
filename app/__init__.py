from flask import Flask


def create_app():
    """
    Application Factory Function
    Creates and configures the Flask application instance.
    """

    app = Flask(__name__)

    # Load configuration
    app.config.from_object("app.config.Config")

    # Initialize extensions here later
    # Example:
    # db.init_app(app)

    # Register blueprints here later
    # Example:
    # from app.routes.auth import auth_bp
    # app.register_blueprint(auth_bp)

    @app.route("/")
    def home():
        return {"message": "CampusConnect API is running"}

    return app