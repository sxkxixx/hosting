from fastapi import APIRouter, Request, File, HTTPException, Response
from fastapi.templating import Jinja2Templates
from user.models import User
from video.models import Video, Like, Comment
from video.s3_client import s3, bucket_name
from video.schemas import VideoModel

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post('/upload_video')
async def upload_video(request: Request):
    form = await request.form()
    try:
        VideoModel(**form)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    title, description = form.get('title'), form.get('description')
    file: File(...) = form.get('video_file')
    try:
        user = User.select().where(User.id == 1).get()
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        video = Video(
            title=title,
            description=description,
            owner_id=user.id,
            cloud_name=f'{user.id}{file.filename}'
        )
        video.save()
        url = video.url
        return Response({'status': 200, 'url': f'{url}'})
    except:
        HTTPException(status_code=400, detail='Bad Request')


@video_router.get('/video/{id}')
async def get_video(id: str):
    try:
        video = Video.select().where(id == Video.id).get()
    except:
        return HTTPException(status_code=400, detail='Bad Request')
    url = video.url
    likes_amount = Like.select().count
    comments = Comment.select('comment_text').where(Comment.video_id == id)
    return Response({'id': video.id, 'title': video.title, 'description': video.description, 'url': url,
                     'likes': likes_amount, 'comments': comments})
