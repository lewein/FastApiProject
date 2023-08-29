from typing import Optional
from pydantic import validator
from sqlmodel import SQLModel, Field
from uuid import UUID
from datetime import datetime


class UserModel(SQLModel, table=True):
    id_user: Optional[int] = Field(default=None, primary_key=True, nullable=False)
    name_user: str = ''
    hashed_pwd: str = None
    number: Optional[str] = None
    role: Optional[str] = 'Stuff'
    create_date: Optional[datetime] = datetime.now()
    update_date: Optional[datetime] = None

    @validator('number')
    def number_valid(cls, v):
        if not v:
            return None
        if not (
                ('+7' in v and len(v) == 12) or
                ('8' == v[0] and len(v) == 11) or
                ('9' == v[0] and len(v) == 10)
        ):
            raise ValueError('Invalid user number')
        return v

    # @validator('id_user')
    # def hexlify_token(cls, value):
    #     """ Конвертирует UUID в hex строку """
    #     if value:
    #         return value.hex

    # class Config:
    #
    #     arbitrary_types_allowed = True


class UserModelCreate(SQLModel):
    name_user: str
    number: str
    role: Optional[str] = 'Stuff'
    create_date: Optional[datetime] = datetime.now()


class UserModelOut(SQLModel):
    name_user: str
    number: str
    role: Optional[str] = 'Stuff'


class CityModel(SQLModel, table=True):
    id_city: Optional[UUID] = Field(default=None, primary_key=True, nullable=False)
    name_city: str
    postal_code: Optional[int]
    district: Optional[str] = 'Russia'

    class Config:
        orm_mode = False
        arbitrary_types_allowed = True


class Token(SQLModel):
    access_token: str
    token_type: str

