from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from starlette import status
from app.services.ollama import ollama_service
from app.models.model import GenerationRequest, ChatRequest
from app.core.exceptions import ModelNotFoundException, OllamaBaseException

router = APIRouter(prefix="/api", tags=["Generation"])


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate(request: GenerationRequest) -> dict:
    try:
        requested_model = request.model
        if ":" not in requested_model:
            requested_model += ":latest"
        available_models = await ollama_service.get_models()
        model_names = [model["name"] for model in available_models["models"]]
        if requested_model not in model_names:
            raise ModelNotFoundException(requested_model)
        response = await ollama_service.generate_text(request=request)
        return response
    except ModelNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise OllamaBaseException("Failed to generate response", "GENERATION_ERROR")

    return response


@router.post("/chat", status_code=status.HTTP_201_CREATED)
async def chat(request: ChatRequest) -> dict:
    try:
        requested_model = request.model
        if ":" not in requested_model:
            requested_model += ":latest"
        available_models = await ollama_service.get_models()
        model_names = [model["name"] for model in available_models["models"]]
        if requested_model not in model_names:
            raise ModelNotFoundException(requested_model)
        response = await ollama_service.chat(request)
    except ModelNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise OllamaBaseException("Failed to generate response", "CHAT_ERROR")

    return response
