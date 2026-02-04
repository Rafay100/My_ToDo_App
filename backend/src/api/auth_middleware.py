from fastapi import Request, HTTPException, Depends
from jose import jwt, JWTError
import os
from sqlmodel import Session, select
from sqlalchemy import cast as sql_cast, String, func
from src.db import get_session
from src.models.models import User

SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key")
ALGORITHM = "HS256"

async def get_current_user(request: Request, session: Session = Depends(get_session)):
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
        # Query using the string representation directly
        statement = select(User).where(sql_cast(User.id, String) == user_id)
        user = session.exec(statement).first()
        if not user:
            raise HTTPException(status_code=401, detail="User not found")
        return user_id

    except (JWTError, ValueError):
        raise HTTPException(status_code=401, detail="Invalid token")
