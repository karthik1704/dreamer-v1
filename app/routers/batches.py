from fastapi import APIRouter, Depends, HTTPException, Path
from starlette import status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, List
from app.database import get_async_db
from app.dependencies.auth import get_current_student, get_current_user

from app.models.batches import Batch
from app.schemas.batches import BatchCreate, BatchSchema


router = APIRouter(prefix="/notes", tags=["Notes"])

db_dep = Annotated[AsyncSession, Depends(get_async_db)]
user_dep = Annotated[dict, Depends(get_current_user)]
student_dep = Annotated[dict, Depends(get_current_student)]


@router.get("/", response_model=List[BatchSchema])
async def get_all_batches(db: db_dep, user: user_dep):

    batches = await Batch.get_all(db, [])

    return batches


@router.get("/{id}/", response_model=BatchSchema)
async def get_batch(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    batch_detail = await Batch.get_one(db, [Batch.id == id])

    return batch_detail


@router.post("/", status_code=status.HTTP_201_CREATED)  # status code 201 for created
async def create_batch(data: BatchCreate, db: db_dep, user: user_dep):

    new_batch_data = data.model_dump()

    await Batch.create_batch(db, new_batch_data)


@router.put("/{id}/", response_model=BatchSchema)
async def update_batch(
    data: BatchCreate, db: db_dep, user: user_dep, id: int = Path(gt=0)
):

    updated_data = data.model_dump()

    batch = await Batch.get_one(db, [Batch.id == id])

    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )

    batch.update_batch(updated_data)


@router.delete("/{id}/",  status_code=status.HTTP_204_NO_CONTENT)
async def delete_batch(db: db_dep, user: user_dep, id: int = Path(gt=0)):

    batch = await Batch.get_one(db, [Batch.id == id])

    if not batch:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Batch not found",
        )

    await db.delete(batch)
    await db.commit()

