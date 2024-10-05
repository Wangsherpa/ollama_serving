from fastapi import APIRouter
from starlette import status
from app.services.ollama import ollama_service

router = APIRouter(prefix="/api", tags=["Model Management"])


@router.get("/tags", status_code=status.HTTP_200_OK)
async def list_models():
    response = await ollama_service.get_models()
    return response


@router.get("/ps", status_code=status.HTTP_200_OK)
async def list_current_running_models():
    response = await ollama_service.get_current_running_models()
    return response


@router.post("/pull", status_code=status.HTTP_201_CREATED)
async def pull_model(name: str):
    response = await ollama_service.pull_model(name)
    return response


@router.delete("/delete", status_code=status.HTTP_201_CREATED)
async def delete_model(name: str):
    response = await ollama_service.delete_model(name)
    return response
