from fastapi import APIRouter
from starlette import status
from app.services.ollama import ollama_service

router = APIRouter(prefix="/api", tags=["Model Management"])


@router.get("/tags", status_code=status.HTTP_200_OK)
async def list_models():
    response = await ollama_service.get_models()
    return response
