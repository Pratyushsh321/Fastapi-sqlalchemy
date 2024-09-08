from jose import JWTError, jwt  # type: ignore
from datetime import datetime, timedelta
from . import schema
from fastapi import Depends, status, HTTPException
from fastapi.security import OAuth2PasswordBearer

oauth2_schema = OAuth2PasswordBearer(
    tokenUrl="login"
)  # login we are getting from auth.py
# SECRET KEY
# Algorithm
# Expiration time
# taken from documentation of Fastapi oauth2
SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update(
        {"exp": expire}
    )  # added to data to ensure when it is going to expire

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt


# to verify if the token is correct or not
def verify_access_token(token: str, credentials_exception):
    try:

        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)

        id = payload.get("user_id")

        if id is None:
            raise credentials_exception

        token_data = schema.Token_data(id=str(id))
        return token_data

    except JWTError:
        raise credentials_exception


def get_current_user(
    token: str = Depends(oauth2_schema),
):  # this function is used to get user after we validate data from user by verify_access_token
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    return verify_access_token(token, credentials_exception).id
