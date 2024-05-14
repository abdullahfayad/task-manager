import os


class Config:
    SQLALCHEMY_DATABASE_URI = (
        "postgresql://postgres:postgres@postgres:5432/task_manager"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = "abdullah"
    CELERY_BROKER_URL = "redis://redis:6379/0"
    RESULT_BACKEND = "redis://redis:6379/0"
    MONGO_URI = (
        "mongodb://mongo:27017/logging?retryWrites=true&w=majority&appName=Cluster0"
    )
    MAIL_SERVER = "smtp.gmail.com"
    MAIL_PORT = 587
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False
    MAIL_USERNAME = "jadjack900@gmail.com"
    MAIL_PASSWORD = "cpjk pwfn uvbg bmcf"
    MAIL_DEFAULT_SENDER = ("Tal2k", "jadjack900@gmail.com")
