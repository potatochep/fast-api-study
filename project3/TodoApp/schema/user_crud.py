from sqlalchemy.orm import Session
from database import repository
from models import Users


@repository
def save_new_user_info(new_user: Users, db: Session):
    db.add(new_user)
    
@repository
def get_user_by_user_name(username:str, db:Session) -> Users:
    user = db.query(Users).filter(Users.username == username).first()
    return user
