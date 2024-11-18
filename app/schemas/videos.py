from pydantic import BaseModel


class VideoSchema(BaseModel):
    id:int
    video_title: str
    video_link: str
    video_description: str
    video_type: str
    batch_id: int

    class Config:
        orm_mode = True


class VideoCreate(BaseModel):
    video_title: str
    video_link: str
    video_description: str
    video_type: str
    batch_id: int
