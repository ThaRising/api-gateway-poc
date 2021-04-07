import fastapi
import peewee
import requests
from argon2 import PasswordHasher, exceptions as argon_exc
from fastapi import (
    FastAPI, Body, HTTPException, status, Request
)
from fastapi.responses import Response
from fastapi.security import HTTPBearer
from jose import jwt
from pydantic import BaseModel as _BaseModel

from shared import get_state_adapter, PeeweeGetterDict

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


@app.post("/auth/users/", response_model=UserResponse)
def users_create(user_data: TokenSchema = Body(...)):
    data = user_data.dict()
    pw = PasswordHasher()
    data["password"] = pw.hash(data.get("password"))
    return UserModel.create(**data)


@app.post("/auth/tokens/", response_model=AccessTokenResponse)
def tokens_create(user_data: TokenSchema = Body(...)):
    data = user_data.dict()
    user = UserModel.get_or_none(UserModel.username == data.get("username"))
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
    pw = PasswordHasher()
    try:
        pw.verify(user.password, data.get("password"))
    except argon_exc.VerifyMismatchError or argon_exc.VerificationError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    token = jwt.encode(
        {"username": user.username}, key=SECRET, algorithm="HS256"
    )
    return {"access": token}


# Catchall Route
@app.api_route("/{full_path:path}", methods=[
    "GET", "POST", "PATCH", "PUT", "DELETE", "OPTIONS", "HEAD"
])
def sample(
        req: Request,
        full_path: str,
        token: str = fastapi.Depends(HTTPBearer(
            auto_error=False, scheme_name="Bearer"
        ))
):
    user = {}
    if token:
        user = jwt.decode(token, key=SECRET, algorithms="HS256")
    opa_input = {
        "input": {
            "method": req.method,
            "path": full_path.split("/"),
            "subject": {
                "username": user.get("username", None)
            }
        }
    }
    res = requests.post(
        "http://policies:8181/v1/data/authz/allow",
        json=opa_input,
        headers={"content-type": "application/json"}
    )
    content = res.json()
    if (
            not (r := content.get("result")) or
            r is False or
            res.status_code != status.HTTP_200_OK
    ):
        return Response(status_code=status.HTTP_403_FORBIDDEN)

    return Response(
        headers={"x-current-user": token},
        status_code=status.HTTP_200_OK
    )


__all__ = ["app"]
