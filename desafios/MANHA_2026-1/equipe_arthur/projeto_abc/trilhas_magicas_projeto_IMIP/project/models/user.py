from flask_login import UserMixin
from extensions import db
import bcrypt


class User(UserMixin, db.Model):
    """Usuário do sistema: aluno ou professor."""
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    user_type = db.Column(db.String(20), nullable=False)  # professor | aluno

    student = db.relationship("Student", back_populates="user", uselist=False, cascade="all, delete-orphan")

    def set_password(self, raw_password: str):
        """Gera o hash da senha com bcrypt."""
        hashed = bcrypt.hashpw(raw_password.encode("utf-8"), bcrypt.gensalt())
        self.password = hashed.decode("utf-8")

    def check_password(self, raw_password: str) -> bool:
        """Confere se a senha digitada bate com o hash salvo."""
        return bcrypt.checkpw(raw_password.encode("utf-8"), self.password.encode("utf-8"))

    @property
    def is_teacher(self):
        return self.user_type == "professor"

    @property
    def is_student(self):
        return self.user_type == "aluno"
