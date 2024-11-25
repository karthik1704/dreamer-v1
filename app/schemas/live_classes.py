from datetime import datetime
from pydantic import BaseModel


class LiveClassSchema(BaseModel):
    id: int
    batch_id: int
    class_link: str
    start_time: datetime
    end_time: datetime

    class Config:
        from_attributes = True


class LiveClassCreate(BaseModel):
    class_link: str
    start_time: datetime
    end_time: datetime
    batch_id: int
