from typing import Optional
import fastapi_jsonrpc as jsonrpc
from fastapi import HTTPException, Request, Response, Depends, Body, Form, UploadFile, File
from app.core.models.models import User, Video, Comment, Like, View
from app.utils.hasher import get_current_user, get_unique_name
from app.utils.s3_client import upload_file
from app.core.schemas.schemas import CommentUploadSchema
import logging

video_router = jsonrpc.Entrypoint(path='/api/v1/video')

logging.basicConfig(filename='app/logs.log', level=logging.INFO)


@video_router.method(tags=['video'])
async def main_page(user: User = Depends(get_current_user)) -> dict:
    videos = await Video.objects.select_related('user_views').order_by('-user_views__count').all()
    return {
        'user': user.email if user else None,
        'videos': [{
            'id': video.id,
            'title': video.title,
            'owner': {
                'id': video.owner.id,
                'email': video.owner.email
            }
        } for video in videos]
    }


@video_router.post('/upload_video', tags=['video'])
async def upload_video(request: Request, response: Response, title: str = Form(...),
                       description: str = Form(...),
                       video_file: UploadFile = File(...),
                       preview_file: Optional[UploadFile | None] = File(...)):
    user = await get_current_user(request, response)
    if not user:
        logging.warning(f'Upload Video: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        cloud_video_name = 'videos/' + get_unique_name(filename=video_file.filename)
        result = await upload_file(video_file, cloud_video_name)
        if not result:
            raise HTTPException(status_code=400, detail='Bad Request')
        preview_cloud_name = None
        if preview_file:
            preview_cloud_name = 'previews/' + get_unique_name(preview_file.filename)
            await upload_file(preview_file, preview_cloud_name)
        video = Video(
            title=title, description=description,
            owner=user, video_cloud_name=cloud_video_name, preview_cloud_name=preview_cloud_name
        )
        await video.save()
        url = await video.video_url()
        logging.info(f'Upload Video: Video {video.id} successfully uploaded')
        return {'status': 200, 'url': f'{url}'}
    except Exception as e:
        logging.error(f'Upload Video: Something went wrong {e}')
        HTTPException(status_code=400, detail='e')


@video_router.method(tags=['video'])
async def upload_comment(comment_data: CommentUploadSchema, user: User = Depends(get_current_user)) -> dict:
    if not user:
        logging.warning(f'Upload Comment: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = await Video.objects.get(comment_data.video_id == Video.id)
    except Exception as e:
        logging.warning(f'Upload Comment: No Video: {e}')
        raise HTTPException(status_code=400, detail='Bad Request')
    comment = await Comment(
        comment_text=comment_data.comment_text,
        owner=user,
        video=video
    ).save()
    # await video.video_comments.add(comment)
    logging.info(f'Upload Comment: Comment {comment.id} uploaded')
    logging.info(comment)
    return {'comment': comment.id, 'status': 'uploaded'}


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
    if comment.owner == user:
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
        like_record = await Like.objects.get(video.id == Like.video.id and user.id == Like.user.id)
        logging.info(f'Change Like Status: {like_record.id} deleted')
        await like_record.delete()
        return {'status': 'Removed'}
    except:
        like_record = Like(user=user.id, video=video_id)
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
        await View.objects.create(video=id, user=user.id)
        try:
            await Like.objects.get(Like.video == video.id and Like.user == user.id)
            is_liked = True
            await View.objects.create(user=user, video=video)
        except:
            is_liked = False
    try:
        logging.info(f'Get Video: Video({id}) data returned')
        comments = await video.video_comments.all()
        return {'video': {
            'url': await video.video_url(),
            'title': video.title,
            'description': video.description,
            'likes': await video.likes_amount,
        },
                'comments': [{'id': comment.id,
                              'owner': (await User.objects.get(User.id == comment.owner.id)).email,
                              'text': comment.comment_text,
                              'created_at': comment.created_at} for comment in comments],
                'is_liked': is_liked}
    except Exception as e:
        logging.error(f'Get Video: {e}')


@video_router.method(tags=['video'])
async def delete_video(video_id: int = Body(...), user: User = Depends(get_current_user)) -> dict:
    if not user:
        logging.warning(f'Delete Video: No User')
        raise HTTPException(status_code=401, detail='Unauthorized')
    try:
        video = await Video.objects.get(Video.id == video_id)
    except:
        logging.warning(f'Delete Video: User {user.id}, No Video {video_id}')
        raise HTTPException(status_code=400, detail='Bad Request')
    if user == video.owner:
        context = {'video': video.id, 'status': 'deleted'}
        video.delete_from_s3()
        await video.delete()
        return context
    logging.error(f'Delete Video: User-{user.email} can\'t delete video-{video.id}')
    raise HTTPException(status_code=400, detail='Bad Request')


@video_router.method(tags=['video'])
async def delete_like_record(like_id: int = Body(...)) -> str:
    like = await Like.objects.get(Like.id == like_id)
    await like.delete()
    return 'deleted'
