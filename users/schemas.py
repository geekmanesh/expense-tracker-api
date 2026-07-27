from pydantic import BaseModel


class BaseUserSchema(BaseModel):
    username: str
    email: str
