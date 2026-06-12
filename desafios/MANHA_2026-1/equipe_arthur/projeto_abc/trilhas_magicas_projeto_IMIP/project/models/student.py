from extensions import db


class Student(db.Model):
    """Perfil do aluno para personalizar a história."""
    __tablename__ = "students"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False, unique=True)
    age = db.Column(db.Integer, nullable=True)
    favorite_story = db.Column(db.String(150), nullable=True)
    favorite_activity = db.Column(db.String(150), nullable=True)
    reading_level = db.Column(db.String(50), nullable=True)

    user = db.relationship("User", back_populates="student")
    stories = db.relationship("Story", back_populates="student", cascade="all, delete-orphan")
