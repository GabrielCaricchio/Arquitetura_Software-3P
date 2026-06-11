from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, logout_user, current_user
from extensions import db
from models.user import User
from models.student import Student

auth_bp = Blueprint("auth", __name__, url_prefix="")


@auth_bp.route("/register", methods=["GET", "POST"])
def register():
    """Cadastro simples de aluno ou professor."""
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard") if current_user.is_student else url_for("teacher.dashboard"))

    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")
        user_type = request.form.get("user_type", "aluno")

        if not name or not email or not password:
            flash("Preencha todos os campos.", "danger")
            return render_template("register.html")

        if user_type not in ("aluno", "professor"):
            flash("Tipo inválido.", "danger")
            return render_template("register.html")

        existing = User.query.filter_by(email=email).first()
        if existing:
            flash("Esse e-mail já está cadastrado.", "warning")
            return render_template("register.html")

        user = User(name=name, email=email, user_type=user_type)
        user.set_password(password)
        db.session.add(user)
        db.session.flush()

        # Já cria o perfil do aluno para facilitar o fluxo.
        if user_type == "aluno":
            student = Student(user_id=user.id)
            db.session.add(student)

        db.session.commit()
        flash("Cadastro realizado com sucesso. Faça login.", "success")
        return redirect(url_for("auth.login"))

    return render_template("register.html")


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    """Login com Flask-Login."""
    if current_user.is_authenticated:
        return redirect(url_for("student.dashboard") if current_user.is_student else url_for("teacher.dashboard"))

    if request.method == "POST":
        email = request.form.get("email", "").strip().lower()
        password = request.form.get("password", "")

        user = User.query.filter_by(email=email).first()
        if not user or not user.check_password(password):
            flash("E-mail ou senha inválidos.", "danger")
            return render_template("login.html")

        login_user(user)
        flash("Bem-vindo(a) de volta!", "success")
        if user.is_teacher:
            return redirect(url_for("teacher.dashboard"))
        return redirect(url_for("student.dashboard"))

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    """Sai da sessão atual."""
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("home"))
