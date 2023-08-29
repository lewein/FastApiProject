from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.schemas import UserModel, UserModelOut
from app.core.database import get_session
from app.internal.users import add_user, get_user_by_name, get_all_users, update_user_by_name

router = APIRouter()


@router.get("/get_users/", tags=["users"], response_model=list[UserModel])
async def get_users(cursor: AsyncSession = Depends(get_session)):
    response = await get_all_users(cursor)
    return response


@router.post("/get_user/", tags=["users"], response_model=UserModel)
async def get_user(name_user: str, cursor: AsyncSession = Depends(get_session)):
    response = None
    if name_user:
        response = await get_user_by_name(name_user, cursor)
    if response:
        return response


@router.post("/create_user/", tags=["users"], response_model=UserModelOut)
async def create_user(user: dict, cursor: AsyncSession = Depends(get_session)):
    response = await add_user(user, cursor)
    if response:
        return response


@router.put("/update_user/", tags=["users"])
async def update_user(user: dict, cursor: AsyncSession = Depends(get_session)):
    response = await update_user_by_name(user, cursor)
    if response:
        return response


@router.delete("/delete_user/", tags=["users"])
async def update_user(user: dict, cursor: AsyncSession = Depends(get_session)):
    response = await update_user_by_name(user, cursor)
    if response:
        return response
