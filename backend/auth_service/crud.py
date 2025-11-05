from sqlalchemy import select, insert
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException
import logging

from shared.db.models import User
from shared.db.engine import engine
from shared.core.security import verify_password, hash_password
from shared.schemas import UserRegister, UserLogin, UserIn, UserOut

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="INFO")

async def login_db(user: UserLogin, session: AsyncSession) -> UserOut:
    try: 
        find_user_stmt = select(User).where(User.email == user.email)
        async with session:
            result = await session.execute(statement=find_user_stmt)
            db_user = result.scalar_one_or_none()
            if db_user is None:
                raise HTTPException(status_code=404, detail=f"user: {user.email} not found")
            
        if verify_password(plain_password=user.password, hashed_password=db_user.hashed_password):
            return UserOut(
                id=db_user.id,
                email=db_user.email,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                balance=db_user.balance
            )
        else:
            raise HTTPException(status_code=400, detail="incorrect password")

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    

async def register_db(user: UserRegister, session: AsyncSession) -> UserOut:
    try: 
        find_user_stmt = select(User).where(User.email == user.email)
        async with session:
            result = await session.execute(statement=find_user_stmt)
            scalar = result.scalar_one_or_none()
            logger.info(scalar)
            if scalar is not None:
                raise HTTPException(status_code=404, detail=f"user: {user.email} already exist")
            
            create_stmt = insert(User).values(
                email=user.email,
                hashed_password=hash_password(user.password),
                first_name=user.first_name,
                last_name=user.last_name
            ).returning(User)
            result = await session.execute(create_stmt)
            await session.commit()
            db_user = result.scalar_one()

            return UserOut(
                id=db_user.id,
                email=db_user.email,
                first_name=db_user.first_name,
                last_name=db_user.last_name,
                balance=db_user.balance
            )

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    

async def get_user_by_id(user_id: int, session: AsyncSession) -> UserOut:
    try:
        stmt = select(User).where(User.id == user_id)
        async with session:
            result = await session.execute(statement=stmt)
        db_user = result.scalar_one()
        return UserOut(
            id=db_user.id,
            email=db_user.email,
            first_name=db_user.first_name,
            last_name=db_user.last_name,
            balance=db_user.balance
        )
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")

    
