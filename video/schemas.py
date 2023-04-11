from pydantic import BaseModel
from fastapi import File, UploadFile


class VideoModel(BaseModel):
    title: str
    description: str
    video_file: bytes = File(...)
