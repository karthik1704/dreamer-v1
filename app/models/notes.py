
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import DateTime, ForeignKey, Text, select,desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin


from app.models.batches import Batch

class Note (Base, DefaultFieldsMixin):
    __tablename__="notes"

    note: Mapped[str]
    note_link: Mapped[str]
    note_description: Mapped[str]

    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False)

    batch: Mapped["Batch"] = relationship("Batch", back_populates="batch_notes")

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
    async def create_note(cls, db: AsyncSession, note):
        db.add(note)
        await db.commit()
        await db.refresh(note)
    
    def update_note(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)
    
    
