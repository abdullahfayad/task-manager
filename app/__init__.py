from pymongo import MongoClient
from flask import Flask, render_template

from .auth import auth
from .task import task
from config import Config
from .extensions import db, migrate, jwt, celery, mail


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    mongo_client = MongoClient(app.config["MONGO_URI"])
    mongo_db = mongo_client.get_default_database()
    app.mongo_client = mongo_client
    app.mongo_db = mongo_db

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)
    mail.init_app(app)

    celery.conf.update(
        broker_url=app.config["CELERY_BROKER_URL"],
        result_backend=app.config["RESULT_BACKEND"],
        include=["app.celery_tasks"],
    )

    @app.route("/")
    def index():
        return render_template("index.html")

    app.register_blueprint(auth, url_prefix="/auth")
    app.register_blueprint(task, url_prefix="/tasks")

    return app, celery
