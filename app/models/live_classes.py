from datetime import datetime
from tracemalloc import start
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import DateTime, ForeignKey, Text, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin

if TYPE_CHECKING:
    from .batches import Batch


class LiveClass (Base, DefaultFieldsMixin):
    __tablename__="live-classes"

    class_link: Mapped[str]
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False, unique=True)
    start_time: Mapped[datetime]
    end_time: Mapped[datetime]

    batch: Mapped["Batch"] = relationship("Batch", back_populates="live_classes")

    @classmethod
    async def get_all(cls, db_session:AsyncSession, where_condition:list[Any]):
        _stmt = select(cls).where(*where_condition).order_by(desc(cls.id))
        _results = await db_session.execute(_stmt)
        return _results.scalars()
    
    @classmethod    
    async def get_one(cls, database_session: AsyncSession, where_conditions: list[Any]):
        _stmt = select(cls).where(*where_conditions)
        _result = await database_session.execute(_stmt)
        return _result.scalars().first()
    
    @classmethod
    async def create_live_classes(cls, db: AsyncSession, live_class):
        db.add(live_class)
        await db.commit()
        await db.refresh(live_class)
        
    def update_live_classes(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)