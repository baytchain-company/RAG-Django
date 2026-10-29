"""Django settings for django-rag."""
import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


def env(key, default=None):
    return os.getenv(key, default)


SECRET_KEY = env("DJANGO_SECRET_KEY", "dev-only-change-me")
DEBUG = env("DJANGO_DEBUG", "1") == "1"
ALLOWED_HOSTS = env("DJANGO_ALLOWED_HOSTS", "localhost,127.0.0.1").split(",")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "apps.documents",
    "apps.rag",
    "apps.api",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]
WSGI_APPLICATION = "config.wsgi.application"

# PostgreSQL + pgvector is required (vector search runs inside the database).
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("POSTGRES_DB", "rag"),
        "USER": env("POSTGRES_USER", "rag"),
        "PASSWORD": env("POSTGRES_PASSWORD", "rag"),
        "HOST": env("POSTGRES_HOST", "localhost"),
        "PORT": env("POSTGRES_PORT", "5432"),
    }
}

LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Tashkent"
USE_I18N = True
USE_TZ = True
STATIC_URL = "static/"
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
DATA_UPLOAD_MAX_MEMORY_SIZE = 20 * 1024 * 1024

REST_FRAMEWORK = {
    "DEFAULT_RENDERER_CLASSES": ["rest_framework.renderers.JSONRenderer"],
}

# ---------------------------------------------------------------- RAG settings
RAG = {
    # Embeddings: "sentence-transformers" (free, local), "ollama", "openai", "hash" (offline demo/tests)
    "EMBEDDING_PROVIDER": env("RAG_EMBEDDING_PROVIDER", "sentence-transformers"),
    "EMBEDDING_MODEL": env("RAG_EMBEDDING_MODEL", "intfloat/multilingual-e5-small"),
    # Must match the model. e5-small = 384, nomic-embed-text = 768, text-embedding-3-small = 1536.
    "EMBEDDING_DIM": int(env("RAG_EMBEDDING_DIM", "384")),
    # LLM: "ollama" (free, local), "openai" (any OpenAI-compatible API), "none" (returns the found chunks)
    "LLM_PROVIDER": env("RAG_LLM_PROVIDER", "ollama"),
    "LLM_MODEL": env("RAG_LLM_MODEL", "llama3.2"),
    "OLLAMA_URL": env("OLLAMA_URL", "http://localhost:11434"),
    "OPENAI_BASE_URL": env("OPENAI_BASE_URL", "https://api.openai.com/v1"),
    "OPENAI_API_KEY": env("OPENAI_API_KEY", ""),
    # Chunking: the most important part of RAG quality.
    "CHUNK_SIZE": int(env("RAG_CHUNK_SIZE", "500")),
    "CHUNK_OVERLAP": int(env("RAG_CHUNK_OVERLAP", "100")),
    "TOP_K": int(env("RAG_TOP_K", "4")),
    # Chunks farther than this cosine distance are ignored (0 = identical, 2 = opposite).
    "MAX_DISTANCE": float(env("RAG_MAX_DISTANCE", "0.8")),
}
