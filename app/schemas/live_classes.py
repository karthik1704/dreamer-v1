from datetime import datetime
from pydantic import BaseModel

from app.schemas.batches import BatchSchema


class LiveClassSchema(BaseModel):
    id: int
    class_name:str
    batch_id: int
    class_link: str
    start_time: datetime
    end_time: datetime

    batch: BatchSchema


    class Config:
        from_attributes = True


class LiveClassCreate(BaseModel):
    class_link: str
    class_name: str
    start_time: datetime
    end_time: datetime
    batch_id: int
