from datetime import datetime

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update

from app.db.schemas import UserModel, UserModelOut
from app.core.utils import HTTP_ERROR, logger
from app.core.auth import get_password_hash, verify_password


async def add_user(user: dict, cursor: AsyncSession):
    try:
        user_dict = UserModel(**user)
        cursor.add(user_dict)
        await cursor.commit()
    except Exception as ex:
        logger.error(f'{datetime.now()} User create error: {ex}')
        HTTP_ERROR()
    result = UserModelOut(**user)
    return result


async def update_user_by_name(user: dict, cursor: AsyncSession):
    name = user.pop('name_user', None)
    if not name:
        HTTP_ERROR(message='No name for selection')
    try:
        user['update_date'] = datetime.now()
        await cursor.execute(
            update(UserModel).
            where(UserModel.name_user == name).
            values(**user)
        )
        await cursor.commit()
    except Exception as ex:
        mess = f'User create error: {ex}'
        logger.error(f'{datetime.now()} {mess}')
        HTTP_ERROR(message=mess)
    return True


async def update_user(name_user: str, cursor: AsyncSession):
    pass


async def update_user_password(name_user: str, password: str, cursor: AsyncSession):
    user = await get_user_by_name(name_user=name_user, cursor=cursor)
    try:
        user['update_date'] = datetime.now()
        old_pwd = user.get('hashed_pdw')
        if not old_pwd or verify_password(password, old_pwd):
            await cursor.execute(
                update(UserModel).
                where(UserModel.name_user == name_user).
                values({'hashed_pwd': get_password_hash(password)})
            )
        else:
            HTTP_ERROR(message='Passwords do not match')
        await cursor.commit()
    except Exception as ex:
        mess = f'User password update error: {ex}'
        logger.error(f'{datetime.now()} {mess}')
        HTTP_ERROR(message=mess)


async def delete_user(name_user: str, cursor: AsyncSession):
    pass


async def get_all_users(cursor: AsyncSession):
    result = await cursor.execute(select(UserModel))
    response = [row.UserModel for row in result.fetchall()]
    return response


async def get_user_by_name(name_user: str, cursor: AsyncSession):
    if not name_user:
        HTTP_ERROR(message='Name not specified')

    result = await cursor.execute(select(UserModel).where(UserModel.name_user == name_user))
    result = result.fetchone()
    if not result:
        HTTP_ERROR(message='Name not found')
    return result.UserModel






