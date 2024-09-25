from fastapi import APIRouter, HTTPException
from app.services.ollama import ollama_service

router = APIRouter()  # TODO: add prefix


@router.post("/generate")
async def generate(model: str, prompt: str) -> dict:
    response = ollama_service.generate_text(model=model, prompt=prompt)
    return response
