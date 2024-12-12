from datetime import datetime
from typing import TYPE_CHECKING, List, Optional, Any
from uuid import uuid4

from sqlalchemy import DateTime, ForeignKey, Nullable, String, Text, select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped, mapped_column, relationship, joinedload

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin


from app.models.batches import Batch


class NoteCategory(Base, DefaultFieldsMixin):
    __tablename__ = "note_categories"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=True)
    category_name: Mapped[str]
    parent_id: Mapped[int] = mapped_column(
        ForeignKey("note_categories.id"), nullable=True
    )

    image: Mapped[str] = mapped_column(Text, nullable=True)

    parent: Mapped[Optional["NoteCategory"]] = relationship(
        "NoteCategory",
        remote_side=[id],
        primaryjoin="NoteCategory.parent_id == NoteCategory.id",
        back_populates="children",
        lazy="selectin",
    )
    children: Mapped[List["NoteCategory"]] = relationship(
        "NoteCategory", back_populates="parent", lazy="selectin"
    )
    notes: Mapped[List["Note"]] = relationship(
        "Note", back_populates="category", lazy="selectin"
    )
    batch: Mapped["Batch"] = relationship(
        "Batch", back_populates="note_categories", lazy="selectin"
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
            .options(joinedload(cls.children))
            .order_by(desc(cls.id))
        )
        _results = await db_session.execute(_stmt)
        categories = _results.unique().scalars().all()

        return categories

    @classmethod
    async def get_one(cls, database_session: AsyncSession, where_conditions: list[Any]):
        _stmt = (
            select(cls).where(*where_conditions)
            .options(joinedload(cls.parent))
            .options(joinedload(cls.children))
            .order_by(desc(cls.id))
        )
        _result = await database_session.execute(_stmt)
        return _result.scalars().first()

    @classmethod
    async def create_note_category(cls, db: AsyncSession, note):
        db.add(note)
        await db.commit()
        await db.refresh(note)

    def update_note_category(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)


class Note(Base, DefaultFieldsMixin):
    __tablename__ = "notes"

    note: Mapped[str]
    note_link: Mapped[str]
    note_description: Mapped[str]

    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False)
    category_id: Mapped[int] = mapped_column(
        ForeignKey("note_categories.id"), nullable=True
    )
    batch: Mapped["Batch"] = relationship(
        "Batch", back_populates="batch_notes", lazy="selectin"
    )
    category: Mapped["NoteCategory"] = relationship(
        "NoteCategory", back_populates="notes", lazy="selectin"
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
    async def create_note(cls, db: AsyncSession, note):
        db.add(note)
        await db.commit()
        await db.refresh(note)

    def update_note(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)
