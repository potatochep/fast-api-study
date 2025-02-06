from sqlalchemy.orm import Session
from database import repository
from models import Todos

@repository
def get_all_todos(db:Session):
    return db.query(Todos).all()

@repository
def get_todo_by_id(todo_id:int, db:Session):
    todo_model = db.query(Todos).filter(Todos.id == todo_id).first()
    
    return todo_model