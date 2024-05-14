from flask import (
    Blueprint,
    flash,
    redirect,
    request,
    jsonify,
    render_template,
    session,
    url_for,
)
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


from .models import User
from .extensions import db
from app.utils.log import log_event

auth = Blueprint("auth", __name__)


@auth.route("/signup", methods=["POST"])
def signup():
    email = request.form.get("email")
    username = request.form.get("username")
    password = request.form.get("password")
    user_type = request.form.get("user_type")

    user = User.query.filter(
        (User.username == username.lower()) | (User.email == email.lower())
    ).first()
    if user:
        return redirect(url_for("auth.register_form"))

    user = User(username=username, email=email, user_type=user_type)
    user.set_password(password)
    db.session.add(user)
    db.session.commit()

    log_event("User Registration", "User successfully registered", email)

    return redirect(url_for("auth.login_form"))


@auth.route("/signin", methods=["POST"])
def signin():
    email = request.form.get("email")
    password = request.form.get("password")

    user = User.query.filter_by(email=email).first()
    if user and user.verify_password(password):
        access_token = create_access_token(
            identity=dict(id=user.id, email=user.email, user_type=user.user_type.name)
        )
        session["access_token"] = access_token

        log_event("User Login", "User successfully logged in", email)

        return redirect(url_for("task.get_tasks"))

    return redirect(url_for("auth.login_form"))


@auth.route("/login")
def login_form():
    return render_template("login.html")


@auth.route("/register")
def register_form():
    return render_template("register.html")
