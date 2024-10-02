import httpx
from typing import Dict, Any

from app.core.config import settings
from app.models.model import GenerationRequest, ChatRequest


class OllamaService:
    def __init__(self, base_url: str = settings.OLLAMA_URL):
        self.base_url = base_url

    async def get_models(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                result = response.json()
                return result
        except httpx.HTTPStatusError as exc:
            raise Exception(f"OllamaService returned status code: {exc.status_code}.")
        except Exception as exc:
            raise Exception(f"Failed to connect to ollama service.")

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

    async def chat(self, request: ChatRequest) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/chat",
                    json=request.model_dump(),
                    timeout=600.0,
                )
                response.raise_for_status()
                result = response.json()
                return result
        except httpx.HTTPStatusError as exc:
            raise Exception(
                f"OllamaService returned status code {exc.response.status_code}"
            )
        except Exception as exc:
            raise Exception("Failed to connect to ollama service.")


ollama_service = OllamaService()
