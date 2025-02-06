from fastapi import FastAPI, Depends, HTTPException, Path
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from starlette import status
import models
from database import repository, transactinal
from models import Todos

app = FastAPI()


class TodoRequest(BaseModel):
    title: str = Field(min_length=3, max_length=100)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=8)
    complte: bool


# @app.get("/")
# async def read_all(db: Session = Depends(get_db)):
#     return db.query(Todos).all()


# @app.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
# async def read_todo(db: Session = Depends(get_db), todo_id: int = Path(gt=0)):
#     todo_model = db.query(Todos).filter(Todos.id == todo_id).first()

#     if todo_model is not None:
#         return todo_model
#     else:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail="Todo Not Found"
#         )

@transactinal
def save_new_todo(todo_request: TodoRequest):
    new_todo = Todos(**todo_request.model_dump())
    todo_crud(new_todo=new_todo)
    
@repository
def todo_crud(new_todo:Todos, db:Session):
    db.add(new_todo)
    db.commit()

@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo_request: TodoRequest):
    print(todo_request)
    save_new_todo(todo_request=todo_request)

