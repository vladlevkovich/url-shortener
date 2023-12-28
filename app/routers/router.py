from fastapi import Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession
from app.database.db import get_db
from app.schemas.schema import UrlUpdate
from app.services.service import *
from .base_router import router


@router.get('/{url_key}')
async def get_target_url(url_key: str, db: AsyncSession = Depends(get_db)):
    return await get_url(db=db, url_key=url_key)


@router.post('/url')
async def url_create(data: BaseUrl, db: AsyncSession = Depends(get_db)):
    return await create_url(data=data, db=db)


@router.get('/{url_key}/{url_secret}')
async def get_statistic(key: str, secret: str, db: AsyncSession = Depends(get_db)):
    return await url_statistic(key=key, secret=secret, db=db)


@router.put('/{url_key}/{url_secret}')
async def update_url(key: str, secret: str, url_data: UrlUpdate, db: AsyncSession = Depends(get_db)):
    return await url_update(key=key, secret=secret, db=db, url_data=url_data)


@router.delete('/{url_key}/{url_secret}')
async def url_delete(key: str, secret: str, db: AsyncSession = Depends(get_db)):
    return await delete_url(key=key, secret=secret, db=db)
