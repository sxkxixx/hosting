import datetime
from fastapi import Depends, Response, HTTPException, Body, UploadFile, File
from app.utils.hasher import Hasher, get_current_user
from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_MINUTES
from app.core.models import User, Video, Role, Claim
from app.core.schemas import UserRegister, UserSchema, ClaimSchema
from app.core.exceptions import UserExistsError, WrongDataError, UserNotExistsError, AuthError, UploadError
import fastapi_jsonrpc as jsonrpc
from app.utils.s3_client import upload_file
from app.utils.hasher import get_unique_name
from app.core.config import AVATARS_DIR
import logging

user_route = jsonrpc.Entrypoint(path='/api/v1/user')

logging.basicConfig(filename='app/logs.log', level=logging.INFO)


@user_route.method(tags=['user'], errors=[UserExistsError, WrongDataError])
async def register(user: UserRegister) -> dict:
    email, username, password, password_repeat = user.email.lower(), user.username.lower(), user.password, user.password_repeat
    try:
        user_by_data = await User.objects.filter((User.email == email) | (User.username == username)).get()
        logging.warning(f'Register: User {user_by_data.email} already exist')
        raise UserExistsError()
    except:
        user_by_data = None
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
        return {'detail': 'Пользователь {} успешно создан'.format(user.email)}
    except Exception as e:
        logging.error(f'Register: {e}')
        raise HTTPException(status_code=400, detail='Bad Request')


@user_route.method(tags=['user'], errors=[WrongDataError, UserNotExistsError])
async def login(response: Response, user: UserSchema) -> dict:
    email, password = user.email.lower(), user.password
    if not (email and password):
        raise WrongDataError()
    try:
        user = await User.objects.get(User.email == email)
    except:
        raise UserNotExistsError()
    try:
        if Hasher.verify_password(password, user.hashed_password):
            data = {'sub': email}
            access_token = Hasher.get_encode_token(data)
            refresh_token = Hasher.get_encode_token(data, datetime.timedelta(seconds=REFRESH_TOKEN_EXPIRE_MINUTES))
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
def logout(response: Response, user: User = Depends(get_current_user)) -> dict:
    if user:
        response.delete_cookie('access_token')
        response.delete_cookie('refresh_token')
        logging.info(f'Logout: {user.email} logout')
    return {'user': user.username if user else 'No user', 'status': 'Logout'}


@user_route.method(tags=['user'], errors=[AuthError])
async def profile(user: User = Depends(get_current_user)) -> dict:
    if not user:
        logging.warning(f'Profile: No user')
        raise AuthError()
    try:
        videos = await Video.objects.filter(user.id == Video.owner.id).all()
    except:
        logging.error(f'Profile: No video for user {user.id}')
        videos = []
    context = {
        'avatar': await user.avatar_url(),
        'username': user.username,
        'email': user.email,
        'videos': [{'id': video.id, 'title': video.title, 'preview': await video.preview_url()} for video in videos]
    }
    return context


@user_route.method(tags=['user'], errors=[AuthError, WrongDataError])
async def create_claim(claim_schema: ClaimSchema = Body(...), user: User = Depends(get_current_user)) -> dict:
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
def current_user(user: User = Depends(get_current_user)) -> dict:
    if not user:
        raise AuthError()
    logging.info(f'Current User: {user.email}')
    return {'email': user.email}


@user_route.method(tags=['user'], errors=[AuthError])
async def delete_user(user: User = Depends(get_current_user)) -> str:
    if not user:
        raise AuthError()
    await user.delete()
    logging.info(f'Delete User: {user.email} deleted')
    return 'deleted'


@user_route.post(tags=['user'], path='/upload_avatar')
async def upload_avatar(avatar: UploadFile = File(...), user: User = Depends(get_current_user)):
    if not user:
        raise HTTPException(status_code=401, detail='Unauthorized')
    unique_avatar_name = AVATARS_DIR + get_unique_name(avatar.filename)
    result = await upload_file(avatar, unique_avatar_name)
    if not result:
        raise HTTPException(status_code=400, detail='Bad Request')
    await user.update(avatar=unique_avatar_name)
    return {'avatar': await user.avatar_url()}
