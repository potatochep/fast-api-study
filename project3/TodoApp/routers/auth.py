from datetime import datetime, timedelta, timezone
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from models import Users
from database import transactinal
from schema import user_crud
from passlib.context import CryptContext
from starlette import status
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError

router = APIRouter(
    prefix='/auth',
    tags=['auth']
)

bcrypt_context = CryptContext(schemes=["bcrypt"])
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")

SECRET_KEY = "asdhgajhsgdjakhg1231jgjkhdgsakjhfsb"
ALGORITHM = "HS256"


class CreateUserRequest(BaseModel):
    email: str
    useranme: str
    first_name: str
    last_name: str
    password: str
    role: str


class Token(BaseModel):
    access_token: str
    token_type: str


@transactinal
def create_new_user(new_user_request: CreateUserRequest):
    new_user = Users(
        email=new_user_request.email,
        username=new_user_request.useranme,
        first_name=new_user_request.first_name,
        role=new_user_request.role,
        hased_password=bcrypt_context.hash(new_user_request.password),
        is_active=True,
    )

    user_crud.save_new_user_info(new_user=new_user)

    return new_user


@router.post("/creat-user/", status_code=status.HTTP_201_CREATED)
async def create_user(create_user_request: CreateUserRequest):
    create_new_user(create_user_request)


def create_acces_token(username: str, user_id: int, expires_delta: timedelta) -> jwt:

    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


@transactinal
def authenticate_user(username: str, password: str):
    user_info: Users = user_crud.get_user_by_user_name(username=username)
    if not user_info:
        return ""
    if not bcrypt_context.verify(password, user_info.hased_password):
        return ""

    token = create_acces_token(user_info.username, user_info.id, timedelta(minutes=20))
    return token


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )

        return {"username": username, "id": user_id}
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]
):
    token = authenticate_user(form_data.username, form_data.password)

    if token == "":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
        )

    return {"access_token": token, "token_type": "bearer"}
