import logging
import datetime
import fastapi_jsonrpc as jsonrpc
from fastapi import Depends, HTTPException, Response, Body
from core.config import REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from core.schemas import UserSchema
from utils.auth import get_current_user, Hasher, get_object_by_id
from core.models import User, Claim, Comment
from core.exceptions import AuthError, NoUserError, NoAdminError, WrongDataError

admin_route = jsonrpc.Entrypoint(path='/api/v1/admin')
logging.basicConfig(filename='app/logs.log', level=logging.INFO)


@admin_route.method(tags=['admin'], errors=[NoUserError, NoAdminError, WrongDataError])
async def admin_login(admin_schema: UserSchema, response: Response) -> dict:
    try:
        admin: User = await User.objects.get(User.email == admin_schema.email)
        logging.info(f'Admin Login: Admin({admin_schema.email}) loging in')
    except:
        raise NoUserError()
    if not admin.is_superuser:
        logging.warning(f'Admin Login: User({admin.email}) is not Admin')
        raise NoAdminError()
    if Hasher.verify_password(admin_schema.password, admin.hashed_password):
        data = {'sub': admin.email}
        access_token = Hasher.get_encode_token(data)
        refresh_token = Hasher.get_encode_token(data, datetime.timedelta(seconds=REFRESH_TOKEN_EXPIRE_MINUTES))
        response.set_cookie(key='access_token', value=access_token, httponly=True, expires=ACCESS_TOKEN_EXPIRE_MINUTES)
        response.set_cookie(key='refresh_token', value=refresh_token, httponly=True,
                            expires=REFRESH_TOKEN_EXPIRE_MINUTES)
        logging.info(f'Admin Login: Successfully login {admin.email}')
        return {'user': admin.email, 'status': 'Authorized'}
    logging.error(f'Admin Login: Incorrect password for Admin({admin.email})')
    raise WrongDataError()


@admin_route.method(tags=['admin'], errors=[NoAdminError])
async def admin_claims(admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise NoAdminError()
    try:
        comment_claims = [
            {'id': claim.id, 'comment': (await Comment.objects.get(Comment.id == claim.claim_object_id)).comment_text,
             'claim': claim.description}
            for claim in await Claim.objects.filter((Claim.status == 'sent') & (Claim.claim_type == 'comment')).all()
        ]
        video_claims = [
            {'id': claim.id, 'video_id': claim.claim_object_id, 'claim': claim.description} for claim in
            await Claim.objects.filter((Claim.status == 'sent') & (Claim.claim_type == 'video')).all()
        ]

        return {'comment_claims': comment_claims, 'video_claims': video_claims}
    except Exception as e:
        print(e)


@admin_route.method(tags=['admin'], errors=[NoAdminError])
async def change_claim_status(claim_id: int = Body(...), status: str = Body(...),
                              admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise NoAdminError()
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    if status not in {'approved', 'denied'}:
        raise HTTPException(status_code=400, detail='Bad Request')
    await claim.update(status=status)
    return {'claim': claim.id, 'status': claim.status}


@admin_route.method(tags=['admin'], errors=[NoAdminError])
async def get_claim_object(claim_id: int = Body(...), admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise NoAdminError()
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    claim_object = await get_object_by_id(claim.claim_type, claim.claim_object_id)
    return claim_object


@admin_route.method(tags=['admin'], errors=[NoAdminError])
async def delete_claim(claim_id: int = Body(...), admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise NoAdminError()
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    await claim.delete()
    return {'claim': claim_id, 'status': 'deleted'}
