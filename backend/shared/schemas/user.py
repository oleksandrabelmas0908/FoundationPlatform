from pydantic import BaseModel, EmailStr


class UserIn(BaseModel):
    email: EmailStr
    first_name: str | None = None
    last_name: str | None = None


class UserOut(UserIn):
    id: int


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserRegister(UserLogin, UserIn):
    pass


