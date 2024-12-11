from datetime import datetime
from email.mime import image
from typing import TYPE_CHECKING, List, Optional, Any
from unicodedata import category
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, String, Text, select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin

if TYPE_CHECKING:
    from .batches import Batch


class VideoCategory(Base, DefaultFieldsMixin):
    __tablename__ = "video_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    category_code: Mapped[str] = mapped_column(
        String(60), unique=True, default=lambda: str(uuid4())
    )
    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=True)
    category_name: Mapped[str]
    image: Mapped[str] = mapped_column(Text, nullable=True)
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("video_categories.id"), nullable=True
    )

    parent: Mapped[Optional["VideoCategory"]] = relationship(
        "VideoCategory",
        remote_side=[id],
        primaryjoin="VideoCategory.parent_id == VideoCategory.id",
        back_populates="children",
        lazy="selectin",
    )
    children: Mapped[List["VideoCategory"]] = relationship(
        "VideoCategory", back_populates="parent", lazy="selectin"
    )
    videos: Mapped[List["Video"]] = relationship(
        "Video", back_populates="category", lazy="selectin"
    )
    batch: Mapped["Batch"] = relationship(
        "Batch", back_populates="video_categories", lazy="selectin"
    )

    @classmethod
    async def get_all(cls, db_session: AsyncSession, where_condition: list[Any]):
        _stmt = (
            select(cls)
            .where(*where_condition)
            .options(joinedload(cls.parent))
            .options(joinedload(cls.children))
            .options(joinedload(cls.batch))
            .order_by(desc(cls.id))
        )
        _results = await db_session.execute(_stmt)
        categories = _results.unique().scalars().all()

        return categories

    @classmethod
    async def get_all_without_repeat(
        cls, db_session: AsyncSession, where_condition: list[Any]
    ):
        _stmt = (
            select(cls)
            .where(cls.parent_id == None, *where_condition)
            .order_by(desc(cls.id))
        )
        _results = await db_session.execute(_stmt)
        categories = _results.unique().scalars().all()

        return categories

    @classmethod
    async def get_one(cls, database_session: AsyncSession, where_conditions: list[Any]):
        _stmt = (
            select(cls)
            .where(*where_conditions)
            .options(joinedload(cls.parent))
            .options(joinedload(cls.children))
            .order_by(desc(cls.id))
        )
        _result = await database_session.execute(_stmt)
        return _result.scalars().first()

    @classmethod
    async def create_video_category(cls, db: AsyncSession, note):
        db.add(note)
        await db.commit()
        await db.refresh(note)

    def update_video_category(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)


class Video(Base, DefaultFieldsMixin):
    __tablename__ = "videos"

    video_title: Mapped[str]
    video_link: Mapped[str]
    video_description: Mapped[str]
    video_type: Mapped[str]

    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("video_categories.id"), nullable=True
    )

    batch: Mapped["Batch"] = relationship("Batch", back_populates="batch_videos", lazy="selectin")
    category: Mapped[Optional["VideoCategory"]] = relationship(
        "VideoCategory", back_populates="videos", lazy="selectin"
    )

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
    async def create_video(cls, db: AsyncSession, video):
        db.add(video)
        await db.commit()
        await db.refresh(video)

    def update_video(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)
