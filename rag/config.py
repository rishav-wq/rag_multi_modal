import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent

load_dotenv(BASE_DIR / ".env")  # load environment variables


DATA_DIR = BASE_DIR / "data"
ARTIFACTS_DIR = BASE_DIR / "artifacts"
ARTIFACTS_DIR.mkdir(exist_ok=True)

FAISS_INDEX_PATH = ARTIFACTS_DIR / "faiss.index"
METADATA_PATH = ARTIFACTS_DIR / "metadata.json"


EMBEDDING_MODEL_NAME = os.getenv(
    "EMBEDDING_MODEL_NAME", "sentence-transformers/all-MiniLM-L6-v2"
)  # default embedding model

# Online LLM provider
LLM_PROVIDER = os.getenv("LLM_PROVIDER", "groq")  # groq or openrouter

# Groq API (Fast inference - Recommended)
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.1-8b-instant")  # works well

# OpenRouter API (Alternative - supports Grok, GPT, Claude, etc.)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY", "")
OPENROUTER_MODEL = os.getenv("OPENROUTER_MODEL", "x-ai/grok-beta")

# Optional offline LLM via Ollama (e.g. llama3.2, mistral, phi3)
USE_OLLAMA = os.getenv("USE_OLLAMA", "false").lower() == "true"
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "llama3.2")  # or phi3:mini, mistral, etc


def ensure_data_dir() -> None:
    DATA_DIR.mkdir(exist_ok=True)

