from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from passlib.hash import bcrypt
from tortoise.exceptions import DoesNotExist

from models.app_models import User_Pydantic, User, RankModel, UserDTO
import jwt

auth = APIRouter()
router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='/auth/token')
JWT_SECRET = 'myjwtsecret'


async def auth_user(username: str, password: str):
    try:
        user = await User.get(username=username)
        if not user:
            return False
        if not user.verify_password(password):
            return False
        return user
    except DoesNotExist:
        return False


@auth.post('/token')
async def token(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await auth_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )

    user_obj = await User_Pydantic.from_tortoise_orm(user)

    token = jwt.encode(user_obj.dict(), JWT_SECRET)
    return {'access_token': token, 'token_type': 'bearer'}


async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        payload = jwt.decode(token, JWT_SECRET, algorithms=['HS256'])
        user = await User.get(id=payload.get('id'))
    except:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid username or password'
        )
    return await User_Pydantic.from_tortoise_orm(user)


@auth.get('/{user_id}/unit')
async def get_user_unit(user_id: int = None):
    try:
        user = await User.get(id=user_id)
        return user.unit
    except DoesNotExist:
        return {'message': 'User not found'}



@auth.post('/users', response_model=User_Pydantic)
async def create_user(user: UserDTO):
    user_obj = await User(
        username=user.username,
        password_hash=bcrypt.hash(user.password),
        email=user.email,
        name=user.name,
        surname=user.surname,
        thirdname=user.thirdname,
        rank=await RankModel.get(id=user.rank_id),
        unit=user.unit,
        is_admin=user.is_admin
    )
    await user_obj.save()
    return await User_Pydantic.from_tortoise_orm(user_obj)


@auth.get('/users/me', response_model=User_Pydantic)
async def get_user(user: User_Pydantic = Depends(get_current_user)):
    return user
