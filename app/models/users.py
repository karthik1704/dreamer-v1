from datetime import datetime
from typing import TYPE_CHECKING, Any, Optional

from sqlalchemy import Boolean, DateTime, ForeignKey,  desc, func, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import Mapped,  mapped_column, relationship

from app.models import Base
from app.models.default_fields import DefaultFieldsMixin




class User(Base, DefaultFieldsMixin):
    __tablename__ = "users"

    first_name: Mapped[Optional[str]]
    last_name: Mapped[Optional[str]]
    email: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str]

    phone: Mapped[Optional[str]]
    date_joined: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now()
    )
    last_login: Mapped[Optional[datetime]] = mapped_column(DateTime(timezone=True))
    is_active: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_staff: Mapped[bool] = mapped_column(Boolean(), default=False)
    is_superuser: Mapped[bool] = mapped_column(Boolean(), default=False)


    profile: Mapped[Optional['UserProfile']] = relationship("UserProfile", back_populates="user")

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
    async def create_user(cls, db: AsyncSession, desk):
        db.add(desk)
        await db.commit()
        await db.refresh(desk)
        user_profile = UserProfile(user_id=desk.id)
        db.add(user_profile)
        await db.commit()

    def update_user(self, updated_data):
        for field, value in updated_data.items():
            setattr(self, field, value)




class UserProfile(Base, DefaultFieldsMixin):
    __tablename__ = "user_profiles"

    user_id: Mapped[int] = mapped_column(ForeignKey('users.id'), primary_key=True)
    bio: Mapped[str] = mapped_column(nullable=True)
    profile_picture: Mapped[str] = mapped_column(nullable=True)
    user: Mapped['User'] = relationship("User", back_populates="profile")
