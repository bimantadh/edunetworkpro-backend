from api.v1.user.serializers import UserCreate,TokenSchema,requestdetails
import jwt
from datetime import datetime 
from api.v1.user.models import User
from db.database import Base, SessionLocal,engine
from sqlalchemy.orm import Session
from fastapi import FastAPI, Depends, HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from utils.auth_bearer import JWTBearer
from functools import wraps
from utils.utils import create_access_token,create_refresh_token,verify_password,get_hashed_password
from db.database import get_session

ACCESS_TOKEN_EXPIRE_MINUTES = 30  # 30 minutes
REFRESH_TOKEN_EXPIRE_MINUTES = 60 * 24 * 7 # 7 days
ALGORITHM = "HS256"
JWT_SECRET_KEY = "narscbjim@$@&^@&%^&RFghgjvbdsha"   # should be kept secret
JWT_REFRESH_SECRET_KEY = "13ugfdfgh@#$%^@&jkl45678902"

app = FastAPI()


@app.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password =get_hashed_password(user.password)

    new_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email, password=encrypted_password )

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return {"message":"user created successfully"}

@app.post('/login' ,response_model=TokenSchema)
def login(request: requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access=create_access_token(user.id)
    refresh = create_refresh_token(user.id)

    
    db.commit()
   
    return {
        "access_token": access,
        "refresh_token": refresh,
    }

