from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import os
from typing import Any
from sqlalchemy.ext.declarative import as_declarative, declared_attr

load_dotenv()

engine = create_engine(url=os.getenv("DATABASE_URL"), echo=True)
SessionLocal = sessionmaker(bind=engine, expire_on_commit=False)

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


