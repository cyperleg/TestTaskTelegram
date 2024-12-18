from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from typing import Annotated, Optional, List
from app.schemas import Token, User, APITelegram, UserIn, DialogSchema, APICode
from app.user import UserDAL
from app.jwt_token import create_access_token, credentials_exception, get_user_by_token
from telegram.schemas import FilterBy, TypeBy, AuthException, APIException
from telegram.client import TelegramAPI

router = APIRouter()


@router.post("/create")
async def create_user(user: UserIn):
    try:
        UserDAL.create_user(user)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return {"message": f"User {user.login} created successfully"}


@router.post("/token")
async def login_for_access_token(form_data: Annotated[OAuth2PasswordRequestForm, Depends()]) -> Token:
    try:
        user = UserDAL.get_user(User(login=form_data.username, password=form_data.password))
    except ValueError:
        raise credentials_exception
    access_token = create_access_token(data={"sub": user.login})
    return Token(access_token=access_token, token_type="bearer")


@router.get("/user/me")
async def get_user(user: Annotated[get_user_by_token, Depends()]) -> User:
    return user


@router.put("/user/set_api")
async def set_user_api(user: Annotated[get_user_by_token, Depends()], api: APITelegram):
    temp_user = user
    temp_user.api = api
    try:
        temp_user.hash_phone = await TelegramAPI(temp_user).create_new_session()
    except APIException as e:
        raise HTTPException(status_code=status.HTTP_429_TOO_MANY_REQUESTS, detail=f"Telegram API cooldown {str(e)}")
    UserDAL.update_account(temp_user)


@router.put("/user/auth")
async def auth_user(user: Annotated[get_user_by_token, Depends()], code: APICode):
    await TelegramAPI(user).authorise(code)


@router.get(f"/user/dialog/{TypeBy}{FilterBy}")
async def get_dialog(user: Annotated[get_user_by_token, Depends()], dialog_type: Optional[TypeBy],
                     dialog_filter: Optional[FilterBy]) -> List[DialogSchema]:
    try:
        res = await TelegramAPI(user).get_dialogs(dialog_filter, dialog_type)
    except AuthException:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Telegram account unauthorised")

    return res
