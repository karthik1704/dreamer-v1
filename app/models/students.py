from datetime import datetime
from typing import Optional

from sqlalchemy import DateTime, ForeignKey, Text
from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin




class Student(Base, DefaultFieldsMixin):

    __tablename__="students"

    student_code: Mapped[str] = mapped_column(unique=True, nullable=False)
    first_name: Mapped[str] = mapped_column(nullable=False)
    last_name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    date_of_birth: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    gender: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)

    student_profile: Mapped[Optional["StudentProfile"]] = relationship("StudentProfile", back_populates="student")


    


class StudentProfile(Base, DefaultFieldsMixin):
    student_id: Mapped[str] = mapped_column(ForeignKey("students.student_id"), nullable=False)

    student_photo: Mapped[Optional[str]] = mapped_column(nullable=True)
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


    student: Mapped[Student] = relationship("Student", back_populates="student_profile")