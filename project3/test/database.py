from contextvars import ContextVar
from functools import wraps
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from sqlalchemy.ext.declarative import declarative_base
from fastapi import FastAPI, Depends

# 데이터베이스 설정
SQLALCHEMY_DATABASE_URL = "sqlite:///./todos.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

db_session_context = ContextVar("db_session", default=None)


def transactinal(func):
    
    """
    aa
    DB 커넥션 연결을 위한 세션 생성
    서비스 레이어에 어노테이션 적용    
    """     
    @wraps(func)
    def wrap_func(*args, **kwargs):
        db_session = db_session_context.get()
        if db_session is None:
            db_session = SessionLocal()
            db_session_context.set(db_session)
            try:
                result = func(*args, **kwargs)
                db_session.commit()
            except Exception as e:
                db_session.rollback()
                raise e
            finally:
                db_session.close()
                db_session_context.set(None)
        else:
            return func(*args, **kwargs)
        return result
    return wrap_func


def repository(func):
    """DB 세션을 자동으로 주입하는 데코레이터"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        db_session = db_session_context.get()
        if db_session is None:
            raise RuntimeError("DB 세션이 설정되지 않았습니다. API 엔드포인트에서 get_db()를 실행해야 합니다.")
        return func(*args, **kwargs, db=db_session)
    
    return wrapper        


Base = declarative_base()