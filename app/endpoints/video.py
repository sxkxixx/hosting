import fastapi_jsonrpc as jsonrpc
from fastapi import File, HTTPException, Request, Response, Depends, Body
from app.core.models.models import User, Video, Comment, Like, View
from app.utils.hasher import get_current_user
from app.utils.s3_client import upload_file
from app.core.schemas.schemas import VideoUploadSchema, CommentUploadSchema
import logging

video_router = jsonrpc.Entrypoint(path='/api/v1/video')

logging.basicConfig(filename='app/logs.log', level=logging.INFO)


@video_router.post('/upload_video', tags=['video'])
async def upload_video(request: Request, response: Response):
    user = await get_current_user(request, response)
    if not user:
        logging.warning(f'Upload Video: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    form = await request.form()
    try:
        VideoUploadSchema(**form)
    except:
        logging.error(f'Upload Video: Incorrect data of video schema: {form}')
        HTTPException(status_code=400, detail='Bad Request')

    title, description = form.get('title'), form.get('description')
    file: File(...) = form.get('file')
    try:
        user = await User.objects.get(User.id == user.id)
        upload_file(file)
        video = Video(
            title=title, description=description,
            owner_id=user.id, cloud_name=f'{user.id}{file.filename}'
        )
        await video.save()
        url = video.url
        logging.info(f'Upload Video: Video {video.id} successfully uploaded')
        return Response({'status': 200, 'url': f'{url}'})
    except:
        logging.error(f'Upload Video: Something went wrong')
        HTTPException(status_code=400, detail='Bad Request')


@video_router.method(tags=['video'])
async def upload_comment(comment_data: CommentUploadSchema, user: User = Depends(get_current_user)) -> bool:
    if not user:
        logging.warning(f'Upload Comment: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = await Video.objects.get(comment_data.video_id == Video.id)
    except:
        logging.warning(f'Upload Comment: No Video')
        raise HTTPException(status_code=400, detail='Bad Request')
    comment = Comment(
        comment_text=comment_data.comment_text,
        owner_id=user.id,
        video_id=video.video_id
    )
    await comment.save()
    logging.info(f'Upload Comment: Comment {comment.id} uploaded')
    return True


@video_router.method(tags=['video'])
async def delete_comment(comment_id: int = Body(...), user: User = Depends(get_current_user)) -> dict:
    if not user:
        logging.warning(f'Delete Comment: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        comment = await Comment.objects.get(Comment.id == comment_id)
    except:
        logging.warning(f'Delete Comment: No comment {comment_id}')
        raise HTTPException(status_code=400, detail='Bad Request')
    if comment.owner_id == user.id:
        context = {'comment': comment.id, 'status': 'deleted'}
        await comment.delete()
        logging.info(f'Delete Comment: Comment Deleted {comment_id}')
        return context
    logging.error(f'Delete Comment: User-{user.id} can\'t delete Comment-{comment.id}')
    raise HTTPException(status_code=400, detail='Bad Request')


@video_router.method(tags=['video'])
async def change_like_status(video_id: int, user: User = Depends(get_current_user)) -> dict:
    if not user:
        logging.warning(f'Change Like Status: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = await Video.objects.get(Video.id == video_id)
    except:
        logging.warning(f'Change Like Status: No Video')
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        like_record = await Like.objects.get(video.id == Like.video_id and user.id == Like.user_id)
        logging.info(f'Change Like Status: {like_record.id} deleted')
        await like_record.delete()
        return {'status': 'Removed'}
    except:
        like_record = Like(user_id=user.id, video_id=video_id)
        await like_record.save()
        logging.info(f'Change Like Status: {like_record.id} deleted')
        return {'status': 'Added'}


@video_router.method(tags=['video'])
async def get_video(id: int, user: User = Depends(get_current_user)) -> dict:
    try:
        video = await Video.objects.get(id == Video.id)
    except:
        logging.warning(f'Get Video: No Video {id}')
        raise HTTPException(status_code=400, detail='Bad Request')
    is_liked = False
    if user:
        await View.objects.create(video_id=id, user_id=user.id)
        try:
            await Like.objects.get(Like.video_id == video.id and Like.user_id == user.id)
            is_liked = True
        except:
            is_liked = False
    logging.info(f'Get Video: Video({id}) data returned')
    return {'url': video.url,
            'comments': [{'user': await User.objects.get(User.id == comment.owner_id).username,
                          'comment_text': comment.comment_text,
                          'created_at': comment.created_at} for comment in video.video_comments],
            'title': video.title,
            'description': video.description,
            'likes': await video.likes_amount,
            'is_liked': is_liked}


@video_router.method(tags=['video'])
async def delete_video(video_id: int = Body(...), user: User = Depends(get_current_user)):
    if not user:
        logging.warning(f'Delete Video: No User')
        raise HTTPException(status_code=401, detail='Bad Request')
    try:
        video = await Video.objects.get(Video.id == video_id)
    except:
        logging.warning(f'Delete Video: User {user.id}, No Video {video_id}')
        raise HTTPException(status_code=400, detail='Bad Request')
    if user.id == video.owner_id:
        context = {'video': video.id, 'status': 'deleted'}
        await video.delete()
        return context
    logging.error(f'Delete Video: User-{user.id} can\'t delete video-{video.id}')
    raise HTTPException(status_code=400, detail='Bad Request')
