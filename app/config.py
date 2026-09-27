import os


class Config:
    # Base directory of the project
    BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

    # Security
    SECRET_KEY = os.environ.get("SECRET_KEY", "change-this-secret-key-in-production")

    # Database
    SQLALCHEMY_DATABASE_URI = (
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'social.db')}"
    )

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Optional settings
    DEBUG = True