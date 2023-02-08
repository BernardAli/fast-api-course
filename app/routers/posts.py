from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter, Response
from sqlalchemy.orm import Session

from .. import models, schemas, OAuth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), get_current_user: int = Depends(OAuth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    # print(limit)
    # print(search)
    posts = db.query(models.Post).filter(models.Post.owner_id == get_current_user.id).\
        filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    # print(posts)
    return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_post(post: schemas.CreatePost, db: Session = Depends(get_db), get_current_user: int = Depends(OAuth2.get_current_user)):
    # post_dict = post.dict()
    # post_dict['id'] = randrange(0, 10e10)
    # my_posts.append(post_dict)
    # cursor.execute("""INSERT INTO posts( title, content, published) VALUES (%s, %s, %s) RETURNING *""",
    #                (post.title, post.content, post.published))
    # new_post = cursor.fetchone()
    # conn.commit()
    # print(get_current_user.id)
    new_post = models.Post(owner_id=get_current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.PostResponse)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = find_post(id)
    # cursor.execute("""SELECT * FROM posts WHERE id=%s """, (int(id), ))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), get_current_user: int = Depends(OAuth2.get_current_user)):
    # deleting post
    # find the index of the array that has the required ID
    # my_posts.pop(index)
    # index = find_index_post(id)
    # cursor.execute("""DELETE FROM posts WHERE id=%s RETURNING *""", (int(id),))
    # index = cursor.fetchone()
    post = post = db.query(models.Post).filter(models.Post.id == id)
    if not post.first():
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if post.first().owner_id != get_current_user.id:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")
    # my_posts.pop(index)
    # conn.commit()
    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.PostResponse)
def update_post(id: int, updated_post: schemas.UpdatePost, db: Session = Depends(get_db), get_current_user: int = Depends(OAuth2.get_current_user)):
    # index = find_index_post(id)
    # cursor.execute("""UPDATE posts SET title=%s, content=%s, published=%s where id=%s RETURNING *""",
    #                (post.title, post.content, post.published, int(id) ),)
    # index = cursor.fetchone()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    if post_query.first() is None:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"Post with id: {id} was not found"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {id} was not found")
    if post_query.first().owner_id != get_current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not authorized")

    # post_dict = post.dict()
    # post_dict['id'] = id
    # my_posts[index] = post_dict
    # conn.commit()
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_query.first()