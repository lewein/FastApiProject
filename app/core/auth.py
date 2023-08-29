from datetime import datetime, timedelta
from typing import Annotated

from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, status
from jose import JWTError, jwt
from passlib.context import CryptContext

from app.core.database import redis_db
from app.core.settings import settings
from app.core.utils import HTTP_ERROR, logger
from app.db.schemas import UserModel


ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_HOUR = 8
SECRET_KEY = settings.SECRET_KEY

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


async def is_authorized(name_user: str) -> dict:
    if name_user:
        jwt_token = redis_db.get(f'{name_user}:jwt_token')
        return {'access_token': jwt_token, 'token_type': 'bearer'}
    else:
        return {}


def create_token(data: dict, expires_time=None) -> str:
    data_encode = data.copy()
    if expires_time:
        expire = datetime.utcnow() + expires_time
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    data_encode.update({"exp": expire})
    jwt_token = jwt.encode(data_encode, SECRET_KEY, algorithm=ALGORITHM)
    return jwt_token


def get_user_by_token(token):
    return 'alena'


async def auth_user(user: UserModel, password: str) -> dict:
    if not verify_password(password, user.hashed_pwd):
        raise HTTP_ERROR(
            code=status.HTTP_401_UNAUTHORIZED,
            message="Incorrect password. Check your password or set a new one and try again",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token_expires = timedelta(hours=ACCESS_TOKEN_EXPIRE_HOUR)
    jwt_token = create_token(
        data={'sub': f'{user.id_user}_{user.name_user}'},
        expires_time=access_token_expires
    )

    try:
        key = f'{user.name_user}:jwt_token'
        redis_db.set(key, jwt_token)
        redis_db.expire(key, time=ACCESS_TOKEN_EXPIRE_HOUR*3600)
    except Exception as ex:
        logger.error(f'Redis error while setting data - {ex}')

    return {'access_token': jwt_token, 'token_type': 'bearer'}


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    user = get_user_by_token(token)
    if not user:
        HTTP_ERROR()
    return user







