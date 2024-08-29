from flask import Flask
from src.tax_report import tax_report
from src.database import db
import os
from dotenv import load_dotenv

load_dotenv()


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI=os.getenv(
            'SQLALCHEMY_DATABASE_URI'),
    )

    if test_config:
        app.config.from_mapping(test_config)

    db.init_app(app)

    with app.app_context():
        db.create_all()

    app.register_blueprint(tax_report)

    @app.get("/")
    def index():
        return "Hello World"

    return app
