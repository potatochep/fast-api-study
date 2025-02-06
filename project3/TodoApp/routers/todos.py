from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
from database import repository, transactinal
from models import Todos
from schema import todo_crud
from .auth import get_current_user

router = APIRouter()

user_dependency = Annotated[dict, Depends(get_current_user)]


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=8)
    complte: bool


@transactinal
def read_all_todo():
    return todo_crud.get_all_todos()


@transactinal
def get_todo_by_id(todo_id: int):
    return todo_crud.get_todo_by_id(todo_id=todo_id)


@router.get("/")
async def read_all():
    return read_all_todo()


@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(todo_id: int = Path(gt=0)):
    todo_model = get_todo_by_id(todo_id=todo_id)

    if todo_model is not None:
        return todo_model
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found"
        )


@transactinal
def save_new_todo(todo_request: TodoRequest, user_id: int):
    new_todo = Todos(**todo_request.model_dump(), owner_id=user_id)
    todo_crud(new_todo=new_todo)


@repository
def todo_crud(new_todo: Todos, db: Session):
    db.add(new_todo)
    db.commit()


@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, todo_request: TodoRequest):

    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED)
    
    print(user)

    save_new_todo(todo_request=todo_request, user_id=user['id'])
