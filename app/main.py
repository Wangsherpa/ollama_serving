from fastapi import FastAPI
from app.api.routers import router

app = FastAPI()
app.include_router(router)


@app.get("/")
async def root():
    return {
        "message": "Welcome to Ollama. Go to http://ollama_url/docs to access swagger-ui."
    }
