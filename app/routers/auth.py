from fastapi import APIRouter, Depends, status, HTTPException, Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm  # type: ignore
from app.routers import user
from sqlalchemy.orm import Session  # type: ignore to call database session
from .. import database, schema, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schema.Token)  # imported from schema class Token
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(),  # we are taking data for login via OAuth2PasswordRequestForm
    db: Session = Depends(database.get_db),
):
    # user_credentials to access user information

    # requesting database to retrive all the user credentials
    user = (
        db.query(models.User)
        .filter(
            models.User.email == user_credentials.username
        )  # in user_credentials.username user name can be anything id,email tc
        .first()
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )
    #
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Invalid Credentials"
        )

    # create atoken
    # return token
    access_token = oauth2.create_access_token(
        data={"user_id": user.id}
    )  # data is id of user which we want  to login

    return {"access_token": access_token, "token_type": "bearer"}
