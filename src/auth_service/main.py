import peewee
from argon2 import PasswordHasher
from fastapi import FastAPI, Body, HTTPException, status
from jose import jwt
from pydantic import BaseModel as _BaseModel

from ..shared import get_state_adapter, PeeweeGetterDict

DATABASE_NAME = "auth.db"
SECRET = "secret"

db = get_state_adapter(
    peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)
)
app = FastAPI()


class ModelBase(peewee.Model):
    class Meta:
        database = db


class UserModel(ModelBase):
    username = peewee.CharField(unique=True)
    password = peewee.CharField()


class BaseModel(_BaseModel):
    class Config:
        orm_mode = True
        getter_dict = PeeweeGetterDict


class TokenSchema(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    username: str


class AccessTokenResponse(BaseModel):
    access: str


@app.on_event("startup")
async def migrate():
    db.connect()
    db.create_tables([UserModel])
    db.close()


@app.post("users/", response_model=UserResponse)
def users_create(user_data: TokenSchema = Body(...)):
    data = user_data.dict()
    pw = PasswordHasher()
    data["password"] = pw.hash(data.get("password"))
    return UserModel(**data).create()


@app.post("tokens/", response_model=AccessTokenResponse)
def tokens_create(user_data: TokenSchema = Body(...)):
    data = user_data.dict()
    user = UserModel.get_or_none(UserModel.username == data.get("username"))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pw = PasswordHasher()
    if not pw.verify(user.password, data.get("password")):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = jwt.encode(
        {"username": user.username}, key=SECRET, algorithm="HS256"
    )
    return token


__all__ = ["app"]
