
from typing import List, Optional
from pydantic import BaseModel, Field, field_validator, validator


class NoteCategoryCreate(BaseModel):
    category_name: str
    parent_id: Optional[int] = None
    batch_id: int

    @field_validator('parent_id', mode="before")
    def validate_parent_id(cls, v):
        if v=="":
            return None
        return v


class NoteSchema(BaseModel):
    id: int
    note:str
    note_link:str
    note_description:str
    batch_id: int
    category_id:Optional[int]

    class Config:
        from_attributes = True

class NoteCreate(BaseModel):
    note:str
    note_link:str
    note_description:str
    batch_id: int
    category_id:Optional[int] = None




class ParentCategorySchema(BaseModel):
    id: int
    category_name: str
   

    class Config:
        from_attributes = True

class NoteCategorySchema(BaseModel):
    id: int
    category_name: str
    batch_id: Optional[int]
    parent_id: Optional[int] = None
    parent: Optional["ParentCategorySchema"] = None
    children: Optional[List["NoteCategorySchema"]] = []
    # notes: Optional[List["NoteSchema"]] 

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True  # Handles recursive types

    
    @field_validator('children', mode='before')
    def ensure_list(cls, v):
        if v is None:
            return []
        return list(v)

NoteCategorySchema.model_rebuild()