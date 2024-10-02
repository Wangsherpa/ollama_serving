from fastapi import FastAPI
from app.api.routers import generation
from app.api.routers import model_management

app = FastAPI()
app.include_router(generation.router)
app.include_router(model_management.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Ollama. Go to http://ollama_url/docs to access swagger-ui."
    }
