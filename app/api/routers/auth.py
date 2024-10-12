from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.db.base import get_db
from app.models.auth import Token, UserRequest
from app.db.models import Users
from app.core.auth import authenticate_user, bcrypt_context, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

db_dependency = Annotated[Session, Depends(get_db)]


@router.post("/")
async def create_user(db: db_dependency, create_user_req: UserRequest):
    create_user_model = Users(
        email=create_user_req.email,
        username=create_user_req.username,
        first_name=create_user_req.first_name,
        last_name=create_user_req.last_name,
        role=create_user_req.role,
        hashed_password=bcrypt_context.hash(create_user_req.password),
    )
    db.add(create_user_model)
    db.commit()


@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()], db: db_dependency
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(status_code=401, detail="Could not validate user.")
    token = create_access_token(
        user.username, user.id, user.role, expires_delta=timedelta(minutes=20)
    )
    return Token(**{"access_token": token, "token_type": "bearer"})
