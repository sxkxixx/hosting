import logging
import datetime
import fastapi_jsonrpc as jsonrpc
from fastapi import Depends, HTTPException, Response, Body
from app.core.config import REFRESH_TOKEN_EXPIRE_MINUTES, ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.schemas.schemas import UserSchema
from app.utils.hasher import get_current_user, Hasher, get_object_by_id
from app.core.models.models import User, Claim

admin_route = jsonrpc.Entrypoint(path='/api/v1/admin')
logging.basicConfig(filename='app/logs.log', level=logging.INFO)


@admin_route.method(tags=['admin'])
async def admin_login(admin_schema: UserSchema, response: Response) -> dict:
    try:
        admin: User = await User.objects.get(User.email == admin_schema.email)
        logging.info(f'Admin Login: Admin({admin_schema.email}) loging in')
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    if not admin.is_superuser:
        logging.warning(f'Admin Login: User({admin.email}) is not Admin')
        raise HTTPException(status_code=400, detail='Bad Request')
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
    raise HTTPException(status_code=400, detail='Bad Request')


@admin_route.method(tags=['admin'])
async def admin_claims(admin: User = Depends(get_current_user)) -> list[dict]:
    if not admin.is_superuser:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        claims = await Claim.objects.filter(status='sent').all()
        return [{'claim_id': claim.id, 'description': claim.description,
                 'claim_type': claim.claim_type, 'owner': claim.owner.id,
                 'claim_object_id': claim.claim_object_id, 'status': claim.status} for claim in claims]
    except Exception as e:
        print(e)
    # return claims


@admin_route.method(tags=['admin'])
async def change_claim_status(claim_id: int = Body(...), status: str = Body(...),
                              admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    if status not in {'approved', 'denied'}:
        raise HTTPException(status_code=400, detail='Bad Request')
    claim.status = status
    await claim.save()
    return {'claim': claim.id, 'status': claim.status}


@admin_route.method(tags=['admin'])
async def get_claim_object(claim_id: int = Body(...), admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    claim_object = await get_object_by_id(claim.claim_type, claim.claim_object_id)
    return claim_object


@admin_route.method(tags=['admin'])
async def delete_claim(claim_id: int = Body(...), admin: User = Depends(get_current_user)) -> dict:
    if not admin.is_superuser:
        raise HTTPException(status_code=400, detail='Bad Request')
    try:
        claim = await Claim.objects.get(Claim.id == claim_id)
    except:
        raise HTTPException(status_code=400, detail='Bad Request')
    await claim.delete()
    return {'claim': claim_id, 'status': 'deleted'}
