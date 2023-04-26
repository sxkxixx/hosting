import fastapi_jsonrpc as jsonrpc
from fastapi import File, HTTPException, Request, Response, Depends
from app.core.models.models import User, Video, Comment, Like, View
from app.utils.hasher import get_current_user
from app.utils.s3_client import upload_file
from app.core.schemas.schemas import VideoUploadSchema, CommentUploadSchema

video_router = jsonrpc.Entrypoint(path='/api/v1/video')


@video_router.post('/upload_video', tags=['video'])
async def upload_video(request: Request):
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
        user = await User.objects.get(User.id == 1)
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
async def upload_comment(comment_data: CommentUploadSchema, user: User = Depends(get_current_user)) -> bool:
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = await Video.objects.get(comment_data.video_id == Video.id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    comment = Comment(
        comment_text=comment_data.comment_text,
        owner_id=user.id,
        video_id=comment_data.video_id
    )
    await comment.save()
    return True


@video_router.method(tags=['video'])
async def change_like_status(video_id: int, user: User = Depends(get_current_user)) -> dict:
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = await Video.objects.get(Video.id == video_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        like_record = await Like.objects.get(video_id == Like.video_id and user.id == Like.user_id)
        await like_record.delete()
        return {'status': 'like is removed'}
    except:
        await Like.objects.create(user_id=user.id, video_id=video_id)
        return {'status': 'like is added'}


@video_router.method(tags=['video'])
async def get_video(id: int, user: User = Depends(get_current_user)) -> dict:
    try:
        video = await Video.objects.get(id == Video.id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    is_liked = False
    if user:
        await View.objects.create(video_id=id, user_id=user.id)
        try:
            await Like.objects.get(Like.video_id == video.id and Like.user_id == user.id)
            is_liked = True
        except:
            is_liked = False
    return {'url': video.url,
            'comments': [{'user': User.get_by_id(comment.owner_id).username,
                          'comment_text': comment.comment_text,
                          'created_at': comment.created_at} for comment in video.video_comments],
            'title': video.title,
            'description': video.description,
            'likes': video.video_likes_count,
            'is_liked': is_liked}
