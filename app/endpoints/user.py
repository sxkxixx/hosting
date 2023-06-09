from fastapi import Depends, Response, HTTPException, Body, UploadFile, File, BackgroundTasks
from utils.auth import Hasher, get_unique_name, get_current_user_v2
from core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES, AVATARS_DIR
from core.models import User, Video, Role, Claim, Subscription
from core.schemas import UserRegister, UserSchema, ClaimSchema
from core.exceptions import UserExistsError, WrongDataError, NoUserError, AuthError
import fastapi_jsonrpc as jsonrpc
from utils.s3_client import upload_file, delete_object
from utils.utils import get_user_videos, is_valid_signature
from utils.smtp_task import send_message
from utils.message_templates import on_register_template
import logging

user_route = jsonrpc.Entrypoint(path='/api/v1/user')
logging.basicConfig(filename='logs.log', level=logging.INFO)


@user_route.method(tags=['user'], errors=[UserExistsError, WrongDataError])
async def register(user: UserRegister, response: Response, background_task: BackgroundTasks) -> dict:
    email, username, password, password_repeat = user.email.lower(), user.username.lower(), user.password, user.password_repeat
    user_by_data = await User.objects.filter((User.email == email) | (User.username == username)).all()
    if user_by_data:
        raise UserExistsError()
    if user_by_data or password != password_repeat:
        logging.warning(f'Register: Bad try to register a user')
        raise WrongDataError()
    try:
        user_role = await Role.objects.get(Role.role_name == 'User')
        user = User(
            username=username,
            email=email,
            hashed_password=Hasher.get_hash_password(password),
            role=user_role,
        )
        await user.save()
        logging.info(f'User {user.email} created')
        data = {'sub': user.email}
        access_token = Hasher.get_encode_token(data)
        refresh_token = Hasher.get_encode_token(data, REFRESH_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key='access_token', value=access_token, httponly=True,
                                expires=ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True,
                                expires=REFRESH_TOKEN_EXPIRE_MINUTES)
        background_task.add_task(send_message, 'Регистрация на видеохостинге', on_register_template, user.email)
        return {'detail': 'Пользователь {} успешно создан'.format(user.email)}
    except Exception as e:
        logging.error(f'Register: {e}')
        raise HTTPException(status_code=400, detail='Bad Request')


@user_route.method(tags=['user'], errors=[WrongDataError, NoUserError])
async def login(response: Response, user: UserSchema) -> dict:
    email, password = user.email.lower(), user.password
    if not (email and password):
        raise WrongDataError()
    user = await User.objects.get_or_none(User.email == email)
    if not user:
        raise NoUserError()
    try:
        if Hasher.verify_password(password, user.hashed_password):
            data = {'sub': user.email}
            access_token = Hasher.get_encode_token(data,)
            refresh_token = Hasher.get_encode_token(data, REFRESH_TOKEN_EXPIRE_MINUTES)
            response.set_cookie(key='access_token', value=access_token, httponly=True,
                                expires=ACCESS_TOKEN_EXPIRE_MINUTES)
            response.set_cookie(key='refresh_token', value=refresh_token, httponly=True,
                                expires=REFRESH_TOKEN_EXPIRE_MINUTES)
            logging.info(f'Login: Successfully login {user.email}')
            return {'user': user.email, 'status': 'Authorized'}
        logging.warning(f'Login: Incorrect password for {user.email}')
        raise WrongDataError()
    except Exception as e:
        logging.error(f'Login: {e}')
        raise HTTPException(status_code=400, detail='Bad Request')


@user_route.method(tags=['user'])
def logout(response: Response, user: User = Depends(get_current_user_v2)) -> dict:
    if user:
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        logging.info(f'Logout: {user.email} logout')
    return {'user': user.username if user else 'No user', 'status': 'Logout'}


@user_route.method(tags=['user'], errors=[AuthError])
async def profile(user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        logging.warning(f'Profile: No user')
        raise AuthError()
    videos = await Video.objects.filter(user.id == Video.owner.id).all()
    viewed_videos = await Video.objects.select_related('user_views').exclude(owner=user).filter(user_views__user=user).all()
    context = {
        'avatar': await user.avatar_url(),
        'username': user.username,
        'email': user.email,
        'videos': [{'id': video.id, 'title': video.title, 'preview': await video.preview_url()} for video in videos],
        'viewed_videos': [{'id': video.id, 'title': video.title, 'owner': (await User.objects.get(User.id == video.owner.id)).email, 'preview': await video.preview_url()} for video in viewed_videos]
    }
    return context


@user_route.method(tags=['user'], errors=[AuthError, WrongDataError])
async def create_claim(claim_schema: ClaimSchema = Body(...), user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        logging.warning('Send Claim: No User')
        raise AuthError()
    if not (claim_schema.claim_type and claim_schema.claim_object_id and claim_schema.description):
        raise WrongDataError()
    try:
        claim = Claim(
            description=claim_schema.description,
            claim_type=claim_schema.claim_type,
            owner=user,
            claim_object_id=claim_schema.claim_object_id
        )
        await claim.save()
        logging.info(f'Create Claim: {claim.id}')
        return {'claim': {'id': claim.id, 'description': claim.description}, 'status': 'created'}
    except Exception as e:
        logging.error(f'Create Claim: {e}')
        raise WrongDataError()


@user_route.method(tags=['user'], errors=[AuthError])
def current_user(user: User = Depends(get_current_user_v2)) -> dict:
    if not user:
        raise AuthError()
    logging.info(f'Current User: {user.email}')
    return {'email': user.email}


@user_route.method(tags=['user'], errors=[AuthError])
async def delete_user(user: User = Depends(get_current_user_v2)) -> str:
    if not user:
        raise AuthError()
    await user.delete()
    logging.info(f'Delete User: {user.email} deleted')
    return 'deleted'


@user_route.post(tags=['user'], path='/api/v1/upload_avatar')
async def upload_avatar(avatar: UploadFile = File(...), user: User = Depends(get_current_user_v2)):
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    if not is_valid_signature(file_type='image', file=avatar):
        raise HTTPException(status_code=404, detail='Bad file type')
    avatar.file.seek(0)
    if user.avatar:
        await delete_object(user.avatar)
    unique_avatar_name = AVATARS_DIR + get_unique_name(avatar.filename)
    result = await upload_file(avatar, unique_avatar_name)
    if not result:
        raise HTTPException(status_code=400, detail='Bad Request')
    await user.update(avatar=unique_avatar_name)
    return {'avatar': await user.avatar_url()}


@user_route.method(tags=['user'], errors=[NoUserError])
async def get_user_page(user_id: int, user: User = Depends(get_current_user_v2)) -> dict:
    requested_user = await User.objects.get_or_none(User.id == user_id)
    if not requested_user:
        raise NoUserError()
    subscribed = False
    if user:
        subscribed = await Subscription.objects.get_or_none((Subscription.user.id == user.id) & (Subscription.aim_user.id == user_id))
    return {
        'user': {
            'id': requested_user.id,
            'email': requested_user.email,
            'username': requested_user.username,
            'avatar': await requested_user.avatar_url()
        },
        'videos': await get_user_videos(user_id),
        'subscribed': bool(subscribed)
    }


@user_route.method(tags=['user'], errors=[AuthError, NoUserError])
async def set_subscribe(user_id: int, current_user: User = Depends(get_current_user_v2)) -> dict:
    if not current_user:
        raise AuthError
    if current_user.id == user_id:
        raise WrongDataError()
    aim_user = await User.objects.get_or_none(User.id == user_id)
    if not aim_user:
        raise NoUserError()
    try:
        await Subscription.objects.create(
            user=current_user,
            aim_user=aim_user
        )
        return {'user': current_user.id, 'aim_user': user_id, 'status': 'subscribed'}
    except:
        raise WrongDataError()


@user_route.method(tags=['user'], errors=[AuthError, NoUserError])
async def delete_subscribe(user_id: int, current_user: User = Depends(get_current_user_v2)) -> dict:
    if not current_user:
        raise AuthError
    subscription = await Subscription.objects.get_or_none((Subscription.user.id == current_user.id) & (Subscription.aim_user.id == user_id))
    if not subscription:
        raise WrongDataError()
    await subscription.delete()
    return {'user': current_user.id, 'aim_user': user_id, 'status': 'deleted'}

