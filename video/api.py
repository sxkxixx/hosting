import fastapi_jsonrpc as jsonrpc
from fastapi import File, HTTPException, Request, Response, Depends
from user.hasher import get_current_user
from user.models import User
from video.models import Video, Comment, Like
from video.s3_client import upload_file
from video.schemas import VideoUploadSchema, CommentUploadSchema

video_router = jsonrpc.Entrypoint(path='/api/v1/video')


@video_router.post('/upload_video', tags=['video'])
async def upload_video_test(request: Request):
    user = get_current_user(request)
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    form = await request.form()
    try:
        VideoUploadSchema(**form)
    except:
        HTTPException(status_code=400, detail='Bad Request')

    title, description = form.get('title'), form.get('description')
    file: File(...) = form.get('file')
    try:
        user = User.select().where(User.id == 1).get()
        upload_file(file)
        video = Video(
            title=title, description=description,
            owner_id=user.id, cloud_name=f'{user.id}{file.filename}'
        )
        video.save()
        url = video.url
        return Response({'status': 200, 'url': f'{url}'})
    except:
        HTTPException(status_code=400, detail='Bad Request')


@video_router.method(tags=['video'])
def upload_comment(comment_data: CommentUploadSchema, user: User = Depends(get_current_user)) -> str:
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = Video.select().where(comment_data.video_id == Video.id).get()
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    comment = Comment(
        comment_text=comment_data.comment_text,
        owner_id=user.id,
        video_id=comment_data.video_id
    )
    comment.save()
    return 'Comment successfully uploaded'


@video_router.method(tags=['video'])
def change_like_status(video_id: int, user: User = Depends(get_current_user)) -> dict:
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = Video.get_by_id(video_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        like_record = Like.get(video_id == Like.video_id and user.id == Like.user_id)
        like_record.delete_instance()
        return {'status': 'like is deleted'}
    except:
        like_record = Like(user_id=user.id, video_id=video_id)
        like_record.save()
        return {'status': 'like is added'}
