import fastapi_jsonrpc as jsonrpc
from fastapi import File, HTTPException, Request, Response
from user.models import User
from video.models import Video
from video.s3_client import s3, bucket_name
from video.schemas import VideoModel
video_router = jsonrpc.Entrypoint(path='/api/v1/video')


@video_router.post('/upload_video')
async def upload_video_test(request: Request):
    form = await request.form()
    try:
        VideoModel(**form)
    except:
        HTTPException(status_code=400, detail='Bad Request')

    title, description = form.get('title'), form.get('description')
    file: File(...) = form.get('file')
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
