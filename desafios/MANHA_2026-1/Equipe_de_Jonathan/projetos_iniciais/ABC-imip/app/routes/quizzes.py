from flask import Blueprint, request, jsonify

from app.models import (
    Question,
    Attempt,
    Answer
)

from app import db

quiz_bp = Blueprint(
    "quiz",
    __name__,
    url_prefix="/quizzes"
)

# =========================
# ENVIAR RESPOSTAS
# =========================

@quiz_bp.route("/submit", methods=["POST"])
def submit_quiz():

    data = request.get_json()

    score = 0

    # Cria tentativa
    attempt = Attempt(
        student_id=data["student_id"],
        quiz_id=data["quiz_id"],
        score=0
    )

    db.session.add(attempt)
    db.session.commit()

    # Percorre respostas
    for answer in data["answers"]:

        # Busca questão
        question = Question.query.get(
            answer["question_id"]
        )

        # Verifica acerto
        is_correct = (
            answer["student_answer"].lower()
            ==
            question.correct_answer.lower()
        )

        # Soma ponto
        if is_correct:
            score += 1

        # Salva resposta
        new_answer = Answer(
            attempt_id=attempt.id,
            question_id=question.id,
            student_answer=answer["student_answer"],
            is_correct=is_correct
        )

        db.session.add(new_answer)

    # Atualiza nota
    attempt.score = score

    db.session.commit()

    return jsonify({
        "message": "Quiz enviado",
        "score": score
    })