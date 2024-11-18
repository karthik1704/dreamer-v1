
from pydantic import BaseModel


class NoteSchema(BaseModel):
    id: int
    note:str
    note_link:str
    note_description:str
    batch_id: int

    class Config:
        orm_mode = True

class NoteCreate(BaseModel):
    note:str
    note_link:str
    note_description:str
    batch_id: int