from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils, oauth2
from sqlalchemy import func  # type: ignore
from typing import List
from sqlalchemy.orm import Session  # type: ignore
from ..database import get_db  # absolute import


router = APIRouter(tags=["Posts"])


@router.get("/posts", response_model=List[schema.PostOut])
def get_posts(db: Session = Depends(get_db)):
    #     # db.execute("""SELECT * FROM posts """)
    #     # posts = db.fetchall()
    # posts = db.query(models.Post).all()

    # To perform left join on the table
    results = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )
    return results


@router.post("/posts", response_model=schema.Post)
def create_posts(
    post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):  # it comes from oauth.py after verify_access_token forces user to login
    # db = get_db()
    # db.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s) RETURNING * """,(post.title, post.content, post.published),)
    # new_post = db.fetchone()
    # conn.commit()
    new_post = models.Post(
        owner_id=current_user, **post.model_dump()
    )  # **post.model_dump=(title=post.title, content=post.content,published=post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/posts/{id}", response_model=schema.PostOut)
def get_post(
    id: int,
    db: Session = Depends(get_db),
    user_id: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, (str(id)))
    # post = cursor.fetchone()
    # post = db.query(models.Post).filter(models.Post.id == id).first()

    post = (
        db.query(models.Post, func.count(models.Vote.post_id).label("votes"))
        .join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True)
        .group_by(models.Post.id)
    )

    if not post:
        raise HTTPException(
            status_code=404,
            detail=f"post with id {id} was not found",
        )
    # response.status_code = status
    # return {"msg": f"post with id {id} was not found"}
    return post


@router.delete("/posts/{id}")
def delete_post(
    id: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute("""DELETE FROM posts WHERE id=%s returning *""", (str(id)))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post == None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id} does not exists",
        )
    if post.owner_id() != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/posts/{id}", response_model=schema.Post)
def update_post(
    id: int,
    updated_post: schema.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    # cursor.execute(
    #     f"""UPDATE posts SET title='{post.title}', content='{post.content}',published='{post.published}' WHERE id ={id} RETURNING *"""
    # )
    # updated_post = cursor.fetchone()
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=404, detail=f"post with id:{id}not found")
    if post.owner_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform request action",
        )

    post_query.update(updated_post.model_dump())
    db.commit()
    return post_query.first()
