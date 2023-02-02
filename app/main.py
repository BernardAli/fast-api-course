from typing import Optional
import time

import psycopg2
from psycopg2.extras import RealDictCursor

from fastapi import FastAPI, Body, Response, status, HTTPException
from pydantic import BaseModel
from random import randrange

app = FastAPI()


class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    # rating: Optional[int] = 4


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


@app.get("/")
def root():
    return {"message": "Hello World"}


@app.get("/posts/")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    # print(posts)
    return {"data": posts}


@app.post("/posts/", status_code=status.HTTP_201_CREATED)
def create_post(post: Post):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10e10)
    # my_posts.append(post_dict)
    cursor.execute("""INSERT INTO posts( title, content, published) VALUES (%s, %s, %s) RETURNING *""",
                   (post.title, post.content, post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return {"new_post": new_post}


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # post = find_post(id)
    cursor.execute("""SELECT * FROM posts WHERE id=%s """, (int(id), ))
    post = cursor.fetchone()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return {"post_detail": post}


@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    # deleting post
    # find the index of the array that has the required ID
    # my_posts.pop(index)
    # index = find_index_post(id)
    cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (int(id),))
    index = cursor.fetchone()
    if not index:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    # my_posts.pop(index)
    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@app.put("/posts/{id}")
def update_post(id: int, post: Post):
    # index = find_index_post(id)
    cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s RETURNING *""",
                   (post.title, post.content, post.published, int(id) ),)
    index = cursor.fetchone()
    if index is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    conn.commit()
    return {'date': index}
