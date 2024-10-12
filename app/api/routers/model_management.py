from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from starlette import status
from app.core.exceptions import ModelNotFoundException, OllamaBaseException
from app.services.ollama import ollama_service
from app.core.auth import get_current_user


router = APIRouter(prefix="/api", tags=["Model Management"])

user_dependency = Annotated[dict, Depends(get_current_user)]


@router.get("/tags", status_code=status.HTTP_200_OK)
async def list_models(user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        response = await ollama_service.get_models()
    except Exception as e:
        raise OllamaBaseException("Failed to get models", "MODEL_MGMT_ERROR")
    return response


@router.get("/ps", status_code=status.HTTP_200_OK)
async def list_current_running_models(user: user_dependency):
    if not user:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        response = await ollama_service.get_current_running_models()
    except Exception as e:
        raise OllamaBaseException("Failed to get current model", "MODEL_MGMT_ERROR")
    return response


@router.post("/pull", status_code=status.HTTP_201_CREATED)
async def pull_model(name: str, user: user_dependency):
    if user:
        if user.get("role") not in ["admin"]:
            raise HTTPException(
                status_code=401, detail="Operation not permitted for users."
            )
    else:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        response = await ollama_service.pull_model(name)
    except Exception as e:
        raise OllamaBaseException("Failed to pull model", "MODEL_MGMT_ERROR")
    return response


@router.delete("/delete", status_code=status.HTTP_201_CREATED)
async def delete_model(name: str, user: user_dependency):
    if user:
        if user.get("role") not in ["admin"]:
            raise HTTPException(
                status_code=401, detail="Operation not permitted for users."
            )
    else:
        raise HTTPException(status_code=401, detail="Not Authenticated")
    try:
        requested_model = name
        if ":" not in requested_model:
            requested_model += ":latest"
        available_models = await ollama_service.get_models()
        model_names = [model["name"] for model in available_models["models"]]
        if requested_model not in model_names:
            raise ModelNotFoundException(requested_model)
        response = await ollama_service.delete_model(name)
    except ModelNotFoundException as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception:
        raise OllamaBaseException("Failed to delete model", "MODEL_MGMT_ERROR")
    return response
