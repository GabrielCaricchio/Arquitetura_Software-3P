import os
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_DIR.mkdir(exist_ok=True)

class Config:
    """Configuração simples para rodar localmente no VS Code."""
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-trocar")
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{DATABASE_DIR / 'trilhas.db'}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # OpenRouter
    OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
    OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "openai/gpt-4o-mini")
    OPENROUTER_BASE_URL = os.getenv("OPENROUTER_BASE_URL", "https://openrouter.ai/api/v1/chat/completions")
