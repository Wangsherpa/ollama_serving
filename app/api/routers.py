from fastapi import APIRouter, HTTPException
from starlette import status
from app.services.ollama import ollama_service
from app.models.model import GenerationRequest

router = APIRouter()  # TODO: add prefix


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate(request: GenerationRequest) -> dict:
    response = await ollama_service.generate_text(request=request)
    return response
