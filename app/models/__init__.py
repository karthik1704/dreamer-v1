from sqlalchemy.orm import DeclarativeBase

class Base(DeclarativeBase):
    pass

    
from .users import User, UserProfile
from .students import Student, StudentProfile
from .notes import Note
from .videos import Video