from fastapi import APIRouter, Depends
from typing import Annotated
import logging

from crud import get_user_payments, get_found_payments, create_payment_db
from shared.core.security import oauth2_scheme, verify_access_token
from shared.db.engine import AsyncSession, get_db
from shared.schemas import PaymentSchema


router = APIRouter(prefix="/payments")

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="route")

@router.get("/")
async def get_user_payment_history(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db)
) -> list[PaymentSchema]:
    
    user_id = verify_access_token(token=token)
    logger.info(user_id)
    return await get_user_payments(session=session, user_id=user_id)


@router.get("/{found_id}")
async def get_found_payment_history(
    found_id: int,
    session: AsyncSession = Depends(get_db)
) -> list[PaymentSchema]:
    return await get_found_payments(session=session, found_id=found_id)


@router.post("/{found_id}")
async def pay_to_found(
    amount: float,
    found_id: int,
    token: Annotated[str, Depends(oauth2_scheme)],
    session: AsyncSession = Depends(get_db)
) -> PaymentSchema:
    user_id = verify_access_token(token)
    return await create_payment_db(session=session, user_id=user_id, found_id=found_id, amount=amount)