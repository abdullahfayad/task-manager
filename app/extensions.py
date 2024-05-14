from celery import Celery
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager


db = SQLAlchemy()
celery = Celery()
jwt = JWTManager()
migrate = Migrate()
mail = Mail()
