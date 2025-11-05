from pydantic import BaseModel


class FoundCreate(BaseModel):
    name: str
    description: str
    goal: float


class FoundIn(FoundCreate):
    current: float = 0
    user_id: int


class FoundOut(FoundIn):
    id: int