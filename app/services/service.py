from sqlalchemy import select
from fastapi import HTTPException, status
from fastapi.responses import RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.schema import BaseUrl, UrlUpdate
from app.models.model import Url
import validators
import secrets


def raise_bad_request(message):
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail=message
    )


async def get_url(db: AsyncSession, url_key: str):
    url = await db.scalar(select(Url).where(Url.key == url_key, Url.is_active))
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Url not found'
        )
    url.clicks += 1
    await db.commit()
    return RedirectResponse(url.target_url)


async def create_url(data: BaseUrl, db: AsyncSession):
    if not validators.url(data.target_url):
        raise_bad_request(message='Invalid url')

    chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    key = ''.join(secrets.choice(chars) for _ in range(5))
    secret_key = ''.join(secrets.choice(chars) for _ in range(8))
    new_url = Url(
        key=key,
        target_url=data.target_url,
        secret_key=secret_key
    )
    db.add(new_url)
    await db.commit()
    return new_url


async def url_statistic(db: AsyncSession, key: str, secret: str):
    url = await db.scalar(select(Url).where(
        Url.key == key,
        Url.secret_key == secret
    ))
    if not url:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid key or secret key'
        )
    return url


async def url_update(key: str, secret: str, db: AsyncSession, url_data: UrlUpdate):
    url = await db.scalar(select(Url).where(
        Url.key == key,
        Url.secret_key == secret
    ))
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Url not found'
        )

    for name, value in url_data.model_dump(exclude_unset=True).items():
        setattr(url, name, value)

    await db.commit()
    return url


async def delete_url(db: AsyncSession, secret: str, key: str):
    url = await db.scalar(select(Url).where(
        Url.secret_key == secret,
        Url.key == key
    ))
    if not url:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Url not found'
        )

    await db.delete(url)
    await db.commit()
    return {'message': f'{url.target_url} deleted'}
