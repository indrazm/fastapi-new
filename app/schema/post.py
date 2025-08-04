from pydantic import BaseModel


class PostCreate(BaseModel):
    title: str
    content: str


class PostRead(BaseModel):
    id: str
    title: str
    content: str
