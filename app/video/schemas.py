from pydantic import BaseModel
from fastapi import File


class VideoUploadSchema(BaseModel):
    title: str
    description: str
    video_file: bytes = File(...)


class CommentUploadSchema(BaseModel):
    video_id: int
    comment_text: str
