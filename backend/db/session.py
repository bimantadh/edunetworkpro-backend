from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError
from api.v1.user.models import User
from fastapi import FastAPI, Depends, HTTPException,status,Request
import jwt
from utils.auth_bearer import jwt_bearer
from utils.utils import create_access_token, create_refresh_token, ALGORITHM, JWT_SECRET_KEY, JWT_REFRESH_SECRET_KEY



load_dotenv()

engine = create_engine(url=os.getenv("DATABASE_URL"), echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_current_user(token: str = Depends(jwt_bearer), db: Session = Depends(SessionLocal)):
    try:
        payload = jwt.decode(token, "secret_key", algorithms=["HS256"])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")
        db_user = db.query(User).filter(User.id == user_id).first()
        if db_user is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
        return db_user
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")