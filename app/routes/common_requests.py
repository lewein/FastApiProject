from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.auth import is_authorized, auth_user, get_current_user
from app.core.database import get_session
from app.core.utils import HTTP_ERROR, logger
from app.db.schemas import Token, UserModel
from app.internal.users import get_user_by_name

router = APIRouter()


@router.get("/ping")
async def root():
    return {"message": "Pong"}


@router.post("/token", response_model=Token)
async def auth(
        form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
        cursor: Annotated[AsyncSession, Depends(get_session)]
):
    user = await get_user_by_name(name_user=form_data.username, cursor=cursor)
    if not user or not user.name_user:
        raise HTTP_ERROR(
            code=status.HTTP_401_UNAUTHORIZED,
            message="No user for authorization",
            headers={"WWW-Authenticate": "Bearer"}
        )
    jwt_token = await is_authorized(form_data.username)
    if jwt_token.get('access_token'):
        return jwt_token
    user = await auth_user(user=user, password=form_data.password)
    return user


@router.get("/users/me", tags=["users"])
async def read_users_me(current_user: Annotated[UserModel, Depends(get_current_user)]):
    return current_user


