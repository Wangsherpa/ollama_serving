from fastapi import APIRouter, HTTPException
from starlette import status
from app.services.ollama import ollama_service
from app.models.model import GenerationRequest, ChatRequest

router = APIRouter(prefix="/api", tags=["Generation"])


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate(request: GenerationRequest) -> dict:
    response = await ollama_service.generate_text(request=request)
    return response


@router.post("/chat", status_code=status.HTTP_201_CREATED)
async def chat(request: ChatRequest) -> dict:
    response = await ollama_service.chat(request)
    return response
