import os
from flask import Flask
from dotenv import load_dotenv

from config import Config
from extensions import db, migrate, login_manager
from models.user import User
from routes.auth import auth_bp
from routes.student import student_bp
from routes.teacher import teacher_bp
from routes.story import story_bp


def create_app():
    """Cria e configura o app Flask."""
    load_dotenv()

    app = Flask(__name__)
    app.config.from_object(Config)

    # Garante que o diretório do banco exista antes do SQLAlchemy abrir o arquivo.
    os.makedirs("database", exist_ok=True)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(teacher_bp)
    app.register_blueprint(story_bp)

    @app.route("/")
    def home():
        from flask import render_template
        return render_template("home.html")

    # Criação automática das tabelas para facilitar a primeira execução.
    with app.app_context():
        db.create_all()

    return app


app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
