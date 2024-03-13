from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import Session
from typing import Optional
from jose import JWTError
from fastapi import FastAPI, Depends, HTTPException,status,Request
import jwt
from api.v1.user import models
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


def get_current_user(
    db: Session = Depends(get_session),
    token: str = Depends(create_access_token),
    skip_verify: Optional[bool] = False
) -> models.User:
    """
    Dependency function to get the current user based on the provided access token.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    try:
        payload = jwt.decode(token, JWT_SECRET_KEY, algorithms=[ALGORITHM])
        sub = payload.get("sub")
        if sub is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    
    if not skip_verify:
        db_user = db.query(models.User).filter(models.User.id == sub).first()
        if db_user is None:
            raise credentials_exception
    
    return db_user


