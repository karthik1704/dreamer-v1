from typing import Optional
from pydantic import BaseModel


class EnquirySchema(BaseModel):
    id: int
    are_you: str
    enquirer_name: str
    standard: str
    board: str
    email: str
    phone: str
    district: str

    status: Optional[str] = None

    class Config:
        from_attributes = True


class EnquiryCreateSchema(BaseModel):
    are_you: str
    enquirer_name: str
    standard: str
    board: str
    email: str
    phone: str
    district: str

    status: Optional[str] = None


class EnquiryPatchSchema(BaseModel):
    status: str
