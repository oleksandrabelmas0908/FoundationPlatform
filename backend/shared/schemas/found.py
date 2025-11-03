from pydantic import BaseModel


class FoundIn(BaseModel):
    name: str
    description: str
    goal: int
    current: int

    user_id: int


class FoundOut(FoundIn):
    id: int