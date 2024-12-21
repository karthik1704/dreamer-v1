
from datetime import datetime
from typing import TYPE_CHECKING, Optional, Any

from sqlalchemy import DateTime, ForeignKey, Text, select, desc
from sqlalchemy.orm import Mapped,  mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin
if TYPE_CHECKING:
    from .notes import Note
    from .videos import Video
    from .students import Student
    from .live_classes import LiveClass
    from .notes import NoteCategory
    from .videos import VideoCategory


class Batch (Base, DefaultFieldsMixin):
    __tablename__="batches"

    batch_name: Mapped[str]
    batch_code: Mapped[str]
    mode: Mapped[str]
    target: Mapped[str]
    board: Mapped[Optional[str]]

    
    batch_notes: Mapped[list["Note"]] = relationship("Note", back_populates="batch")
    batch_videos: Mapped[list["Video"]] = relationship("Video", back_populates="batch")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="batch")
    live_classes: Mapped[list["LiveClass"]] = relationship("LiveClass", back_populates="batch")
    note_categories: Mapped[list["NoteCategory"]] = relationship("NoteCategory", back_populates="batch")
    video_categories: Mapped[list["VideoCategory"]] = relationship("VideoCategory", back_populates="batch")
    live_classes: Mapped[list["LiveClass"]] = relationship("LiveClass", back_populates="batch")
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
    async def create_batch(cls, db: AsyncSession, desk):
        db.add(desk)
        await db.commit()

    def update_batch(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)
