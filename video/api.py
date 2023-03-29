from fastapi import APIRouter, Request, File, UploadFile
from fastapi.templating import Jinja2Templates
from user.models import User
from video.models import Video
from video.s3_client import s3, bucket_name

video_router = APIRouter()
templates = Jinja2Templates(directory='templates')


@video_router.post('/upload_video')
async def upload_video(file: UploadFile = File(...)):
    try:
        s3.upload_fileobj(file.file, bucket_name, file.filename)
        url = s3.generate_presigned_url(
            'get_object',
            Params={"Bucket": bucket_name, "Key": file.filename}, ExpiresIn=300
        )
        return {'status': 200, 'url': url}
    except:
        return {'status': 404}


@video_router.post('/test_upload_video')
async def upload_video(request: Request):
    form = await request.form()
    title, description = form.get('title'), form.get('description')
    file: File(...) = form.get('file')
    # try:
    admin = User.select().where(User.id == 1).get()
    s3.upload_fileobj(file.file, bucket_name, file.filename)
    video = Video(
        title=title,
        description=description,
        owner_id=admin.id,
        cloud_name=f'{admin.id}{file.filename}'
    )
    video.save()
    url = video.url
    return {'status': 200, 'url': f'{url}'}
    # except:
    #     return {'status': 404}
