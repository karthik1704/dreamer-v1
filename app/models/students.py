from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey,  desc, func, select, Text
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin
from app.models.batches import Batch


class Student(Base, DefaultFieldsMixin):

    __tablename__="students"

    batch_id: Mapped[int] = mapped_column(ForeignKey("batches.id"), nullable=False)
    student_code: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)

    student_profile: Mapped[Optional["StudentProfile"]] = relationship("StudentProfile", back_populates="student",  lazy="selectin")
    batch: Mapped["Batch"] = relationship("Batch", back_populates="students", lazy="selectin")

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
    async def create_student(cls, db: AsyncSession, desk):
        db.add(desk)
        await db.commit()
        await db.refresh(desk)
        student_profile = StudentProfile(user_id=desk.id)
        db.add(student_profile)
        await db.commit()

    def update_student(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)

    


class StudentProfile(Base, DefaultFieldsMixin):
    __tablename__="student_profiles"


    student_id: Mapped[str] = mapped_column(ForeignKey("students.id"), nullable=False)
    
    student_photo: Mapped[Optional[str]] = mapped_column(nullable=True)
    father_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    mother_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    father_phone_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    mother_phone_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    siblings_phone_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    personal_number: Mapped[Optional[str]] = mapped_column(nullable=True)
    age: Mapped[Optional[int]] = mapped_column(nullable=True)
    school_name: Mapped[Optional[str]] = mapped_column(nullable=True)
    district: Mapped[Optional[str]] = mapped_column(nullable=True)
    state: Mapped[Optional[str]] = mapped_column(nullable=True)
    address: Mapped[Optional[str]] = mapped_column(Text,nullable=True)
    blood_group: Mapped[Optional[str]] = mapped_column(nullable=True)


    student: Mapped["Student"] = relationship("Student", back_populates="student_profile")



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

   
    def update_profile(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)