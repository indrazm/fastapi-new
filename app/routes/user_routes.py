from fastapi import APIRouter, Depends
from sqlmodel import Session

from app.models.engine import db_session
from app.schema.users import UserCreate, UserRead
from app.services.user_service import create_user, get_user, get_users

users_router = APIRouter(prefix="/users", tags=["users"])


@users_router.get("/", response_model=list[UserRead])
def get_users_api(db: Session = Depends(db_session)):
    return get_users(db)


@users_router.get("/{user_id}", response_model=UserRead)
def get_user_api(user_id: str, db: Session = Depends(db_session)):
    return get_user(db, user_id)


@users_router.post("/", response_model=UserRead)
def create_user_api(user: UserCreate, db: Session = Depends(db_session)):
    return create_user(db, user)
