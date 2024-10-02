from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    model: str = Field(
        description="Name of the model to use.", min_length=1, default="phi3:latest"
    )
    prompt: str = Field(
        description="User prompt",
        default="Hi, what is the color of the sky? Provide one word answer only.",
    )
    stream: bool = False
