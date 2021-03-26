import peewee
from fastapi import FastAPI
from ..shared import get_state_adapter

DATABASE_NAME = "service.db"

db = get_state_adapter(
    peewee.SqliteDatabase(DATABASE_NAME, check_same_thread=False)
)
app = FastAPI()
