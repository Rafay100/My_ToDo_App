from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
import os
from sqlmodel import Session, select
from src.db import get_session
from src.models.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

async def get_current_user(request: Request):
    # Better Auth stores session in session_token cookie
    token = request.cookies.get("session_token")
    if not token:
        raise HTTPException(status_code=401, detail="Not authenticated")

    # The token from Better Auth is a JWT, decode it to get user info
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: str = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=401, detail="Invalid token")

        # Verify user exists in database
        session: Session = next(get_session())
        try:
            user = session.get(User, user_id)
            if not user:
                raise HTTPException(status_code=401, detail="User not found")
            return user_id
        finally:
            session.close()

    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token")
