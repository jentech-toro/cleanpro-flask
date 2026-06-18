from flask import Flask
from app.models.product import db
from dotenv import load_dotenv
import os

load_dotenv()


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "dev-fallback-key")

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cleanpro.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routes.public import public
    from app.routes.admin import admin
    from app.routes.auth import auth

    app.register_blueprint(public)
    app.register_blueprint(admin)
    app.register_blueprint(auth)

    with app.app_context():
        from app.models import customer, order  # noqa: F401 — register models
        db.create_all()

    return app