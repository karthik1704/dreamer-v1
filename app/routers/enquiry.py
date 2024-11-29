from turtle import st
from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.enquiry import Enquiry
from app.schemas.enquiry import EnquiryPatchSchema, EnquirySchema, EnquiryCreateSchema

router = APIRouter(prefix="/enquiry", tags=["Enquiry"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[EnquirySchema])
async def get_all_enquiries(db: db_dep, user: user_dep):

    enquiries = await Enquiry.get_all(db, [])

    return enquiries


@router.get("/{id}/", response_model=EnquirySchema)
async def get_enquiry(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    enquiry_detail = await Enquiry.get_one(db, [Enquiry.id == id])

    if not enquiry_detail:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Enquiry not found",
        )

    return enquiry_detail


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_enquiry(
    enquiry: EnquiryCreateSchema,
    db: db_dep,
):

    new_enquiry = enquiry.model_dump()
    enquiry = Enquiry(**new_enquiry)

    await Enquiry.create_enquiry(db, enquiry)


# @router.patch("/{id}/", status_code=status.HTTP_204_NO_CONTENT)
# async def patch_enquiry(enquiry:EnquiryPatchSchema, db: db_dep, user: user_dep, id: int = Path(gt=0) ):
