from flask_mail import Message

from .extensions import celery, mail


@celery.task
def send_email(email, subject, message):
    try:
        msg = Message(
            subject=subject,
            recipients=[email],
        )
        msg.body = message
        mail.send(msg)
        return "Mail sent!"
    except Exception as e:
        print(str(e))
