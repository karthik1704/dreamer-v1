
from typing import Any, Optional
from sqlalchemy import  select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped
from app.models import Base
from app.models.default_fields import DefaultFieldsMixin


class Enquiry(Base, DefaultFieldsMixin):
    __tablename__ = "enquiry"

    are_you: Mapped[str]
    enquirer_name: Mapped[str]
    standard: Mapped[str]
    board: Mapped[str]
    email: Mapped[str]
    phone: Mapped[str]
    district: Mapped[str]

    status:Mapped[Optional[str]]

    @classmethod
    async def get_all(cls, db_session: AsyncSession, where_condition: list[Any]):
        _stmt = select(cls).where(*where_condition).order_by(desc(cls.id))
        _results = await db_session.execute(_stmt)
        return _results.scalars()

    @classmethod
    async def get_one(cls, database_session: AsyncSession, where_conditions: list[Any]):
        _stmt = select(cls).where(*where_conditions)
        _result = await database_session.execute(_stmt)
        return _result.scalars().first()

    @classmethod
    async def create_enquiry(cls, db: AsyncSession, enquiry):
        db.add(enquiry)
        await db.commit()
        await db.refresh(enquiry)

    def update_enquiry(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)
