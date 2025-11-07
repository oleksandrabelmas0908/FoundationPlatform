from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert, update, delete
from fastapi import HTTPException
import logging

from shared.schemas import FoundOut, FoundIn, FoundCreate
from shared.db.models import Found, User


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(name="info")


async def is_user_owner(session: AsyncSession, user_id: int, found_id: int) -> bool:
    try:
        find_found_stmt = select(Found).where(Found.id == found_id)
        async with session:
            result = await session.execute(find_found_stmt)

        found = result.scalar_one_or_none()
        if found is None:
            raise HTTPException(status_code=404, detail=f"No found with id {found_id}")
        
        return found.id == found_id

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


async def get_founds_db(session: AsyncSession, limit: int | None = 10) -> list[FoundOut]:
    try:
        stmt = select(Found).limit(limit)
        async with session:
            result = await session.execute(stmt)
        
        list_founds = []
        for found in result.scalars().all():
            # logger.info()
            list_founds.append(FoundOut(
                id=found.id,
                name=found.name,
                description=found.description,
                goal=found.goal,
                current=found.current,
                user_id=found.user_id
            ))
        return list_founds

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    

async def create_found_db(session: AsyncSession, user_id: int, found_data: FoundCreate) -> FoundOut:
    try:
        stmt = insert(Found).values(user_id=user_id, **found_data.model_dump()).returning(Found)
        async with session:
            result = await session.execute(stmt)
            await session.commit()
        found = result.scalar_one()
        logger.info(found_data.model_dump())
        return FoundOut(id=found.id, user_id=user_id, **found_data.model_dump())

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    

async def change_found_db(session: AsyncSession, user_id: int, found_id: int, new_name: str | None, new_description: str | None, new_goal: float | None, new_current: float | None) -> FoundOut:
    try:
        if not is_user_owner(session=session, user_id=user_id, found_id=found_id):        
            raise HTTPException(status_code=400, detail=f"User: {user_id} is not owner of this found")

        find_stmt = select(Found).where(Found.id == found_id)
        async with session:
            found_result = await session.execute(find_stmt)

            db_found = found_result.scalar_one_or_none()

            if db_found is None:
                raise HTTPException(status_code=404, detail=f"No found with id {found_id}")
            
            name = new_name if new_name is not None else db_found.name
            description = new_description if new_description is not None else db_found.description
            goal = new_goal if new_goal is not None else db_found.goal
            current = new_current if new_current is not None else db_found.current
        
            update_stmt = update(Found).where(Found.id == db_found.id).values(name=name, description=description, goal=goal, current=current).returning(Found)
            update_result = await session.execute(update_stmt)
            await session.commit()

        update_found = update_result.scalar_one()
        return FoundOut(
            id=update_found.id,
            name=update_found.name,
            description=update_found.description,
            goal=update_found.goal,
            current=update_found.current,
            user_id=user_id
        )

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    

async def delete_found_db(session: AsyncSession, found_id: int, user_id: int) -> int:
    try:
        if not is_user_owner(session=session, user_id=user_id, found_id=found_id):        
            raise HTTPException(status_code=400, detail=f"User: {user_id} is not owner of this found")

        delete_stmt = delete(Found).where(Found.id == found_id)
        async with session:
            await session.execute(delete_stmt)
            await session.commit()

        return found_id

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")
    

async def get_found_db(session: AsyncSession, found_id: int) -> FoundOut:
    try:
        stmt = select(Found).where(Found.id == found_id)
        async with session:
            result = await session.execute(stmt)
        
        found = result.scalar_one_or_none()

        if found is None:
                raise HTTPException(status_code=404, detail=f"No found with id {found_id}")        

        return FoundOut(
                id=found.id,
                name=found.name,
                description=found.description,
                goal=found.goal,
                user_id=found.user_id
            )

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    

async def get_user_founds_db(session: AsyncSession, user_id) -> list[FoundOut]:
    try:
        stmt = select(Found).where(Found.user_id == user_id)
        async with session:
            result = await session.execute(stmt)
        
        list_founds = []
        for found in result.scalars().all():
            list_founds.append(FoundOut(
                id=found.id,
                name=found.name,
                description=found.description,
                goal=found.goal,
                user_id=found.user_id
            ))
        return list_founds

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")
    

async def pay_to_found(session: AsyncSession, user_id: int, found_id: int, amount: float):
    try:
        async with session:
            result_user = await session.execute(
                select(User.balance).where(User.id == user_id)
            )
            changed_balance = result_user.scalar_one() - amount
            update_user = await session.execute(
                update(User).where(User.id == user_id).values(balance=changed_balance)
            )
            
            result_found = await session.execute(
                select(Found.current).where(Found.id == found_id)
            )
            changed_current = result_found.scalar_one() + amount
            update_found = await session.execute(
                update(Found).where(Found.id == found_id).values(current=changed_current)
            )
            await session.commit()

    except Exception as e:
        raise HTTPException(status_code=404, detail=f"{e}")