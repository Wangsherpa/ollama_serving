from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.api.routers import generation
from app.api.routers import model_management
from app.core.exceptions import OllamaBaseException

app = FastAPI()
app.include_router(generation.router)
app.include_router(model_management.router)


# Exception handlers
@app.exception_handler(OllamaBaseException)
async def ollama_exception_handler(request, exc: OllamaBaseException):
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal Server Error",
            "detail": str(exc),
            "error_code": exc.error_code,
        },
    )


@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc: HTTPException):
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": "HTTP Exception",
            "detail": exc.detail,
            "error_code": f"HTTP_{exc.status_code}",
        },
    )


@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request, exc: RequestValidationError):
    return JSONResponse(
        status_code=422,
        content={
            "error": "Validation Error",
            "detail": str(exc),
            "error_code": "VALIDATION_ERROR",
        },
    )


@app.get("/")
async def root():
    return {
        "message": "Welcome to Ollama. Go to http://ollama_url/docs to access swagger-ui."
    }
