from fastapi import APIRouter, Depends
from typing import Annotated

from shared.db.engine import AsyncSession, get_db
from shared.schemas import FoundOut, FoundIn, FoundCreate
from shared.core.security import oauth2_scheme, verify_access_token
from crud import get_founds_db, create_found_db, change_found_db, delete_found_db, get_found_db, get_user_founds_db


router = APIRouter(prefix="/founds", tags=["found"])


@router.get("/")
async def get_founds(
    session: Annotated[AsyncSession, Depends(get_db)],
    limit: int | None = None
) -> list[FoundOut]: 
    foundation_list = await get_founds_db(session, limit)
    return foundation_list
    


@router.post("/")
async def create_found(
    session: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    found_schema: FoundCreate
) -> FoundOut: 
    
    user_id = verify_access_token(token)
    found = await create_found_db(session=session, user_id=user_id, found_data=found_schema)
        
    return found


@router.patch("/{found_id}")
async def change_found(
    session: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    found_id: int,
    name: str | None = None,
    description: str | None = None,
    goal: float | None = None,
    current: float | None = None
) -> FoundOut: 
    
    user_id = verify_access_token(token)
    found = await change_found_db(session=session, user_id=user_id, found_id=found_id, new_name=name, new_description=description, new_goal=goal, new_current=current)
    return found


@router.delete("/{found_id}")
async def delete_found(
    session: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
    found_id: int
) -> int: 
    user_id = verify_access_token(token)
    return await delete_found_db(session=session, found_id=found_id, user_id=user_id)


@router.get("/{found_id}")
async def get_found(
    session: Annotated[AsyncSession, Depends(get_db)],
    found_id: int
) -> FoundOut: 
    return await get_found_db(session=session, found_id=found_id)


@router.get("/myfounds/{user_id}")
async def get_current_user_founds(
    session: Annotated[AsyncSession, Depends(get_db)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> list[FoundOut]: 
    user_id = verify_access_token(token)
    return await get_user_founds_db(session=session, user_id=user_id)


