from fastapi import HTTPException


class OllamaBaseException(Exception):
    """
    Base exception class for Ollama-Gateway.
    All custom exceptions in the application should inherit from this.
    """

    def __init__(self, message: str, error_code: str):
        self.message = message
        self.error_code = error_code
        super().__init__(self.message)


class OllamaServiceException(OllamaBaseException):
    """
    Exception raised when there's an error with the Ollama service.
    """

    def __init__(self, message: str):
        super().__init__(message, "OLLAMA_SERVICE_ERROR")


class ModelNotFoundException(OllamaBaseException):
    """Exception raised when a requested model is not found."""

    def __init__(self, model: str):
        super().__init__(f"Model {model} not found", "MODEL_NOT_FOUND")
