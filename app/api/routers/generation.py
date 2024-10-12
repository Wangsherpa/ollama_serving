from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import StreamingResponse
from starlette import status
from app.services.ollama import ollama_service
from app.models.llm import GenerationRequest, ChatRequest
from app.core.exceptions import ModelNotFoundException, OllamaBaseException
from app.core.auth import get_current_user

router = APIRouter(prefix="/api", tags=["Generation"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.post("/generate", status_code=status.HTTP_201_CREATED)
async def generate(request: GenerationRequest, user: user_dependency) -> dict:
    try:
        if user is None:
            raise HTTPException(status_code=401, detail="Not Authenticated")
        requested_model = request.model
        if ":" not in requested_model:
            requested_model += ":latest"
        available_models = await ollama_service.get_models()
        model_names = [model["name"] for model in available_models["models"]]
        if requested_model not in model_names:
            raise ModelNotFoundException(requested_model)

        if request.stream:
            return StreamingResponse(
                ollama_service.stream_response(request), media_type="text/event-stream"
            )
        else:
            response = await ollama_service.generate_text(request=request)
            return response
    except ModelNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise OllamaBaseException("Failed to generate response", "GENERATION_ERROR")


@router.post("/chat", status_code=status.HTTP_201_CREATED)
async def chat(request: ChatRequest, user: user_dependency) -> dict:
    try:
        if not user:
            raise HTTPException(status_code=401, detail="Not Authenticated")
        requested_model = request.model
        if ":" not in requested_model:
            requested_model += ":latest"
        available_models = await ollama_service.get_models()
        model_names = [model["name"] for model in available_models["models"]]
        if requested_model not in model_names:
            raise ModelNotFoundException(requested_model)
        if request.stream:
            return StreamingResponse(
                ollama_service.stream_response(request, chat=True),
                media_type="text/event-stream",
            )
        else:
            response = await ollama_service.chat(request)
            return response
    except ModelNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        raise OllamaBaseException("Failed to generate response", "CHAT_ERROR")
