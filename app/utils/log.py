import datetime

from flask import current_app


def log_event(event_type, description, data):
    mongo_db = current_app.mongo_db
    mongo_db.logs.insert_one(
        {
            "event_type": event_type,
            "description": description,
            "data": data,
            "timestamp": datetime.datetime.utcnow(),
        }
    )
