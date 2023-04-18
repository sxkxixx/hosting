import uvicorn
from app.db import db
from app.user.api import user_route
from app.video.api import video_router
from app.video.models import Video, Like, Comment
from app.user.models import Role, User
from fastapi.middleware.cors import CORSMiddleware
import fastapi_jsonrpc as jsonrpc


app = jsonrpc.API(
    title='Video Hosting'
)


app.bind_entrypoint(user_route)
app.bind_entrypoint(video_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)


if __name__ == "__main__":
    db.connect()
    db.create_tables([Role, User, Video, Like, Comment])
    uvicorn.run(app, host='127.0.0.1', port=8000)
