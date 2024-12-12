from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, validator, field_serializer

from app.schemas.batches import BatchSchema


class NoteCategoryCreate(BaseModel):
    category_name: str
    parent_id: Optional[int] = None
    batch_id: int
    image: Optional[str] = None

    @field_validator('parent_id', mode="before")
    def validate_parent_id(cls, v):
        if v=="":
            return None
        return v


class ParentCategorySchema(BaseModel):
    id: int
    category_name: str
   

class NoteSchemaForCategory(BaseModel):
    id: int
    note:str
    note_link:str
    note_description:str
    batch_id: int
    category_id:Optional[int]

class NoteSchema(BaseModel):
    id: int
    note:str
    note_link:str
    note_description:str
    batch_id: int
    category_id:Optional[int]
    batch: Optional[BatchSchema]
    category: Optional[ParentCategorySchema]

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    note:str
    note_link:str
    note_description:str
    batch_id: int
    category_id:Optional[int] = None




class NoteCategorySchema(BaseModel):
    id: int
    category_name: str
    batch_id: Optional[int]
    image: Optional[str]
    parent_id: Optional[int] = None
    parent: Optional["ParentCategorySchema"] = None
    children: list["NoteCategorySchema"] = []
    notes: Optional[List["NoteSchemaForCategory"]] 
    batch: Optional["BatchSchema"]
    class Config:
        from_attributes = True
   
   
NoteCategorySchema.model_rebuild()