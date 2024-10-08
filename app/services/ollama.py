import httpx
from typing import Dict, Any, Union

from app.core.config import settings
from app.core.exceptions import OllamaServiceException
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
            raise OllamaServiceException(
                f"OllamaService returned status code: {exc.status_code}."
            )
        except Exception as exc:
            raise OllamaServiceException(f"Failed to connect to ollama service.")

    async def get_current_running_models(self) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(f"{self.base_url}/api/ps")
                response.raise_for_status()
                result = response.json()
                return result
        except httpx.HTTPStatusError as exc:
            raise OllamaServiceException(
                f"OllamaService returned status code: {exc.status_code}."
            )
        except Exception as exc:
            raise OllamaServiceException(f"Failed to connect to ollama service.")

    async def pull_model(self, name: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{self.base_url}/api/pull",
                    json={"name": name, "stream": False},
                    timeout=600.0,
                )
                response.raise_for_status()
                result = response.json()
                return result
        except httpx.HTTPStatusError as exc:
            raise OllamaServiceException(
                f"OllamaService returned status code: {exc.status_code}."
            )
        except Exception as exc:
            raise OllamaServiceException(f"Failed to connect to ollama service.")

    async def delete_model(self, name: str) -> Dict[str, Any]:
        try:
            async with httpx.AsyncClient() as client:
                response = await client.request(
                    method="DELETE",
                    url=f"{self.base_url}/api/delete",
                    json={"name": name},
                    timeout=300.0,
                )
                response.raise_for_status()
                return {"status": "success"}
        except httpx.HTTPStatusError as exc:
            raise OllamaServiceException(
                f"OllamaService returned status code: {exc.status_code}."
            )
        except Exception as exc:
            raise OllamaServiceException(f"Failed to connect to ollama service.")

    async def stream_response(
        self, request: Union[GenerationRequest, ChatRequest], chat: bool = False
    ):
        url = f"{self.base_url}/api/generate"
        if chat:
            url = f"{self.base_url}/api/chat"
        try:
            async with httpx.AsyncClient() as client:
                async with client.stream(
                    method="POST",
                    url=url,
                    json=request.model_dump(exclude=["stream"]),
                    timeout=600.0,
                ) as response:
                    response.raise_for_status()
                    async for chunk in response.aiter_bytes():
                        yield chunk
        except httpx.HTTPStatusError as exc:
            raise OllamaServiceException(
                f"OllamaService returned status code {exc.response.status_code}."
            )
        except Exception as exc:
            raise OllamaServiceException("Failed to connect to ollama service.")

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
            raise OllamaServiceException(
                f"OllamaService returned status code {exc.response.status_code}."
            )
        except Exception as exc:
            raise OllamaServiceException("Failed to connect to ollama service.")

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
            raise OllamaServiceException(
                f"OllamaService returned status code {exc.response.status_code}"
            )
        except Exception as exc:
            raise OllamaServiceException("Failed to connect to ollama service.")


ollama_service = OllamaService()
