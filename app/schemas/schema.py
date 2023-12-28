from pydantic import BaseModel


class BaseUrl(BaseModel):
    target_url: str


class UrlUpdate(BaseUrl):
    is_active: bool
