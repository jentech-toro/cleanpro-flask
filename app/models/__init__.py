from flask import Flask
from app.models.product import db
from .customer import Customer


def create_app():

    app = Flask(
        __name__,
        template_folder="templates",
        static_folder="static"
    )

    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///cleanpro.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)

    from app.routers import main
    app.register_blueprint(main)

    with app.app_context():
        db.create_all()

    return app