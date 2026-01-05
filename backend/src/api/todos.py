from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import List, Optional
from uuid import UUID
from datetime import datetime
from src.db import get_session
from src.models.models import Todo
from src.api.auth_middleware import get_current_user

router = APIRouter(prefix="/todos", tags=["todos"])

@router.get("/", response_model=List[Todo])
def list_todos(session: Session = Depends(get_session), user_id: str = Depends(get_current_user)):
    statement = select(Todo).where(Todo.user_id == UUID(user_id))
    results = session.exec(statement)
    return results.all()

@router.post("/", response_model=Todo, status_code=status.HTTP_201_CREATED)
def create_todo(title: str, session: Session = Depends(get_session), user_id: str = Depends(get_current_user)):
    todo = Todo(title=title, user_id=UUID(user_id))
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(id: UUID, session: Session = Depends(get_session), user_id: str = Depends(get_current_user)):
    todo = session.get(Todo, id)
    if not todo or todo.user_id != UUID(user_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    session.delete(todo)
    session.commit()
    return None

@router.patch("/{id}", response_model=Todo)
def update_todo(id: UUID, title: Optional[str] = None, is_completed: Optional[bool] = None, session: Session = Depends(get_session), user_id: str = Depends(get_current_user)):
    todo = session.get(Todo, id)
    if not todo or todo.user_id != UUID(user_id):
        raise HTTPException(status_code=404, detail="Todo not found")
    if title is not None:
        todo.title = title
    if is_completed is not None:
        todo.is_completed = is_completed
    todo.updated_at = datetime.utcnow()
    session.add(todo)
    session.commit()
    session.refresh(todo)
    return todo
