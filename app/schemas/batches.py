
from pydantic import BaseModel
from ..models.batches import Batch
from enum import Enum

class BatchSchema(BaseModel):
    id: int
    batch_name: str
    batch_code: str
    mode: str
    target: str
    board: str

    class Config:
        from_attributes = True


class BatchCreate(BaseModel):
    batch_name: str
    batch_code: str
    mode: str
    board: str
    target: str
