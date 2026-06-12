from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from models.user import User
from models.student import Student
from models.story import Story

teacher_bp = Blueprint("teacher", __name__, url_prefix="/teacher")


def teacher_required():
    """Proteção simples para a área do professor."""
    if not current_user.is_authenticated or not current_user.is_teacher:
        flash("Área exclusiva para professores.", "warning")
        return False
    return True


@teacher_bp.route("/dashboard")
@login_required
def dashboard():
    if not teacher_required():
        return redirect(url_for("auth.login"))

    students = Student.query.all()
    stories = Story.query.order_by(Story.created_at.desc()).all()
    total_students = User.query.filter_by(user_type="aluno").count()
    total_teachers = User.query.filter_by(user_type="professor").count()
    total_stories = Story.query.count()

    return render_template(
        "teacher_dashboard.html",
        students=students,
        stories=stories,
        total_students=total_students,
        total_teachers=total_teachers,
        total_stories=total_stories,
    )


@teacher_bp.route("/reports")
@login_required
def reports():
    if not teacher_required():
        return redirect(url_for("auth.login"))

    stories = Story.query.order_by(Story.created_at.desc()).all()
    return render_template("reports.html", stories=stories)
