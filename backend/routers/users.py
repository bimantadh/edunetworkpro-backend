from api.v1.user.serializers import UserCreate,TokenSchema,requestdetails
from fastapi import APIRouter,Depends,HTTPException,status
from db.session import Session, get_session
from api.v1.user.models import User
from utils.utils import get_hashed_password, verify_password, create_access_token, create_refresh_token
from api.v1.consultancy.models import Consultancy


router = APIRouter()

@router.post("/register")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    existing_user = session.query(User).filter_by(email=user.email).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    encrypted_password = get_hashed_password(user.password)

    new_user = User(first_name=user.first_name, last_name=user.last_name, email=user.email, password=encrypted_password, type=user.type, phone=user.phone)

    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Check if the user's type is 'consultancy'
    if user.type.lower() == 'consultancy':
        # Create a Consultancy record
        new_consultancy = Consultancy(
            name=f"{user.first_name} {user.last_name}",  # Assuming first_name is used as the name for the consultancy
            email=user.email,
            phone=user.phone,
        )
        session.add(new_consultancy)
        session.commit()

    return {"message": "user created successfully"}

@router.post('/login' ,response_model=TokenSchema)
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