from fastapi import FastAPI
from app.api.routers import generation

app = FastAPI()
app.include_router(generation.router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Ollama. Go to http://ollama_url/docs to access swagger-ui."
    }
