from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated
import logging

from crud import login_db, register_db, get_user_by_id
from shared.schemas import UserLogin, UserRegister, UserOut
from shared.db.engine import get_db, AsyncSession
from shared.core.security import create_access_token, verify_access_token, oauth2_scheme


router = APIRouter(prefix="/auth", tags=["auth"])
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="AAAAAAAAAAAAAAAAAAA")

@router.post("/login")
async  def login(
    request: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    session: AsyncSession = Depends(get_db)
) -> dict:
    logger.info(request)
    user_schema = UserLogin(
        email=form_data.username,
        password=form_data.password
    )
    user = await login_db(user_schema, session)

    token = create_access_token(user.id)

    return {"access_token": token, "token_type": "bearer"}


@router.post("/register")
async def register(
    user_register: UserRegister,
    session: AsyncSession = Depends(get_db)
) -> str:
    user_schema = UserRegister(
        email=user_register.email,
        password=user_register.password,
        first_name=user_register.first_name,
        last_name=user_register.last_name
    )
    user = await register_db(user=user_schema, session=session)

    token = create_access_token(user.id)

    return token


@router.get("/me")
async def get_current_user(
    request: Request,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db)
) -> UserOut:
    logger.info(type(token))
    user_id = verify_access_token(token=token)
    user = await get_user_by_id(user_id, session)
    return user