
import json
from fastapi import FastAPI, Depends, HTTPException, status
from datetime import datetime, timedelta
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
Depends, HTTPException

# Models


class UserInDB(BaseModel):
    username: str
    hashed_password: str


class Auhtentification():
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    # JWT token creation and verification
    SECRET_KEY = "your_secret_key"  # Replace with a secure key
    ALGORITHM = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES = 30

    oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

    # Load users database
    with open("credentials.json", "r") as file:
        fake_users_db = json.load(file)

    def hash_password(password: str):
        return Auhtentification.pwd_context.hash(password)

    def verify_password(plain_password, hashed_password):
        return Auhtentification.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(data: dict, expires_delta: timedelta = None):
        to_encode = data.copy()
        expire = datetime.utcnow() + (expires_delta or timedelta(minutes=15))
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode, Auhtentification.SECRET_KEY, algorithm=Auhtentification.ALGORITHM)
        return encoded_jwt

    async def get_current_user(token: str = Depends(oauth2_scheme)):
        try:
            payload = jwt.decode(token, Auhtentification.SECRET_KEY, algorithms=[
                                 Auhtentification.ALGORITHM])
            username: str = payload.get("sub")
            if username is None:
                raise HTTPException(status_code=401)
            user = Auhtentification.fake_users_db.get(username)
            if user is None:
                raise HTTPException(status_code=401)
            return user
        except JWTError:
            raise HTTPException(status_code=401)
