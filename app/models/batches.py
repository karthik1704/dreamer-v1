
from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin
if TYPE_CHECKING:
    from .notes import Note
    from .videos import Video
    from .students import Student


class Batch (Base, DefaultFieldsMixin):
    __tablename__="batches"

    batch_name: Mapped[str]
    batch_code: Mapped[str]
    mode: Mapped[str]
    board: Mapped[Optional[str]]
    batch_year: Mapped[int]

    
    batch_notes: Mapped[list["Note"]] = relationship("Note", back_populates="batch")
    batch_videos: Mapped[list["Video"]] = relationship("Video", back_populates="batch")
    students: Mapped[list["Student"]] = relationship("Student", back_populates="batch")