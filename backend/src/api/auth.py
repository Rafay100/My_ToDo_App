from fastapi import APIRouter, HTTPException, Depends, Response
from pydantic import BaseModel
import bcrypt
from jose import jwt
from sqlmodel import Session, select
from datetime import datetime, timedelta
import os

from src.db import get_session
from src.models.models import User

router = APIRouter(prefix="/api/v1", tags=["auth"])


class SignupRequest(BaseModel):
    name: str
    email: str
    password: str


class SigninRequest(BaseModel):
    email: str
    password: str

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7  # 7 days


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return bcrypt.checkpw(plain_password.encode(), hashed_password.encode())


def get_password_hash(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


@router.post("/signup")
def signup(data: SignupRequest, response: Response, session: Session = Depends(get_session)):
    # Check if user already exists
    existing = session.exec(select(User).where(User.email == data.email)).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    # Create new user
    hashed_password = get_password_hash(data.password)
    user = User(name=data.name, email=data.email, hashed_password=hashed_password)
    session.add(user)
    session.commit()
    session.refresh(user)

    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Set cookie
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to False for local development without HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7  # 7 days
    )

    return {"message": "User created successfully", "user_id": str(user.id)}


@router.post("/signin")
def signin(data: SigninRequest, response: Response, session: Session = Depends(get_session)):
    user = session.exec(select(User).where(User.email == data.email)).first()

    if not user or not verify_password(data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid email or password")

    # Create JWT token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Set cookie
    response.set_cookie(
        key="session_token",
        value=access_token,
        httponly=True,
        secure=False,  # Set to False for local development without HTTPS
        samesite="lax",
        max_age=60 * 60 * 24 * 7  # 7 days
    )

    return {"message": "Sign in successful", "user_id": str(user.id)}


@router.post("/signout")
def signout(response: Response):
    response.delete_cookie(
        key="session_token",
        httponly=True,
        secure=False,
        samesite="lax"
    )
    return {"message": "Sign out successful"}
