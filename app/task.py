from flask import (
    request,
    session,
    jsonify,
    url_for,
    redirect,
    Blueprint,
    render_template,
)
from flask_jwt_extended import decode_token, jwt_required, get_jwt_identity

from app.celery_tasks import send_email


from .extensions import db
from .models import Task, Priority
from app.utils.log import log_event

task = Blueprint("task", __name__)


@task.route("/", methods=["GET"])
def get_tasks():
    tasks = []
    access_token = session.get("access_token")

    if not access_token:
        return redirect(url_for("auth.login_form"))

    decoded_token = decode_token(access_token)
    user_info = decoded_token["sub"]
    user_type = user_info.get("user_type")
    user_id = user_info.get("id")

    if user_type == "admin":
        tasks = Task.query.all()
    else:
        tasks = Task.query.filter_by(user_id=user_id).all()

    return render_template("tasks.html", tasks=tasks)


@task.route("/<int:task_id>", methods=["GET"])
@jwt_required()
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(
        {
            "id": task.id,
            "name": task.name,
            "description": task.description,
            "priority": task.priority.name,
            "due_date": task.due_date.isoformat(),
        }
    )


@task.route("/", methods=["POST"])
@jwt_required()
def create_task():
    user_id = get_jwt_identity().get("id")
    email = get_jwt_identity().get("email")
    data = request.form
    name, description, priority, due_date = (
        data[k] for k in ("name", "description", "priority", "due_date")
    )
    priority = Priority[priority]
    task = Task(
        name=name,
        user_id=user_id,
        priority=priority,
        due_date=due_date,
        description=description,
    )
    db.session.add(task)
    db.session.commit()

    log_event("Task Creation", "Task created successfully", data)
    send_email.delay(email, "Task Created", "Task created successfully")

    return Task.to_dict(task)


@task.route("/update/<int:task_id>", methods=["POST"])
@jwt_required()
def edit_task(task_id):
    email = get_jwt_identity().get("email")
    task = Task.query.get_or_404(task_id)

    data = request.form
    task.name = data["name"]
    task.description = data["description"]
    task.priority = Priority[data["priority"]]
    task.due_date = data["due_date"]
    db.session.commit()

    log_event("Task Update", "Task updated successfully", data)
    send_email.delay(email, "Task Updated", "Task updated successfully")

    return redirect("/tasks")


@task.route("/<int:task_id>", methods=["DELETE"])
@jwt_required()
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()

    log_event("Task Deletion", "Task deleted successfully", task_id)

    return jsonify({"message": "Task deleted successfully"})
