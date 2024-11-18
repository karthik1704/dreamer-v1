from datetime import datetime
from typing import Optional
from pydantic import BaseModel

from app.schemas.batches import BatchSchema

class StudentProfileSchema(BaseModel):
    student_id: str
    student_photo: Optional[str] = None
    father_phone_number: Optional[str] = None
    mother_phone_number: Optional[str] = None
    siblings_phone_number: Optional[str] = None
    personal_number: Optional[str] = None
    age: Optional[int] = None
    school_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None

class CreateStudentProfile(BaseModel):
    student_id: str
    student_photo: Optional[str] = None
    father_phone_number: Optional[str] = None
    mother_phone_number: Optional[str] = None
    siblings_phone_number: Optional[str] = None
    personal_number: Optional[str] = None
    age: Optional[int] = None
    school_name: Optional[str] = None
    district: Optional[str] = None
    state: Optional[str] = None
    address: Optional[str] = None
    blood_group: Optional[str] = None



class StudentSchema(BaseModel):
    id:int
    batch_id: int
    student_code: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: datetime
    gender: str

    student_profile: Optional[StudentProfileSchema]
    batch: Optional[BatchSchema]


    class Config:
        orm_mode = True


class StudentCreate(BaseModel):
    batch_id: int
    student_code: str
    first_name: str
    last_name: str
    email: str
    date_of_birth: datetime
    gender: str
    student_profile: Optional[CreateStudentProfile]


