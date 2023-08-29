from fastapi import APIRouter, Depends
from app.db.schemas import CityModel
from app.core.database import get_session
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.utils import logger

router = APIRouter()


@router.get("/cities/", tags=["cities"])
async def read_cities():
    return {'Error': 'city is not defined'}


@router.post("/cities_read/", response_model=CityModel)
async def read_cities(city: CityModel, cursor: AsyncSession = Depends(get_session)):
    city = CityModel(id_city=city.id_city, name_city=city.name_city, postal_code=city.postal_code)
    cursor.add(city)
    await cursor.commit()
    await cursor.refresh(city)
    logger.info(f'city {city.name_city} was added with id: {city.id_city}')
    return city

