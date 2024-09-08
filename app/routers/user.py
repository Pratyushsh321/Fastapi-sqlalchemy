from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from .. import models, schema, utils
from sqlalchemy.orm import Session  # type: ignore
from ..database import get_db  # absolute import

router = APIRouter(tags=["Users"])


@router.post("/users", response_model=schema.UserOut)
def create_user(user: schema.UserCreate, db: Session = Depends(get_db)):
    # hash the password-user.password
    hashed_password = utils.hash(user.password)  # type: ignore
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get("/users/{id}", response_model=schema.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()

    if not user:
        raise HTTPException(satatus_code=404, detail=f"User with id:{id} not found")

    return user
