from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required, current_user
from models.story import Story

story_bp = Blueprint("story", __name__, url_prefix="/stories")


@story_bp.route("/<int:story_id>")
@login_required
def view_story(story_id):
    """Página da história criada."""
    story = Story.query.get_or_404(story_id)
    if current_user.is_student and story.student.user_id != current_user.id:
        flash("Você não pode ver a história de outro aluno.", "warning")
        return redirect(url_for("student.dashboard"))
    return render_template("story.html", story=story)
