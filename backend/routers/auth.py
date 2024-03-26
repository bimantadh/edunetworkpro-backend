from api.v1.user.serializers import TokenSchema,requestdetails
from fastapi import APIRouter,Depends,HTTPException,status
from db.session import Session, get_session
from api.v1.user.models import User
from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from utils.auth_bearer import jwt_bearer



router = APIRouter(prefix="/api/v1/auth")



@router.post('/token', response_model=TokenSchema)
async def login(request: requestdetails, db: Session = Depends(get_session)):
    user = db.query(User).filter(User.email == request.email).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Incorrect email")
    hashed_pass = user.password
    if not verify_password(request.password, hashed_pass):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Incorrect password"
        )
    
    access_token = create_access_token(user.id)
    token_type = "bearer"
    user_type = user.type  # Fetching user type
    
    db.commit()
   
    return {
        "access": access_token,
        "token_type": token_type,
        "user_type": user_type  # Including user type in the response
    }
