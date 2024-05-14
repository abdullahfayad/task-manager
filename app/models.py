import enum
from sqlalchemy import Enum
from werkzeug.security import generate_password_hash, check_password_hash

from .extensions import db


class UserType(enum.Enum):
    regular = "regular"
    admin = "admin"


class Priority(enum.Enum):
    low = "Low"
    high = "High"
    medium = "Medium"


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(256))
    user_type = db.Column(Enum(UserType), default=UserType.regular, nullable=False)
    tasks = db.relationship("Task", backref="owner")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=False)
    priority = db.Column(Enum(Priority), nullable=False)
    due_date = db.Column(db.Date, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "priority": self.priority.value,
            "due_date": self.due_date.isoformat(),
        }
