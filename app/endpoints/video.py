from typing import Optional
import fastapi_jsonrpc as jsonrpc
from fastapi import HTTPException, Depends, Body, Form, UploadFile, File
from core.models import User, Video, Comment, Like, View
from core.exceptions import AuthError, NoVideoError, NoCommentError, WrongDataError
from utils.auth import get_current_user_v2, get_unique_name
from utils.s3_client import upload_file
from core.schemas import CommentUploadSchema
import logging

video_router = jsonrpc.Entrypoint(path='/api/v1/video')
logging.basicConfig(filename='logs.log', level=logging.INFO)


@video_router.method(tags=['video'])
async def main_page(user: User = Depends(get_current_user_v2)) -> dict:
    try:
        videos = sorted(await Video.objects.select_related('user_views').all(), key=lambda x: len(x.user_views), reverse=True)
        logging.info(f'Main Page')
        return {
            'user': user.email if user else None,
            'videos': [{
                'id': video.id,
                'title': video.title,
                'preview': await video.preview_url(),
                'views': await video.views_amount(),
                'owner': {
                    'id': video.owner.id,
                    'email': (await User.objects.get(User.id == video.owner.id)).email,
                    'avatar': await (await User.objects.get(User.id == video.owner.id)).avatar_url()
                }
            } for video in videos]
        }
    except Exception as e:
        logging.error(f'{e}')


@video_router.post('/api/v1/upload_video', tags=['video'])
async def upload_video(user: User = Depends(get_current_user_v2), title: str = Form(...),
                       description: str = Form(...),
                       video_file: UploadFile = File(...),
                       preview_file: Optional[UploadFile | None] = File(...)):
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


@video_router.method(tags=['video'], errors=[AuthError, NoVideoError])
async def upload_comment(comment_data: CommentUploadSchema, user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        logging.warning(f'Upload Comment: No User')
        raise AuthError()
    video = await Video.objects.get_or_none(comment_data.video_id == Video.id)
    if not video:
        logging.warning(f'Upload Comment: No Video: {comment_data.video_id}')
        raise NoVideoError()
    comment = await Comment(
        comment_text=comment_data.comment_text,
        owner=user,
        video=video
    ).save()
    logging.info(f'Upload Comment: Comment {comment.id} uploaded')
    return {'comment': comment.id, 'status': 'uploaded', 'user': user.email}


@video_router.method(tags=['video'], errors=[AuthError, NoCommentError, WrongDataError])
async def delete_comment(comment_id: int = Body(...), user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        logging.warning(f'Delete Comment: No User')
        raise AuthError()
    comment = await Comment.objects.get_or_none(Comment.id == comment_id)
    if not comment:
        logging.warning(f'Delete Comment: No comment {comment_id}')
        raise NoCommentError()
    if comment.owner == user:
        context = {'comment': comment.id, 'status': 'deleted'}
        await comment.delete()
        logging.info(f'Delete Comment: Comment Deleted {comment_id}')
        return context
    logging.error(f'Delete Comment: User-{user.id} can\'t delete Comment-{comment.id}')
    raise WrongDataError()


@video_router.method(tags=['video'], errors=[AuthError, NoVideoError])
async def change_like_status(video_id: int, user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        logging.warning(f'Change Like Status: No User')
        raise AuthError()
    video = await Video.objects.get_or_none(Video.id == video_id)
    if not video:
        logging.warning(f'Change Like Status: No Video')
        raise NoVideoError()
    try:
        like_record = await Like.objects.get(video.id == Like.video.id and user.id == Like.user.id)
        logging.info(f'Change Like Status: {like_record.id} deleted')
        await like_record.delete()
        return {'status': 'Removed'}
    except:
        like_record = Like(user=user.id, video=video_id)
        await like_record.save()
        logging.info(f'Change Like Status: {like_record.id} added')
        return {'status': 'Added'}


@video_router.method(tags=['video'], errors=[NoVideoError])
async def get_video(id: int, user: User = Depends(get_current_user_v2)) -> dict:
    video = await Video.objects.get_or_none(id == Video.id)
    if not video:
        logging.warning(f'Get Video: No Video {id}')
        raise NoVideoError()
    if user:
        await View.objects.create(video=id, user=user.id)
    try:
        logging.info(f'Get Video: Video({id}) data returned')
        comments = await video.video_comments.all()
        owner = await User.objects.get(User.id == video.owner.id)
        return {
            'video': {
                'preview': await video.preview_url(),
                'url': await video.video_url(),
                'title': video.title,
                'description': video.description,
                'likes': await video.likes_amount(),
                'views': await video.views_amount(),
                'comments': [{'id': comment.id,
                              'owner': (await User.objects.get(User.id == comment.owner.id)).email,
                              'text': comment.comment_text} for comment in comments]
            },
            'user': {
                'owner_id': owner.id,
                'owner_avatar': await owner.avatar_url(),
                'owner_email': owner.email,
            }
        }
    except Exception as e:
        logging.error(f'Get Video: {e}')


@video_router.method(tags=['video'], errors=[AuthError, NoVideoError, WrongDataError])
async def delete_video(video_id: int = Body(...), user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        logging.warning(f'Delete Video: No User')
        raise AuthError()
    video = await Video.objects.get_or_none(Video.id == video_id)
    if not video:
        logging.warning(f'Delete Video: User {user.id}, No Video {video_id}')
        raise NoVideoError()
    if user == video.owner:
        context = {'video': video.id, 'status': 'deleted'}
        await video.delete_from_s3()
        await video.delete()
        return context
    logging.error(f'Delete Video: User-{user.email} can\'t delete video-{video.id}')
    raise WrongDataError()
