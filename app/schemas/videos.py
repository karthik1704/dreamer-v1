from token import OP
from typing import Optional
from pydantic import BaseModel, field_validator

from app.schemas.batches import BatchSchema


class VideoSchemaForCategory(BaseModel):
    id:int
    video_title: str
    video_link: str
    video_description: str
    video_type: str
    batch_id: int
    category_id: Optional[int]

class VideoCategoryParentSchema(BaseModel):
    id: int
    category_name: str
    category_code: str
    image: str
    parent_id: Optional[int] = None
    


class VideoCategorySchema(BaseModel):
    id: int
    category_name: str
    category_code: str
    image: Optional[str]
    parent_id: Optional[int] = None
    batch_id: int
    parent: Optional["VideoCategoryParentSchema"] = None
    children: list["VideoCategorySchema"] = []
    videos: Optional[list["VideoSchemaForCategory"]] = []
    batch: Optional[BatchSchema]
    class Config:
        from_attributes = True

VideoCategorySchema.model_rebuild()

class VidoeCategoryCreate(BaseModel):
    category_name: str
    parent_id: Optional[int] = None
    batch_id: int
    image: Optional[str] = None

    @field_validator('parent_id', mode="before")
    def validate_parent_id(cls, v):
        if v=="":
            return None
        return v



class VideoSchema(BaseModel):
    id:int
    video_title: str
    video_link: str
    video_description: str
    video_type: str
    batch_id: int
    category_id: Optional[int]
    # category: Optional[VideoCategorySchema]
    batch: Optional["BatchSchema"]

    class Config:
        from_attributes = True


class VideoCreate(BaseModel):
    video_title: str
    video_link: str
    video_description: str
    video_type: str
    batch_id: int
    category_id: int
