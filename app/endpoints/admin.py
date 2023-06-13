from core.config import REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from core.exceptions import AuthError, NoUserError, NoAdminError, WrongDataError
from fastapi import Depends, HTTPException, Response, Body, BackgroundTasks
from utils.auth import get_current_user_v2, Hasher, get_object_by_id
from utils.message_templates import on_delete_video_template, on_delete_account_template
from core.models import User, Claim, Comment, Video
from utils.s3_client import delete_object
from utils.smtp_task import send_message
from core.schemas import UserSchema
import fastapi_jsonrpc as jsonrpc
import logging

admin_route = jsonrpc.Entrypoint(path='/api/v1/admin')
logging.basicConfig(filename='logs.log', level=logging.INFO)


@admin_route.method(tags=['admin'], errors=[NoUserError, NoAdminError, WrongDataError])
async def admin_login(admin_schema: UserSchema, response: Response) -> dict:
    admin: User = await User.objects.get_or_none(User.email == admin_schema.email)
    if not admin:
        logging.info(f'Admin Login: Admin({admin_schema.email}) loging in')
        raise NoUserError()
    if not admin.is_superuser:
        logging.warning(f'Admin Login: User({admin.email}) is not Admin')
        raise NoAdminError()
    if Hasher.verify_password(admin_schema.password, admin.hashed_password):
        data = {'sub': admin.email}
        access_token = Hasher.get_encode_token(data)
        refresh_token = Hasher.get_encode_token(data, REFRESH_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key='access_token', value=access_token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True,
                            expires=REFRESH_TOKEN_EXPIRE_MINUTES)
        logging.info(f'Admin Login: Successfully login {admin.email}')
        return {'user': admin.email, 'status': 'Authorized'}
    logging.error(f'Admin Login: Incorrect password for Admin({admin.email})')
    raise WrongDataError()


@admin_route.method(tags=['admin'], errors=[AuthError])
async def admin_claims(admin: User = Depends(get_current_user_v2)) -> dict:
    if not admin.is_superuser:
        raise AuthError()
    try:
        comment_claims = [
            {'id': claim.id, 'comment': (await Comment.objects.get(Comment.id == claim.claim_object_id)).comment_text,
             'claim': claim.description}
            for claim in await Claim.objects.filter((Claim.claim_type == 'comment')).all()
        ]
        video_claims = [
            {'id': claim.id, 'video_id': claim.claim_object_id, 'claim': claim.description} for claim in
            await Claim.objects.filter((Claim.claim_type == 'video')).all()
        ]
        return {'comment_claims': comment_claims, 'video_claims': video_claims}
    except Exception as e:
        print(e)


@admin_route.method(tags=['admin'], errors=[AuthError, WrongDataError])
async def change_claim_status(claim_id: int = Body(...), status: str = Body(...),
                              admin: User = Depends(get_current_user_v2)) -> dict:
    if not admin.is_superuser:
        raise AuthError()
    claim = await Claim.objects.get_or_none(Claim.id == claim_id)
    if not claim:
        raise WrongDataError()
    if status not in {'approved', 'denied'}:
        raise WrongDataError()
    if status == 'denied':
        await claim.delete()
        return {'claim': claim.id, 'status': claim.status}
    claim_object = await get_object_by_id(claim.claim_type, claim.claim_object_id)
    await claim_object.delete()
    same_object_claims = await Claim.objects.filter(
        (Claim.claim_type == claim.claim_type) & (Claim.claim_object_id == claim.claim_object_id)).all()
    for claim in same_object_claims:
        await claim.delete()
    return {'claim': claim.id, 'status': claim.status, 'object': 'deleted'}


@admin_route.method(tags=['admin'], errors=[AuthError])
async def get_claim_object(claim_id: int = Body(...), admin: User = Depends(get_current_user_v2)) -> dict:
    if not admin.is_superuser:
        raise AuthError()
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    claim_object = await get_object_by_id(claim.claim_type, claim.claim_object_id)
    return claim_object


@admin_route.method(tags=['admin'], errors=[AuthError])
async def delete_claim(claim_id: int = Body(...), admin: User = Depends(get_current_user_v2)) -> dict:
    if not admin.is_superuser:
        raise AuthError()
    claim = await Claim.objects.get_or_none(Claim.id == claim_id)
    if not claim:
        raise HTTPException(status_code=400, detail='Bad Request')
    await claim.delete()
    return {'claim': claim_id, 'status': 'deleted'}


@admin_route.method(tags=['admin'], errors=[AuthError])
async def get_videos(admin: User = Depends(get_current_user_v2)) -> list:
    if not admin.is_superuser:
        raise AuthError()
    videos = await Video.objects.all()
    return [{'id': video.id,
             'title': video.title,
             'owner': (await User.objects.get(User.id == video.owner.id)).email,
             'preview': await video.preview_url()} for video in videos]


@admin_route.method(tags=['admin'], errors=[AuthError])
async def get_users(admin: User = Depends(get_current_user_v2)) -> list:
    if not admin.is_superuser:
        raise AuthError()
    users = await User.objects.all()
    return [{'id': user.id, 'email': user.email, 'avatar': await user.avatar_url()} for user in users]


@admin_route.method(tags=['admin'], errors=[AuthError, WrongDataError])
async def delete_video(video_id: int, background_tasks: BackgroundTasks, admin: User = Depends(get_current_user_v2)) -> dict:
    if not admin.is_superuser:
        raise AuthError()
    video = await Video.objects.get_or_none(Video.id == video_id)
    if not video:
        raise WrongDataError()
    background_tasks.add_task(send_message, 'Удаление видео', on_delete_video_template, (await User.objects.get(User.id == video.owner.id)).email)
    await delete_object(video.video_cloud_name)
    await delete_object(video.preview_cloud_name)
    await video.delete()
    return {'id': video.id, 'status': 'deleted'}


@admin_route.method(tags=['admin'], errors=[AuthError, WrongDataError])
async def delete_user(user_id: int, background_tasks: BackgroundTasks, admin: User = Depends(get_current_user_v2)) -> dict:
    if not admin.is_superuser:
        raise AuthError()
    user = await User.objects.get_or_none(User.id == user_id)
    if not user:
        raise WrongDataError()
    if user.avatar:
        await delete_object(user.avatar)
    background_tasks.add_task(send_message, 'Аккаунт удалён', on_delete_account_template, user.email)
    await user.delete()
    return {'id': user.id, 'status': 'deleted'}



