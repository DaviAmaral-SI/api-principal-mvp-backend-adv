from pydantic import BaseModel

class ErrorSchema(BaseModel):
    """Esquema para representar mensagens de erro."""
    message: str