import httpx
from typing import List, Dict, Any

from app.core.config import settings


class OllamaService:
    def __init__(self, base_url: str = settings.OLLAMA_URL):
        self.base_url = base_url

    # TODO: Make this function asynchronous
    def generate_text(self, model: str, prompt: str) -> Dict[str, Any]:
        try:
            with httpx.Client() as client:
                response = client.post(
                    f"{self.base_url}/api/generate",
                    json={"model": model, "prompt": prompt, "stream": False},
                    timeout=600.0,
                )
                response.raise_for_status()
                result = response.json()
                return result
        except httpx.HTTPStatusError as exc:
            # TODO: Create custom exception class for Ollama service.
            raise Exception(
                f"OllamaService returned status code {exc.response.status_code}."
            )
        except Exception as exc:
            raise Exception("Failed to connect to ollama service.")

    def chat(self, model: str, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        # TOTO: Implementation required
        return {"message": "Not implemented."}


ollama_service = OllamaService()
