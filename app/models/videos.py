
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import DateTime, ForeignKey, Text, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin

if TYPE_CHECKING:
    from .batches import Batch


class Video (Base, DefaultFieldsMixin):
    __tablename__="videos"

    video_title: Mapped[str]
    video_link: Mapped[str]
    video_description: Mapped[str]
    video_type: Mapped[str]

    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False)

    batch: Mapped["Batch"] = relationship("Batch", back_populates="batch_videos")

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
    async def create_video(cls, db: AsyncSession, video):
        db.add(video)
        await db.commit()
        await db.refresh(video)
        
    def update_video(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)