from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, validator, field_serializer

from app.schemas.batches import BatchSchema


class NoteCategoryCreate(BaseModel):
    category_name: str
    parent_id: Optional[int] = None
    batch_id: int

    @field_validator('parent_id', mode="before")
    def validate_parent_id(cls, v):
        if v=="":
            return None
        return v


class ParentCategorySchema(BaseModel):
    id: int
    category_name: str
   

    class Config:
        from_attributes = True

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
    parent_id: Optional[int] = None
    parent: Optional["ParentCategorySchema"] = None
    children: List["NoteCategorySchema"] = []
    # notes: Optional[List["NoteSchema"]] 

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Handles recursive types
   
    @field_validator('children', mode='before')
    def ensure_list(cls, v):
        # Handle both None and empty iterables
        if v is None:
            return []
        # Convert SQLAlchemy collection to list
        return list(v)

    @field_serializer('children')
    def serialize_children(self, children, _):
        # Safely handle serialization without triggering lazy loading
        try:
            return [
                NoteCategorySchema.model_validate(child) 
                for child in (children or [])
                if child is not None  # Add null check
            ]
        except Exception:
            return []
NoteCategorySchema.model_rebuild()