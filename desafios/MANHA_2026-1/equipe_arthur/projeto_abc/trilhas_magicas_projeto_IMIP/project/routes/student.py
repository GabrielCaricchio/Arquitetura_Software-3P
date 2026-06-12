from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_required, current_user
from extensions import db
from models.student import Student
from models.story import Story
from models.challenge import Challenge
from services.openrouter_service import generate_story

student_bp = Blueprint("student", __name__, url_prefix="/student")


def student_required():
    """Proteção simples para impedir acesso de professor às páginas do aluno."""
    if not current_user.is_authenticated or not current_user.is_student:
        flash("Área exclusiva para alunos.", "warning")
        return False
    return True


@student_bp.route("/dashboard")
@login_required
def dashboard():
    if not student_required():
        return redirect(url_for("auth.login"))

    student = Student.query.filter_by(user_id=current_user.id).first()
    stories = Story.query.filter_by(student_id=student.id).order_by(Story.created_at.desc()).all() if student else []
    return render_template("student_dashboard.html", student=student, stories=stories)


@student_bp.route("/profile", methods=["GET", "POST"])
@login_required
def profile():
    if not student_required():
        return redirect(url_for("auth.login"))

    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        student = Student(user_id=current_user.id)
        db.session.add(student)

    if request.method == "POST":
        age = request.form.get("age") or None
        favorite_story = request.form.get("favorite_story", "").strip()
        favorite_activity = request.form.get("favorite_activity", "").strip()
        reading_level = request.form.get("reading_level", "").strip()

        student.age = int(age) if age else None
        student.favorite_story = favorite_story
        student.favorite_activity = favorite_activity
        student.reading_level = reading_level

        db.session.commit()
        flash("Perfil atualizado com sucesso.", "success")
        return redirect(url_for("student.dashboard"))

    return render_template("create_story.html", student=student)


@student_bp.route("/generate-story", methods=["POST"])
@login_required
def generate_story_route():
    if not student_required():
        return redirect(url_for("auth.login"))

    student = Student.query.filter_by(user_id=current_user.id).first()
    if not student:
        flash("Crie seu perfil primeiro.", "warning")
        return redirect(url_for("student.profile"))

    student.age = int(request.form.get("age")) if request.form.get("age") else None
    student.favorite_story = request.form.get("favorite_story", "").strip()
    student.favorite_activity = request.form.get("favorite_activity", "").strip()
    student.reading_level = request.form.get("reading_level", "").strip()

    if not student.age or not student.favorite_story or not student.favorite_activity or not student.reading_level:
        db.session.commit()
        flash("Preencha o perfil completo para gerar a história.", "warning")
        return render_template("create_story.html", student=student)

    profile = {
        "name": current_user.name,
        "age": student.age,
        "favorite_story": student.favorite_story,
        "favorite_activity": student.favorite_activity,
        "reading_level": student.reading_level,
    }

    from flask import current_app
    generated = generate_story(
        profile=profile,
        api_key=current_app.config["OPENROUTER_API_KEY"],
        model=current_app.config["OPENROUTER_MODEL"],
        base_url=current_app.config["OPENROUTER_BASE_URL"],
    )

    story = Story(
        student_id=student.id,
        title=generated["title"],
        content=generated["content"],
    )
    db.session.add(story)
    db.session.flush()

    for item in generated["challenges"]:
        challenge = Challenge(
            story_id=story.id,
            question=item["question"],
            answer=item["answer"],
        )
        db.session.add(challenge)

    db.session.commit()
    flash("História criada com sucesso!", "success")
    return redirect(url_for("story.view_story", story_id=story.id))


@student_bp.route("/quiz/<int:story_id>", methods=["GET", "POST"])
@login_required
def quiz(story_id):
    if not student_required():
        return redirect(url_for("auth.login"))

    story = Story.query.get_or_404(story_id)
    challenges = story.challenges
    result = None

    if request.method == "POST":
        score = 0
        total = len(challenges)
        answers = []
        for i, challenge in enumerate(challenges, start=1):
            user_answer = request.form.get(f"answer_{i}", "").strip().lower()
            expected = (challenge.answer or "").strip().lower()
            answers.append(user_answer)

            # Correção simples e leve: considera certo se a resposta do aluno contém a palavra-chave esperada.
            if expected and (expected in user_answer or user_answer in expected):
                score += 1

        result = {
            "score": score,
            "total": total,
        }

    return render_template("quiz.html", story=story, challenges=challenges, result=result)
