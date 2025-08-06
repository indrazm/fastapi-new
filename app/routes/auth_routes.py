from ssl import SSLSession

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from app.core.settings import settings
from app.models.database import User
from app.models.engine import db_session
from app.schema.auth import LoginResponse, UserLogin
from app.schema.users import UserCreate, UserRead
from app.services import auth_service

auth_router = APIRouter(
    prefix="/auth",
    tags=["auth"],
)


@auth_router.post("/register", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def register(user: UserCreate, db: SSLSession = Depends(db_session)):
    hashed_password = auth_service.hash_password(user.password)
    user.password = hashed_password

    try:
        new_user = User(**user.model_dump())
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return new_user
    except IntegrityError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))


@auth_router.post("/login", response_model=LoginResponse)
def login(user: UserLogin, db: Session = Depends(db_session)):
    statement = select(User).where(User.email == user.email)
    result = db.exec(statement)
    db_user = result.first()

    if not db_user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    if not auth_service.verify_password(user.password, db_user.password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid password")

    access_token = auth_service.create_access_token(data={"sub": db_user.email})
    return LoginResponse(access_token=access_token, token_type="bearer")


@auth_router.get("/login_google", name="login_google")
async def login_google(request: Request):
    return await auth_service.oauth.google.authorize_redirect(request, settings.GOOGLE_REDIRECT_URI)


@auth_router.get("/callback")
async def callback_google(request: Request):
    token = await auth_service.oauth.google.authorize_access_token(request)
    return token
