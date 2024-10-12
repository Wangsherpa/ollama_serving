import os
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    # Ollama configuration
    OLLAMA_URL: str = os.getenv("OLLAMA_URL", "http://localhost:11434")
    OLLAMA_KEEP_ALIVE: str = os.getenv("OLLAMA_KEEP_ALIVE", "5m")
    OLLAMA_HOST: str = os.getenv("OLLAMA_HOST", "0.0.0.0")
    OLLAMA_USE_GPU: bool = os.getenv("OLLAMA_USE_GPU", "false").lower() == "true"


settings = Settings()
