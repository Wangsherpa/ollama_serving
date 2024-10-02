import httpx
from typing import List, Dict, Any

from app.core.config import settings
from app.models.model import GenerationRequest


class OllamaService:
    def __init__(self, base_url: str = settings.OLLAMA_URL):
        self.base_url = base_url

    async def generate_text(self, request: GenerationRequest) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/generate",
                    json=request.model_dump(),
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
