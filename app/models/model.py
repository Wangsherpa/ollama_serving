from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field


class GenerationRequest(BaseModel):
    model: str = Field(
        description="Name of the model to use.", min_length=1, default="phi3:latest"
    )
    prompt: str = Field(
        description="User prompt",
        min_length=1,
        default="Hi, what is the color of the sky? Provide one word answer only.",
    )
    stream: Optional[bool] = False


class ChatRole(str, Enum):
    user = "user"
    system = "system"
    assistant = "assistant"


class ChatMessage(BaseModel):
    role: ChatRole = Field("Supported roles: system, user and assistant.")
    content: str = Field(min_length=1)


class ChatRequest(BaseModel):
    model: str = Field(
        description="Name of the model to use.", min_length=1, default="phi3:latest"
    )
    messages: List[ChatMessage] = Field(
        description="List of messages to be passed to the model.",
        default=[{"role": "user", "content": "What is the color of the sky?"}],
    )
    stream: Optional[bool] = False
