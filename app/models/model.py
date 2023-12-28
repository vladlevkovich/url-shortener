from sqlalchemy import func
from sqlalchemy.orm import mapped_column, Mapped
from app.database.base_model import Base
import datetime


class Url(Base):
    __tablename__ = 'urls'

    id: Mapped[int] = mapped_column(primary_key=True)
    key: Mapped[str] = mapped_column(unique=True, index=True)
    secret_key: Mapped[str] = mapped_column(unique=True, index=True)
    target_url: Mapped[str] = mapped_column(index=True)
    is_active: Mapped[bool] = mapped_column(default=True)
    clicks: Mapped[int] = mapped_column(default=0)
    created: Mapped[datetime.datetime] = mapped_column(server_default=func.now())
