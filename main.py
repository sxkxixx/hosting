from fastapi import FastAPI, Request
import uvicorn
from user.models import Role, User
from database import db
from user.api import user_route
from video.api import video_router
from video.models import Video, Like, Comment
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title='Video Hosting'
)
app.include_router(user_route)
app.include_router(video_router)

origins = [
    "http://localhost",
    "http://localhost:8080",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

if __name__ == "__main__":
    db.connect()
    db.create_tables([Role, User, Video, Like, Comment])
    uvicorn.run(app, host="127.0.0.1", port=8000)
