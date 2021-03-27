import peewee
from fastapi import FastAPI, Request

from shared import get_state_adapter

DATABASE_NAME = "service.db"
SECRET = "secret"

db = get_state_adapter(
    peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)
)
app = FastAPI()


@app.get("/items")
def items_list(req: Request):
    return {
        "msg": "OK",
        "headers": req.headers
    }


__all__ = ["app"]
