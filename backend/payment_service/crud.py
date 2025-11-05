from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from fastapi import HTTPException
import logging

from shared.schemas import PaymentSchema
from shared.db.models import Payment


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="porno")


async def get_user_payments(session: AsyncSession, user_id: int) -> list[PaymentSchema]:
    try: 
        stmt = select(Payment).where(Payment.user_id == user_id)
        async with session:
            result = await session.execute(stmt)

        list_payments = []
        for payment in result.scalars().all():
            list_payments.append(PaymentSchema(
                id=payment.id,
                payment_date=payment.date,
                user_id=payment.user_id,
                found_id=payment.found_id,
                amount=payment.amount
            ))

        return list_payments
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    

async def get_found_payments(session: AsyncSession, found_id: int) -> list[PaymentSchema]:
    try: 
        stmt = select(Payment).where(Payment.found_id == found_id)
        async with session:
            result = await session.execute(stmt)

        list_payments = []
        for payment in result.scalars().all():
            list_payments.append(PaymentSchema(
                id=payment.id,
                payment_date=payment.date,
                user_id=payment.user_id,
                found_id=payment.found_id,
                amount=payment.amount
            ))

        return list_payments
    
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    

async def create_payment_db(session: AsyncSession, user_id: int, found_id: int, amount: float) -> PaymentSchema:
    try:
        stmt = insert(Payment).values(user_id=user_id, found_id=found_id, amount=amount).returning(Payment)
        async with session:
            result = await session.execute(stmt)
            await session.commit()

        payment = result.scalar_one()
        return PaymentSchema(
            id=payment.id,
            payment_date=payment.date,
            user_id=payment.user_id,
            found_id=payment.found_id, 
            amount=amount
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")