from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
from typing import Annotated
from app.db.models import Users

SECRET_KEY = "5e171b56207248524b8b84df5fb5576ccb0e3b4457749d61e008217539c63ab0"
ALGORITHM = "HS256"

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")


def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user


def create_access_token(
    username: str, user_id: int, user_role: str, expires_delta: timedelta
):
    encode = {"username": username, "id": user_id, "role": user_role}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)


async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("username")
        user_id: int = payload.get("id")
        user_role: str = payload.get("role")
        if not username or not user_id:
            raise HTTPException(status_code=401, detail="Could not validate user.")
        return {"username": username, "user_id": user_id, "role": user_role}
    except JWTError:
        raise HTTPException(status_code=401, detail="Could not validate user.")
