from typing import Optional, List
import time

import psycopg2
from psycopg2.extras import RealDictCursor
from fastapi import FastAPI
from . import models
from .database import engine
from .routers import posts, users


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn = psycopg2.connect(host='localhost', database='revised_fastapi', user='allgift', password='Matt6:33',
                                cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Database connection was successful")
        break
    except Exception as error:
        print("Connection to Database failed")
        print("Error", error)
        time.sleep(5)


my_posts = [
    {
        "id": 1,
        "title": "title of post 1",
        "content": "content of post 1"
    },
    {
        "id": 2,
        "title": "title of post 2",
        "content": "content of post 2"
    },
]


def find_post(id):
    for p in my_posts:
        if p['id'] == id:
            return p


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


app.include_router(posts.router)
app.include_router(users.router)


@app.get("/")
def root():
    return {"message": "Hello World"}





