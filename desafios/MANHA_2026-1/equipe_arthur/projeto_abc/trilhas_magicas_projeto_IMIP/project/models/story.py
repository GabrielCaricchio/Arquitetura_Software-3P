from datetime import datetime
from extensions import db


class Story(db.Model):
    """História criada pela IA para o aluno."""
    __tablename__ = "stories"

    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    content = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    student = db.relationship("Student", back_populates="stories")
    challenges = db.relationship("Challenge", back_populates="story", cascade="all, delete-orphan")
